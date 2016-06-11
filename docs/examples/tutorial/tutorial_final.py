import eventlet

from pycommunicate.server.bases.views import View
from pycommunicate.server.bases.controller import ControllerFactory
from pycommunicate.server.app.communicate import CommunicateApp

app = CommunicateApp()

# This class uses some greenlet things and is beyond the scope of this tutorial


class TodoReader:
    def __init__(self):
        self.todos = {}
        self.last_todo = 0
        try:
            with open('todo.txt', 'r') as old:
                for i, line in enumerate(old.readlines()):
                    self.todos[i] = line
                    self.last_todo = max(self.last_todo, i)
        except IOError:
            pass
        self.add_queue = eventlet.queue.Queue()
        self.adds = {}
        self.remove_queue = eventlet.queue.Queue()

    def add_daemon(self):
        while True:
            add = self.add_queue.get()

            self.todos[self.last_todo + 1] = add
            self.adds[add].put(self.last_todo + 1)
            self.last_todo += 1

            with open('todo.txt', 'w') as new:
                for index in self.todos:
                    new.write(self.todos[index] + ("\n" if not self.todos[index].endswith("\n") else ""))

    def del_daemon(self):
        while True:
            d = self.remove_queue.get()

            del self.todos[d]
            self.last_todo = 0
            for i in self.todos:
                self.last_todo = max(self.last_todo, i)

            with open('todo.txt', 'w') as new:
                for index in self.todos:
                    new.write(self.todos[index] + ("\n" if not self.todos[index].endswith("\n") else ""))

    def start(self):
        pool = eventlet.greenpool.GreenPool(2)
        pool.spawn_n(self.add_daemon)
        pool.spawn_n(self.del_daemon)

    def add(self, text):
        self.add_queue.put(text)
        self.adds[text] = eventlet.queue.Queue()

    def wait_on(self, text):
        ind = self.adds[text].get()
        del self.adds[text]
        return ind

    def remove(self, index):
        self.remove_queue.put(index)

todo = TodoReader()
todo.start()  # start up the TodoReader.


class TodoView(View):
    def render(self):
        return self.controller.templater.render("home.html")

    def make_handler(self, index):
        def handler():
            todo.remove(index)

            todo_div = self.html_wrapper.element_by_selector("#todo{}".format(index))
            todo_div.delete()
        return handler

    def add_handler(self):
        text = "- " + self.html_wrapper.element_by_selector("#next").get_property("value")
        todo.add(text)
        self.html_wrapper.element_by_selector("#next").set_property("value", "")
        index = todo.wait_on(text)
        todo_div = self.html_wrapper.element_by_selector("#todo")
        todo_page_div = todo_div.append_element_inside_self("div", "todo{}".format(index))
        text_p = todo_page_div.append_element_inside_self("p", "todoText{}".format(index))
        text_p.content.set(text)
        button = todo_page_div.append_element_inside_self("button", "todoRemove{}".format(index))
        button.add_event_listener("click", self.make_handler(index))
        button.content.set("Remove")

    def load(self):
        # add existing todos:
        todo_div = self.html_wrapper.element_by_selector("#todo")

        loading_message = self.html_wrapper.element_by_selector("#loadingBar")
        loading_message.delete()

        for index in todo.todos:
            text = todo.todos[index]
            todo_page_div = todo_div.append_element_inside_self("div", "todo{}".format(index))
            text_p = todo_page_div.append_element_inside_self("p", "todoText{}".format(index))
            text_p.content.set(text)
            button = todo_page_div.append_element_inside_self("button", "todoRemove{}".format(index))
            button.add_event_listener("click", self.make_handler(index))
            button.content.set("Remove")

        add_button = self.html_wrapper.element_by_selector("#add")
        add_button.add_event_listener("click", self.add_handler)

controller = ControllerFactory().add_view(TodoView).set_default_view(TodoView)
app.add_controller("/", controller)

app.set_secret_key("todo_secrets!")
app.run()

