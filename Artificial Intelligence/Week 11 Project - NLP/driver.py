"""
CSMM.101X - Columbia University - Artificial Intelligence - Week 11 Project - NLP
"""
# Import necessary libraries
from csv import writer
from text_classifier import TextClassifier


def write_results(filename, test_preds):
    with open(filename, 'w', newline='') as preds_file:
        csv_writer = writer(preds_file)
        for prediction in test_preds:
            csv_writer.writerow([prediction])


def main():

    train_path = "../resource/lib/publicdata/aclImdb/train/"  # use terminal to ls files under this directory
    test_path = "../resource/lib/publicdata/imdb_te.csv"  # test data for grade evaluation

    sentiment_classifier = TextClassifier(
        stop_words_file='stopwords.en.txt',
        train_path=train_path,
        test_path=test_path
    )

    '''
        train a SGD classifier using unigram representation,
        predict sentiments on imdb_te.csv, and write output to
        unigram.output.txt
    '''
    sentiment_classifier.train_using_tfidf(n_gram=1)
    predictions = sentiment_classifier.test_using_count(n_gram=1)
    write_results('unigram.output.txt', predictions)

    '''
        train a SGD classifier using bigram representation,
        predict sentiments on imdb_te.csv, and write output to
        bigram.output.txt
    '''
    sentiment_classifier.train_using_tfidf(n_gram=2)
    predictions = sentiment_classifier.test_using_count(n_gram=2)
    write_results('bigram.output.txt', predictions)

    '''
        train a SGD classifier using unigram representation
        with tf-idf, predict sentiments on imdb_te.csv, and write
        output to unigramtfidf.output.txt
    '''
    sentiment_classifier.train_using_tfidf(n_gram=1)
    predictions = sentiment_classifier.test_using_tfidf(n_gram=1)
    write_results('unigramtfidf.output.txt', predictions)

    '''
        train a SGD classifier using bigram representation
        with tf-idf, predict sentiments on imdb_te.csv, and write
        output to bigramtfidf.output.txt
    '''
    sentiment_classifier.train_using_tfidf(n_gram=2)
    predictions = sentiment_classifier.test_using_tfidf(n_gram=2)
    write_results('bigramtfidf.output.txt', predictions)


if __name__ == "__main__":
    main()
