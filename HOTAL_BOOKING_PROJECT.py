 ####HOTAL BOOKING MANAGEMENT PROJECT #####
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkcalendar import DateEntry

# Create database and table
def create_db():
    conn = sqlite3.connect('hotel_management.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            room_type TEXT NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add booking
def add_booking():
    name = entry_name.get()
    room_type = entry_room_type.get()
    check_in = entry_check_in.get()
    check_out = entry_check_out.get()

    if not (name and room_type and check_in and check_out):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return
    
    if check_in >= check_out:
        messagebox.showwarning("Input Error", "Check-out date must be after check-in date")
        return

    conn = sqlite3.connect('hotel_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO bookings (name, room_type, check_in, check_out) VALUES (?, ?, ?, ?)',
              (name, room_type, check_in, check_out))
    conn.commit()
    conn.close()

    clear_fields()
    messagebox.showinfo("Success", "Booking added successfully!")

# Function to view bookings
def view_bookings():
    conn = sqlite3.connect('hotel_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    rows = c.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)
    
    for id, name, room_type, check_in, check_out in rows:
        tree.insert('', tk.END, values=(id, name, room_type, check_in, check_out))

# Function to delete a booking
def delete_booking():
    booking_id = entry_booking_id.get()
    
    if not booking_id:
        messagebox.showwarning("Input Error", "Please enter a booking ID to delete")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?")
    if confirm:
        conn = sqlite3.connect('hotel_management.db')
        c = conn.cursor()
        c.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        conn.commit()
        conn.close()

        entry_booking_id.delete(0, tk.END)
        messagebox.showinfo("Success", "Booking deleted successfully!")
        view_bookings()

# Function to edit a booking
def edit_booking():
    booking_id = entry_booking_id.get()
    name = entry_name.get()
    room_type = entry_room_type.get()
    check_in = entry_check_in.get()
    check_out = entry_check_out.get()

    if not booking_id:
        messagebox.showwarning("Input Error", "Please enter a booking ID to edit")
        return

    if not (name and room_type and check_in and check_out):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    if check_in >= check_out:
        messagebox.showwarning("Input Error", "Check-out date must be after check-in date")
        return

    conn = sqlite3.connect('hotel_management.db')
    c = conn.cursor()
    c.execute('UPDATE bookings SET name = ?, room_type = ?, check_in = ?, check_out = ? WHERE id = ?',
              (name, room_type, check_in, check_out, booking_id))
    conn.commit()
    conn.close()

    clear_fields()
    messagebox.showinfo("Success", "Booking updated successfully!")
    view_bookings()

# Function to search for a booking
def search_booking():
    search_term = entry_booking_id.get()
    conn = sqlite3.connect('hotel_management.db')
    c = conn.cursor()
    if search_term.isdigit():
        c.execute('SELECT * FROM bookings WHERE id = ?', (search_term,))
    else:
        c.execute('SELECT * FROM bookings WHERE name LIKE ?', ('%' + search_term + '%',))
    rows = c.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)
    
    if rows:
        for id, name, room_type, check_in, check_out in rows:
            tree.insert('', tk.END, values=(id, name, room_type, check_in, check_out))
    else:
        messagebox.showinfo("Search Result", "No bookings found.")

# Function to clear input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_room_type.delete(0, tk.END)
    entry_check_in.delete(0, tk.END)
    entry_check_out.delete(0, tk.END)
    entry_booking_id.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("700x600")
root.configure(bg="#e0f7fa")  # Light cyan background color

# Create frames for better layout
frame_input = tk.Frame(root, bg="#b2ebf2")
frame_input.pack(pady=10, padx=10, fill='x')

frame_buttons = tk.Frame(root, bg="#b2ebf2")
frame_buttons.pack(pady=10)

frame_view = tk.Frame(root, bg="#b2ebf2")
frame_view.pack(pady=10, fill='both', expand=True)

# Create UI elements with color and font adjustments
label_style = {'bg': "#b2ebf2", 'font': ('Arial', 12)}
entry_style = {'width': 35, 'bg': "#ffffff", 'font': ('Arial', 12)}

tk.Label(frame_input, text="Guest Name", **label_style).grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_name = tk.Entry(frame_input, **entry_style)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Room Type", **label_style).grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_room_type = tk.Entry(frame_input, **entry_style)
entry_room_type.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Check-in Date", **label_style).grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_check_in = DateEntry(frame_input, width=12, background='darkblue', foreground='white', borderwidth=2)
entry_check_in.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Check-out Date", **label_style).grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_check_out = DateEntry(frame_input, width=12, background='darkblue', foreground='white', borderwidth=2)
entry_check_out.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Booking ID (for deletion)", **label_style).grid(row=4, column=0, padx=5, pady=5, sticky='w')
entry_booking_id = tk.Entry(frame_input, **entry_style)
entry_booking_id.grid(row=4, column=1, padx=5, pady=5)

# Buttons with customized appearance
button_style = {'padx': 10, 'pady': 5, 'bg': '#4db6ac', 'fg': 'white', 'font': ('Arial', 10, 'bold')}
button_style_hover = {'bg': '#00796b', 'activebackground': '#004d40'}

def create_button(text, command):
    button = tk.Button(frame_buttons, text=text, command=command, **button_style)
    button.pack(side=tk.LEFT, padx=5)
    button.bind("<Enter>", lambda e: button.config(**button_style_hover))
    button.bind("<Leave>", lambda e: button.config(**button_style))
    return button

create_button("Book Room", add_booking)
create_button("Edit Booking", edit_booking)
create_button("View Bookings", view_bookings)
create_button("Delete Booking", delete_booking)
create_button("Search Booking", search_booking)

# Create Treeview for displaying bookings
columns = ("ID", "Name", "Room Type", "Check-in", "Check-out")
tree = ttk.Treeview(frame_view, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Guest Name")
tree.heading("Room Type", text="Room Type")
tree.heading("Check-in", text="Check-in Date")
tree.heading("Check-out", text="Check-out Date")

# Treeview styling
tree.pack(pady=10, fill='both', expand=True)
tree.column("ID", width=40)
tree.column("Name", width=200)
tree.column("Room Type", width=120)
tree.column("Check-in", width=120)
tree.column("Check-out", width=120)

# Customize Treeview colors
tree.tag_configure('oddrow', background="#e1f5fe")  # Light blue for odd rows
tree.tag_configure('evenrow', background="#ffffff")  # White for even rows

# Create database
create_db()

# Run the application
root.mainloop()
