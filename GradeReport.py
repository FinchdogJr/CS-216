# GradeReport.py
# spring 2025
# Lukas Finch
# final project
# function read CSV file, summarizes data, draws graph, writes summary to CSV

import tkinter as tk
from tkinter import Canvas
import os


# called by File, Open
def process_data():
    canvas.delete("all")  # clear old chart

    # read GRADES.txt and tally counts
    grades = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    try:
        with open("GRADES.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line.isdigit():
                    score = int(line)
                    if 90 <= score <= 100:
                        grades['A'] += 1
                    elif 80 <= score <= 89:
                        grades['B'] += 1
                    elif 70 <= score <= 79:
                        grades['C'] += 1
                    elif 60 <= score <= 69:
                        grades['D'] += 1
                    else:
                        grades['F'] += 1
    except FileNotFoundError:
        canvas.create_text(150, 150, text="GRADES.txt not found", font=("Arial", 14))
        return

    total = sum(grades.values())
    if total == 0:
        canvas.create_text(150, 150, text="No valid data in GRADES.txt", font=("Arial", 14))
        return

    # Pie chart drawing
    colors = {'A': "Green", 'B': "navy", 'C': "brown", 'D': "grey", 'F': "Black"}

    start = 270
    for grade in grades:
        count = grades[grade]
        if count > 0:
            extent = count / total * 360
            canvas.create_arc(50, 50, 250, 250, start=start, extent=extent, fill=colors[grade])
            start += extent

    # Draw legend - Ai was a great help for this part
    legend_x = 270
    legend_y = 60
    spacing = 20
    for grade, color in colors.items():
        canvas.create_rectangle(legend_x, legend_y, legend_x + 15, legend_y + 15, fill=color)
        canvas.create_text(legend_x + 25, legend_y + 8, anchor='w', text=f"{grade}: {grades[grade]}", font=("Arial", 10))
        legend_y += spacing

    # Write to CSV
    file_name = "SUMMARY.csv"
    try:
        with open(file_name, "w") as out:
            out.write("Grade,Count\n")
            for grade in grades:
                out.write(f"{grade},{grades[grade]}\n")
        canvas.create_text(150, 280, text=f"SUMMARY.csv written", font=("Arial", 10))
    except Exception:
        canvas.create_text(150, 280, text="Error writing to SUMMARY.csv", fill="red", font=("Arial", 10))


# clear graph - called by File, New
def clear_graph():
    canvas.delete("all")

# exit program - called by File, Exit
def exit_program():
    main.destroy()

# main window setup
main = tk.Tk()
main.geometry('400x350')
main.title('P10 Project')

# create canvas
canvas = Canvas(main, width=500, height=500, bg='white')
canvas.pack()

# Create a menu bar
menu_bar = tk.Menu(main)

# Add "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=clear_graph)
file_menu.add_separator()
file_menu.add_command(label="Open", command=process_data)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_program)
menu_bar.add_cascade(label="File", menu=file_menu)

# Set the menu bar
main.config(menu=menu_bar)

# wait for menu selections
main.mainloop()

