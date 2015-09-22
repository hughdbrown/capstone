#!/usr/bin/env python
from __future__ import print_function, absolute_import

# Standard library
import os
import os.path
from sys import stderr, exit
import re
import string
from datetime import datetime

# 3rd party libraries
import simplejson
import pandas as pd
from pandas import DataFrame, Series
import numpy as np

from bs4 import BeautifulSoup

from pymongo import MongoClient

from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

import matplotlib.pyplot as plt

from wordcloud import WordCloud


from script.utils.clean_data import visible_text, clean, SCRIPT, STYLE, LINK, CONDITIONAL, HEAD


CLEAN_DIR = "topic-modeling/clean"
RAW_DIR = "topic-modeling/raw"
SHORT_URL_COUNT = "data/short_url_count"

NUMBER = re.compile(r'''\d+''')
LANGUAGES = [
    'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian',
    'italian', 'norwegian', 'portuguese', 'russian', 'spanish', 'swedish', 'turkish'
]

# Pay no attention to the man behind the curtain
CSS_STOP_WORDS = [
    'html', 'head', 'body', 'div', 'li', 'span', 'script', 'image',
    'amp', 'href', 'com', 'ie8', 'css', 'ico', 'img', 'id',
    'http', 'www',
    'var', 'alt',
    'lte', 'lt', 'ie', 'endif', 'iemobile',
    'caption', 'imageposition', 'php',
    'banner', 'tr', 'td', 'icon', 'jpg', 'px', 'font', 'class', 'sub', 'nav',
    'block', 'coltype', 'droplayer', '_blank', 'target',
    'md', 'mt', 'bd', 'link', 'stylesheet', 'quot', 'menu', 'ul', 'li', 'rel',
    'width', 'height', 'clear', 'empty', 'url',
    'caption', 'content', 'code', 'dropdown', 'src', 'png', 'title', 'meta',
    'whatsapp', 'hide', 'close', 'focus', 'tag', 'iphone', 'javascript', 'links',
    'ms', 'mg', 'inner', 'lst', 'hd', 'widget', 'twitter', 'facebook', 't', 'tumblr',
    'button', 'login',
    'linkedin', 'pinterest', "instagram", 'apple',
    "center", "false", "strong", "images", "mr", "contact", "home", "start",
    "ft", "fr", "uk", "us", "co",
    "applelayer", "cookies",
    "rss", "version", "text", "post", "ab", "container",
    "header", "ii",
]


STOP_WORDS = (
    stopwords.words('danish') +
    stopwords.words('dutch') +
    stopwords.words('english') +
    stopwords.words('french') +
    stopwords.words('italian') +
    stopwords.words('spanish') +
    stopwords.words('german') +
    stopwords.words('portuguese') +
    stopwords.words('russian') +
    CSS_STOP_WORDS +
    list(string.punctuation)
)

