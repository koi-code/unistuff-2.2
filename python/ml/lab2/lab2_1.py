# Импорт необходимых библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import PCA, KernelPCA, SparsePCA, FactorAnalysis
from sklearn.metrics import mean_squared_error

# Загрузка данных
url = "https://raw.githubusercontent.com/akmand/datasets/master/glass.csv"
df = pd.read_csv(url)

# Предварительная обработка данных
var_names = df.columns.tolist()[:-1]  # названия признаков
labels = df['Type'].values  # метки классов
data = df.drop('Type', axis=1).values.astype(float)  # описательные признаки

# Нормировка данных
data_normalized = preprocessing.minmax_scale(data)

# Построение парных диаграмм рассеяния
fig, axs = plt.subplots(2, 4, figsize=(15, 8))
for i in range(data_normalized.shape[1] - 1):
    row, col = i // 4, i % 4
    scatter = axs[row, col].scatter(data_normalized[:, i], data_normalized[:, i+1], c=labels, cmap='hsv', alpha=0.7)
    axs[row, col].set_xlabel(var_names[i])
    axs[row, col].set_ylabel(var_names[i+1])
fig.colorbar(scatter, ax=axs, label='Class')
plt.tight_layout()
plt.show()

# PCA: Понижение размерности до 2 компонент
pca = PCA(n_components=2)
pca_data = pca.fit_transform(data_normalized)

# Вывод информации о PCA
print("Объясненная дисперсия (PCA):", pca.explained_variance_ratio_)
print("Собственные значения (PCA):", pca.singular_values_)

# Визуализация результатов PCA
plt.figure(figsize=(8, 6))
plt.scatter(pca_data[:, 0], pca_data[:, 1], c=labels, cmap='hsv')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.colorbar(label='Class')
plt.title('PCA: Проекция данных на две главные компоненты')
plt.show()

# Определение числа компонент для 85% дисперсии
pca_full = PCA().fit(data_normalized)
explained_variance = np.cumsum(pca_full.explained_variance_ratio_)
n_components_85 = np.argmax(explained_variance >= 0.85) + 1
print(f"Компоненты для 85% дисперсии: {n_components_85}")

# Восстановление данных после PCA
pca_restored = pca.inverse_transform(pca_data)
mse_pca = mean_squared_error(data_normalized, pca_restored)
print(f"Ошибка восстановления PCA: {mse_pca:.5f}")

# Исследование различных решателей PCA
solvers = ['auto', 'full', 'arpack', 'randomized']
for solver in solvers:
    pca_solver = PCA(n_components=2, svd_solver=solver)
    pca_solver.fit(data_normalized)
    print(f"\nРешатель: {solver}\nОбъясненная дисперсия:", pca_solver.explained_variance_ratio_)

# KernelPCA с разными ядрами
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
plt.figure(figsize=(12, 10))
for i, kernel in enumerate(kernels):
    kpca = KernelPCA(n_components=2, kernel=kernel, gamma=0.1)
    kpca_data = kpca.fit_transform(data_normalized)
    plt.subplot(2, 2, i+1)
    plt.scatter(kpca_data[:, 0], kpca_data[:, 1], c=labels, cmap='hsv', alpha=0.7)
    plt.title(f'Kernel: {kernel}')
    plt.colorbar()
plt.tight_layout()
plt.show()

# SparsePCA
spca = SparsePCA(n_components=2, alpha=0.5)
spca_data = spca.fit_transform(data_normalized)
plt.figure(figsize=(8, 6))
plt.scatter(spca_data[:, 0], spca_data[:, 1], c=labels, cmap='hsv')
plt.title('SparsePCA')
plt.colorbar(label='Class')
plt.show()

# Факторный анализ
fa = FactorAnalysis(n_components=2)
fa_data = fa.fit_transform(data_normalized)
plt.figure(figsize=(8, 6))
plt.scatter(fa_data[:, 0], fa_data[:, 1], c=labels, cmap='hsv')
plt.title('Factor Analysis')
plt.colorbar(label='Class')
plt.show()

# Сравнение проекций PCA и FA
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
ax1.scatter(pca_data[:, 0], pca_data[:, 1], c=labels, cmap='hsv')
ax1.set_title('PCA')
ax2.scatter(fa_data[:, 0], fa_data[:, 1], c=labels, cmap='hsv')
ax2.set_title('Factor Analysis')
plt.show()