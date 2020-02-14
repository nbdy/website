from argparse import ArgumentParser
from sanic import Sanic
from sanic.response import text
from dateutil import parser
from datetime import datetime
from os.path import isfile
import jinja2
import jinja2_sanic
from json import load

# todo having keks with scrapers/bots


class Server(object):
    app = None
    github_url = None
    template_projects = None
    template_about = None
    template_home = None

    def __init__(self, cfg):
        self.app = Sanic(__name__)
        self.app.static("/css", "./static/css")
        self.app.static("/js", "./static/js")
        self.app.static("/img", "./static/img")
        jinja2_sanic.setup(
            self.app,
            loader=jinja2.FileSystemLoader("templates")
        )

        @self.app.route("/robots.txt", methods=["GET"])
        async def robots(req):
            return text("kek")

        @self.app.route("/", methods=["GET"])
        @jinja2_sanic.template("home.html")
        async def root(req):
            return self.template_home

        @self.app.route("/index", methods=["GET"])
        @jinja2_sanic.template("home.html")
        async def index(req):
            return self.template_home

        @self.app.route("/home", methods=["GET"])
        @jinja2_sanic.template("home.html")
        async def home(req):
            return self.template_home

        @self.app.route("/about", methods=["GET"])
        @jinja2_sanic.template("about.html")
        async def about(req):
            return self.template_about

        @self.app.route("/projects", methods=["GET"])
        @jinja2_sanic.template("projects.html")
        async def projects(req):
            return self.template_projects

        self.template_home = {
            "github_url": cfg["github_url"],
            "build_server": cfg["build_server"]
        }

        self.template_about = self.template_home
        self.template_about.update(cfg["template"]["about"])
        self.template_about["age"] = int((datetime.now() - parser.parse(self.template_about["birthDate"])).days / 365)
        self.template_projects = self.template_home
        self.template_projects.update(cfg["template"]["projects"])

    def run(self):
        if a.ssl_key is None and a.ssl_cert is None:
            self.app.run(a.host, a.port, debug=a.debug)
        else:
            self.app.run(a.host, a.port, debug=a.debug, ssl={"cert": a.ssl_cert, "key": a.ssl_key})


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1", type=str, help="host address")
    ap.add_argument("-p", "--port", default=8080, type=int, help="host port")
    ap.add_argument("-d", "--debug", action="store_true", help="debug or not")
    ap.add_argument("-sc", "--ssl-cert", default=None, type=str, help="ssl certificate")
    ap.add_argument("-sk", "--ssl-key", default=None, type=str, help="ssl key")
    ap.add_argument("-c", "--config", default="config.json", help="configuration file")
    a = ap.parse_args()
    if not isfile(a.config):
        print("no config specified. exiting.")
        exit()
    s = Server(load(open(a.config)))
    s.run()
