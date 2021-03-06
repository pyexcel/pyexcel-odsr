# -*- coding: utf-8 -*-
DESCRIPTION = (
    'a plugin to pyexcel and provides the capbility to read data in ods for' +
    'mats using tailored messytables.' +
    ''
)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

intersphinx_mapping = {
    'pyexcel': ('http://pyexcel.readthedocs.io/en/latest/', None),
}
spelling_word_list_filename = 'spelling_wordlist.txt'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'pyexcel-odsr'
copyright = u'2015-2017 Onni Software Ltd.'
version = '0.5.2'
release = '0.5.2'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'pyexcel-odsrdoc'
latex_elements = {}
latex_documents = [
    ('index', 'pyexcel-odsr.tex',
     'pyexcel-odsr Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'pyexcel-odsr',
     'pyexcel-odsr Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'pyexcel-odsr',
     'pyexcel-odsr Documentation',
     'Onni Software Ltd.', 'pyexcel-odsr',
     DESCRIPTION,
     'Miscellaneous'),
]
