import pandas as pd
import pickle
from datetime import datetime

from pathlib import Path


class Predicting:
    def __init__(
            self, model_path:Path, output_result_path:Path, dataset:pd.DataFrame,
            ):
        self.model_path = model_path
        self.dataset = dataset
        self.model = None
        self.results = None

        self.creating_factors()
        self.making_prediction()
        self.building_results()
        self.exporting_results(output_result_path)

    def making_prediction(self):
        self.dataset.drop(["Flight"], axis=1, inplace=True)
        model = pickle.load(open(self.model_path, "rb"))
        self.model = model
        self.results = self.model.predict(self.dataset)

    def building_results(self):
        self.dataset["Prediction"] = self.results

    def exporting_results(self, output_path):
        breakpoint()
        version_date = datetime.today().strftime("%Y%m%d%H%M")
        file = f"Output_Airline_Delay_{version_date}.xlsx"
        with pd.ExcelWriter(output_path / file) as writer:
            self.dataset.to_excel(
                excel_writer=writer, 
                sheet_name="Output_Airline_Delay",
                index=False
            )

    def creating_factors(self):
        airline_dimension = pd.read_excel(
            "./dimension/Airline_Dimension.xlsx",
            sheet_name="Airline_Output"
            ).set_index(["Airline"]).to_dict()["Airline_Factor"]

        airport_dimension = pd.read_excel(
            "./dimension/Airport_Dimension.xlsx",
            sheet_name="Airport_Output"
            ).set_index(["Airport"]).to_dict()["Airport_Factor"]

        self.dataset["Airline"] = self.dataset["Airline"].map(
            airline_dimension
        )

        self.dataset["AirportFrom"] = self.dataset["AirportFrom"].map(
            airport_dimension
        )

        self.dataset["AirportTo"] = self.dataset["AirportTo"].map(
            airport_dimension
        )
        print(self.dataset)


if __name__ == "__main__":
    __ROOT_PATH__ = Path(__file__).resolve().parent.parent
    input_path = __ROOT_PATH__ / "data/airlines_delay_new.xlsx"
    output_results_path = __ROOT_PATH__ / "export/"
    model_path = __ROOT_PATH__ / "src/model/AirDelay_Predictor.sav"
    dataset_to_predict = pd.read_excel(input_path)

    prediction = Predicting(
        model_path, output_results_path, dataset_to_predict
    )

    print(prediction.results)
