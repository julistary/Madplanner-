import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

def scatterploteo(columna1,columna2,title,df,x):
    """
    Plots a scatterplot with the selected data
    Args:
        coulmna1(str): the name of a column to represent in the scatterplot
        coulmna2(str): the name of a column to represent in the scatterplot
        title(str): the title of the plot
        df(df): the dataframe to work with
        x(str): the name of the axis "x"
    Returns:
        The plot
    """
        
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.scatterplot(x = columna1, y= columna2,data = df, palette = "pastel")
    ax.set_title(title)
    plt.xlabel(x)
    return plt

def countploteo(columna1,columna2,title,df):
    """
    Plots a countplot with the selected data
    Args:
        coulmna1(str): the name of a column to represent in the countplot
        coulmna2(str): the name of a column to represent in the countplot
        title(str): the title of the plot
        df(df): the dataframe to work with
    Returns:
        The plot
    """
        
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.countplot(x = columna1, data = df, palette = "pastel", hue=columna2)
    ax.set_title(title)
    return plt

def histploteo(columna,titulo,df):
    """
    Plots a histplot with the selected data
    Args:
        coulmna(str): the name of a column to represent in the histplot
        title(str): the title of the plot
        df(df): the dataframe to work with
    Returns:
        The plot
    """
        
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.histplot(x = columna, data = df, color = "lightblue")
    ax.set_title(titulo)
    ax.axvline(x=df[columna].median(), color="darkblue", label="median")
    ax.legend()
    return plt

def countploteo_no_hue(columna,titulo,df): 
    """
    Plots a countplot with the selected data
    Args:
        coulmna(str): the name of a column to represent in the countplot
        title(str): the title of the plot
        df(df): the dataframe to work with
    Returns:
        The plot
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.countplot(x = columna, data = df, palette = "pastel")
    ax.set_title(titulo)
    return plt

def clustersplot(df):
    """
    Plots all the variables of a cluster
    Args:
        df(df): the dataframe to work with
    Returns:
        The plot
    """
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(15, 10))

    sns.histplot(x = "age", data = df, color = "lightblue", ax=axs[0,0])
    axs[0,0].set_title("age")
    axs[0,0].axvline(x=df["age"].median(), color="darkblue", label="median")
    axs[0,0].legend()

    sns.countplot(x=df["filter"], ax=axs[0, 1], palette="pastel")
    axs[0,1].set_title("filter")

    sns.countplot(x=df["gender"], ax=axs[0, 2], palette="pastel")
    axs[0,2].set_title("gender")

    sns.countplot(x=df["ocupation"], ax=axs[1, 0], palette="pastel")
    axs[1,0].set_title("ocupation")

    sns.countplot(x=df["children"], ax=axs[1, 1], palette="pastel")
    axs[1,1].set_title("children")

    sns.countplot(x=df["residence"], ax=axs[1, 2], palette="pastel")
    axs[1,2].set_title("residence")

    sns.histplot(x = "hour", data = df, color = "lightblue", ax=axs[0,3])
    axs[0,3].set_title("hour")
    axs[0,3].axvline(x=df["hour"].median(), color="darkblue", label="median")
    axs[0,3].legend()

    sns.histplot(x = "month", data = df, color = "lightblue", ax=axs[1,3])
    axs[1,3].set_title("month")
    axs[1,3].axvline(x=df["month"].median(), color="darkblue", label="median")
    axs[1,3].legend()

    return fig