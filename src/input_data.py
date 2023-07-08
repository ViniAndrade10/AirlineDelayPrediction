import pandas as pd
from pathlib import Path


class InputData:
    def __init__(self, file):
        self.file = file
        self.table = pd.read_csv(file)
        self.airports = None

        self.getAirports()
        self.getAirlines()
        self.dropCols()

    def getAirports(self):
        airports = self.table["AirportFrom"].unique()
        self.airports = airports

    def getAirlines(self):
        airlines = self.table["Airline"].unique()
        self.airlines = airlines

    def dropCols(self):
        self.table.drop(["Flight"], axis=1, inplace=True)
