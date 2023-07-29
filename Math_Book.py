import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def find_critical_points(coefficients, order):
    derivative_coefficients = [coefficients[i] * (order - i) for i in range(order)]
    roots = np.roots(derivative_coefficients)
    critical_points = [(root, evaluate_function(coefficients, order, root)) for root in roots]
    return critical_points


def evaluate_function(coefficients, order, x):
    result = 0
    for i in range(order + 1):
        result += coefficients[i] * x ** (order - i)
    return result


def plot_function_with_table_and_comments(coefficients, order):
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = evaluate_function(coefficients, order, X)
    critical_points = find_critical_points(coefficients, order)
    df = pd.DataFrame(critical_points, columns=['x', 'f(x)'])

    fig = plt.figure()
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.quiver(X, Y, np.zeros_like(Z), np.ones_like(Z), np.zeros_like(Z), Z)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Field of the Function')

    ax2 = fig.add_subplot(222, projection='3d')
    surf = ax2.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    fig.colorbar(surf, ax=ax2)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('Surface Plot of the Function')

    ax3 = fig.add_subplot(223)
    ax3.axis('off')
    table = ax3.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    ax3.set_title('Points Critiques')

    ax4 = fig.add_subplot(224)
    ax4.axis('off')
    intervals = calculate_intervals(coefficients, order)
    comments = generate_monotonicity_comments(intervals)
    ax4.text(0, 0, comments, fontsize=10)
    ax4.set_title('Monotonicity')

    plt.tight_layout()
    plt.show()


def get_function_coefficients():
    def on_click(coefficients):
        try:
            coefficients.extend([float(entry.get()) for entry in entries])
            root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid coefficients.")

    root = tk.Tk()
    root.title("Enter Coefficients")

    entries = []
    for i in range(order + 1):
        label = tk.Label(root, text=f"Coefficient for x^{order - i}")
        label.pack()

        entry = tk.Entry(root)
        entry.pack()
        entries.append(entry)

    button = tk.Button(root, text="Submit", command=lambda: on_click(coefficients))
    button.pack()

    root.mainloop()


def calculate_intervals(coefficients, order):
    derivative_coefficients = [coefficients[i] * (order - i) for i in range(order)]

    intervals = []
    prev_sign = np.sign(derivative_coefficients[0])

    for i in range(1, len(derivative_coefficients)):
        sign = np.sign(derivative_coefficients[i])
        if sign != prev_sign:
            intervals.append((i - 1, i))
        prev_sign = sign

    if prev_sign == 0:
        intervals.append((len(derivative_coefficients) - 1, len(derivative_coefficients)))

    return intervals


def generate_monotonicity_comments(intervals):
    comments = []
    for interval in intervals:
        if interval[0] == 0:
            comment = f"Function is decreasing in (-∞, x{interval[1]})"
        elif interval[1] == len(coefficients):
            comment = f"Function is increasing in (x{interval[0]}, +∞)"
        else:
            comment = f"Function is decreasing in (x{interval[0]}, x{interval[1]})"
        comments.append(comment)
    return "\n".join(comments)



# Example Usage

order = int(input("Enter the order N of the function (N < 10): "))

coefficients = []
get_function_coefficients()

if len(coefficients) != order + 1:
    messagebox.showerror("Error", "Incorrect number of coefficients.")
    exit()

plot_function_with_table_and_comments(coefficients, order)
