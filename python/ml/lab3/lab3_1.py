import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Загрузка данных
all_data = pd.read_csv('dataset_group.csv', header=None)

# Получение уникальных ID покупателей и товаров
unique_id = list(set(all_data[1]))
items = list(set(all_data[2]))

# Формирование датасета для анализа
dataset = [[elem for elem in all_data[all_data[1] == id][2] if elem in items] 
           for id in unique_id]

# Кодирование данных
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

# Анализ с алгоритмом Apriori
## a) Минимальная поддержка 0.3
results = apriori(df, min_support=0.3, use_colnames=True)
results['length'] = results['itemsets'].apply(len)
print("Результаты (min_support=0.3):\n", results)

## b) Ограничение max_len=1
results_maxlen1 = apriori(df, min_support=0.3, use_colnames=True, max_len=1)
print("\nРезультаты (max_len=1):\n", results_maxlen1)

## c) Наборы размера 2
results_size2 = results[results['length'] == 2]
print("\nНаборы размера 2:\n", results_size2)
print("\nКоличество наборов размера 2:", len(results_size2))

## d) Зависимость количества наборов от поддержки
supports = np.arange(0.05, 1.0, 0.01)
counts = []
for s in supports:
    res = apriori(df, min_support=s, use_colnames=True)
    counts.append(len(res))

plt.plot(supports, counts)
plt.xlabel('Уровень поддержки')
plt.ylabel('Количество наборов')
plt.title('Зависимость количества наборов от уровня поддержки')
plt.grid(True)
plt.savefig('support_vs_count.png')
plt.close()

## e) Пороговые значения поддержки для наборов разного размера
thresholds = {}
for size in [1, 2, 3]:
    for s in supports:
        res = apriori(df, min_support=s, use_colnames=True)
        res['length'] = res['itemsets'].apply(len)
        if len(res[res['length'] == size]) == 0:
            thresholds[size] = s
            break

print("Пороговые значения поддержки:", thresholds)

## f) Новый датасет (поддержка 0.38)
results_38 = apriori(df, min_support=0.38, use_colnames=True, max_len=1)
new_items = [list(elem)[0] for elem in results_38['itemsets']]
new_dataset = [[elem for elem in all_data[all_data[1] == id][2] if elem in new_items] 
               for id in unique_id]

# Дальнейшие шаги (g-l) аналогичны с заменой датасета/параметров