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
import scattertext



from fsa_utils.commons import get_asset_root, get_file_content



class Text_wordcloud(object):
    def __init__(self, list_directory, encoding:str='utf-8', html=False, numbers=True, with_stopwords=True, lowercase=True, language='french', plus_stopwords:list=None):
        self.directory = list_directory
        self.encoding=encoding
        self.stopwords = list(set(stopwords.words(language)))
        if plus_stopwords is not None:
            for i in plus_stopwords:
                self.stopwords.append(i)
        self.text = self.concat_text(html, numbers, with_stopwords, lowercase)
        self.wordcloud = WordCloud(width=800, height=400).generate(self.text)

    def concat_text(self, html, numbers, with_stopwords, lowercase):
        """
        concat the different texts into one
        :param html: say if you need to decode the &.... in the html file
        :type html: BOOL
        :param numbers: tell if you wanna remove the numbers
        :type numbers: Bool
        :return: text of the different text all concat
        :rtype: str
        """
        cfg = get_asset_root()
        text = ""
        for i in self.directory:
            director = get_file_content(cfg, i)
            cur_text = open(director,encoding=self.encoding)
            cur_text = cur_text.read()
            if html == True:
                cur_text = Text_wordcloud.clean_html(cur_text)
            if numbers == True:
                cur_text = Text_wordcloud.clean_numbers(cur_text)
            if with_stopwords == True:
                cur_text = Text_wordcloud.clean_stopwords(cur_text, self.stopwords)
            if lowercase == True:
                cur_text = Text_wordcloud.clean_maj(cur_text)
            text = f"{text} {cur_text}"
        return text

    def save_text(self, directory):
        write_text = open(directory, "w", encoding="utf-8")
        write_text.write(self.text)
        write_text.close()

    def show(self):
        image = self.wordcloud.to_image()
        image.show()

    @staticmethod
    def clean_numbers(text:str):
        """
        remove all the numbers from a text
        """
        list_numbers = [i for i in range(0, 10)]
        list_numbers = [str(i) for i in list_numbers]
        for i in list_numbers:
            text = text.replace(i, "")
        return text

    @staticmethod
    def clean_html(text:str):
        """
        remove all the & and the <> from the text
        """
        regexp = "&.+?;"
        list_of_html = re.findall(regexp, text)
        dict_replace_entities = {}
        for i in list_of_html:
            dict_replace_entities[i] = replace_entities(i)
        for key, value in dict_replace_entities.items():
            text = text.replace(key, value)
        regp = "<.+?>"
        list_of_html = re.findall(regp, text)
        for i in list_of_html:
            text = text.replace(i, "")
        return text

    @staticmethod
    def clean_stopwords(text:str, stop_words:list):
        LOGGER.info(stop_words)
        word_tokens = text.split()

        word_tokens = [i.lower() for i in word_tokens]

        filtered_sentence = [w for w in word_tokens if w not in stop_words]
        text = str.join(" ", filtered_sentence)
        LOGGER.info(text)
        return text

    @staticmethod
    def clean_maj(text:str):
        word_tokens = text.split()

        word_tokens = [i.lower() for i in word_tokens]
        text = str.join(" ", word_tokens)
        return text


if __name__ == "__main__":
    g = Text_wordcloud(["french_books_no_meta/Zola_assommoir"], language='french', plus_stopwords=["plu","cette","cela","tous","là","toute", "tout", "plus", "c'était","ça"])
    g.show()