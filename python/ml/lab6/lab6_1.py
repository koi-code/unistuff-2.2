import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('CC GENERAL.csv').iloc[:,1:].dropna()

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# П.4: Перебор eps (при min_samples по умолчанию = 5)
eps_values = np.linspace(0.1, 2.0, 50)
clusters = []
noise_percent = []

for eps in eps_values:
    db = DBSCAN(eps=eps).fit(scaled_data)
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    clusters.append(n_clusters)
    noise_percent.append((labels == -1).mean() * 100)

# Построение графиков
plt.plot(eps_values, clusters, label='Количество кластеров')
plt.plot(eps_values, noise_percent, label='Шум (%)')
plt.xlabel('eps')
plt.legend()

# Пример для eps=0.5, min_samples=10
db = DBSCAN(eps=0.5, min_samples=10).fit(scaled_data)
labels = db.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
noise_percent = (labels == -1).mean() * 100

print(f"Кластеры: {n_clusters}, Шум: {noise_percent:.2f}%")

from sklearn.decomposition import PCA

# Понижение размерности
pca = PCA(n_components=2)
data_2d = pca.fit_transform(scaled_data)

# Рисуем кластеры (метки из DBSCAN)
plt.scatter(data_2d[:,0], data_2d[:,1], c=labels, cmap='viridis')
plt.title('DBSCAN (до PCA)')