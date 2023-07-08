import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from data_wrangling import DataManipulation

class DataPreparation:
    def __init__(
            self, dataframe:pd.DataFrame, 
            target_var: str, test_size:float
            ):
        self.dataframe = dataframe
        self.target_var = target_var
        self.test_size = test_size
        self.X = None
        self.y = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.getVars()
        self.trainTestSplit()

    def getVars(self):
        self.y = self.dataframe[self.target_var]
        self.X = self.dataframe.drop([self.target_var], axis=1)

    def trainTestSplit(self):
        self.X_train, self.X_test, self.y_train, self.y_test = \
        train_test_split(self.X, self.y, test_size=self.test_size)


class ModelTraining:
    def __init__(
            self, n_estimators:int, max_depth:int,
            X_train, X_test, y_train, y_test
            ):
        self.model = None
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def accuracyCheck(self, y_prediction):
        accuracy = accuracy_score(self.y_test, y_pred=y_prediction)
        return accuracy


    def modelTraining(self):
        self.model = RandomForestClassifier(
            n_estimators=self.n_estimators, 
            max_depth=self.max_depth
            )

        self.model.fit(self.X_train, self.y_train)
        result_model = self.model.predict(self.X_test)
        accuracy = self.accuracyCheck(result_model)

        # if accuracy
        # vai ser necessário fazer uma processo como esse acima, mas para
        # um modelo que já exista old.model
        # para comparar o treinamento de um modelo antigo em uso,
        # com o modelo em treinamento novo, utilizando as mesmas bases de dados.





# model_randomforest_v5 = RandomForestClassifier(
#     n_estimators=150, max_depth=8, 
#     )

# model_randomforest_v5.fit(X_train, y_train)