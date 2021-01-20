from argparse import ArgumentParser
from sanic import Sanic
from sanic.response import text, redirect
from dateutil import parser
from datetime import datetime
from os.path import isfile
from os import listdir
import jinja2
import jinja2_sanic
from json import load
from random import randint, choices


class Utils(object):
    PATHS = ["~jeff", "cgi-bin", "tmp", "..", "wp-admin", "saucyfiles", "danger", "administration", "root", "images",
             "~admin", "www", "html", ".git", "wp-content", "passwd", "shadow", ".git"]

    @staticmethod
    def generate_path(depth=4):
        return '/'.join(choices(Utils.PATHS, k=depth))

    @staticmethod
    def generate_robots_txt(user_agent="*", lines=25, path_min_depth=1, path_max_path=6):
        r = "User-agent: {0}\n".format(user_agent)
        for _ in range(lines):
            r += "Disallow: {0}\n".format(Utils.generate_path(randint(path_min_depth, path_max_path)))
        return r


class Server(object):
    app = None

    github_url = None

    template_home = None

    def get_template(self, d):
        return dict(self.template_home, **d)

    @staticmethod
    def count_dict_list_items(d, k=None):
        r = 0
        if k is None:
            k = d.keys()
        for _ in k:
            r += len(d[_])
        return r

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
            return text(Utils.generate_robots_txt(req.headers.get("user-agent") or "*"))

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
            return self.get_template(cfg["template"]["about"])

        @self.app.route("/projects", methods=["GET"])
        @jinja2_sanic.template("projects.html")
        async def projects(req):
            return self.get_template(cfg["template"]["projects"])

        @self.app.route("/apps/<path:path>", methods=["GET"])
        @jinja2_sanic.template("app.html")
        async def app(req, path):
            print("se")
            if path in self.template_home["apps"]:
                r = self.get_template(cfg["template"]["apps"][path])
                print(r)
                return r
            return redirect("/")

        self.template_home = {
            "github_url": cfg["github_url"],
            "build_server": cfg["build_server"],
            "apps": cfg["template"]["apps"].keys(),
            "age": int((datetime.now() - parser.parse(cfg["template"]["about"]["birthDate"])).days / 365),
            "projects": self.count_dict_list_items(cfg["template"]["projects"]["languages"])
        }

        self.template_about = self.template_home

        for k in cfg["template"]["apps"].keys():
            _d = "/img/" + cfg["template"]["apps"][k]["name"] + "/"
            cfg["template"]["apps"][k]["images"] = list({"show": "<img src='%s' class='d-block w-100'>" % (_d + _)}
                                                        for _ in listdir("static" + _d))

    def run(self):
        self.app.run(a.host, a.port, debug=a.debug)


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1", type=str, help="host address")
    ap.add_argument("-p", "--port", default=8080, type=int, help="host port")
    ap.add_argument("-d", "--debug", action="store_true", help="debug or not")
    ap.add_argument("-c", "--config", default="config.json", help="configuration file")
    a = ap.parse_args()
    if not isfile(a.config):
        print("no config specified. exiting.")
        exit()
    s = Server(load(open(a.config)))
    s.run()
