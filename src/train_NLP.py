import pandas as pd
import re, string, unicodedata
import nltk
from nltk.corpus import stopwords
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
import numpy as np


dat=pd.read_csv('../data/review_set.csv',encoding='utf-8')
dat['review']=dat['review'].apply(lambda x: 1 if int(x)>3 else 0)



train, test = train_test_split(dat, test_size=0.2, random_state=1)
X_train = train.text
X_test = test.text
y_train = train['review']
y_test = test['review']



en_stopwords = set(stopwords.words("english")) 

vectorizer = CountVectorizer(
    analyzer = 'word',
    lowercase = True,
    ngram_range=(1, 1),
    stop_words = en_stopwords)

kfolds = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)

np.random.seed(1)

pipeline_svm = make_pipeline(vectorizer, 
                            SVC(probability=True, kernel="linear", class_weight="balanced"))

grid_svm = GridSearchCV(pipeline_svm,
                    param_grid = {'svc__C': [0.01, 0.1, 1]}, 
                    cv = kfolds,
                    scoring="roc_auc",
                    verbose=1,   
                    n_jobs=-1) 

grid_svm.fit(X_train, y_train)

joblib.dump(grid_svm, '../train.pkl') 

f_test=open("../data/test.txt",'w')
f_test_lb=open("../data/test_lb.txt",'w')

for i in X_test:
	f_test.write(i.encode('utf8')+"\n")
for i in y_test:
	f_test_lb.write(str(i)+"\n")

f_test.close()
f_test_lb.close()







