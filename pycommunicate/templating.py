import jinja2


class Templater:
    def __init__(self, controller_or_app):
        self.app = controller_or_app.app if hasattr(controller_or_app, 'app') else controller_or_app

        self.env = jinja2.Environment(
            loader=jinja2.ChoiceLoader(
                (
                    jinja2.PackageLoader('pycommunicate'),
                    jinja2.FileSystemLoader(self.app.template_directory)
                )
            )
        )

        def add_includes():
            return self.render_includes()

        self.env.globals.update({
            'add_includes': add_includes
        })

    def render(self, template, **kwargs):
        return self.env.get_template(template).render(**kwargs)

    def render_includes(self):
        return self.render('__pycommunicate_html/includes.html')
