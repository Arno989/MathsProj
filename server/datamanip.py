import threading
import logging
import pickle
import pandas as pd
import numpy as np


dataset = pd.read_csv("server/movies.csv", encoding="ISO-8859-1")
#pd.describe_option("display")
print(dataset.shape)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", 15)
pd.set_option("display.width", None)
pd.set_option("display.m", None)

print(dataset.company.unique())


print(dataset.loc[dataset["genre"] == "Action"])

