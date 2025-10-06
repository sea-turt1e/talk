# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "manga-graph-presentation-stapy"
copyright = "2025, sea-turt1e"
author = "sea-turt1e"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_revealjs",
    'sphinxemoji.sphinxemoji',
]

revealjs_script_plugins = [
    # Reveal.js組み込みのシンタックスハイライトプラグインを使う
    {
        "name": "RevealHighlight",
        "src": "revealjs/plugin/highlight/highlight.js",
    },
    {
        "name": "RevealNotes",
        "src": "revealjs/plugin/notes/notes.js",
    },
]
revealjs_css_files = [
    # プラグインとセットで対応するCSSが同梱されているので、これを追加で使用
    "revealjs/plugin/highlight/zenburn.css",
]

revealjs_style_theme = 'serif'

templates_path = ["_templates"]
exclude_patterns = []

language = "ja"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