r1 = re.compile(r'''.* germanwings .*''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
r2 = re.compile(r'''.* 9525 .*''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
r3 = re.compile(r'''.* copilot .*''', re.VERBOSE | re.IGNORECASE | re.DOTALL)
r4 = re.compile(r'''.* Andreas \s+ Lubitz .*''', re.VERBOSE | re.IGNORECASE | re.DOTALL)


def germanwings_score(text):
    return sum(1 for r in (r1, r2, r3, r4) if r.match(text))


def extract_documents():
    """
    Pull documents from mongodb, store on drive
    """
    client = MongoClient()
    conn = client.data
    coll = conn.germanwings

    query = {'text': {'$exists': 1}, 'exc': {'$exists': 0}}
    selection = {'text': 1, 'short_url': 1}
    for i, doc in enumerate(coll.find(query, selection)):
        short_url, text = tuple(doc[x] for x in ("short_url", "text"))
        print("Extracting {0} {1}".format(i, short_url), file=stderr)
        filename = os.path.join(RAW_DIR, short_url)
        with open(filename, "w") as f:
            ascii = text.encode('ascii', 'ignore')
            f.write(ascii)


def clean_documents():
    """
    Produce clean HTML for the documents
    """
    start = datetime.now()
    for i, raw_filename in enumerate(os.listdir(RAW_DIR)):
        fullpath = os.path.join(RAW_DIR, raw_filename)
        if os.path.isfile(fullpath):
            print("Cleaning {0} {1}".format(i, fullpath), file=stderr)
            try:
                with open(fullpath, "r") as f:
                    text = f.read()
                    text = clean(text)
                    soup = BeautifulSoup(text, "html.parser")
                    cleaned = visible_text(soup)
                    score = germanwings_score(cleaned)
                    if not score:
                        print("not germanwings: {0}".format(raw_filename))
                    else:
                        clean_filename = os.path.join(CLEAN_DIR, raw_filename)
                        with open(clean_filename, "w") as f:
                            f.write(cleaned.encode("ascii", "ignore"))
            except Exception as exc:
                print("{0}: {1}".format(fullpath, exc), file=stderr)
    end = datetime.now()
    print("Elapsed time to clean: {0}".format(end - start), file=stderr)


def topic_model(df):
    data = df["text"]
    multiplier = df["count"]
    print("Creating vectorizer", file=stderr)
    tfidf = TfidfVectorizer(stop_words=STOP_WORDS, input='content', lowercase=True, use_idf=True, max_features=1000)
    features = tfidf.fit_transform(data)
    print("features after vectorizing: {0}".format(features.shape))
    print("Scaling feature matrix by multiplier", file=stderr)
    f = np.array(features.todense())
    features = np.multiply(f, multiplier[:, np.newaxis])
    print("features after scaling: {0}".format(features.shape))
    feature_names = tfidf.get_feature_names()
    return features, feature_names


def read_all_documents():
    documents = []
    for raw_filename in os.listdir(CLEAN_DIR):
        fullpath = os.path.join(CLEAN_DIR, raw_filename)
        with open(fullpath) as f:
            text = f.read().lower()
        for regex in (HEAD, SCRIPT, STYLE, LINK, CONDITIONAL, NUMBER):
            text = regex.sub("", text)
        doc = {
            'short_url': raw_filename,
            'text': text,
        }
        documents.append(doc)
    df = DataFrame(documents)
    df.set_index("short_url")
    return df


def print_topics(features, feature_names):
    # http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf.html
    n_topics, n_top_words = 5, 12
    nmf = NMF(n_components=n_topics)
    nmf.fit(features)
    for topic_idx, topic in enumerate(nmf.components_):
        print("Topic #{0}:".format(topic_idx))
        indexes = topic.argsort()
        print(" ".join(
            feature_names[i]
            for i in indexes[:-n_top_words - 1:-1]
        ))
    print('-' * 30)


def calculate_topics(features, n_topics):
    # http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf.html
    nmf = NMF(n_components=n_topics)
    return nmf, nmf.fit_transform(features)


def calculate_topic_words(nmf, feature_names, n_top_words):
    sorted_topic_iter = ((topic.argsort(), topic) for topic in nmf.components_)
    return [
        {
            feature_names[i]: int(1000 * topic[i])
            for i in indexes[:-n_top_words - 1:-1]
        }
        for indexes, topic in sorted_topic_iter
    ]


def title_from_mapping(mapping):
    r = re.compile(r"""
        ^short_url_count.*
        \-
        (?P<country>[A-Z]{2})
        \-
        (?P<year>\d{4})
        \-
        (?P<month>\d{2})
        \-
        (?P<day>\d{2})
        \.json
    """, re.VERBOSE)
    g = r.match(mapping).groupdict()
    return g["country"], int(g["year"]), int(g["month"]), int(g["day"])


def save_topic(topic, mapping, serial):
    country, year, month, day = title_from_mapping(mapping)
    wc = WordCloud(background_color='white', width=800, height=1800)
    wc.generate_from_frequencies(topic.items())
    plt.figure(figsize=(9, 6))
    title = "{0}: {1}-{2}-{3}".format(country, year, month, day)
    plt.title(title, fontsize=18)
    plt.axis('off')
    plt.imshow(wc)
    # plt.tight_layout()
    filename = "wc-{0}-{1}-{2}-{3}-{4}.png".format(country, year, month, day, serial)
    fullpath = os.path.join("images", filename)
    plt.savefig(fullpath)
    plt.close()


def save_topic2(topic, serial):
    wc = WordCloud(background_color='white', width=800, height=1800)
    wc.generate_from_frequencies(topic.items())
    plt.figure(figsize=(9, 6))
    title = "Topic {0}".format(serial)
    plt.title(title, fontsize=18)
    plt.axis('off')
    plt.imshow(wc)
    # plt.tight_layout()
    filename = "topic-{0}.png".format(serial)
    fullpath = os.path.join("images", filename)
    plt.savefig(fullpath)
    plt.close()


def topic_modeling():
    print("Reading all the GermanWings documents into memory", file=stderr)
    df = read_all_documents()
    df.set_index(["short_url"])
    for i, mapping in enumerate(os.listdir(SHORT_URL_COUNT)):
        fullpath = os.path.join(SHORT_URL_COUNT, mapping)
        print("Loading {0}: {1}".format(i, fullpath), file=stderr)
        with open(fullpath) as f:
            d = simplejson.loads(f.read())
            urls_with_count = DataFrame(d)
            urls_with_count.set_index(["short_url"])

        # Produce short_url / text / hit_count
        print("Merging dataframes", file=stderr)
        filtered_df = df.merge(right=urls_with_count)
        print("Topic model of merged dataframe", file=stderr)
        features, vocab = topic_model(filtered_df)
        topics = calculate_topics(features, vocab)
        for i, topic in enumerate(topics):
            save_topic(topic, mapping, i)


def read_all_hits():
    filename = os.path.join("data", "hits-aggregated.csv")
    df = pd.read_csv(filename, names=["short_url", "count"])
    df.set_index(["short_url"])
    return df


def topic_modeling2():
    n_topics, n_top_words = 15, 32

    # short_url / text
    print("Reading all the GermanWings documents into memory", file=stderr)
    df = read_all_documents()
    print("short_url/text: {0}".format(df.shape))

    # short_url / hits
    print("Reading all the document hits", file=stderr)
    df_doc_hits = read_all_hits()
    print("short_url/count: {0}".format(df_doc_hits.shape))

    # short_url / text / hits
    print("Merging dataframes", file=stderr)
    filtered_df = df.merge(right=df_doc_hits)
    print("short_url/count: {0}".format(filtered_df.shape))

    print("Creating features and vocab", file=stderr)
    features, feature_names = topic_model(filtered_df)

    print("NMF", file=stderr)
    nmf, doc_topic = calculate_topics(features, n_topics)
    print("doc_topic: {0}".format(doc_topic.shape))

    topic_words = calculate_topic_words(nmf, feature_names, n_top_words)
    for i, topic in enumerate(topic_words, start=1):
        save_topic2(topic, i)


def main():
    # extract_documents()
    # clean_documents()
    # topic_modeling()
    topic_modeling2()


if __name__ == '__main__':
    main()