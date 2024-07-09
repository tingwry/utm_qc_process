from functions.qc_functions.corrosion_rate import corrosionRateLT, corrosionRateST
from functions.qc_functions.remaining_life import remainingLife
from functions.qc_functions.tnorm_diff import TnormDiff
from functions.qc_functions.tprev_diff import TprevDiffDecrease, TprevDiffIncrease
from functions.qc_functions.tr_diff import TrDiff


def QC_data(criteria_list, completeTable):
  result_df = completeTable.copy()
  for i in criteria_list:
    if i['criteria'] == 'nominal thickness difference (Tn - Ta)':
      result_df = TnormDiff(i['criteria'], i['operator'] ,i['value'], i['value_type'], result_df)
    elif i['criteria'] == 'critical thickness difference (Ta - Tr)':
      result_df = TrDiff(i['criteria'], i['operator'] ,i['value'], i['value_type'], result_df)
    elif i['criteria'] == 'last reading difference (Tprev - Ta)':
      result_df = TprevDiffDecrease(i['criteria'], i['operator'] ,i['value'], i['value_type'], result_df)
    elif i['criteria'] == 'last reading difference (Ta - Tprev)':
      result_df = TprevDiffIncrease(i['criteria'], i['operator'] ,i['value'], i['value_type'], result_df)
    elif i['criteria'] == 'Remaining Life':
      result_df = remainingLife(i['criteria'], i['operator'] ,i['value'], result_df)
    elif i['criteria'] == 'Corrosion rate (ST)':
      result_df = corrosionRateST(i['criteria'], i['operator'] ,i['value'], i['value_type'], result_df)
    elif i['criteria'] == 'Corrosion rate (LT)':
      result_df = corrosionRateLT(i['criteria'], i['operator'] ,i['value'], i['value_type'], result_df)

  return result_df