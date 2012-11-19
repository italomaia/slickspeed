# -*- coding:utf-8 -*-

"""
Flask/python based version of the PHP project slickspeed.
"""

from flask import Flask
from flask import request, render_template, send_file

from ConfigParser import ConfigParser

# load framework configurations
config = ConfigParser()
config.readfp(open('config.ini'))

# loads selectors used in the test
selectors = map(lambda line: line.strip(), open('selectors.list').readlines())

frameworks = {}
for section in config.sections():
    frameworks[section] = dict(config.items(section))

app = Flask(__name__)
app.debug = True

if not app.debug:
    app.use_x_sendfile = True


@app.route("/")
def index():
    """
    Main page
    """
    return render_template(
        "index.html",
        frameworks=frameworks,
        selectors=selectors)


@app.route("/template.txt")
def see_template():
    """
    Shows the test template
    """
    return send_file('templates/template.txt')


@app.route("/test")
def test():
    """
    Renders the test template and framework.
    """
    framework = request.args.get('framework')

    if framework in frameworks:
        values = frameworks[framework]
        framework = {
            'name': framework,
            'url': values['url'],
            'function': values['function']
        }
        return render_template(
            "template.html",
            framework=framework,
            selectors=selectors)
    else:
        return 'ERRO'


if __name__ == "__main__":
    app.run()
