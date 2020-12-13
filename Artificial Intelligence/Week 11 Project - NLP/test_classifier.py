"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 11 Project - NLP
"""
# Import necessary libraries
from os import walk
import pandas as pd
from csv import writer
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import SGDClassifier


class TextClassifier:

    def __init__(self, stop_words_file=None, train_path=None, test_path=None):
        self.train_path = train_path
        self.stop_words_file = stop_words_file
        self.stop_words_list = list()
        self.stop_words_set = set()
        self.extract_stop_words()
        self.train_file_path = self.merge_csv_files(self.train_path)
        self.clf = None
        self.vocabulary = None
        self.train_data = self.get_train_data(self.train_file_path)
        self.test_data = self.get_test_data(test_path)

    def extract_stop_words(self):
        with open(self.stop_words_file, 'r') as sw_file:
            self.stop_words_list = sw_file.read().splitlines()
            self.stop_words_set = set(self.stop_words_list)

    def format_text(self, raw_text):

        formatted_text = raw_text.replace('<br />', ' ')
        for c in punctuation:
            formatted_text = raw_text.replace(c, ' ')

        words_list = formatted_text.split()
        formatted_text = ' '.join([word for word in words_list if word.lower not in self.stop_words_set])
        return formatted_text

    def merge_csv_files(self, input_dir=None, merged_csv='imdb_tr.csv'):

        pos_neg_folders = ['pos/', 'neg/']
        with open(merged_csv, 'w', newline='') as merge_csv_file:
            csv_writer = writer(merge_csv_file)
            # Add Column Header
            csv_writer.writerow(['', 'text', 'polarity'])
            index = -1
            for folder in pos_neg_folders:
                folder_path = f"{input_dir}/{folder}"
                for root, dirs, filenames in walk(folder_path):
                    for filename in filenames:
                        index = index + 1
                        polarity = 1 if folder == 'pos/' else 0
                        with open(f"{folder_path}/{filename}", 'r') as text_file:
                            text = text_file.read().strip()
                        formatted_text = self.format_text(text)
                        csv_writer.writerow([index, formatted_text, polarity])
        return merged_csv

    @staticmethod
    def load_csv_to_df(file_path=None, encoding="utf-8"):
        return pd.read_csv(file_path, encoding=encoding)

    def get_train_data(self, file_path='imdb_tr.csv'):
        df = self.load_csv_to_df(file_path, encoding="utf-8")
        return df

    def get_test_data(self, file_path='imdb_tr.sample.csv', encoding='ISO-8859-1'):
        df = self.load_csv_to_df(file_path, encoding=encoding)
        df['text'] = df['text'].apply(self.format_text)
        return df

    def apply_sgd_classifier(self, vectorizer=None):
        matrix = vectorizer.fit_transform(self.train_data['text'])
        self.vocabulary = vectorizer.vocabulary_
        clf = SGDClassifier(loss='modified_huber', penalty='l1')
        clf.fit(matrix, self.train_data['polarity'])
        self.clf = clf

    def train_using_count(self, n_gram=1):
        count_vectorizer = CountVectorizer(ngram_range=(1, n_gram),
                                           stop_words=self.stop_words_list)
        self.apply_sgd_classifier(count_vectorizer)

    def train_using_tfidf(self, n_gram=1):
        tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, n_gram),
                                           stop_words=self.stop_words_list)
        return self.apply_sgd_classifier(tfidf_vectorizer)

    def test_using_tfidf(self, n_gram=1):
        vectorizer = TfidfVectorizer(ngram_range=(1, n_gram),
                                     stop_words=self.stop_words_list,
                                     vocabulary=self.vocabulary)

        matrix = vectorizer.fit_transform(self.test_data['text'])
        return self.clf.predict(matrix)

    def test_using_count(self, n_gram=1):
        vectorizer = CountVectorizer(ngram_range=(1, n_gram),
                                     stop_words=self.stop_words_list,
                                     vocabulary=self.vocabulary)

        matrix = vectorizer.fit_transform(self.test_data['text'])
        return self.clf.predict(matrix)
