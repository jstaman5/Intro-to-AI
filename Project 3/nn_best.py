#Jared Staman

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelBinarizer
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn.model_selection import GridSearchCV
from keras.constraints import maxnorm
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import os
import tensorflow as tf

import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('INFO')
tf.compat.v1.disable_eager_execution()

def main():
    
    #get rid of bad data ('?' or ' ')
    missing_values = ["?", " "]
    df = pd.read_csv("mushrooms.csv", na_values = missing_values)
    df = df.dropna()

    #encode to switch data from strings to ints
    df = df.apply(LabelEncoder().fit_transform)

    #y is target (p or e), X is all other features
    X = df.iloc[:, 1:23].values
    y = df.iloc[:,0].values

    #split training and test data
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = .3, random_state = 0)
    
    #standardize data
    scaler = MinMaxScaler(feature_range=(0,1))
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    #General Keras Model function
    def DynamicModel(neuron_one=1, neuron_two=1, activation_one='sigmoid', activation_two='sigmoid'):
        """ 
        A sequential Keras model that has an input layer, one 
        hidden layer with a dymanic number of units, and an output layer.
        """
        model = Sequential()
        model.add(Dense(neuron_one, input_dim=22, activation=activation_one, name='layer_1'))
        model.add(Dense(neuron_two, activation=activation_two, name='layer_2'))
        model.add(Dense(2, activation='sigmoid', name='output_layer'))
        
        # Don't change this!
        model.compile(loss="categorical_crossentropy",
                    optimizer="adam",
                    metrics=['accuracy'])
        return model

    #create the model using the function
    model = KerasClassifier(build_fn=DynamicModel, epochs=200, batch_size=20, verbose=0)

    #define hyperparamters
    param_grid = [
        {
            'activation_one': ['linear'], 
            'activation_two': ['linear'], 
            'neuron_one': [1],
            'neuron_two': [1]
        }
    ]

    grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1)
    grid_result = grid.fit(x_train, y_train)

    #print accuracy, confusion matrix: precision and recall
    print("%f using %s" % (grid_result.best_score_, grid_result.best_params_))
    y_pred = grid.predict(x_test)
    print(classification_report(y_test, y_pred))
    


    return

if __name__ == "__main__":
    main()