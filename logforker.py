__author__ = 'Senior9324'
from urllib.request import *
from urllib.error import *
from urllib.parse import *
from bs4 import BeautifulSoup
from sys import  argv
from os import path, mkdir
from dateutil import parser
from datetime import datetime
import time
import json

export = {}
def getlog(document):
	url = "https://namu.wiki/history/{title}"
	headers = {'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	rev = 0
	while(True):
		try:
			if rev > 0:
				req = Request(url=url.format(title=quote(document)) + "?rev="+str(rev), headers=headers)
			else:
				req = Request(url=url.format(title=quote(document)), headers=headers)
			response = urlopen(req)
			html = response.read().decode()
			try:
				if(html.index("g-recaptcha") > 0):
					print("Too many request ERROR")
					break
			except:
				pass
			soup = BeautifulSoup(html, 'html.parser')
			for item in soup.article.find_all("li"):
				# date
				rawdate = item.contents[0].strip()
				date = parser.parse(rawdate)
				stamp = time.mktime(date.timetuple())
				timestamp = datetime.utcfromtimestamp(stamp)
				isodate = timestamp.isoformat()
				
				# rev
				revitem = item.find(type="radio")
				thisrev = int(revitem["value"])
				if rev == 0:
					rev = thisrev
				
				# author
				author = item.select('strong a[href^="/contribution/"]')
				output = ""
				which = ""
				if not author:
					output = item.select('a[href^="/contribution/"]')[0].string
					which = "ip"
				else:
					output = author[0].string
					which = "username"
				
				# special comment
				spcomment = item.i
				if spcomment:
					spcomment = item.i.string
				
				# comment
				comment = item.find(style="color: gray").string
				if not comment:
					comment = ""
				else:
					comment = comment.strip()
				
				if spcomment:
					comment = spcomment + ": " + comment
				
				export[thisrev] = {
					"date": isodate,
					"comment": comment
				}
				export[thisrev][which] = output
			rev -= 31
			if rev < 1:
				break
			time.sleep(3)
		except HTTPError as e:
			print(e)
			break
	f = open(document.replace("/", "%3A").replace(":", "")+".log", mode='w')
	f.write(json.dumps(export, ensure_ascii=False))
	f.close()

if (__name__ == "__main__"):
	getlog("SCP-106")