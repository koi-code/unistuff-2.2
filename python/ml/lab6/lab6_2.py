import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import OPTICS
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('CC GENERAL.csv').iloc[:,1:].dropna()

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

optics = OPTICS(min_samples=10, max_eps=0.5).fit(scaled_data)

# График достижимости
plt.figure()
plt.plot(np.arange(len(scaled_data)), optics.reachability_[optics.ordering_])
plt.title('График достижимости')

# Визуализация кластеров (аналогично DBSCAN)
plt.scatter(data_2d[:,0], data_2d[:,1], c=optics.labels_, cmap='viridis')

metrics = ['euclidean', 'manhattan', 'cosine', 'l1', 'l2']
for metric in metrics:
    optics = OPTICS(metric=metric).fit(scaled_data)
    # Анализ результатов (количество кластеров, шум)