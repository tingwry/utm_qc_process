def TprevDiffDecrease(criteria, operator, value, value_type, result_df, tolerance=1e-6):
    try:
        if value_type == 'number':
            diff = round(result_df['Previous Reading'], 3) - round(result_df['Latest Reading'], 3)
        elif value_type == '%':
            diff = round((result_df['Previous Reading'] - result_df['Latest Reading']) / result_df['Previous Reading'] * 100, 0)

        value = float(value)

        if value_type == '%':
            column_name = criteria + ' ' + operator + ' ' + str(value) + '%'
        else:
            column_name = criteria + ' ' + operator + ' ' + str(value)

        if operator == 'equals':
            result_df[column_name] = abs(diff - value) < tolerance
        elif operator == 'does not equal':
            result_df[column_name] = abs(diff - value) >= tolerance
        elif operator == 'is greater than':
            result_df[column_name] = (diff - value) > tolerance
        elif operator == 'is greater than or equal to':
            result_df[column_name] = (diff - value) >= -tolerance
        elif operator == 'is less than':
            result_df[column_name] = (diff - value) < -tolerance
        elif operator == 'is less than or equal to':
            result_df[column_name] = (diff - value) <= tolerance
        else:
            raise ValueError(f"Unsupported operator: {operator}")

        return result_df
    except KeyError:
        raise KeyError("Required columns not found in the DataFrame")
    except ValueError as ve:
        raise ValueError(f"Error in value conversion: {str(ve)}")
    except Exception as e:
        raise RuntimeError(f"Error in TprevDiffDecrease: {str(e)}")





# def TprevDiffIncrease(criteria, operator, value, value_type, result_df, tolerance=1e-6):
#     if value_type == 'number':
#         diff = round(result_df['Latest Reading'], 3) - round(result_df['Previous Reading'], 3)
#     elif value_type == '%':
#         diff = round((result_df['Latest Reading'] - result_df['Previous Reading']) / result_df['Latest Reading'] * 100, 0)

#     value = float(value)

#     if value_type == '%':
#         column_name = criteria + ' ' + operator + ' ' + str(value) + '%'
#     else:
#         column_name = criteria + ' ' + operator + ' ' + str(value)

#     if operator == 'equals':
#         result_df[column_name] = abs(diff - value) < tolerance
#     elif operator == 'does not equal':
#         result_df[column_name] = abs(diff - value) >= tolerance
#     elif operator == 'is greater than':
#         result_df[column_name] = (diff - value) > tolerance
#     elif operator == 'is greater than or equal to':
#         result_df[column_name] = (diff - value) >= -tolerance
#     elif operator == 'is less than':
#         result_df[column_name] = (diff - value) < -tolerance
#     elif operator == 'is less than or equal to':
#         result_df[column_name] = (diff - value) <= tolerance
#     else:
#         raise ValueError(f"Unsupported operator: {operator}")

#     return result_df
