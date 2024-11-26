import tkinter as tk
from tkinter import messagebox
import subprocess

def run_mapreduce():
    try:
        subprocess.run(["python3", "map-reduce/mapreduce_visualization.py"], check=True)
        messagebox.showinfo("Успішно", "MapReduce візуалізація завершена!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Помилка", f"Помилка при виконанні MapReduce скрипту: {e}")

def run_random_forest():
    try:
        subprocess.run(["python3", "random-forest/randomforest_visualization.py"], check=True)
        messagebox.showinfo("Успішно", "Random Forest візуалізація завершена!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Помилка", f"Помилка при виконанні Random Forest скрипту: {e}")

def run_deep_learning():
    try:
        subprocess.run(["python3", "deep-learning/deepLearningVisualization.py"], check=True)
        messagebox.showinfo("Успішно", "Deep Learning візуалізація завершена!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Помилка", f"Помилка при виконанні Deep Learning скрипту: {e}")

root = tk.Tk()
root.title("Big Data Visualization")
root.geometry("300x400")

mapreduce_button = tk.Button(root, text="Запустити MapReduce", command=run_mapreduce)
mapreduce_button.pack(pady=20)

random_forest_button = tk.Button(root, text="Запустити Random Forest", command=run_random_forest)
random_forest_button.pack(pady=20)

deep_learning_button = tk.Button(root, text="Запустити Deep Learning", command=run_deep_learning)
deep_learning_button.pack(pady=20)

root.mainloop()