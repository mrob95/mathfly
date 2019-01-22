# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, quote
from dragonfly import Clipboard, Key
import re

# takes URL, returns beautiful soup
def request_page(url):
    header = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=header)
    response = urlopen(request)
    html = response.read()
    htmlsoup = BeautifulSoup(html, features="lxml")
    return htmlsoup

# Returns url of first result from goodreads
def goodreads_results(searchstr):
    searchstr = '/search?q=' + quote(searchstr)
    url = "https://www.goodreads.com" + searchstr
    htmlsoup = request_page(url)
    links_list = []
    refre = re.compile(r'/book/show/.*\?from_search=true')
    for link in htmlsoup.find_all("a"):
        link_url = link.get("href")
        if type(link_url) is str:
            if refre.search(link_url):
                links_list.append("https://www.goodreads.com" + link_url)
    return links_list

'''
get_book_data is the main scraping function. It takes a goodreads book url and returns a
dict with the following fields:
title
authors (list)
authors_string (string, author names separated with " and ")
edition
pub_date (often of the form 29th May 2006)
pub_year (the last word of pub_date, hopefully the year)
publisher
first_published (for old books, this is often different to the edition date)
'''
def get_book_data(url):
    htmlsoup = request_page(url)
    data = {}

    data["authors"] = []
    for link in htmlsoup.find_all("a", { "class": "authorName" }):
        for span in link.find_all("span", { "itemprop": "name"}):
            data["authors"].append(span.text)
    data["authors_string"] =  " and ".join(data["authors"])

    heading1 = htmlsoup.find("h1", {"id":"bookTitle"})
    data["title"] = heading1.text.replace("\n", "").strip()

    details = ""
    for row in htmlsoup.find_all("div", {"class":"row"}):
        edition_span = row.find("span", {"itemprop":"bookEdition"})
        if edition_span is not None:
            data["edition"] = edition_span.text
        details = details + row.text

    pub_date_match = re.search(r'Published\n(.*)\n', details)
    if pub_date_match:
        data["pub_date"] = pub_date_match.group(1).strip()
        data["pub_year"] = data["pub_date"].split(" ")[-1]
    else:
        data["pub_date"] = ""
        data["pub_year"] = ""

    publisher_match = re.search(r'by\ (.*)\n', details)
    if publisher_match:
        data["publisher"] = publisher_match.group(1).strip()
    else:
        data["publisher"] = ""

    first_published_match = re.search(r'first\ published\ (.*)\)', details)
    if first_published_match:
        data["first_published"] = first_published_match.group(1).strip().split(" ")[-1]
    else:
        data["first_published"] = ""

    return data

'''
Takes the dict from get_book_data and builds a bibTeX-style citation which
can be appended directly to a .bib file. Example citations:

@book{wedgwood1938thirty,
 title={The Thirty Years War},
 author={C.V. Wedgwood and Anthony Grafton},
 year={1938},
 publisher={New York Review of Books},
 note={2005}
}
@book{russell2006like,
 title={Like Engend'ring Like: Heredity and Animal Breeding in Early Modern England},
 author={Nicholas Russell},
 year={2006},
 publisher={Cambridge University Press}
}
'''
def build_citation(data):
    # create strings for building a bibtex tag - last name of first author, first word of title
    first_name = data["authors"][0].lower().split(" ")[-1]
    first_title = data["title"].lower().replace("the ", "").split(" ")[0]

    citation1 = "@book{"
    citation2 = ",\n " + "title={" + data["title"] + "},\n author={" + data["authors_string"] + "},\n year={"
    citation3 = "},\n publisher={" + data["publisher"] + "}"
    citation4 = "\n}\n"

    # If the year first published is not the same as the year the returned edition was published,
    # format the year as first published/edition published
    if data["first_published"] == "":
        tag = first_name + data["pub_year"] + first_title
        year_formatted = data["pub_year"]
    elif data["pub_year"] == "":
        tag = first_name + data["first_published"] + first_title
        year_formatted = data["first_published"]
    else:
        tag = first_name + data["first_published"] + first_title
        citation4 = ",\n note={" + data["pub_year"] + "}\n}\n"
        year_formatted = data["first_published"]
    ref = citation1 + tag + citation2 + year_formatted + citation3 + citation4
    return ref

'''
Searches a given book name, builds citation from the first result, if any
'''
def citation_from_name(book_name):
    search_results = goodreads_results(book_name)
    if search_results == []:
        print("No results found on goodreads")
        ref = ""
    else:
        url = search_results[0]
        data = get_book_data(url)
        ref = build_citation(data)
    return ref
