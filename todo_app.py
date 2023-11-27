import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to load existing tasks from a JSON file
def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            try:
                tasks = json.load(file)
            except json.decoder.JSONDecodeError:
                tasks = {'tasks': []}
        return tasks
    else:
        return {'tasks': []}

# Function to save tasks to a JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=2)

# Function to display the list of tasks in a GUI window
def display_tasks_gui(tasks):
    task_list = "\n--- Your To-Do List ---\n"
    if tasks['tasks']:
        for i, task in enumerate(tasks['tasks'], start=1):
            task_list += f"{i}. {task['title']} - {task['date']}\n"
    else:
        task_list += "Your to-do list is empty."
    
    messagebox.showinfo("To-Do List", task_list)

# Function to add a new task
def add_task_gui(tasks):
    title = simpledialog.askstring("Input", "Enter task title:")
    date_str = simpledialog.askstring("Input", "Enter due date (YYYY-MM-DD):")
    
    try:
        due_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    tasks['tasks'].append({'title': title, 'date': due_date})
    save_tasks(tasks)
    messagebox.showinfo("Success", f"Task '{title}' added successfully!")

# Function to remove a task
def remove_task_gui(tasks):
    task_list = display_tasks_gui(tasks)
    task_number = simpledialog.askinteger("Input", f"{task_list}\nEnter the number of the task to remove:")

    if task_number and 1 <= task_number <= len(tasks['tasks']):
        removed_task = tasks['tasks'].pop(task_number - 1)
        save_tasks(tasks)
        messagebox.showinfo("Success", f"Task '{removed_task['title']}' removed successfully!")
    else:
        messagebox.showerror("Error", "Invalid task number. Please enter a valid number.")

# Function to update a task
def update_task_gui(tasks):
    task_list = display_tasks_gui(tasks)
    task_number = simpledialog.askinteger("Input", f"{task_list}\nEnter the number of the task to update:")

    if task_number and 1 <= task_number <= len(tasks['tasks']):
        task = tasks['tasks'][task_number - 1]
        new_title = simpledialog.askstring("Input", f"Enter a new title for '{task['title']}':")
        new_date_str = simpledialog.askstring("Input", f"Enter a new due date for '{task['title']}' (YYYY-MM-DD):")

        try:
            new_due_date = datetime.strptime(new_date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        task['title'] = new_title
        task['date'] = new_due_date
        save_tasks(tasks)
        messagebox.showinfo("Success", f"Task '{new_title}' updated successfully!")
    else:
        messagebox.showerror("Error", "Invalid task number. Please enter a valid number.")

# Main function for the GUI
def main_gui():
    tasks = load_tasks()

    root = tk.Tk()
    root.title("To-Do List")

    label = tk.Label(root, text="To-Do List Application", font=("Helvetica", 16))
    label.pack(pady=10)

    while True:
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        display_button = tk.Button(button_frame, text="Display Tasks", command=lambda: display_tasks_gui(tasks))
        display_button.grid(row=0, column=0, padx=5)

        add_button = tk.Button(button_frame, text="Add Task", command=lambda: add_task_gui(tasks))
        add_button.grid(row=0, column=1, padx=5)

        remove_button = tk.Button(button_frame, text="Remove Task", command=lambda: remove_task_gui(tasks))
        remove_button.grid(row=0, column=2, padx=5)

        update_button = tk.Button(button_frame, text="Update Task", command=lambda: update_task_gui(tasks))
        update_button.grid(row=0, column=3, padx=5)

        exit_button = tk.Button(button_frame, text="Exit", command=root.destroy)
        exit_button.grid(row=0, column=4, padx=5)

        root.mainloop()

if __name__ == "__main__":
    main_gui()
