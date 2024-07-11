def corrosionRateST(criteria, operator, value, value_type, result_df):
    try:
        cr_st = result_df['Corrosion Rate (ST)']
        value = float(value)

        if value_type == '%':
            column_name = criteria + ' ' + operator + ' ' + str(value) + '%'
        else:
            column_name = criteria + ' ' + operator + ' ' + str(value)

        if operator == 'equals':
            result_df[column_name] = (cr_st == value)
        elif operator == 'does not equal':
            result_df[column_name] = (cr_st != value)
        elif operator == 'is greater than':
            result_df[column_name] = (cr_st > value)
        elif operator == 'is greater than or equal to':
            result_df[column_name] = (cr_st >= value)
        elif operator == 'is less than':
            result_df[column_name] = (cr_st < value)
        elif operator == 'is less than or equal to':
            result_df[column_name] = (cr_st <= value)
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
        return result_df
    except KeyError:
        raise KeyError("Column 'Corrosion Rate (ST)' not found in the DataFrame")
    except ValueError as ve:
        raise ValueError(f"Error in value conversion: {str(ve)}")
    except Exception as e:
        raise RuntimeError(f"Error in corrosionRateST: {str(e)}")





def corrosionRateLT(criteria, operator, value, value_type, result_df):
    try:
        cr_lt = result_df['Corrosion Rate (LT)']
        value = float(value)

        if value_type == '%':
            column_name = criteria + ' ' + operator + ' ' + str(value) + '%'
        else:
            column_name = criteria + ' ' + operator + ' ' + str(value)

        if operator == 'equals':
            result_df[column_name] = (cr_lt == value)
        elif operator == 'does not equal':
            result_df[column_name] = (cr_lt != value)
        elif operator == 'is greater than':
            result_df[column_name] = (cr_lt > value)
        elif operator == 'is greater than or equal to':
            result_df[column_name] = (cr_lt >= value)
        elif operator == 'is less than':
            result_df[column_name] = (cr_lt < value)
        elif operator == 'is less than or equal to':
            result_df[column_name] = (cr_lt <= value)
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
        return result_df
    except KeyError:
        raise KeyError("Column 'Corrosion Rate (LT)' not found in the DataFrame")
    except ValueError as ve:
        raise ValueError(f"Error in value conversion: {str(ve)}")
    except Exception as e:
        raise RuntimeError(f"Error in corrosionRateLT: {str(e)}")
