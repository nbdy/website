from requests import get
from bs4 import BeautifulSoup


class GitHub(object):
    @staticmethod
    def get_next_page(soup):
        n = soup.find(attrs={"class": "paginate-container"})
        for btn in n.find("a", attrs={"class": "btn"}):
            print(btn)

    @staticmethod
    def get_project_statistics(soup):
        ret = {
            "commits": soup.find(attrs={"class": "commits"}).text.strip().split()[0],
            "language_percentages": []
        }
        '''
        print(soup.find("details"))
        g = soup.find("div", attrs={"class": "repository-lang-stats-graph"})
    
        for lang in g.find_all("span"):
            lang, percentage = lang.attr("aria-label").split()
            ret["language_percentages"].append({"language": lang, "percentage": percentage})
        '''
        return ret

    @staticmethod
    def get_repos(username, soup):
        ret = []
        b = GitHub.get_base_url(username)
        for repo in soup.find_all(attrs={"class": "source"}):
            n = repo.find("h3").text.strip()
            language = repo.find(attrs={"itemprop": "programmingLanguage"})
            if language is not None:
                language = language.text
            result = {
                "name": n,
                "url": b + "/" + n,
                "description": repo.find(attrs={"itemprop": "description"}).text.strip(),
                "primary_language": language,
            }
            result_soup = GitHub.get_soup(result["url"])
            result["project_stats"] = GitHub.get_project_statistics(result_soup)
            ret.append(result)
        return ret

    @staticmethod
    def get_base_url(username):
        return "https://github.com/{0}".format(username)

    @staticmethod
    def get_repo_url(username):
        return "{0}?tab=repositories".format(GitHub.get_base_url(username))

    @staticmethod
    def get_soup(url):
        d = get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"})
        return BeautifulSoup(d.content, "lxml")

    def __init__(self, username):
        self.username = username

    def get(self):
        u = GitHub.get_repo_url(self.username)
        s = GitHub.get_soup(u)
        return GitHub.get_repos(self.username, s)


if __name__ == '__main__':
    print(GitHub("smthnspcl").get())
