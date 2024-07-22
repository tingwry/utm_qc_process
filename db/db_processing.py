import os
import numpy as np
import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import warnings
from datetime import datetime
from functools import lru_cache

# Global variable to store the processed DataFrame
_cached_df = None

# Function to process Excel file
def process_excel(db_file_path, sheetname, db_input_unit, output_unit):
    global _cached_df

    if _cached_df is not None:
        return _cached_df

    wb = openpyxl.load_workbook(db_file_path, data_only=True)
    ws = wb[sheetname]

    # Process DataFrame
    df = pd.DataFrame(ws.values)
    df.columns = [
        "A",
        "B",
        "Equipment ID",
        "D",
        "E",
        "F",
        "TML Group ID",
        "H",
        "TML ID",
        "Nominal Thickness",
        "Minimum Thickness",
        "Readings",
        "Measurement Taken Date",
        "N",
        "O",
        "P",
        "Q",
        "R"
    ]

    # Convert to numeric, coercing errors to NaN
    df["Nominal Thickness"] = pd.to_numeric(df["Nominal Thickness"], errors='coerce')
    df["Minimum Thickness"] = pd.to_numeric(df["Minimum Thickness"], errors='coerce')
    df["Readings"] = pd.to_numeric(df["Readings"], errors='coerce')
        

    # Specify the expected date format
    # date_format = "%m/%d/%Y %I:%M:%S %p"
    # Convert 'Measurement Taken Date' to datetime
    df["Measurement Taken Date"] = pd.to_datetime(df["Measurement Taken Date"], errors='coerce')
    df = df.sort_values(by="Measurement Taken Date", ascending=False)

    # Drop rows with NaN values in "Nominal Thickness" or "Minimum Thickness"
    df.dropna(subset=["Nominal Thickness", "Minimum Thickness", "Readings", "Measurement Taken Date"], inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    df = df.reset_index(drop=True)

    _cached_df = df
    return df

def fixedInfoTable(processed_df):
    df = processed_df.copy()

    df = df[
        [
            "Equipment ID",
            "TML Group ID",
            "TML ID",
            "Nominal Thickness",
            "Minimum Thickness"
        ]
    ]

    return df

def InspectionsTable(processed_df):
    df = processed_df.copy()

    df = df[
        [
            "Equipment ID",
            "TML Group ID",
            "TML ID",
            "Readings",
            "Measurement Taken Date"
        ]
    ]

    return df
