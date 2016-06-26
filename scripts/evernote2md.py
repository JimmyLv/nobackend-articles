import html2text
import os
import codecs
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

pattern = re.compile(r'\!\[\]\((.*?)\.resources', re.S)

for root, dirs, files in os.walk('./evernote'):
	for file in files:
		if file.find('.html') != -1:
			filename = file.split(".html")[0]
			file_pathname = os.path.join(root,filename)
			with codecs.open(file_pathname+'.md', 'w', 'utf-8') as outfile, codecs.open(file_pathname+".html", 'rU', 'utf-8') as infile:
				html_data = infile.read()
				md_data = html2text.html2text(html_data)

				md_data = md_data.replace("\[","[").replace("\]","]")

				md_data = pattern.sub('![](./' + filename + '.resources', md_data)

				# print md_data
				outfile.write(md_data)
