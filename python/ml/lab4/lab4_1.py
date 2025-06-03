import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, fpmax, association_rules
import networkx as nx

# --------- Шаг 1: Загрузка данных ---------
url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/groceries.csv"
all_data = pd.read_csv(url, header=None)
print("Первые 5 строк данных:")
print(all_data.head())

# --------- Шаг 2: Преобразование данных ---------
# Удаление NaN и создание списка транзакций
transactions = []
for i in range(len(all_data)):
    transaction = [item for item in all_data.iloc[i] if isinstance(item, str)]
    transactions.append(set(transaction))

# --------- Шаг 3: Уникальные товары ---------
unique_items = set()
for transaction in transactions:
    unique_items.update(transaction)
    
print(f"\nКоличество уникальных товаров: {len(unique_items)}")
print(f"Примеры товаров: {list(unique_items)[:5]}")

# --------- Шаг 4: Подготовка для MLxtend ---------
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
data = pd.DataFrame(te_ary, columns=te.columns_)

# --------- Шаг 5: FPGrowth ---------
fp_res = fpgrowth(data, min_support=0.03, use_colnames=True)
print("\nРезультаты FPGrowth:")
print(fp_res.head())

# --------- Шаг 6: FPMax ---------
fpmax_res = fpmax(data, min_support=0.03, use_colnames=True)
print("\nРезультаты FPMax:")
print(fpmax_res.head())

"""
Разница между FPGrowth и FPMax:
FPGrowth находит ВСЕ частые наборы, удовлетворяющие min_support.
FPMax находит только МАКСИМАЛЬНЫЕ частые наборы (не имеющие надмножеств с той же частотой).
"""

# --------- Шаг 7: Топ-10 товаров (гистограмма) ---------
item_counts = data.sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
item_counts.plot(kind='bar', color='skyblue')
plt.title('Топ-10 самых популярных товаров')
plt.ylabel('Частота')
plt.xlabel('Товар')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# --------- Шаг 8: Анализ ограниченного набора товаров ---------
selected_items = ['whole milk', 'yogurt', 'soda', 'tropical fruit', 'shopping bags',
                  'sausage', 'whipped/sour cream', 'rolls/buns', 'other vegetables',
                  'root vegetables', 'pork', 'bottled water', 'pastry',
                  'citrus fruit', 'canned beer', 'bottled beer']

# Фильтрация транзакций
filtered_trans = []
for trans in transactions:
    filtered_trans.append([item for item in trans if item in selected_items])

# Повторная подготовка данных
te_ary_filtered = te.fit(filtered_trans).transform(filtered_trans)
data_filtered = pd.DataFrame(te_ary_filtered, columns=te.columns_)

# FPGrowth и FPMax для отфильтрованных данных
fp_res_filtered = fpgrowth(data_filtered, min_support=0.05, use_colnames=True)
fpmax_res_filtered = fpmax(data_filtered, min_support=0.05, use_colnames=True)

print("\nFPGrowth (фильтр):", fp_res_filtered.shape[0], "наборов")
print("FPMax (фильтр):", fpmax_res_filtered.shape[0], "наборов")

# --------- Шаг 9: Зависимость числа правил от поддержки ---------
supports = np.arange(0.01, 0.2, 0.01)
counts = {'FPGrowth': [], 'FPMax': []}

for sup in supports:
    fp = fpgrowth(data, min_support=sup, use_colnames=True)
    fpm = fpmax(data, min_support=sup, use_colnames=True)
    counts['FPGrowth'].append(len(fp))
    counts['FPMax'].append(len(fpm))

plt.figure(figsize=(10, 6))
plt.plot(supports, counts['FPGrowth'], 'o-', label='FPGrowth')
plt.plot(supports, counts['FPMax'], 's-', label='FPMax')
plt.title('Зависимость количества наборов от уровня поддержки')
plt.xlabel('Минимальная поддержка')
plt.ylabel('Количество наборов')
plt.legend()
plt.grid(True)
plt.show()

# --------- Шаг 10: Ассоциативные правила ---------
# Генерация частых наборов
freq_items = fpgrowth(data, min_support=0.05, use_colnames=True)

# Генерация правил с min_confidence=0.3
rules = association_rules(freq_items, metric="confidence", min_threshold=0.3)
print("\nАссоциативные правила (первые 5):")
print(rules.head())

"""
Колонки в rules:
- antecedents: Набор-условие (левая часть правила)
- consequents: Набор-следствие (правая часть правила)
- antecedent support: Поддержка antecedents
- consequent support: Поддержка consequents
- support: Поддержка всего правила (A ∪ B)
- confidence: Достоверность = P(B|A) = support(A ∪ B) / support(A)
- lift: Лифт = [support(A ∪ B)] / [support(A) * support(B)]
- leverage: Леверидж = support(A ∪ B) - support(A) * support(B)
- conviction: Уверенность = [1 - support(B)] / [1 - confidence]
"""

# --------- Шаг 11: Визуализация графа ---------
def draw_rules_graph(rules_df, num_rules=10):
    G = nx.DiGraph()
    
    for _, row in rules_df.head(num_rules).iterrows():
        ant = ", ".join(list(row['antecedents']))
        cons = ", ".join(list(row['consequents']))
        weight = row['support'] * 100  # Масштабирование для ширины
        conf = row['confidence']
        
        G.add_edge(ant, cons, weight=weight, confidence=conf)
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(14, 10))
    
    # Рисуем узлы и ребра
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    # Рисуем ребра с шириной и подписями
    for edge in G.edges(data=True):
        nx.draw_networkx_edges(
            G, pos, 
            edgelist=[(edge[0], edge[1])], 
            width=edge[2]['weight'],
            alpha=0.7
        )
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels={(edge[0], edge[1]): f"Conf: {edge[2]['confidence']:.2f}"},
            font_size=9
        )
    
    plt.title('Ассоциативные правила (Ширина ребра = Support, Подпись = Confidence)')
    plt.axis('off')
    plt.show()

# Генерация правил для визуализации
viz_rules = association_rules(freq_items, metric="confidence", min_threshold=0.4)
draw_rules_graph(viz_rules, 15)

# --------- Шаг 12: Анализ метрик ---------
metrics = ['support', 'confidence', 'lift', 'conviction']
stats = {}
for metric in metrics:
    stats[metric] = {
        'mean': rules[metric].mean(),
        'median': rules[metric].median(),
        'std': rules[metric].std()
    }
print("\nСтатистика по метрикам:")
print(pd.DataFrame(stats).T)