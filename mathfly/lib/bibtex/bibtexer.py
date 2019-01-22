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
