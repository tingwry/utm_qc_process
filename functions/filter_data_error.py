def filter_data_error(df):
    # Select columns with boolean data type
    bool_columns = df.select_dtypes(include=['bool']).columns

    # Check if at least one of the boolean columns contains True
    filtered_df = df[df[bool_columns].any(axis=1)]

    return filtered_df