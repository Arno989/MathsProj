import threading
import logging
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal

dataset = pd.read_csv("server/movies.csv", encoding="ISO-8859-1")

# for i in range(dataset.score.size):
#     dataset.score[i] = round(dataset.score[i] * 10).astype(int)


# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# pd.set_option("display.width", None)
# pd.set_option("display.max_seq_items", None)


# summies = 0

# for score in dataset.score:
#     summies += Decimal(score)
#     if len(str(score)) > 3:
#         print(score)
#     if not "." in str(score):
#         print(score)
        
# print(summies)
# print(Decimal(summies))
# print(sum(dataset.score))

plt.figure(figsize=(8, 8))


nbins = 100
colors = plt.get_cmap('gnuplot')(np.linspace(0, 1, nbins)) # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
n, bins, patches = plt.hist(dataset.score, bins=nbins)

for patch, color in zip(patches, colors):
    patch.set_facecolor(color)


# plt.hist(dataset.score, bins=100)

# sns.countplot('score', data=dataset)
# plt.xticks(np.arange(0, 10.1, 0.1))

plt.show()

