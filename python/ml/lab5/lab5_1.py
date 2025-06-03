# Импорт библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering, MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_iris
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.cm as cm
import math
import random

# Загрузка данных Iris
iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)
no_labeled_data = iris.data

# ==============================
# K-means кластеризация
# ==============================

# 1. Кластеризация методом k-средних
k_means = KMeans(init='k-means++', n_clusters=3, n_init=15, random_state=42)
k_means.fit(no_labeled_data)

# 2. Получение центров кластеров и меток
k_means_cluster_centers = k_means.cluster_centers_
k_means_labels = pairwise_distances_argmin(no_labeled_data, k_means_cluster_centers)

# 3. Визуализация попарных признаков
features = iris.feature_names
fig, ax = plt.subplots(1, 3, figsize=(18, 5))
colors = ['#4EACC5', '#FF9C34', '#4E9A06']

for pair_idx, (start_idx, end_idx) in enumerate([(0,1), (1,2), (2,3)]):
    for i in range(3):
        # Точки кластера
        my_members = k_means_labels == i
        ax[pair_idx].scatter(
            no_labeled_data[my_members, start_idx],
            no_labeled_data[my_members, end_idx],
            c=colors[i], s=40, alpha=0.7
        )
        
        # Центроиды
        ax[pair_idx].scatter(
            k_means_cluster_centers[i, start_idx],
            k_means_cluster_centers[i, end_idx],
            c='red', marker='X', s=200, edgecolor='black'
        )
    
    ax[pair_idx].set_xlabel(features[start_idx])
    ax[pair_idx].set_ylabel(features[end_idx])
    ax[pair_idx].set_title(f'Признаки {start_idx+1} и {end_idx+1}')

plt.tight_layout()
plt.show()

# Анализ результатов:
# Наилучшее разделение наблюдается для признаков 3 и 4 (длина и ширина лепестка). 
# Параметр n_init определяет количество запусков алгоритма с разными начальными центроидами.
# Большие значения n_init уменьшают вероятность получения субоптимального решения.

# 4. Уменьшение размерности с помощью PCA
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(no_labeled_data)

# Визуализация кластеров в пространстве PCA
plt.figure(figsize=(10, 7))
plt.scatter(
    reduced_data[:, 0], reduced_data[:, 1],
    c=k_means_labels, cmap=cm.viridis, s=50, alpha=0.8
)

# Разметка областей кластеров
x_min, x_max = reduced_data[:, 0].min() - 0.5, reduced_data[:, 0].max() + 0.5
y_min, y_max = reduced_data[:, 1].min() - 0.5, reduced_data[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))
Z = k_means.predict(pca.inverse_transform(np.c_[xx.ravel(), yy.ravel()]))
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.2, cmap=cm.viridis)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('K-means кластеризация с областями решений (PCA)')
plt.colorbar()
plt.show()

# 5. Исследование параметра init
inits = ['random', 'k-means++']
manual_centers = np.array([
    [5.0, 3.4, 1.5, 0.2],
    [6.0, 2.8, 4.5, 1.3],
    [7.0, 3.2, 6.0, 2.0]
])

plt.figure(figsize=(15, 10))
for idx, init_method in enumerate(inits + ['manual']):
    if init_method == 'manual':
        kmeans = KMeans(n_clusters=3, init=manual_centers, n_init=1, random_state=42)
    else:
        kmeans = KMeans(n_clusters=3, init=init_method, n_init=15, random_state=42)
    
    kmeans.fit(no_labeled_data)
    labels = kmeans.predict(no_labeled_data)
    
    plt.subplot(2, 2, idx+1)
    plt.scatter(
        reduced_data[:, 0], reduced_data[:, 1],
        c=labels, s=50, cmap=cm.viridis
    )
    plt.title(f'Инициализация: {init_method}')
    plt.xlabel('PC1')
    plt.ylabel('PC2')

plt.tight_layout()
plt.show()

# 6. Метод локтя для определения оптимального числа кластеров
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(no_labeled_data)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertias, 'bo-')
plt.xlabel('Количество кластеров')
plt.ylabel('Сумма квадратов расстояний')
plt.title('Метод локтя для определения оптимального k')
plt.axvline(x=3, color='r', linestyle='--', alpha=0.5)
plt.grid(True)
plt.show()

