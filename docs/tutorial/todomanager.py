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