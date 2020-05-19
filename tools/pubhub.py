from bs4 import BeautifulSoup
from requests import get
from json import dumps


class GitHub(object):
    @staticmethod
    def get_base_url(username):
        return "https://github.com/{0}".format(username)

    @staticmethod
    def get_repo_url(username):
        return "{0}?tab=repositories".format(GitHub.get_base_url(username))

    @staticmethod
    def get_soup(url):
        return BeautifulSoup(get(url).content, "lxml")

    @staticmethod
    def get_rawgit_url():
        return "https://raw.githubusercontent.com"

    def __init__(self, username):
        self.username = username

    def get_repo_requirements_txt(self, d: BeautifulSoup):
        r = []
        try:

            f = d.find(attrs={"class": "files"}).find(attrs={"title": "requirements.txt"})\
                    .get("href").replace("/blob/", "/")
            d = get(self.get_rawgit_url() + f).content.split()
            for l in d:
                r.append(l.decode("utf-8"))
        except:
            pass
        return r

    @staticmethod
    def replace_all_w_nothing(d, c):
        for _c in c:
            d = d.replace(_c, b"")
        return d

    @staticmethod
    def filter_build_gradle_dependency(d):
        for f in [b"fileTreedir", b"androidTestImplementation", b"testImplementation",
                  b"annotationProcessor", b"def", b"android"]:
            if d.startswith(f):
                return False
        return True

    def get_build_gradle_dependencies(self, d: bytes):
        r = []
        d = d.split(b"\n")[1:]
        for l in d:
            if l in [b"", b"}"]:
                continue
            l = l.strip()
            l = self.replace_all_w_nothing(l, [b"(", b")", b"'", b'"', b"implementation", b" "])
            if not self.filter_build_gradle_dependency(l):
                continue
            r.append(l.decode('utf-8'))
        return r

    def get_repo_build_gradle(self, d: BeautifulSoup):
        f = d.find(attrs={"title": "app"}).get("href").replace("/tree/", "/") + "/build.gradle"
        d = get(self.get_rawgit_url() + f).content.split(b"dependencies")[1]
        return self.get_build_gradle_dependencies(d)

    def get_cmake_dependencies(self, d: BeautifulSoup):
        r = []
        f = d.find(attrs={"title": "CMakeLists.txt"}).get("href").replace("/blob/", "/")
        d = get(self.get_rawgit_url() + f).content.split(b"\n")
        for l in d:
            if l.startswith(b"target_link_libraries"):
                l = self.replace_all_w_nothing(l, [b"target_link_libraries(", b")"]).split()[1:]
                for i in l:
                    r.append("lib" + i.decode('utf-8'))
        return r

    def get_repo_libraries(self, d: BeautifulSoup, repo):
        r = {}
        lngs = repo["details"]["languages"]
        if "python" in lngs:
            r["python"] = self.get_repo_requirements_txt(d)
        if "java" in lngs:
            r["java"] = self.get_repo_build_gradle(d)
        if "kotlin" in lngs:
            r["kotlin"] = self.get_repo_build_gradle(d)
        if "c++" in lngs:
            r["c++"] = self.get_cmake_dependencies(d)
        return r

    @staticmethod
    def get_repo_languages(d: BeautifulSoup):
        r = []
        try:
            ls = d.find(attrs={"class": "repository-lang-stats-graph"})
            for l in ls.find_all("span"):
                r.append(l.text.lower())
        except:
            pass
        return r

    def get_repo_details(self, repositories):
        print("getting details")
        for repo in repositories:
            rs = self.get_soup(repo["url"])
            print(repo["url"])
            repo["details"] = {
                "languages": {},
                "libraries": {}
            }
            repo["details"]["languages"] = self.get_repo_languages(rs)
            repo["details"]["libraries"] = self.get_repo_libraries(rs, repo)
        return repositories

    def get_repos(self, d: BeautifulSoup):
        r = []
        print("fetching repos")
        for repo in d.find_all(attrs={"class": "source"}):
            if repo is None:
                continue
            lng = repo.find("span", {"itemprop": "programmingLanguage"})
            dsc = repo.find("p", {"itemprop": "description"})
            nme = repo.find("h3").text.strip()
            if "\n" in nme:
                continue
            if dsc is not None:
                dsc = str(dsc.text.strip()),
            if lng is not None:
                lng = lng.text
            t = {
                "name": nme,
                "url": "",
                "description": dsc,
                "mainLanguage": lng,
                "details": {}
            }
            t["url"] = "https://github.com/" + self.username + "/" + t["name"].strip()
            r.append(t)
        r = self.get_repo_details(r)
        return r

    @staticmethod
    def has_next_page(s: BeautifulSoup):
        pc = s.find("div", {"class": "paginate-container"})
        for i in pc.find_all("a", {"BtnGroup-item"}):
            if i.text == "Next":
                return i.get("href")
        return False

    def get(self):
        p = 1
        u = GitHub.get_repo_url(self.username)
        s = self.get_soup(u)
        r = []
        print("getting page {0}".format(p))
        r += self.get_repos(s)
        while True:
            u = self.has_next_page(s)
            if not u:
                break
            p += 1
            print(u)
            print("getting page {0}".format(p))
            s = self.get_soup(u)
            r += self.get_repos(s)
        return r


if __name__ == '__main__':
    repos = GitHub("smthnspcl").get()
    print(repos)
    with open("stuff.json", "w") as o:
        o.write(dumps(repos, indent=4, sort_keys=True))
    print("done")
