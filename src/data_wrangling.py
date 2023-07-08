# type:ignore
from pathlib import Path
from imblearn.over_sampling import SMOTE
from input_data import InputData


class DataManipulation:
    def __init__(self, file, target_var: str):
        self.input_data = InputData(file=file)
        self.dataframe = self.input_data.table
        self.target_var = target_var
        self.classes = None
        self.prediction_var = None
        self.balanced_df = None

        self.changeAirport()
        self.changeAirlineNames()
        self.proportionCheck()

    def dataBalancing(self, x, y):
        overSampler = SMOTE()
        self.balanced_df = overSampler.fit_resample(x, y)

    def proportionCheck(self):
        self.classes = self.dataframe[self.target_var]
        self.prediction_var = self.dataframe.drop([self.target_var], axis=1)

        first_class = self.classes.value_counts()[0]
        second_class = self.classes.value_counts()[1]
        proportion = (first_class / second_class) - 1

        if proportion >= 0.05:
            self.dataBalancing(self.prediction_var, self.classes)
        else:
            self.balanced_df = self.dataframe

    def changeAirlineNames(self):
        airline_range = range(0, len(self.input_data.airlines))
        mapping_airline = dict(zip(self.input_data.airlines, airline_range))
        self.dataframe["Airline"] = self.dataframe["Airline"].map(
            mapping_airline
            )

    def changeAirport(self):
        airport_range = range(0, len(self.input_data.airports))
        mapping_airport = dict(
            zip(self.input_data.airports, airport_range)
        )
        self.dataframe["AirportFrom"] = self.dataframe["AirportFrom"].map(
            mapping_airport
        )
        self.dataframe["AirportTo"] = self.dataframe["AirportTo"].map(
            mapping_airport
            )


if __name__ == "__main__":
    __ROOT_PATH__ = Path(__file__).resolve().parent.parent
    input_path = __ROOT_PATH__ / "data/airlines_delay.csv"
    dataset_input = DataManipulation(input_path, "Class")
    print(dataset_input.dataframe)
