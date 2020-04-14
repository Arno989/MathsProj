import threading
import logging
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



dataset = pd.read_csv("server/movies.csv", encoding="ISO-8859-1")
# pd.describe_option("display")
# print(dataset.shape)

# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# pd.set_option("display.width", None)
# pd.set_option("display.max_seq_items", None)

# print(dataset.company.unique())


# print(dataset.loc[dataset["genre"] == "Action"])
# dataset.score = dataset.score.astype('float64')
# dataset.sort_values(by=['score'])


plt.figure(figsize=(8, 8))
sns.countplot('score', data=dataset)
#plt.plot(dataset.score.value_counts()) 
plt.show()

