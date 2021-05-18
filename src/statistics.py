import pandas as pd

def daynnite(row):    
    """
    Creates a row with the moment of the day based on the hour 
    Args:
        row(df): the row to be translated
    Returns:
        The dataframe with the new column
    """
        
    if row[:2] > "14" and row[:2] <= "20":
        return "evening"
    elif row[:2] > "21" and row[:2] <= "23":
        return "night"
    elif row[:2] > "07" and row[:2] <= "14":
        return "morning"
    else: 
        return "late night"