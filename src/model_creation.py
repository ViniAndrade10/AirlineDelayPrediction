import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os
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
        train_test_split(
            self.X, self.y, 
            test_size=self.test_size,
            shuffle=True
            )


class ModelTraining:
    def __init__(
            self, n_estimators:int, max_depth:int,
            X_train, X_test, y_train, y_test
            ):
        self.model = None
        self.old_model = None
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.accuracy = None

        self.modelTraining()

    def accuracyCheck(self, y_prediction):
        accuracy = accuracy_score(self.y_test, y_pred=y_prediction)
        return accuracy

    def modelTraining(self):
        breakpoint()
        self.model = RandomForestClassifier(
            n_estimators=self.n_estimators, 
            max_depth=self.max_depth
            )

        # Checking if a model already exists
        __ROOT_PATH__ = Path(__file__).resolve().parent.parent
        model_path = __ROOT_PATH__ / "src/model"
        accuracy_old_model = 0

        for file in os.listdir(model_path):
            if file.endswith(".sav") or file.endswith(".pkl"):
                old_model_file = model_path / file
                # Getting the old model to predict the curent data
                # and check its accuracy
                self.old_model = pickle.load(open(old_model_file, "rb"))

                result_old_model = self.old_model.predict(self.X_test)
                accuracy_old_model = self.accuracyCheck(result_old_model)
                print(accuracy_old_model)

        # Creating new model to compare accuracy with previous one
        self.model.fit(self.X_train, self.y_train)
        result_model = self.model.predict(self.X_test)
        self.accuracy = self.accuracyCheck(result_model)

        if self.accuracy > accuracy_old_model:
            model_name = "AirDelay_Predictor.sav"
            pickle.dump(self.model, open(model_path /  model_name, "wb"))

            create_code = datetime.today().strftime("%Y%m%d%H%M")
            ml_ops_path = __ROOT_PATH__ / "src/ml_Ops"
            model_mlOps = f"AirDelay_Predictor_{create_code}.sav"
            pickle.dump(self.model, open(ml_ops_path / model_mlOps, "wb"))

            text_to_write = f"\n{model_mlOps}, {self.accuracy}"

            for text_file in os.listdir(ml_ops_path):
                if text_file.endswith(".txt"):

                    with open(ml_ops_path / text_file, mode="a") as file_opened:
                        file_opened.write(text_to_write)
                else:
                    with open(ml_ops_path / "ml_Ops_Tracking.txt", mode="w") as file_opened:
                        header = "Model_Name, Accuracy"
                        file_opened.write(header)
                        file_opened.write(text_to_write)


if __name__ == "__main__":
    __ROOT_PATH__ = Path(__file__).resolve().parent.parent
    input_path = __ROOT_PATH__ / "data/airlines_delay.csv"
    dimension_path = __ROOT_PATH__ / "src/dimension"
    dataset_input = DataManipulation(
        input_path, "Class", dimension_path
        )
    data_preparation = DataPreparation(
        dataframe=dataset_input.dataframe, 
        target_var="Class", test_size=0.3
        )
    modeling = ModelTraining(
        n_estimators=150, max_depth=8,
        X_train=data_preparation.X_train,
        X_test=data_preparation.X_test,
        y_train=data_preparation.y_train,
        y_test=data_preparation.y_test
    )
    print(modeling.accuracy)
