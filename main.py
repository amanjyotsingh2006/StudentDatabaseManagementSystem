import os
from dotenv import load_dotenv
import mysql.connector
from tkinter import *
from tkinter import messagebox

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME", "students_db"),
    "port": int(os.getenv("DB_PORT", 3307))
}

# -Database Setup
def connect():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            age INT,
            grade VARCHAR(10)
        )
    """)
    conn.commit()
    conn.close()

def insert(name, age, grade):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, age, grade) VALUES (%s, %s, %s)", 
                (name, age, grade))
    conn.commit()
    conn.close()

def view():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def update(id, name, age, grade):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=%s, age=%s, grade=%s WHERE id=%s",
                (name, age, grade, id))
    conn.commit()
    conn.close()


def get_selected_row(event):
    global selected_tuple
    index = listbox.curselection()
    if index:
        selected_tuple = listbox.get(index[0])
        entry_name.delete(0, END)
        entry_name.insert(END, selected_tuple[1])
        entry_age.delete(0, END)
        entry_age.insert(END, selected_tuple[2])
        entry_grade.delete(0, END)
        entry_grade.insert(END, selected_tuple[3])

def view_command():
    listbox.delete(0, END)
    for row in view():
        listbox.insert(END, row)

def add_command():
    insert(name_text.get(), age_text.get(), grade_text.get())
    view_command()

def delete_command():
    try:
        delete(selected_tuple[0])
        view_command()
    except:
        messagebox.showerror("Error", "Select a student to delete")

def update_command():
    try:
        update(selected_tuple[0], name_text.get(), age_text.get(), grade_text.get())
        view_command()
    except:
        messagebox.showerror("Error", "Select a student to update")


connect()
window = Tk()
window.title("Student Database Management (MySQL)")


Label(window, text="Name").grid(row=0, column=0, padx=5, pady=5)
Label(window, text="Age").grid(row=0, column=2, padx=5, pady=5)
Label(window, text="Grade").grid(row=1, column=0, padx=5, pady=5)


name_text = StringVar()
entry_name = Entry(window, textvariable=name_text)
entry_name.grid(row=0, column=1)

age_text = StringVar()
entry_age = Entry(window, textvariable=age_text)
entry_age.grid(row=0, column=3)

grade_text = StringVar()
entry_grade = Entry(window, textvariable=grade_text)
entry_grade.grid(row=1, column=1)


listbox = Listbox(window, height=10, width=50)
listbox.grid(row=2, column=0, columnspan=4, rowspan=6, padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", get_selected_row)

scrollbar = Scrollbar(window)
scrollbar.grid(row=2, column=4, rowspan=6)
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)


Button(window, text="Add Student", width=12, command=add_command).grid(row=2, column=5, pady=2)
Button(window, text="Update", width=12, command=update_command).grid(row=3, column=5, pady=2)
Button(window, text="Delete", width=12, command=delete_command).grid(row=4, column=5, pady=2)
Button(window, text="View All", width=12, command=view_command).grid(row=5, column=5, pady=2)
Button(window, text="Close", width=12, command=window.destroy).grid(row=6, column=5, pady=2)

window.mainloop()
