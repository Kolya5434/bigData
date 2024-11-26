import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tkinter as tk
from tkinter import scrolledtext, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def map_preprocess(data):
    X = data[['trip_distance', 'passenger_count', 'fare_amount', 'total_amount']]
    y = data['payment_type']
    return X, y

def reduce_train(X_train, y_train):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    return clf

def reduce_predict(clf, X_test):
    return clf.predict(X_test)

def visualize_feature_importance(clf, feature_names, root):
    # Візуалізація важливості фіч
    feature_importances = pd.Series(clf.feature_importances_, index=feature_names)
    fig, ax = plt.subplots()
    sns.barplot(x=feature_importances, y=feature_importances.index, ax=ax)
    ax.set_xlabel('Важливість фіч')
    ax.set_ylabel('Фічі')
    ax.set_title('Важливість фіч Random Forest')

    # Вставка графіка в GUI
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()

def run_random_forest():
    try:
        data = pd.read_csv('./data.csv', nrows=10000)

        X, y = map_preprocess(data)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        clf = reduce_train(X_train, y_train)

        y_pred = reduce_predict(clf, X_test)

        report = classification_report(y_test, y_pred)
        text_area.insert(tk.END, report)

        visualize_feature_importance(clf, X.columns, root)

    except Exception as e:
        messagebox.showerror("Помилка", str(e))

root = tk.Tk()
root.title("Random Forest Visualization")
root.geometry("1600x1600")

text_area = scrolledtext.ScrolledText(root, width=70, height=20)
text_area.pack(pady=10)

run_random_forest()

root.mainloop()