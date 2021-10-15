# Lunar Knights Github Page

Repository for markdown based meeting notes.

## Contributing

Create & edit markdown files in the `md` directory. The name of your file should follow the format `YYYYMMDD_your_title.md`. Do not edit `index.html` or `notes/` as they are automatically generated. Feel free to edit the `templates/` files to change the base of each page.

### Dependencies

Create a python virtual environment: `python3 -m venv .venv`

Install the requirements: `pip install -r requirements.txt` or individual packages in your virtual environment:

-   `markdown-it-py`
-   `mdit_py_plugins`
-   `beautifulsoup4`

### Building

Activate your virtual environment and run `python compile.py --help` for instructions.

To add a brand new notes page use `python compile.py --add <FILE>`.

To update a single notes page use `python compile.py -n <FILE>`.

To turn on watch mode use the `-w` flag.

You can also generate an html page for an arbitrary file using `-f <FILE>`

Launch a server locally in the root directory to see changes. For example: `php -S localhost:8080`

