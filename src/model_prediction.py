import pandas as pd
import pickle
from datetime import datetime

from pathlib import Path


class Predicting:
    def __init__(
            self, model_path:Path, output_result_way:str, dataset:pd.DataFrame,
            ):
        self.model_path = model_path
        self.dataset = dataset
        self.model = None
        self.results = None
        self.output_file_name = None
        self.manual_prediction = None
        self.full_prediction = None

        self.creating_factors()
        self.making_prediction()
        self.building_results()
        self.exporting_results(output_result_way)

    def making_prediction(self):
        if "Flight" in self.dataset.columns:
            self.dataset.drop(["Flight"], axis=1, inplace=True)
        model = pickle.load(open(self.model_path, "rb"))
        self.model = model
        self.results = self.model.predict(self.dataset)

    def building_results(self):
        self.dataset["Prediction"] = self.results

    def exporting_results(self, output_way):
        version_date = datetime.today().strftime("%Y%m%d%H%M")
        self.output_file_name = f"Output_Airline_Delay_{version_date}.xlsx"
        if output_way == "":
            self.manual_prediction = self.dataset["Prediction"].values
        else:
            self.full_prediction = self.dataset
            print(self.full_prediction)
            # buffer = BytesIO()
            # with pd.ExcelWriter(buffer) as writer:
            #     self.dataset.to_excel(
            #         excel_writer=writer, 
            #         sheet_name="Output_Airline_Delay",
            #         index=False,
                    
            #     )
            # return buffer

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
    model_path = __ROOT_PATH__ / "src/model/AirDelay_Predictor.sav"
    dataset_to_predict = pd.read_excel(input_path)
    output_results_way = "Excel_Sheet"

    prediction = Predicting(
        model_path, output_results_way, dataset_to_predict
    )

    print(prediction.results)
