import os
import shutil
from pathlib import Path

project = "JsonDispatch Specification"
author = "Infocyph"
version = "3.0"
release = "3.0.0"

root_doc = "index"
language = "en"
extensions = []
exclude_patterns = ["_build"]
nitpicky = True

html_theme = "sphinx_book_theme"
html_title = f"JsonDispatch {release}"
html_baseurl = os.environ.get(
    "READTHEDOCS_CANONICAL_URL",
    "https://docs.infocyph.com/projects/json-dispatch/en/latest/",
)
html_context = {
    "READTHEDOCS": os.environ.get("READTHEDOCS") == "True",
}
html_theme_options = {
    "home_page_in_toc": True,
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": False,
    "use_issues_button": False,
    "use_download_button": True,
}


def copy_conformance_artifacts(app, exception):
    if exception is not None or app.builder.format != "html":
        return

    repository = Path(__file__).resolve().parents[1]
    output = Path(app.outdir)

    for directory in ("schemas", "fixtures"):
        shutil.copytree(
            repository / directory,
            output / directory,
            dirs_exist_ok=True,
        )

    shutil.copy2(repository / "specification.json", output / "specification.json")


def setup(app):
    app.connect("build-finished", copy_conformance_artifacts)
