def remainingLife(criteria, operator, value, value_type, result_df):
    try:
        if value_type == '%':
            raise ValueError(f"Unsupported value type: {value_type}")
        rml = result_df['Remaining Life']
        column_name = criteria + ' ' + operator + ' ' + str(value)
        value = float(value)

        if operator == 'equals':
            result_df[column_name] = (rml == value)
        elif operator == 'does not equal':
            result_df[column_name] = (rml != value)
        elif operator == 'is greater than':
            result_df[column_name] = (rml > value)
        elif operator == 'is greater than or equal to':
            result_df[column_name] = (rml >= value)
        elif operator == 'is less than':
            result_df[column_name] = (rml < value)
        elif operator == 'is less than or equal to':
            result_df[column_name] = (rml <= value)
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
        return result_df
    except KeyError:
        raise KeyError("Column 'Remaining Life' not found in the DataFrame")
    except ValueError as ve:
        raise ValueError(f"Error in value conversion: {str(ve)}")
    except Exception as e:
        raise RuntimeError(f"Error in remainingLife: {str(e)}")
