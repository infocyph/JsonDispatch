# docs/conf.py — JsonDispatch (Sphinx 8.x / Python 3.11+)
from __future__ import annotations
import os, datetime
from subprocess import Popen, PIPE

# --- Project information -----------------------------------------------------
project   = "JsonDispatch – Developer Guide"
author    = "Infocyph"
year_now  = datetime.date.today().strftime("%Y")
copyright = f"2022-{year_now}"

def get_version() -> str:
    # Prefer RTD version (e.g., 'latest', tag names, or branch)
    if os.environ.get("READTHEDOCS") == "True":
        v = os.environ.get("READTHEDOCS_VERSION")
        if v:
            return v
    try:
        # Works in detached HEAD
        pipe = Popen("git rev-parse --abbrev-ref HEAD", stdout=PIPE, shell=True, universal_newlines=True)
        v = (pipe.stdout.read() or "").strip()
        return v or "latest"
    except Exception:
        return "latest"

version = get_version()
release = version
language = "en"

# Sphinx 8 root document
root_doc = "index"

# --- Syntax highlighting (PHP) ----------------------------------------------
from pygments.lexers.web import PhpLexer
from sphinx.highlighting import lexers
highlight_language = "php"
lexers["php"]             = PhpLexer(startinline=True)
lexers["php-annotations"] = PhpLexer(startinline=True)

# --- Extensions --------------------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.phpdomain",
    "sphinx.ext.extlinks",
]

# MyST (Markdown) settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "attrs_block",
    "attrs_inline",
    "tasklist",
    "fieldlist",
    "linkify",
]
myst_heading_anchors = 3

# Autodoc/Napoleon
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
napoleon_google_docstring = True
napoleon_numpy_docstring  = False
autosectionlabel_prefix_document = True

# Intersphinx: only include inventories that exist
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# extlinks shortcut for PHP manual
extlinks = {
    "php": ("https://www.php.net/%s", "%s"),
}

# TODOs visible in HTML
todo_include_todos = True

# --- HTML output (Book Theme) -----------------------------------------------
html_theme = "sphinx_book_theme"
html_theme_options = {
    # You can set your repository URL here if available
    # "repository_url": "https://github.com/infocyph/jsondispatch",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": False,
    "use_issues_button": False,
    "use_download_button": True,   # PDF/ePub when provided by RTD
    "home_page_in_toc": True,
    "show_toc_level": 2,           # depth in right sidebar
}
templates_path   = ["_templates"]
html_static_path = ["_static"]
html_css_files   = ["theme.css"]
html_title       = f"JsonDispatch – {version} Documentation"
html_show_sourcelink = True
html_show_sphinx    = False
html_last_updated_fmt = "%Y-%m-%d"

# --- PDF (LaTeX) options (optional) -----------------------------------------
latex_engine = "xelatex"
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "preamble": "",
    "figure_align": "H",
}

# GitHub context (book theme uses the buttons above)
html_context = {
    "display_github": False,
    "github_user": "infocyph",
    "github_repo": "jsondispatch",
    "github_version": version,
    "conf_py_path": "/docs/",
}

# Substitution for current year
rst_prolog = f"""\
.. |current_year| replace:: {year_now}
"""
