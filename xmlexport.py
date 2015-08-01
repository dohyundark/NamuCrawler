import json
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from sys import argv
import os

def export(title):
	root = Element("mediawiki", attrib={"xml:lang":"ko"})
	page = SubElement(root, "page")
	titlenode = SubElement(page, "title")
	titlenode.text = title
	jsonrawdata = open(title.replace("/", "%3A").replace(":", "") + ".log").read()
	data = json.loads(jsonrawdata)

	for key in sorted(data.keys(), key=int):
		revision = SubElement(page, "revision")
		timestamp = SubElement(revision, "timestamp")
		timestamp.text = data[key]["date"]

		if "username" in data[key]:
			username = SubElement(SubElement(revision, "contributor"), "username")
			username.text = data[key]["username"]
		else:
			ip = SubElement(SubElement(revision, "contributor"), "ip")
			ip.text = data[key]["ip"]

		comment = SubElement(revision, "comment")
		comment.text = data[key]["comment"]

		text = SubElement(revision, "text", attrib={"bytes": str(os.stat(title.replace("/", "%3A").replace(":", "") + "/" + key + ".namu").st_size)})
		text.text = open(title.replace("/", "%3A").replace(":", "") + "/" + key + ".namu").read()

	f = open(title.replace("/", "%3A").replace(":", "")+".xml", mode='wb')
	f.write(tostring(root, encoding="utf-8"))
	f.close()

if (__name__ == "__main__"):
	export(argv[1])