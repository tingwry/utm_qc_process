import pandas as pd
import openpyxl
import numpy as np

def pullInsPoints(fileName, sheetname, input_unit, output_unit):
    path = fileName
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheetname]

    df = pd.DataFrame(ws.values)
    df.columns = [
        "Equipment ID",
        "B",
        "C",
        "TML Group ID",
        "TML ID",
        "Readings",
        "Measurement Date",
        "H",
        "I",
        "J"
    ]

    df = df[
        [
            "Equipment ID",
            "TML Group ID",
            "TML ID",
            "Readings",
            "Measurement Date"
        ]
    ][2:]

    # Convert to numeric, coercing errors to NaN
    df["Readings"] = pd.to_numeric(df["Readings"], errors='coerce')

    # Convert units if necessary
    if output_unit == 'mm':
        if input_unit == 'in':
            df["Readings"] = df["Readings"] * 25.4  # 1 inch = 25.4 mm
    elif output_unit == 'in':
        if input_unit == 'mm':
            df["Readings"] = df["Readings"] / 25.4  # 1 mm = 1/25.4 inch

    # Round Readings to 3 decimal places
    df["Readings"] = df["Readings"].round(3)


    # # Specify the expected date format
    # date_format = "%m/%d/%Y %I:%M:%S %p"

    # Convert 'Measurement Date' to datetime
    # df["Measurement Date"] = pd.to_datetime(df["Measurement Date"], format=date_format, errors='coerce')
    df["Measurement Date"] = pd.to_datetime(df["Measurement Date"], errors='coerce')

    # Drop rows with NaN values
    df.dropna(subset=["Equipment ID","TML Group ID", "TML ID", "Readings", "Measurement Date"], inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    df = df.reset_index(drop=True)

    return df



def combineData(fileName, sheetname, input_unit, output_unit, fixed, inspections):
    points_df = pullInsPoints(fileName, sheetname, input_unit, output_unit)

    # Merge fixed information
    combined_df = points_df.merge(fixed, on=["Equipment ID","TML Group ID", "TML ID"], how="left")

    # Sort the inspections DataFrame by date
    inspections_df = inspections.sort_values(by="Measurement Taken Date", ascending=False)

    # Get the previous reading
    previous_reading = inspections_df.groupby(["Equipment ID","TML Group ID", "TML ID"]).head(1)
    previous_reading = previous_reading.rename(columns={
        "Readings": "Previous Reading",
        "Measurement Taken Date": "Previous Reading Date"
        })

    # Get the initial reading
    initial_reading = inspections_df.groupby(["Equipment ID","TML Group ID", "TML ID"]).tail(1)
    initial_reading = initial_reading.rename(columns={
        "Readings": "Initial Reading",
        "Measurement Taken Date": "Initial Reading Date"
        })

    # Merge the previous reading with the combined_df
    combined_df = combined_df.merge(previous_reading[["Equipment ID","TML Group ID", "TML ID", "Previous Reading", "Previous Reading Date"]], on=["Equipment ID", "TML ID"], how="left")

    # Merge the oldest reading with the combined_df
    combined_df = combined_df.merge(initial_reading[["Equipment ID","TML Group ID", "TML ID", "Initial Reading", "Initial Reading Date"]], on=["Equipment ID", "TML ID"], how="left")


    combined_df = combined_df.rename(columns={
        "Readings": "Latest Reading",
        "Measurement Date": "Latest Reading Date"
        })


    # Rearrange columns
    combined_df = combined_df[['Equipment ID',"TML Group ID", 'TML ID', 'Nominal Thickness', 'Minimum Thickness', 'Initial Reading', 'Initial Reading Date', 'Previous Reading', 'Previous Reading Date', 'Latest Reading', 'Latest Reading Date']]

    # Convert units if necessary
    if output_unit == 'mm':
      combined_df["Nominal Thickness"] = combined_df["Nominal Thickness"] * 25.4
      combined_df["Minimum Thickness"] = combined_df["Minimum Thickness"] * 25.4
      combined_df["Previous Reading"] = combined_df["Previous Reading"] * 25.4
      combined_df["Initial Reading"] = combined_df["Initial Reading"] * 25.4


    # add rml and cr
    # * add if rml and cr in criteria *
     # CR
    years_diff_st = (combined_df["Latest Reading Date"] - combined_df["Previous Reading Date"]).dt.days / 365.25
    years_diff_lt = (combined_df["Latest Reading Date"] - combined_df["Initial Reading Date"]).dt.days / 365.25

    combined_df["Corrosion Rate (ST)"] = (combined_df["Previous Reading"] - combined_df["Latest Reading"]) / years_diff_st
    combined_df["Corrosion Rate (LT)"] = (combined_df["Initial Reading"] - combined_df["Latest Reading"]) / years_diff_lt

    # RML
    combined_df["Remaining Life"] = (combined_df["Latest Reading"] - combined_df["Minimum Thickness"]) / np.maximum(combined_df["Corrosion Rate (ST)"], combined_df["Corrosion Rate (LT)"])


    # Round Readings to 3 decimal places
    combined_df["Nominal Thickness"] = combined_df["Nominal Thickness"].round(3)
    combined_df["Minimum Thickness"] = combined_df["Minimum Thickness"].round(3)
    combined_df["Previous Reading"] = combined_df["Previous Reading"].round(3)
    combined_df["Initial Reading"] = combined_df["Initial Reading"].round(3)

    combined_df["Corrosion Rate (ST)"] = combined_df["Corrosion Rate (ST)"].round(3)
    combined_df["Corrosion Rate (LT)"] = combined_df["Corrosion Rate (LT)"].round(3)
    combined_df["Remaining Life"] = combined_df["Remaining Life"].round(3)


    # Remove duplicate rows
    combined_df.drop_duplicates(inplace=True)

    combined_df = combined_df.reset_index(drop=True)

    return combined_df