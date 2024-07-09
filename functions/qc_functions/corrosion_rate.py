def corrosionRateST(criteria, operator, value, value_type, result_df):
  cr_st = result_df['Corrosion Rate (ST)']
  
  # %

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




def corrosionRateLT(criteria, operator, value, value_type, result_df):
  cr_lt = result_df['Corrosion Rate (LT)']

  # %

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