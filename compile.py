'''
Convert Markdown note files to HTML based webpage.
Author: Sachin
Date created: 09/30/2021
'''

from datetime import datetime
from os import path, listdir
from typing import Tuple
from sys import argv

from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from bs4 import BeautifulSoup # type: ignore

from lunar_plugin import LKRenderer

md = (
	MarkdownIt(renderer_cls=LKRenderer)
	.enable('table')
	.enable('strikethrough')
	.use(anchors_plugin, permalinkBefore=False, permalink=True, min_level=2, max_level=3, permalinkSymbol='#')
)

NOTES = 'md/'

def soup(html: str) -> BeautifulSoup:
	'''alias for calling BeautifulSoup on a string'''
	return BeautifulSoup(html, features='html.parser')

def parse_filename(filename: str) -> Tuple[str, str]:
	'''
	Parse filename into title and date.

	Example: 20210930_my_title.md => "my title", datetime(day=30, month=09, year=2021)

	:param filename: filename to parse
	:return: (title, date string)
	'''

	name, ext = path.splitext(filename)
	date_str, *words = name.split('_')

	try:
		dt = datetime.strptime(date_str, r'%Y%m%d')
	except ValueError as err:
		return name, ''
	
	return ' '.join(words) or 'Unknown', dt.strftime(r"%m/%d/%Y")

def note(md_file: str, template_file: str = 'notes/template.html', dest: str = 'notes/') -> Tuple[str, str, str]:
	'''
	Construct HTML from markdown file and html template

	:param md_file: path to Markdown notes file
	:param template_file: path to template HTML file
	:param dest: path to html destination

	:return: (html path, title, date string)
	'''
	with open(template_file, 'r') as f:
		template = BeautifulSoup(f, features='html.parser')

	with open(md_file, 'r') as f:
		content_md = f.read()
		content_html = md.render(content_md)
		content = BeautifulSoup(content_html, features='html.parser')
	
	directory, filename = path.split(md_file)
	name, ext = path.splitext(filename)

	title, date = parse_filename(filename)
	template.head.title.string = title
	template.body.find(id="page-title").string = title
	template.body.find(id="page-date").string = date
	template.body.append(content)
	
	html_file = path.join(dest, name + '.html')
	with open(html_file, 'w') as f:
		f.write(str(template))
	
	return html_file, title, date

if __name__ == '__main__':

	# compile single file
	if len(argv) > 1:
		for file in argv[1:]: note(file)
		quit()

	with open('templates/main.html', 'r') as f:
		main = BeautifulSoup(f, features='html.parser')

	notes = sorted([path.join(NOTES, file) for file in listdir(NOTES) if file.endswith('.md')])
	for file in reversed(notes):
		link, title, date = note(file)
		print(f'Finished {title} - {date}')
		entry = f'<div><h2><a class="lklink unstyled" href="{link}"><div>{title}<span class="lkdate">{date}</span></div></a></h2></div>'
		main.body.append(soup(entry))
	
	with open('index.html', 'w') as f:
		f.write(str(main))