# 7. Пакетная кластеризация (MiniBatchKMeans)
mbk = MiniBatchKMeans(n_clusters=3, random_state=42)
mbk_labels = mbk.fit_predict(no_labeled_data)

# Сравнение с обычным K-means
plt.figure(figsize=(12, 6))

plt.subplot(121)
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=k_means_labels, cmap=cm.viridis)
plt.title('Стандартный K-means')

plt.subplot(122)
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=mbk_labels, cmap=cm.viridis)
plt.title('MiniBatch K-means')

plt.tight_layout()
plt.show()

# Анализ различий:
# MiniBatch K-means обрабатывает данные небольшими пакетами, что значительно ускоряет обработку больших данных.
# Результаты могут незначительно отличаться из-за стохастической природы алгоритма.

# ==============================
# Иерархическая кластеризация
# ==============================

# 1. Кластеризация на данных Iris
hier = AgglomerativeClustering(n_clusters=3, linkage='average')
hier_labels = hier.fit_predict(no_labeled_data)

# 2. Визуализация результатов
fig, ax = plt.subplots(1, 3, figsize=(18, 5))
for pair_idx, (start_idx, end_idx) in enumerate([(0,1), (1,2), (2,3)]):
    for i in range(3):
        my_members = hier_labels == i
        ax[pair_idx].scatter(
            no_labeled_data[my_members, start_idx],
            no_labeled_data[my_members, end_idx],
            c=colors[i], s=40, alpha=0.7
        )
    ax[pair_idx].set_xlabel(features[start_idx])
    ax[pair_idx].set_ylabel(features[end_idx])
    ax[pair_idx].set_title(f'Признаки {start_idx+1} и {end_idx+1}')

plt.tight_layout()
plt.show()

# Отличия от K-means:
# 1. Не требует предварительного задания числа кластеров
# 2. Создает иерархическую структуру (дендрограмму)
# 3. Менее чувствителен к выбросам
# 4. Работает медленнее на больших данных

# 3. Исследование разного количества кластеров (2-5)
plt.figure(figsize=(15, 10))
for i, n_clusters in enumerate(range(2, 6)):
    hier = AgglomerativeClustering(n_clusters=n_clusters, linkage='average')
    labels = hier.fit_predict(no_labeled_data)
    
    plt.subplot(2, 2, i+1)
    plt.scatter(
        reduced_data[:, 0], reduced_data[:, 1],
        c=labels, cmap=cm.viridis, s=50
    )
    plt.title(f'Число кластеров: {n_clusters}')
    plt.xlabel('PC1')
    plt.ylabel('PC2')

plt.tight_layout()
plt.show()

# 4. Построение дендрограммы
linked = linkage(no_labeled_data, 'ward')
plt.figure(figsize=(15, 7))
dendrogram(linked, truncate_mode='level', p=6)
plt.title('Дендрограмма (уровень 6)')
plt.xlabel('Индекс образца')
plt.ylabel('Расстояние')
plt.show()

# 5. Генерация данных "два кольца"
np.random.seed(42)
data1 = np.zeros((250, 2))
for i in range(250):
    r = random.uniform(1, 3)
    a = random.uniform(0, 2 * math.pi)
    data1[i, 0] = r * math.sin(a)
    data1[i, 1] = r * math.cos(a)

data2 = np.zeros((500, 2))
for i in range(500):
    r = random.uniform(5, 9)
    a = random.uniform(0, 2 * math.pi)
    data2[i, 0] = r * math.sin(a)
    data2[i, 1] = r * math.cos(a)

ring_data = np.vstack((data1, data2))

# 6-7. Иерархическая кластеризация и визуализация
linkage_types = ['ward', 'complete', 'average', 'single']
plt.figure(figsize=(15, 10))

for i, linkage in enumerate(linkage_types):
    hier = AgglomerativeClustering(n_clusters=2, linkage=linkage)
    labels = hier.fit_predict(ring_data)
    
    plt.subplot(2, 2, i+1)
    plt.scatter(
        ring_data[labels==0, 0], ring_data[labels==0, 1], 
        s=30, c='red', alpha=0.7
    )
    plt.scatter(
        ring_data[labels==1, 0], ring_data[labels==1, 1], 
        s=30, c='blue', alpha=0.7
    )
    plt.title(f'Связь: {linkage}')
    plt.xlabel('X')
    plt.ylabel('Y')

plt.tight_layout()
plt.show()