#Jared Staman
#CS 423: Machine Learning

import pandas as pd
import numpy as np
import pylab as pl
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

def main():

    #read in mushrooms csv and scrub bad data (? or " ")
    missing_values = ["?", " "]
    df = pd.read_csv("mushrooms.csv", na_values = missing_values)
    df = df.dropna()

    #change data from strings to ascii values
    df = df.apply(LabelEncoder().fit_transform)

    #split the features and our target (poisonous or edible)
    X = df.iloc[:, 1:23].values
    y = df.iloc[:,0].values

    #split data
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=0)

    #make model using the best hyperparameters from svm_search : linear, C = 34
    svc = svm.SVC(kernel='linear', C = 34).fit(x_train, y_train)

    #test model
    predicted_linear = svc.predict(x_test)

    #print accuracy
    print("SVM + Linear \t\t-> " + str(accuracy_score(y_test, predicted_linear)))

    #print precision recall plot
    print(classification_report(y_test, predicted_linear))
    return

if __name__ == "__main__":
    main()