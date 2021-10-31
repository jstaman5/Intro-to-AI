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
  
    #split our test and training data
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = .8, random_state = 0)
    
    #Coarse Grid Search on hyperparameters
    '''tuned_parameters = [
        {
            'kernel': ['linear'], 
            'C': [1, 10, 100, 1000]
        },
        {
            'kernel': ['poly'], 
            'degree': [2, 3, 4],
            'C': [1, 10, 100, 1000]
        },
        {
            'kernel': ['rbf'], 
            'gamma': [1e-3, 1e-4],
            'C': [1, 10, 100, 1000]
        }
    ]
    scores = ['precision', 'recall']
    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()
        clf = GridSearchCV(
            SVC(), tuned_parameters, scoring='%s_macro' % score
        )
        clf.fit(x_train, y_train)
        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                % (mean, std * 2, params))
        print()
        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(x_test)
        print(classification_report(y_true, y_pred))
        print()    
        print()
        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")'''


    #From the coarse grid search: our best hyperparamters were linear and C=100
    #Fine Search to fine tune the C hyperparameter
    #We are looking for the smallest C value that still gives a 1.000
    #Our result was C = 34
    l = [i for i in range(30,50,1)]
    tuned_parameters = [
        {
            'kernel': ['linear'], 
            'C': l
        }]

    scores = ['precision', 'recall']
    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()
        clf = GridSearchCV(
            SVC(), tuned_parameters, scoring='%s_macro' % score
        )
        clf.fit(x_train, y_train)
        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                % (mean, std * 2, params))
        print()
        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(x_test)
        print(classification_report(y_true, y_pred))
        print()    
        print()
        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
    return

if __name__ == "__main__":
    main()