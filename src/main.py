import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import os

from model_prediction import Predicting

__ROOT_PATH__ = Path(__file__).resolve().parent.parent
dim_path = __ROOT_PATH__ / "src/dimension/"
airline_file = "Airline_Dimension.xlsx"
airport_file = "Airport_Dimension.xlsx"

model_path = __ROOT_PATH__ / "src/model/AirDelay_Predictor.sav"


airline_list = pd.read_excel(
    os.path.join(dim_path, airline_file), sheet_name="Airline_Output"
    )["Airline"].to_list()

airport_list = pd.read_excel(
    os.path.join(dim_path, airport_file), sheet_name="Airport_Output"
    )["Airport"].to_list()

st.title("Flight Delay Predictor ✈️")
st.title(" ")

st.sidebar.title("Manual Input")
flight_time =st.sidebar.number_input("Flight Time [min]", step=60)
flight_distance =st.sidebar.number_input("Flight Distance [Km]", step=100)
airline = st.sidebar.selectbox("Airline", options=airline_list)
airport_from = st.sidebar.selectbox("Airport From:", options=airport_list)
airport_to = st.sidebar.selectbox("Airport To:", options=airport_list)

dict_days = {
    "Sunday": 1, "Monday": 2, "Tuesday": 3, "Wednesday": 4, "Thrusday": 5,
    "Friday": 6, "Saturday": 7
}

week_day = st.sidebar.selectbox(
    "Day of the Week:", 
    options= [index for index in dict_days.keys()]
    )

# This is the sidebar button
run_button_1 = st.sidebar.button("Run Model", key="number_1")

# This function will create a dataframe for the model
def get_data_for_model_manually(list):
    cols = [
        "Time", "Length", "Airline", 
        "AirportFrom", "AirportTo", "DayOfWeek"
        ]
    day_of_week = list[5]
    if day_of_week in dict_days.keys():
        day_of_week_factor = dict_days[day_of_week]
        list.pop(5)
        list.append(day_of_week_factor)

    dataset_output = pd.DataFrame(
        data=list,
    ).T
    dataset_output.columns = cols
    return dataset_output

def run_model(model_path , output_path, dataset):
    prediction = Predicting(
        model_path, output_path, dataset
    )
    if output_path == "":
        return prediction.manual_prediction
    else:
        return prediction.full_prediction


if run_button_1:
    dataset_for_model = get_data_for_model_manually(
        [flight_time, flight_distance, airline, airport_from, airport_to, week_day]
        )

    result = run_model(model_path, "", dataset_for_model)
    st.sidebar.write(result)
    if result == 1 or result == "1":
        st.sidebar.write("The flight will be Delaied")
    else:
        st.sidebar.write("The flight will be on Time")

# Here I'll create two columns
# First Column contains an explanation of the template file
# Second Column, a download button of the excel template file

col_left, col_right =st.columns(spec=2, gap="small")
col_left.text("Template Excel File Download:")

st.title("___________________________________")


uploaded_file = st.file_uploader("Upload Excel File")
if uploaded_file != None:
    if not str(uploaded_file.name).endswith(".xlsx"):
        st.warning("File must be an Excel Sheet.", icon="⚠️")
    else:
        run_button_2 = st.button("Run Model", key="number_2")
        
        if run_button_2:
            dataset_complete = pd.read_excel(uploaded_file)
            predicted_data = run_model(model_path, "Excel_Sheet", dataset_complete)
            st.table(predicted_data)

            buffer = BytesIO()
            with pd.ExcelWriter(buffer) as writer:
                predicted_data.to_excel(  #type: ignore
                    writer, sheet_name="Predictions", index=False
                    )


            st.download_button(
                label="Download Prediction", 
                data=buffer, 
                file_name="Output_Airline_Delay_Prediction.xlsx"
                )

# Creating template download area
cols = [
    "Time", "Length", 
    "Airline", "AirportFrom", 
    "AirportTo", "DayOfWeek"
    ]

data_template = [
    ["duration of flight in minutes",
     "flight length", "responsable airline",
     "airport of departure", "airport of arrival",
     "flight day of the week"]
    ]

dataset_template = pd.DataFrame(data_template)
dataset_template.columns = cols

buffer_template = BytesIO()
with pd.ExcelWriter(buffer_template) as writer:
    dataset_template.to_excel(writer, sheet_name="Template", index=False) #type: ignore

col_right.download_button(
    label="Download Template", 
    data=buffer_template, 
    file_name="Template_Workbook.xlsx"
    )
