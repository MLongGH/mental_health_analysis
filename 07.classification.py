import pandas
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

# load data
data = pandas.read_csv('./data/text-label-csv2.csv')

# shuffle the data
data = data.sample(frac=1).reset_index(drop=True)

# create list from dataframe and split train and test data
train = data[0:300]
test = data[300:]

# extract review and label from train and test data
train_review = train['review'].tolist()
train_label = train['label'].tolist()

test_review = test['review'].tolist()
test_label = test['label'].tolist()

# use pipe line to combine the separate steps
# from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

# load data
categories = ['useful', 'noise']

## train the model with Naive Bayes
from sklearn.pipeline import Pipeline

text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])
text_clf = text_clf.fit(train_review, train_label)

docs_test = test_review
predicted1 = text_clf.predict(docs_test)

print("---------")
print("use Naive Bayes")
print(np.mean(predicted1 == test_label))
print("---------")

## using random forest

text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', RandomForestClassifier()), ])
text_clf = text_clf.fit(train_review, train_label)

docs_test = test_review
predicted2 = text_clf.predict(docs_test)
print("---------")
print("use random forest")
print(np.mean(predicted2 == test_label))
print("---------")

## Use SVM to train data and predict and evaluate
from sklearn.linear_model import SGDClassifier

text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)), ])
_ = text_clf.fit(train_review, train_label)
predicted3 = text_clf.predict(docs_test)
print("---------")
print("use SVM")
print(np.mean(predicted3 == test_label))
print("---------")

# analyze the result
print(metrics.classification_report(test_label, predicted1, target_names=categories))
print(metrics.classification_report(test_label, predicted2, target_names=categories))
print(metrics.classification_report(test_label, predicted3, target_names=categories))

# confusion matrix
# print(metrics.confusion_matrix(test_label, predicted))
