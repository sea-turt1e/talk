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
    # カスタムCSSを追加
    "custom.css",
]

revealjs_style_theme = 'serif'

templates_path = ["_templates"]
exclude_patterns = []

language = "ja"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

revealjs_script_conf = {
    "controls": True,
    "progress": True,
    "history": True,
    "center": True,
    "transition": "none",
    "slideNumber": "c/t",
    # スライドのサイズ設定
    "width": 1280,
    "height": 720,
    # コンテンツの自動スケーリング
    "margin": 0.1,  # スライドの余白
    "minScale": 0.2,  # 最小スケール
    "maxScale": 2.0,  # 最大スケール
}