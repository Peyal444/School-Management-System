import datetime  # To handle date operations
from tkinter import *  # To create the GUI
import tkinter.messagebox as mb  # To display message boxes in the GUI
from tkinter import ttk  # To use Treeview for displaying records
from tkcalendar import DateEntry  # To provide a calendar date picker (install via pip install tkcalendar)
import sqlite3  # To manage the SQLite database

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')  # Connecting to the SQLite database
cursor = connector.cursor()  # Creating a cursor object to execute SQL commands

# Creating the table if it does not exist
connector.execute(
    "CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)

# Function to reset all input fields
def reset_fields():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    # Resetting all the StringVar variables
    for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'stream_strvar']:
        exec(f"{i}.set('')")  # Clearing the value of each StringVar
    dob.set_date(datetime.datetime.now().date())  # Resetting the date entry to current date

# Function to reset the form and delete all records from the Treeview
def reset_form():
    global tree
    tree.delete(*tree.get_children())  # Deleting all records from the Treeview

    reset_fields()  # Resetting the input fields

# Function to display all records from the database in the Treeview
def display_records():
    tree.delete(*tree.get_children())  # Deleting all records from the Treeview

    # Fetching all records from the database
    curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
    data = curr.fetchall()  # Fetching all records

    # Inserting each record into the Treeview
    for records in data:
        tree.insert('', END, values=records)

# Function to add a new record to the database
def add_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    # Getting data from input fields
    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()

    # Checking if any field is empty
    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")  # Displaying error message
    else:
        try:
            # Inserting the record into the database
            connector.execute(
                'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)',
                (name, email, contact, gender, DOB, stream)
            )
            connector.commit()  # Committing the changes to the database
            mb.showinfo('Record added', f"Record of {name} was successfully added")  # Displaying success message
            reset_fields()  # Resetting the input fields
            display_records()  # Displaying updated records
        except:
            mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')  # Displaying error message for incorrect data type

# Function to remove a selected record from the database
def remove_record():
    if not tree.selection():  # Checking if any record is selected
        mb.showerror('Error!', 'Please select an item from the database')  # Displaying error message
    else:
        current_item = tree.focus()  # Getting the currently selected item
        values = tree.item(current_item)
        selection = values["values"]

        tree.delete(current_item)  # Deleting the selected item from the Treeview

        # Deleting the record from the database
        connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()  # Committing the changes to the database

        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.') 
        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')  # Displaying success message

        display_records()  # Displaying updated records

# Function to view and edit the selected record in the input fields
def view_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    current_item = tree.focus()  # Getting the currently selected item
    values = tree.item(current_item)
    selection = values["values"]

    # Extracting date from the selected record
    date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

    # Setting the input fields with the selected record's data
    name_strvar.set(selection[1])
    email_strvar.set(selection[2])
    contact_strvar.set(selection[3])
    gender_strvar.set(selection[4])
    dob.set_date(date)
    stream_strvar.set(selection[6])

# Initializing the GUI window
main = Tk()
main.title('School Management System')  # Setting the title of the window
main.geometry('1000x600')  # Setting the size of the window
main.resizable(0, 0)  # Disabling the resizing of the window

# Creating the background and foreground color variables
lf_bg = 'MediumSpringGreen'  # Background color for the left_frame
cf_bg = 'PaleGreen'  # Background color for the center_frame

# Creating the StringVar variables for input fields
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()

# Placing the components in the main window
Label(main, text="SCHOOL MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

# Creating and placing the left frame
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

# Creating and placing the center frame
center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

# Creating and placing the right frame
right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.375, rely=0.05)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.18)
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.31)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.44)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.57)
Label(left_frame, text="Stream", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.7)

# Creating and placing entry widgets for input fields in the left frame
Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.36)
Entry(left_frame, width=19, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.75)

# Creating and placing option menu for gender selection in the left frame
OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)

# Creating and placing date entry widget for DOB in the left frame
dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)

# Creating and placing submit button in the left frame
Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)

# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)

# Creating and configuring the Treeview widget for displaying records
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Stream"))

# Adding horizontal and vertical scrollbars to the Treeview
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

# Configuring the headings and columns of the Treeview
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()  # Displaying the initial set of records

# Finalizing the GUI window
main.update()  # Updating the window
main.mainloop()  # Running the main loop for the GUI
