import os

import jinja2

import muon


class Template(object):
    DEFAULTS = {
        '.muon/Dockerfile.j2': 'Dockerfile.j2',
        '.muon/inventory.ini.j2': 'inventory.ini.j2',
        '.muon/playbook.yml.j2': 'playbook.yml.j2',
    }

    def __init__(self, context):
        self.context = context

        loader = jinja2.FileSystemLoader(os.getcwd())
        self.cwd_template = jinja2.Environment(loader=loader).get_template

        loader = jinja2.PackageLoader('muon', 'templates')
        self.pkg_template = jinja2.Environment(loader=loader).get_template

    def render(self, template, destination):
        try:
            if os.path.exists(template):
                tpl = self.cwd_template(template)
            elif self.DEFAULTS.get(template, False):
                tpl = self.pkg_template(self.DEFAULTS.get(template))
            else:
                message = "Template file not found `{template}`."
                muon.abort(message, template=template)

            with open(destination, 'w') as fd:
                fd.write(tpl.render(self.context))
        except jinja2.exceptions.TemplateSyntaxError as e:
            message = "Syntax Error: {template}:{e.lineno} {e.message}"
            muon.abort(message, template=template, e=e)
