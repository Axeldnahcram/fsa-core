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

stopwords = set(stopwords.words('french'))
LOGGER.info(stopwords)

from fsa_utils.commons import get_asset_root, get_file_content

list_numbers = [i for i in range(0, 10)]
list_numbers = [str(i) for i in list_numbers]


def bible_anailzation():
    cfg = get_asset_root()
    directory = get_file_content(cfg, "bible_no_end")
    g = open(directory)
    for line in g:
        for i in range(0, 15):
            if line[0] not in list_numbers:
                break
            if line[i] == " ":
                line = line.replace(line[0:i + 1], "")
                break
        print(line)


def text_formater():
    g = get_asset_root()
    directory = f'{g["html_root"]}/bible'
    t = os.listdir(directory)
    for i in range(len(t)):
        t[i] = f'{g["html_root"]}/bible/{t[i]}'
    text_final = open('Bible_finale.txt', "w", encoding='utf-8')
    LOGGER.info(t)
    g = 0
    for director in t:
        f = codecs.open(director, encoding='latin1', errors='ignore')
        text_genese = f.read()
        regexp = "&.+?;"
        list_of_html = re.findall(regexp, text_genese)
        dict_replace_entities = {}
        for i in list_of_html:
            dict_replace_entities[i] = replace_entities(i)
        for key, value in dict_replace_entities.items():
            text_genese = text_genese.replace(key, value)
        # print(text_genese)
        regp = "<.+?>"
        list_of_html = re.findall(regp, text_genese)
        # print(list_of_html)
        for i in list_of_html:
            text_genese = text_genese.replace(i, "")
        # print(text_genese)
        for i in list_numbers:
            text_genese = text_genese.replace(i, "")
        text_genese = text_genese.replace("\n", "")
        text_genese = text_genese.replace("\t", " ")
        # text_genese = text_genese.replace("\t", "")
        text_genese = text_genese.replace(" . ", ". ")
        t = text_genese.split()
        text_genese = text_genese.replace(t[0], "")
        LOGGER.info(director)
        dh = open(f'{t[0]}_{g}.txt', "w", encoding='utf-8')
        dh.write(text_genese)
        dh.close()

        word_tokens = text_genese.split()

        word_tokens = [i.lower() for i in word_tokens]

        filtered_sentence = [w for w in word_tokens if w not in stopwords]
        LOGGER.info(filtered_sentence)
        text = str.join(" ", filtered_sentence)
        text_final.write(text)
        LOGGER.info(text)
        # wc = WordCloud(width=800, height=400).generate(text)
        # image = wc.to_image()
        # image.show()
        g = g + 1
    text_final.close()


def text_cloud(evangile):
    g = get_asset_root()
    directory = f'{g["html_root"]}/bible'
    director = f'{g["html_root"]}/bible/{evangile}.html'

    f = codecs.open(director, encoding='latin1', errors='ignore')
    text_genese = f.read()
    regexp = "&.+?;"
    list_of_html = re.findall(regexp, text_genese)
    dict_replace_entities = {}
    for i in list_of_html:
        dict_replace_entities[i] = replace_entities(i)
    for key, value in dict_replace_entities.items():
        text_genese = text_genese.replace(key, value)
    # print(text_genese)
    regp = "<.+?>"
    list_of_html = re.findall(regp, text_genese)
    # print(list_of_html)
    for i in list_of_html:
        text_genese = text_genese.replace(i, "")
    # print(text_genese)
    for i in list_numbers:
        text_genese = text_genese.replace(i, "")
    text_genese = text_genese.replace("\n", "")
    text_genese = text_genese.replace("\t", " ")
    # text_genese = text_genese.replace("\t", "")
    text_genese = text_genese.replace(" . ", ". ")
    t = text_genese.split()
    text_genese = text_genese.replace(t[0], "")
    for i in [".", ",", ":", "'", "?", "!"]:
        text_genese = text_genese.replace(i, " ")
    LOGGER.info(director)
    dh = open(f'text_fr/{t[0]}.txt', "w", encoding='utf-8')
    dh.write(text_genese)
    dh.close()

    word_tokens = text_genese.split()

    word_tokens = [i.lower() for i in word_tokens]

    filtered_sentence = [w for w in word_tokens if w not in stopwords]
    LOGGER.info(filtered_sentence)
    text = str.join(" ", filtered_sentence)
    LOGGER.info(text)
    wc = WordCloud(width=800, height=400).generate(text)
    image = wc.to_image()
    image.show()


