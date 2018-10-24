from __future__ import division, unicode_literals
import codecs
from bs4 import BeautifulSoup
import urllib
from logzero import logger as LOGGER
import re
import codecs
from w3lib.html import replace_entities
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import pandas as pd
import scattertext as st
import spacy

from fsa_utils.commons import get_asset_root, get_file_content


class Scatter_french_text(object):
    def __init__(self, list_directory, list_author, language:str='fr', encoding = 'utf-8'):
        self.list_text = self.read_directory(list_directory, encoding)
        self.list_author = list_author
        self.df = pd.DataFrame()
        self.df["text"] = self.list_text
        self.df["author"] = self.list_author
        self.language = language
        self.nlp = spacy.load(language)
        self.corpus = st.CorpusFromPandas(self.df, category_col='author', text_col='text', nlp=self.nlp).build()


    def explorer(self, category, not_category, metadata):
        html = st.produce_scattertext_explorer(self.corpus, category=category, not_category_name=not_category, metadata=metadata)
        open("Corpus-Visualization.html", 'wb').write(html.encode('utf-8'))

    @staticmethod
    def read_directory(list_directory, encoding):
        cfg = get_asset_root()
        list_text= []
        for i in list_directory:
            director = get_file_content(cfg, i)
            text = open(director,encoding=encoding)
            text=text.read()
            list_text.append(text)
        return list_text

if __name__ == '__main__':
    g = Scatter_french_text(["french_books_no_meta/Hugo_Miserables1","french_books_no_meta/Zola_assommoir"], ['Hugo', "Zola"])
    g.explorer("Zola", "Hugo",None)