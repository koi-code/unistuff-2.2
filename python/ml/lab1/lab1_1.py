import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing # type: ignore
from sklearn.preprocessing import KBinsDiscretizer, QuantileTransformer, PowerTransformer # type: ignore

# --------------------- 1. Загрузка данных и предобработка ---------------------
# Загрузка датасета
df = pd.read_csv('heart_failure_clinical_records_dataset.csv')

# Исключение бинарных признаков и признака времени
columns_to_drop = ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking', 'time', 'DEATH_EVENT']
df = df.drop(columns=columns_to_drop)

# Проверка
print("Размер датафрейма после удаления столбцов:", df.shape) 
print("Первые 5 строк:", df.head())

# --------------------- 2. Построение гистограмм исходных данных ---------------------
n_bins = 20
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
features = df.columns

for i, feature in enumerate(features):
    row = i // 3
    col = i % 3
    axs[row, col].hist(df[feature], bins=n_bins, edgecolor='black')
    axs[row, col].set_title(feature, fontsize=10)
    axs[row, col].grid(True)

plt.suptitle('Гистограммы исходных данных', fontsize=14)
plt.tight_layout()
plt.savefig('original_histograms.png')
plt.show()

# --------------------- 3. Преобразование в NumPy массив ---------------------
data = df.to_numpy(dtype='float32')

# --------------------- 4. Стандартизация данных (StandardScaler) ---------------------
# Обучение на первых 150 наблюдениях
scaler = preprocessing.StandardScaler().fit(data[:150, :])
data_scaled = scaler.transform(data)

# Гистограммы после стандартизации
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

for i in range(6):
    row = i // 3
    col = i % 3
    axs[row, col].hist(data_scaled[:, i], bins=n_bins, edgecolor='black')
    axs[row, col].set_title(features[i], fontsize=10)
    axs[row, col].grid(True)

plt.suptitle('Гистограммы после StandardScaler', fontsize=14)
plt.tight_layout()
plt.savefig('standard_scaled_histograms.png')
plt.show()

# Расчет мат. ожидания и СКО
mean_before = np.mean(data, axis=0)
std_before = np.std(data, axis=0)
mean_after = np.mean(data_scaled, axis=0)
std_after = np.std(data_scaled, axis=0)

print("Мат. ожидание до стандартизации:", mean_before)
print("СКО до стандартизации:", std_before)
print("Мат. ожидание после стандартизации:", mean_after)
print("СКО после стандартизации:", std_after)

for i, feature in enumerate(features):
    print("{:<30} {:<15.2f} {:<15.2f} {:<15.2f} {:<15.2f}".format(
        feature, 
        mean_before[i], 
        std_before[i],
        mean_after[i],
        std_after[i]
    ))

# --------------------- 5. Приведение к диапазону ---------------------
# MinMaxScaler
min_max_scaler = preprocessing.MinMaxScaler().fit(data)
data_min_max = min_max_scaler.transform(data)

# MaxAbsScaler
max_abs_scaler = preprocessing.MaxAbsScaler().fit(data)
data_max_abs = max_abs_scaler.transform(data)

# RobustScaler
robust_scaler = preprocessing.RobustScaler().fit(data)
data_robust = robust_scaler.transform(data)

# Пользовательский масштабатор [-5, 10]
def custom_scaler(data):
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    scaled = -5 + 15 * (data - min_val) / (max_val - min_val + 1e-8)  # +1e-8 для избежания деления на 0
    return scaled

data_custom = custom_scaler(data)

# --------------------- 6. Нелинейные преобразования ---------------------
# QuantileTransformer, равномерное распределение
quantile_transformer = QuantileTransformer(n_quantiles=100, random_state=0)
data_quantile = quantile_transformer.fit_transform(data)

# QuantileTransformer, нормальное распределение
quantile_normal = QuantileTransformer(n_quantiles=100, output_distribution='normal', random_state=0)
data_quantile_normal = quantile_normal.fit_transform(data)

# PowerTransformer
min_max_scaler = preprocessing.MinMaxScaler().fit(data)
data_min_max_scaled = min_max_scaler.transform(data)

# --------------------- 7. Дискретизация признаков ---------------------
bins_config = {
    'age': 3,
    'creatinine_phosphokinase': 4,
    'ejection_fraction': 3,
    'platelets': 10,
    'serum_creatinine': 2,
    'serum_sodium': 4
}

data_discretized = data.copy()
discretizers = {}

for i, feature in enumerate(features):
    n_bins = bins_config[feature]
    discretizer = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='uniform')
    data_discretized[:, i] = discretizer.fit_transform(data[:, i].reshape(-1, 1)).flatten()
    discretizers[feature] = discretizer

# Вывод границ интервалов
print("Границы интервалов:")
for feature in features:
    edges = discretizers[feature].bin_edges_[0]
    print(f"{feature}: {edges.round(2)}")

# Гистограммы после дискретизации
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
for i in range(6):
    row = i // 3
    col = i % 3
    axs[row, col].hist(data_discretized[:, i], bins=bins_config[features[i]], edgecolor='black')
    axs[row, col].set_title(features[i], fontsize=10)
    axs[row, col].grid(True)

plt.suptitle('Гистограммы после дискретизации', fontsize=14)
plt.tight_layout()
plt.savefig('discretized_histograms.png')
plt.show()