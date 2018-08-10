from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
import numpy as np
from sklearn.metrics import confusion_matrix,accuracy_score
 

f_test=open("../data/test.txt").readlines()
X_test=map(lambda x:x.strip("\n"),f_test)
f_test_lab=open("../data/test_lb.txt").readlines()
y_test=map(lambda x:int(x.strip("\n")),f_test_lab)
grid_svm = joblib.load('../train.pkl') 
X_pred= grid_svm.predict(X_test)
matrix=confusion_matrix(y_test,X_pred)
score=accuracy_score(y_test,X_pred)
print score
print matrix
