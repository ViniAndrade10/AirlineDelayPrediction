import pandas as pd
import pickle
from datetime import datetime

from pathlib import Path


class Predicting:
    def __init__(
            self, model_path:str, dataset:pd.DataFrame
            ):
        self.model_path = model_path
        self.dataset = dataset
        self.model = None
        self.results = None

    def making_prediction(self):
        model = pickle.load(open(self.model_path, "rb"))
        self.model = model
        self.results = self.model.predict(self.dataset)

    def building_results(self):
        self.dataset["Prediction"] = self.results

    def exporting_results(self, output_path):
        version_date = datetime.today().strftime("%Y%m%d%H%M")
        file = f"Output_Airline_Delay_{version_date}.xlsx"
        with pd.ExcelWriter(output_path / file) as writer:
            self.dataset.to_excel(
                excel_writer=writer, 
                sheet_name="Output_Airline_Delay",
                index=False
            )

if __name__ == "__main__":
    __ROOT_PATH__ = Path(__file__).resolve().parent.parent
    input_path = __ROOT_PATH__ / "data/airlines_delay.csv"
    model_path = __ROOT_PATH__ / "model/AirDelay_Predictor.sav"

    # Vai ser necessário criar uma planilha para se tornar o dicionário de
    # Aeroportos e Companias Aéreas para ser possível a substituição 
    # dos valores pelos seus respectivos "Factors"
