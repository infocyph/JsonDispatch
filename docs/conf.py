import os
import sys
from datetime import date

project = "JsonDispatch – Developer Guide"
author = "Infocyph"
copyright = f"{date.today().year}, {author}"
release = "1.0.0"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
]

myst_enable_extensions = [
    "attrs_inline",
    "colon_fence",
    "deflist",
    "fieldlist",
    "linkify",
    "substitution",
    "tasklist",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

copybutton_prompt_text = r"$ |>>> |\(venv\)\$ "
copybutton_prompt_is_regexp = True

nitpicky = True
html_title = "JsonDispatch – Developer Guide"
