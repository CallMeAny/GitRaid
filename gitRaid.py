#! /usr/bin/env python3

# Required:
# pip3 install beautifulsoup4

import sys
import getopt
import os
import urllib
import datetime
from bs4 import BeautifulSoup

def help():
	print("gitRaid.py -f <inputfile || link> -o <outputfile>")
	sys.exit()

def createTag(name, attrib, value, soup):
	tag = soup.new_tag(name, attrs=attrib)
	try:
		tag.string = value
	except:
		tag.string = "<missing value>"

	return tag

def getLink(ifile):
	links = []
	with open(ifile) as infile:
		for line in infile:
			links.append(line)
	return links

def getContent(html):
	soup = BeautifulSoup(html, 'html.parser')
	about = soup.find(itemprop="about")
	author = soup.find(rel="author")
	title = soup.find(itemprop="name")
	readme = soup.find(title="README.md")
	tags_dirty = soup.find(class_="list-topics-container")
	img_dirty = soup.find(class_="markdown-body")

	if about != None:
		about = about.string

	if author != None:
		author = author.string

	if title != None:
		title = title.string

	if readme != None:
		readme = "https://github.com" + readme.attrs["href"]

	tags = []
	if tags_dirty != None:
		for tag in tags_dirty:
			if tag.string != '\n':
				el = tag.string
				tags.append(tag.string)

	image = None
	if img_dirty != None:
		img_dirty = img_dirty.find_all("img")
		for img in img_dirty:
			if "data-canonical-src" not in img.attrs:
				image = img.attrs["src"]
				break

	return (about, author, title, tags, readme, image)

def createContent(link, info):
	soup = BeautifulSoup("<div class='entry'></div>", features="lxml")
	body = soup.div

	(about, author, title, tags, readme, image) = info

	tag_title = createTag("span", {"class": "title"}, title, soup)
	body.append(tag_title)

	tag_author = createTag("span", {"class": "author"}, " by " + author, soup)
	body.append(tag_author)

	tag_link = createTag("a", {"href":link, "class":"repo"}, link, soup)
	body.append(tag_link)

	tag_tab = soup.new_tag("span", attrs={"class":"tab"})
	body.append(tag_tab)	

	body.append("[")

	tag_readme = createTag("a", {"href":readme, "class":"repo"}, "ReadMe.md", soup)
	body.append(tag_readme)

	body.append("]")

	time = str(datetime.datetime.now().date())
	tag_date = createTag("span", {"class":"date"}, time, soup)
	body.append(tag_date)

	for tag in tags:
		tag_tags = createTag("span", {"class":"tag"}, tag, soup)
		body.append(tag_tags)

	tag_about = createTag("p", {"class":"about"}, about, soup)
	body.append(tag_about)

	if image != None:
		tag_img = soup.new_tag("img", attrs={"src": image, "class":"image"})
		body.append(tag_img)

	return body;

def raid(links, soup, ofile):

	for link in links:
		if "github" not in link:
			print("This is not a github repo: ", link)
			continue

		print("LINK:", link)
		try:
			req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
			page = urllib.request.urlopen(req)
		
			if page.getcode() == 200:
				info = getContent(page.read())
				div = createContent(link, info)
				soup.div.append(div)
			else:
				print("Link is broken: " + link)
				print("Status code: " + str(page.getcode()))
		except urllib.error.URLError as e:
			print("Not a valid link: " + link)

	with open(ofile, 'w') as f:
		f.write(str(soup))

if __name__ == "__main__":
	ifile = ""
	ofile = ""

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hf:o:", ["help", "ifile=", "ofile="])
	except:
		help()

	for opt, arg in opts:
		if opt == "-h":
			help()
		elif opt in ("-f", "--ifile"):
			ifile = arg
		elif opt in ("-o", "--ofile"):
			ofile = arg

	if os.path.isfile(ifile):
		links = getLink(ifile)
	else:
		links = [ifile]

	if os.path.isfile(ofile):
		f = open(ofile)
		soup = BeautifulSoup(f, features="lxml")
		f.close()
	else:
		input = '''<html>
<head>
	<title>gitRaid</title>
	<link rel="stylesheet" href="gitRaid.css" />
</head>
<body>
	<div>
	</div>
</html>'''
		soup = BeautifulSoup(input, features="lxml")
	
	raid(links, soup, ofile)