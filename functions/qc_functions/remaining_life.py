def remainingLife(criteria, operator, value, result_df):
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