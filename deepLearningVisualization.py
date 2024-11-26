import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tkinter as tk
from tkinter import scrolledtext, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential


def map_preprocess(data):
    X = data[['trip_distance', 'passenger_count', 'fare_amount', 'total_amount']]
    y = pd.get_dummies(data['payment_type']).values
    return X, y


def create_model(input_dim, num_classes):
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(input_dim,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def visualize_training(history, root):
    fig, ax = plt.subplots(2, 1, figsize=(8, 8))

    ax[0].plot(history.history['loss'], label='Втрати')
    ax[0].plot(history.history['val_loss'], label='Валідовані втрати')
    ax[0].set_title('Втрати')
    ax[0].set_ylabel('Втрати')
    ax[0].set_xlabel('Епоха')
    ax[0].legend()

    ax[1].plot(history.history['accuracy'], label='Точність')
    ax[1].plot(history.history['val_accuracy'], label='Валідована точність')
    ax[1].set_title('Точність')
    ax[1].set_ylabel('Точність')
    ax[1].set_xlabel('Епоха')
    ax[1].legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()
    root.update_idletasks()


def run_deep_learning(root, text_area):
    try:
        # Load the dataset
        data = pd.read_csv('./data.csv', nrows=10000)

        # Preprocess the data
        X, y = map_preprocess(data)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Create the model
        model = create_model(X_train.shape[1], y.shape[1])

        # Train the model
        history = model.fit(X_train, y_train, epochs=50, validation_split=0.2, verbose=0)

        # Predict the results
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_test_classes = np.argmax(y_test, axis=1)

        # Generate classification report
        report = classification_report(y_test_classes, y_pred_classes)
        text_area.insert(tk.END, report)
        text_area.insert(tk.END, "\n")

        # Visualize the training process
        visualize_training(history, root)

        # Show success message
        messagebox.showinfo("Успішно", "Deep Learning візуалізація завершена!")

    except Exception as e:
        messagebox.showerror("Помилка", str(e))


# Create the GUI
def create_gui():
    root = tk.Tk()
    root.title("Deep Learning GUI")

    # Text area for the report
    global text_area
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # Run deep learning without threading
    run_deep_learning(root, text_area)

    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    create_gui()