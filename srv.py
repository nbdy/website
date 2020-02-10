from argparse import ArgumentParser
from sanic import Sanic
from sanic.response import text
from datetime import datetime
import jinja2
import jinja2_sanic


# todo inform user that we are not using cookies
# todo having keks with scrapers/bots


app = Sanic(__name__)
app.static("/css", "./static/css")
app.static("/js", "./static/js")
app.static("/img", "./static/img")
jinja2_sanic.setup(
    app,
    loader=jinja2.FileSystemLoader("templates")
)


BASE_TEMPLATE_PARAMS = {
    "github_url": "https://github.com/smthnspcl"
}

ABOUT_TEMPLATE_PARAMS = {
    "github_url": BASE_TEMPLATE_PARAMS["github_url"],  # todo nicer way to do this?
    "name": "Pascal Eberlein",
    "age": int((datetime.now() - datetime(1996, 10, 27)).days / 365),
    "comm_language_main": "German",
    "comm_languages": ["English"],
    "prog_languages": ["C++", "Java", "Python", "JS", "HTML", "CSS", "SCSS"],
    "sdks": ["Android", "Tizen (4)", "ESP-IDF", "Arduino"],
    "ides": ["CLion", "Android Studio", "PyCharm", "IntelliJ"]
}

PROJECT_TEMPLATE_PARAMS = {
    "languages": {
        "python": [
            {"title": "carpy", "description": "infotainment system"},
            {"title": "pwnpy", "description": "wardriving program",
             "show": '<a href="https://asciinema.org/a/299821" target="_blank"><img src="https://asciinema.org/a/299821.svg" /></a>'},
            {"title": "adbSync", "description": "android sync tool",
             "show": '<a href="https://asciinema.org/a/299825" target="_blank"><img src="https://asciinema.org/a/299825.svg" /></a>'},
            {"title": "pycorsproxy", "description": "cors proxy"},
            {"title": "pybt", "description": "bluetooth library",
             "show": '<a href="https://asciinema.org/a/299826" target="_blank"><img src="https://asciinema.org/a/299826.svg" /></a>'},
            {"title": "seleniumwrapper", "description": "as the name implies"},
            {"title": "wifuzz", "description": "wireless fuzzer"},
            {"title": "pyncddns", "description": "namecheap dyndns updater"},
            {"title": "GlassCap", "description": "pcap reader / file carver"}
        ],
        "java": [
            {"title": "contactsync", "description": "app / syncs contacts via bluetooth"},
            {"title": "abt", "description": "library / bluetooth helper"},
            {"title": "contacts", "description": "app / contacts app w/ encrypted storage"},
            {"title": "adocs", "description": "app / offline android documentation viewer"},
            {"title": "debt", "description": "app / track the debt of your coworkers / colleagues"},
            {"title": "apyide", "description": "app / python editor w/ syntax highlighting"},
            {"title": "shopping", "description": "app / shopping list for infinite stores"},
            {"title": "bluepwn", "description": "app / bluetooth wardriving"}
        ],
        "cpp": [
            {"title": "carpi", "description": "infotainment system"},
            {"title": "pwnpi", "description": "wardriving program",
             "show": '<a href="https://asciinema.org/a/299834" target="_blank"><img src="https://asciinema.org/a/299834.svg" /></a>'},
            {"title": "deauthdetect", "description": "detects deauthentication 802.11 frames",
             "show": '<a href="https://asciinema.org/a/299838" target="_blank"><img src="https://asciinema.org/a/299838.svg" /></a>'},
            {"title": "mbtiles-cpp", "description": "mbtiles/mapbox vector tile reader/writer"},
            {"title": "raycons", "description": "icons drawn with raylib / for carpi"},
            {"title": "raygauge", "description": "gauges drawn with raylib / for carpi"}
        ]
    }
}


@app.route("/robots.txt", methods=["GET"])
async def robots(req):
    return text("kek")


@app.route("/", methods=["GET"])
@jinja2_sanic.template("home.html")
async def root(req):
    return BASE_TEMPLATE_PARAMS


@app.route("/index", methods=["GET"])
@jinja2_sanic.template("home.html")
async def index(req):
    return BASE_TEMPLATE_PARAMS


@app.route("/home", methods=["GET"])
@jinja2_sanic.template("home.html")
async def home(req):
    return BASE_TEMPLATE_PARAMS


@app.route("/about", methods=["GET"])
@jinja2_sanic.template("about.html")
async def about(req):
    return ABOUT_TEMPLATE_PARAMS


@app.route("/projects", methods=["GET"])
@jinja2_sanic.template("projects.html")
async def projects(req):
    return PROJECT_TEMPLATE_PARAMS


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1", type=str, help="host address")
    ap.add_argument("-p", "--port", default=8080, type=int, help="host port")
    ap.add_argument("-d", "--debug", action="store_true", help="debug or not")
    ap.add_argument("-sc", "--ssl-cert", default=None, type=str, help="ssl certificate")
    ap.add_argument("-sk", "--ssl-key", default=None, type=str, help="ssl key")
    a = ap.parse_args()

    if a.ssl_key is None and a.ssl_cert is None:
        app.run(host=a.host, port=a.port, debug=a.debug)
    else:
        app.run(host=a.host, port=a.port, debug=a.debug, ssl={"cert": a.ssl_cert, "key": a.ssl_key})
