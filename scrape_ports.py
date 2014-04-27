#! /usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
from bs4 import BeautifulSoup, NavigableString, Tag

br = mechanize.Browser()
br.open("http://www.e-tsuri.info/")
# print br.title()

soup = BeautifulSoup(br.response().read())

body_tag = soup.body
portlist = soup.find_all("ul", {"class":"port"})

#print portlist

for className in portlist:
    if isinstance(className, Tag):
        atags = className.find_all("a")
        for atag in atags:
            print atag.string.encode('utf-8')