def text_analizer(directory):
    cfg = get_asset_root()
    tr = get_file_content(cfg, directory)
    text = open(tr, encoding="utf-8")
    t = text.read()
    word_tokens = t.split()
    word_tokens = [i.lower() for i in word_tokens]
    LOGGER.info(stopwords)
    filtered_sentence = [w for w in word_tokens if w not in stopwords]
    # LOGGER.info(filtered_sentence)
    text = str.join(" ", filtered_sentence)
    # LOGGER.info(text)
    wc = WordCloud(width=800, height=400).generate(text)
    image = wc.to_image()
    image.show()


def text_analyser_concat(liste_text: list):
    text_final = open('concat_text', "w", encoding='utf-8')
    cfg = get_asset_root()
    for director in liste_text:
        directory = get_file_content(cfg, f'/text_bible_fr/{director}')
        text_genese = open(directory, encoding='utf-8')
        text_genese = text_genese.read()
        text_genese = text_genese.replace("dit", " ")
        # dh = open(f'text_fr/{t[0]}.txt', "w", encoding='utf-8')
        # dh.write(text_genese)
        # dh.close()

        word_tokens = text_genese.split()

        word_tokens = [i.lower() for i in word_tokens]

        filtered_sentence = [w for w in word_tokens if w not in stopwords]
        LOGGER.info(filtered_sentence)
        text = str.join(" ", filtered_sentence)
        text_final.write(text)
        LOGGER.info(text)
        wc = WordCloud(width=800, height=400).generate(text)
        image = wc.to_image()
        image.show()
    text_final.close()


def plot_wc_file(directory):
    text = open(directory, encoding='utf-8')
    text = text.read()
    wc = WordCloud(width=800, height=400).generate(text)
    image = wc.to_image()
    image.show()


if __name__ == "__main__":
    # cfg = get_asset_root()
    # directory = get_file_content(cfg, "bible/01.Genese")
    # print(directory)
    # list_accent= ["acute, grave, circ, cedil"]
    # list_voyel = ["a","e","i","o", "u","y", "c"]
    #
    # f = codecs.open(directory, encoding='latin1', errors='ignore')
    # text_genese = f.read()
    # regexp = "&.+?;"
    # list_of_html = re.findall(regexp, text_genese)
    # dict_replace_entities = {}
    # for i in list_of_html:
    #     dict_replace_entities[i]=replace_entities(i)
    # for key, value in dict_replace_entities.items():
    #     text_genese = text_genese.replace(key, value)
    # # print(text_genese)
    # regp = "<.+?>"
    # list_of_html = re.findall(regp, text_genese)
    # # print(list_of_html)
    # for i in list_of_html:
    #     text_genese = text_genese.replace(i, "")
    # # print(text_genese)
    # for i in list_numbers:
    #     text_genese = text_genese.replace(i,"")
    # text_genese = text_genese.replace("\n", "")
    # text_genese = text_genese.replace("\t", "")
    # text_genese = text_genese.replace(". . ", ". ")
    # text_genese = text_genese.replace("Genèse  ", "")
    # print(text_genese[2000:3000])
    liste_ancien_testa = ["Pierre_23", "Pierre_47", "Jean_8", "Jean_16", "Jean_24", "Jean_27", "Luc_20", "Marc_60",
                          "Matthieu_14", "Pierre_23", "Pierre_47"]
    liste_pentateuque = ["Genèse_13", "Exode_56", "Lévitique_41", "Nombres_62", "Deutéronome_5"]
    liste_histo = ["Josué_21", "Juges_4", "Ruth_53", "Samuel_18", "Samuel_50", "Rois_43", "Rois_63", "Chroniques_17",
                   "Chroniques_48",
                   "Esdras_29", "Esther_28", "Néhémie_1"]
    liste_prophetes = ["Esaïe_19", "Jérémie_40", "Lamentations_54", "Ezéchiel_2", "Daniel_59", "Osée_7", "Joël_26",
                       "Amos_45", "Abdias_58", "Jonas_10", "Michée_44", "Nahum_9", "Habacuc_39", "Sophonie_57",
                       "Aggée_0", "Zacharie_46", "Malachie_36"]
    liste_hagiographes = ["Job_42", "Psaumes_3", "Proverbes_34", "Ecclésiaste_11", "Cantique_52"]
    text_analyser_concat(liste_hagiographes)
    plot_wc_file("concat_text")
