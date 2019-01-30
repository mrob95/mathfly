from dragonfly import Clipboard, Key
from urllib2 import Request, urlopen, quote
from bs4 import BeautifulSoup

import re
import os
import subprocess
import datetime

def get_tag(ref):
    query = re.compile(r'@.*{(.*),')
    tag = re.search(query, ref)
    if tag:
        return tag.group(1)
    else:
        return "No tag found"

# takes URL, returns beautiful soup
def request_page(url):
    header = {'User-Agent': 'Mozilla/5.0', "Cookie":"GSP=CF=4"}
    request = Request(url, headers=header)
    response = urlopen(request)
    html = response.read()
    htmlsoup = BeautifulSoup(html, features="lxml")
    return htmlsoup

def google_scholar_query(searchstr):
    searchstr = '/scholar?q=' + quote(searchstr)
    url = "https://scholar.google.com" + searchstr
    htmlsoup = request_page(url)
    links_list = []
    refre = re.compile(r'https://scholar.googleusercontent.com(/scholar\.bib\?[^"]*)')
    for link in htmlsoup.find_all("a"):
        link_url = link.get("href")
        if refre.search(link_url):
            links_list.append(link_url)
    return links_list

def return_bib(scholar_bib_url):
    bib = request_page(scholar_bib_url).p.text
    return bib

def bib_from_title(query):
    link_list = google_scholar_query(query)
    bib = return_bib(link_list[0])
    return bib

'''
Returns a bibTeX citation for online resources given a url.
eg running bibtex_from_link("https://www.thetimes.co.uk/edition/business/higher-oil-prices-push-shell-profits-up50-x7kk3dg90")
returns:
@online{Higheroilprices,
 title = {Higher oil prices push Shell profits up 50% | Business | The Times},
 author = {},
 year = {},
 url = {https://www.thetimes.co.uk/edition/business/higher-oil-prices-push-shell-profits-up50-x7kk3dg90},
 urldate = {2018-11-01},
}
author and year need to be entered manually.
'''
def bibtex_from_link(url):
    if url[-4:] == ".pdf":
        tag = ""
        title = ""
    else:
        htmlsoup = request_page(url)
        title = htmlsoup.title.text.replace("\n", "").replace(":", "").replace(",", "").strip()
        title_split = title.split()
        if len(title_split) == 0:
            tag = ""
        if len(title_split) == 1:
            tag = title_split[0]
        elif len(title_split) == 2:
            tag = title_split[0] + title_split[1]
        else:
            tag = title_split[0] + title_split[1] + title_split[2]

    author_search = re.search(r'([a-z0-9]*\.(uk|com|co\.uk|org))', url)
    if author_search:
        author = author_search.group(1)
    else:
        author = ""

    year_search = re.search(r'(19|20)[8901]\d', url)
    if year_search:
        year = year_search.group(0)
    else:
        year = ""

    date = datetime.datetime.today().strftime('%Y-%m-%d')
    ref = "@online{" + tag + ",\n title = {" + str(title) + "},\n author = {" + author + "},\n year = {" + year + "},\n url = {" + url + "},\n urldate = {" + date + "}\n}\n"
    return ref