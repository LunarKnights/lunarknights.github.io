# Lunar Knights Github Page

Repository for markdown based meeting notes.

## Contributing

Create & edit markdown files in the `md` directory. The name of your file should follow the format `YYYYMMDD_your_title.md`. Do not edit `index.html` or `notes/` as they are automatically generated. Feel free to edit `md/template.html` or `templates/main.html` to change the base of each page.

### Dependencies

Create a python virtual environment: `python3 -m venv .venv`

Install the requirements: `pip install -r requirements.txt` or individual packages in your virtual environment:

-   `markdown-it-py`
-   `mdit_py_plugins`
-   `beautifulsoup4`

### Building

Activate your virtual environment and run `python compile.py`

For single file updating use `python compile.py <filename>` or with watch mode `python watch.py <filename>`

Launch a server locally in the root directory to see changes. For example: `php -S localhost:8080`

