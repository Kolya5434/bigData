import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
import tkinter as tk
from tkinter import scrolledtext, messagebox, Button
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def map_preprocess(data):
    basket = (data
              .groupby(['transaction_id', 'item'])['item']
              .count().unstack().reset_index().fillna(0)
              .set_index('transaction_id'))
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    return basket

def run_fp_growth(basket, min_support=0.01):
    return fpgrowth(basket, min_support=min_support, use_colnames=True)

def visualize_frequent_itemsets(itemsets, root):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='support', y='itemsets', data=itemsets.sort_values('support', ascending=False))
    plt.xlabel('Support')
    plt.ylabel('Itemsets')
    plt.title('Frequent Itemsets using FP-Growth')

    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()

def run_fp_growth_algorithm(root, text_area):
    try:
        # Загрузите данные
        data = pd.read_csv('../data.csv')  # Измените путь на свой

        # Подготовка данных
        basket = map_preprocess(data)

        # Выполнение FP-Growth
        frequent_itemsets = run_fp_growth(basket)

        # Вывод результатов
        text_area.delete(1.0, tk.END)  # Очищаем текстовое поле перед новой вставкой
        text_area.insert(tk.END, frequent_itemsets.to_string(index=False))

        # Визуализация частых наборов
        visualize_frequent_itemsets(frequent_itemsets, root)

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def create_gui():
    root = tk.Tk()
    root.title("FP-Growth Frequent Itemsets")

    # Текстовое поле для вывода
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # Кнопка для запуска алгоритма
    button = Button(root, text="Запуск FP-Growth", command=lambda: run_fp_growth_algorithm(root, text_area))
    button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()