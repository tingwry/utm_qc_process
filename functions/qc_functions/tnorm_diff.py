def TnormDiff(criteria, operator, value, value_type, result_df, tolerance=1e-6):
    if value_type == 'number':
        diff = round(result_df['Nominal Thickness'], 3) - round(result_df['Latest Reading'], 3)
    elif value_type == '%':
        diff = round((result_df['Nominal Thickness'] - result_df['Latest Reading']) / result_df['Nominal Thickness'] * 100, 0)

    # Ensure value is converted to float for the subtraction operation
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