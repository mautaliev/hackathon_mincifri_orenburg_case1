import requests
from bs4 import BeautifulSoup


def get_data(url, keywords, enterprises):
    articles = []
    resource = 'https://orenburg.media'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip',
        'Accept-Charset': 'utf-8',
        'content-Type': 'charset=utf-8',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.684 Yowser/2.5 Safari/537.36'
    }

    r = requests.get(
        url=url, headers=headers)

    soup = BeautifulSoup(r.content, "html.parser")

    while soup is not None:
        for article in soup.find_all(
                'div', class_='post'):

            articleHeader = article.find('h2', class_='post-title').find('a')
            siteUrl = articleHeader['href']

            newsDateAttr = article.find(
                'div', class_='post-byline').get_text().strip().split()[0]

            newsDate = newsDateAttr.split('.') if newsDateAttr else None

            if newsDate is None:
                continue

            [day, month, year] = newsDate if newsDate else [
                'None', 'None', 'None']

            newsDate = '-'.join([year, month, day]) if newsDate else 'None'
            articleObject = {
                'enterprises': enterprises,
                # 'resource': resource,
                'resource': "Оренбург Медиа",
                'news': articleHeader.get_text().strip(),
                'date': newsDate,
                'link': siteUrl,
                'keywords': keywords,
            }

            if len(articleObject['news']) < 15 or articleObject['news'].find(' ') == -1:
                continue

            articles.append(articleObject)
        nextPageTag = soup.find(
            "a", class_='next page-numbers')

        soup = BeautifulSoup(requests.get(
            url=nextPageTag['href'], headers=headers).content, "html.parser") if nextPageTag else None

    return articles


def orenburgMediaParser(keywords=[], enterprises=[]):
    filter = '+'.join(keywords)+'+'+'+'.join(enterprises)
    searchUrl = "https://orenburg.media/?s=%s" % (
        filter)

    articles = get_data(searchUrl, keywords, enterprises)
    return articles
