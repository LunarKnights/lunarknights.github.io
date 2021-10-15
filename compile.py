'''
Convert Markdown note files to HTML based webpage.
Author: Sachin
Date created: 09/30/2021
'''

import argparse
from datetime import datetime
from os import path, listdir
from typing import Tuple, TextIO, Union
import sys
from sys import argv

from markdown_it import MarkdownIt # type: ignore
from mdit_py_plugins.anchors import anchors_plugin # type: ignore
from bs4 import BeautifulSoup # type: ignore

from lunar_plugin import LKRenderer
from watch import watch

NOTES = 'md/'

def warn(msg: str) -> None:
	print(f'Warning: {msg}', file=sys.stderr)

def error(msg: str, end: bool = False) -> None:
	print(f'Error: {msg}', file=sys.stderr)
	if end: sys.exit(1)

def soup(html: Union[str, TextIO]) -> BeautifulSoup:
	'''alias for calling BeautifulSoup on a string'''
	return BeautifulSoup(html, features='html.parser')

def md_to_html(md_file: TextIO) -> BeautifulSoup:
	'''convert Markdown string to HTML object'''
	md = (
		MarkdownIt(renderer_cls=LKRenderer)
		.enable('table')
		.enable('strikethrough')
		.use(anchors_plugin, permalinkBefore=False, permalink=True, min_level=2, max_level=3, permalinkSymbol='#')
	)
	return soup(md.render(md_file.read()))

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
	except ValueError:
		return name, 'No Date'
	
	return ' '.join(words) or 'Unknown', dt.strftime(r"%m/%d/%Y")

def compile_file(md_file: str) -> str:
	'''
	Compiles generic Markdown document into an HTML document.
	:param md_file: path to Markdown document

	:return: path to html file 
	'''

	directory, name = path.split(md_file)
	name, ext = path.splitext(name)

	if ext != '.md': 
		error(f'{md_file} is not a markdown document.')
		return ''

	with open('templates/doc.html', 'r') as f:
		template = soup(f)
	
	with open(md_file, 'r') as f:
		contents = md_to_html(f)

	template.head.title.string = name
	template.body.append(contents)
	
	html_file = path.join(directory, name + '.html')
	with open(html_file, 'w') as f:
		f.write(str(template))
	
	return html_file

def compile_note(md_file: str, dest: str = 'notes/') -> Tuple[str, str, str]:
	'''
	Construct HTML from markdown file and html template

	:param md_file: path to Markdown notes file
	:param template_file: path to template HTML file
	:param dest: path to html destination

	:return: (html path, title, date string)
	'''
	with open('templates/note.html', 'r') as f:
		template = soup(f) 

	with open(md_file, 'r') as f:
		content = md_to_html(f)
	
	directory, filename = path.split(md_file)
	name, ext = path.splitext(filename)

	title, date = parse_filename(filename)
	template.head.title.string = title
	template.body.find(id='page-title').string = title
	template.body.find(id='page-date').string = date
	template.body.append(content)
	
	html_file = path.join(dest, name + '.html')
	with open(html_file, 'w') as f:
		f.write(str(template))
	
	return html_file, title, date

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Lunar Knights Markdown Static Site Generator')

	group = parser.add_mutually_exclusive_group()

	group.add_argument('-f', '--file', type=str, help='Generate a single site page.')
	group.add_argument('-n', '--note', type=str, help='Generate a single notes page.')
	group.add_argument('--reset', action='store_true', help='Regenerate all note files.')
	group.add_argument('--add', type=str, help='Add a single note to the main directory.')
	parser.add_argument('-w', '--watch', action='store_true', help='Enable watch mode.')

	args = parser.parse_args()

	if args.note is not None:
		if args.watch: watch(file=args.note, callback=compile_note)
		else: compile_note(args.note)
	elif args.file is not None:
		if args.watch: watch(file=args.file, callback=compile_file)
		else: compile_file(args.file)
	elif args.add is not None:
		if args.watch: warn('Argument `watch` is not compatible with `add` and will be ignored.')
		with open('index.html', 'r') as f:
			main = soup(f)

		link, title, date = compile_note(args.add)
			
		entry = f'<div><h2><a class="lklink unstyled" href="{link}"><div>{title}<span class="lkdate">{date}</span></div></a></h2></div>'
		main.body.div.insert(0, soup(entry))
		print(f'Added {title} - {date}')
	elif args.reset:	
		if args.watch: warn('Argument `watch` is not compatible with `reset` and will be ignored.')
		
		with open('templates/main.html', 'r') as f:
			main = soup(f) 

		notes = sorted([path.join(NOTES, file) for file in listdir(NOTES) if file.endswith('.md')])
		for file in reversed(notes):
			link, title, date = compile_note(file)
			print(f'Finished {title} - {date}')
			entry = f'<div><h2><a class="lklink unstyled" href="{link}"><div>{title}<span class="lkdate">{date}</span></div></a></h2></div>'
			main.body.div.append(soup(entry))
	
		with open('index.html', 'w') as f:
			f.write(str(main))

