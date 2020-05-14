from requests import get
from bs4 import BeautifulSoup


def get_next_page(soup):
    n = soup.find(attrs={"class": "paginate-container"})
    for btn in n.find("a", attrs={"class": "btn"}):
        print(btn)


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


def get_repos(username, soup):
    ret = []
    b = get_base_url(username)
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
        result_soup = get_soup(result["url"])
        result["project_stats"] = get_project_statistics(result_soup)
        ret.append(result)
    return ret


def get_base_url(username):
    return "https://github.com/{0}".format(username)


def get_repo_url(username):
    return "{0}?tab=repositories".format(get_base_url(username))


def get_soup(url):
    d = get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"})
    return BeautifulSoup(d.content, "lxml")


user = "smthnspcl"
u = get_repo_url(user)
s = get_soup(u)
r = get_repos(user, s)
print(r)
