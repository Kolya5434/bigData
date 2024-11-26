import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run_mapreduce():
    try:
        data = pd.read_csv('./data.csv', nrows=10000)

        data = data.dropna(subset=['passenger_count', 'total_amount'])
        data['passenger_count'] = pd.to_numeric(data['passenger_count'], errors='coerce')
        data['total_amount'] = pd.to_numeric(data['total_amount'], errors='coerce')
        data = data.dropna(subset=['passenger_count', 'total_amount'])

        def mapper(data):
            map_data = defaultdict(list)
            for _, row in data.iterrows():
                map_data[row['passenger_count']].append(row['total_amount'])
            return map_data

        def reducer(map_data):
            reduced_data = {}
            for key, values in map_data.items():
                reduced_data[key] = sum(values) / len(values)
            return reduced_data

        mapped_data = mapper(data)
        reduced_data = reducer(mapped_data)

        if not reduced_data:
            messagebox.showinfo("Результат", "Немає даних для візуалізації.")
        else:
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
            fig.suptitle('Візуалізація даних про поїздки')

            axs[0].bar(reduced_data.keys(), reduced_data.values(), color='skyblue')
            axs[0].set_xlabel('Кількість пасажирів')
            axs[0].set_ylabel('Середня вартість поїздки')
            axs[0].set_title('Стовпчикова діаграма')
            axs[0].legend(['Середня вартість для кожної категорії'], loc='upper right')

            axs[1].pie(reduced_data.values(), labels=reduced_data.keys(), autopct='%1.1f%%', startangle=90)
            axs[1].set_title('Кругова діаграма')

            axs[1].legend([f'Кількість пасажирів: {key}' for key in reduced_data.keys()], loc='center', bbox_to_anchor=(0.5, -0.2), ncol=1)

            for ax in axs.flat:
                ax.label_outer()

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()
            canvas.draw()

    except Exception as e:
        messagebox.showerror("Помилка", str(e))

root = tk.Tk()
root.title("MapReduce Visualization")

run_mapreduce()

root.mainloop()