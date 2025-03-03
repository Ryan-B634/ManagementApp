# Version 0.2
# To Do:
# Backend
# Task System
# Rest of Pages

import tkinter as tk
from tkinter import messagebox
import pymongo  # Database
from pymongo import MongoClient # Database
import re   # Regular Expression to validate email

# ---------------------------- IMPORTANT CLASS -------------------------------

class Navigating(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)        
        self.wm_title("Management Application")

        self.frames = {}

        for F in [Login, SignUp, Homepage]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the Login frame
        self.show_frame(Login)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Bring the frame to the top

#---------------------------- IMPORTANT CLASS END ----------------------------

# Validating the login details
def validate_login(email_entry, password_entry, controller):
    username = email_entry.get()
    password = password_entry.get()

    # Example valid username and password (Needs to be replaced and linked to a database eventually)
    valid_username = "admin"
    valid_password = "admin"

    client = MongoClient("mongodb://localhost:27017")
    mydb = client["Users"]
    mycol = mydb["UserInfo"]

    CheckUser=mycol.find_one({"Email":username})
    CheckPass=mycol.find_one({"Password":password})

    if not CheckUser == None:
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        controller.show_frame(Homepage)  # Show homepage after successful login
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


# Login Page
class Login(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='Lightblue')

        # Labels and buttons
        tk.Label(self, text = "Company Name",fg="Black", bg="lightblue", font=("Times", 48, "bold")).place(x=720,y=0)
        tk.Label(self, text="Login", fg="Black", bg="lightblue", font=("Times", 48, "bold")).place(x=850, y=100)
        tk.Button(self, text="Sign up", fg="Black", bg="white", font=("Times", 24), command=lambda: controller.show_frame(SignUp)).place(x=885, y=700)

        tk.Label(self, text="Enter Email", fg="Black", bg="lightblue", font=("Times", 24, "bold")).place(x=850, y=200)
        self.LoginEmail = tk.Entry(self, width=45)  # Store the Entry widget as an instance variable
        self.LoginEmail.place(x=800, y=300)

        tk.Label(self, text="Enter Password", fg="Black", bg="lightblue", font=("Times", 24, "bold")).place(x=825, y=400)
        self.LoginPassword = tk.Entry(self, width=45, show="*")  # Store the Entry widget as an instance variable
        self.LoginPassword.place(x=800, y=500)

        # Hide/Show Password button
        self.show_password_button = tk.Button(self, text="Show", fg="Black", bg="white", font=("Times", 18), command=self.toggle_password)
        self.show_password_button.place(x=1250, y=500)

        # Login button that calls the validate_login function
        tk.Button(self, text="Login", fg="Black", bg="white", font=("Times", 24),
                  command=lambda: validate_login(self.LoginEmail, self.LoginPassword, controller)).place(x=895, y=600)


    def toggle_password(self):
        """ Toggle password visibility """
        if self.LoginPassword.cget('show') == "*":
            self.LoginPassword.config(show="")  # Show the password
            self.show_password_button.config(text="Hide")  # Change button text to "Hide"
        else:
            self.LoginPassword.config(show="*")  # Hide the password
            self.show_password_button.config(text="Show")  # Change button text to "Show"

    def closing(self):
        exit()


# SignUp Page
class SignUp(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='Lightblue')

        # Sign-up labels and buttons
        tk.Label(self, text="Sign Up", fg="Black", bg="lightblue", font=("Times", 48, "bold")).place(x=830, y=0)
        tk.Button(self, text="Back To Login", fg="Black", bg="white", font=("Times", 24), command=lambda: controller.show_frame(Login)).place(x=1550, y=0)

        # Sign-up fields
        tk.Label(self, text="Enter Email", fg="Black", bg="lightblue", font=("Times", 24, "bold")).place(x=850, y=200)
        self.SignUpEmail = tk.Entry(self, width=45)
        self.SignUpEmail.place(x=800, y=300)

        tk.Label(self, text="Enter Password", fg="Black", bg="lightblue", font=("Times", 24, "bold")).place(x=830, y=400)
        self.SignUpPassword = tk.Entry(self, width=45, show="*")  # Hide the password initially
        self.SignUpPassword.place(x=800, y=500)

        # Hide/Show Password button
        self.show_password_button = tk.Button(self, text="Show", fg="Black", bg="white", font=("Times", 18), command=self.toggle_password)
        self.show_password_button.place(x=1250, y=500)

        tk.Label(self, text="Confirm Password", fg="Black", bg="lightblue", font=("Times", 24, "bold")).place(x=800, y=600)
        self.SignUpConfirmPassword = tk.Entry(self, width=45, show="*")  # Hide the confirm password initially
        self.SignUpConfirmPassword.place(x=800, y=700)

        # Hide/Show Confirm Password button
        self.show_confirm_password_button = tk.Button(self, text="Show", fg="Black", bg="white", font=("Times", 18), command=self.toggle_confirm_password)
        self.show_confirm_password_button.place(x=1250, y=700)

        # Sign-up button
        tk.Button(self, text="SignUp", fg="Black", bg="white", font=("Ebrima", 24),
                  command=self.addUser).place(x=885, y=900)


    def toggle_password(self):
        """ Toggle password visibility for Sign Up """
        if self.SignUpPassword.cget('show') == "*":
            self.SignUpPassword.config(show="")  # Show the password
            self.show_password_button.config(text="Hide")  # Change button text to "Hide"
        else:
            self.SignUpPassword.config(show="*")  # Hide the password
            self.show_password_button.config(text="Show")  # Change button text to "Show"

    def toggle_confirm_password(self):
        """ Toggle confirm password visibility for Sign Up """
        if self.SignUpConfirmPassword.cget('show') == "*":
            self.SignUpConfirmPassword.config(show="")  # Show the confirm password
            self.show_confirm_password_button.config(text="Hide")  # Change button text to "Hide"
        else:
            self.SignUpConfirmPassword.config(show="*")  # Hide the confirm password
            self.show_confirm_password_button.config(text="Show")  # Change button text to "Show"

    def addUser(self):
        client = MongoClient("mongodb://localhost:27017")
        mydb = client["Users"]
        mycol = mydb["UserInfo"]
            
        cipher = self.controller.cipher

        user = self.LoginBox.get()
        Pwd = self.Pwd.get()
        ConfPwd = self.ConfPass.get()
        FName = self.FirstName.get()
        LName=self.LastName.get()
        EmailRE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


        Exist = mycol.find_one({"Email": user})

        specialchar = re.compile("[$&+,:;=?@#|'<>.-^*()%!]")

        def contains_special_characters(string):
            return bool(specialchar.search(string))

        if Exist is None:

            if EmailRE.match(user):

                if Pwd == ConfPwd:

                    if len(Pwd) >= 8:

                        if contains_special_characters(Pwd):

                            encrypted_password = cipher.encrypt(Pwd.encode())

                            NewUser = [{"First Name":FName,"Last Name":LName,"Email": user, "Password": encrypted_password}]
                            mycol.insert_many(NewUser)
                            messagebox.showinfo("Success","User Registered Successfully.")
                            self.AcceptClear()
                        else:
                            messagebox.showerror("Error","Password Must Contain At Least one Special Character")
                            self.clear()

                    else:
                        messagebox.showerror("Error","Password Must Be At Least 8 Characters")
                        self.clear()
                else:
                    messagebox.showerror("Error","Passwords Do Not Match")
                    self.clear()
            else:
                messagebox.showerror("Error","Please Enter A Valid Email")
                self.clear()
        else:
            messagebox.showerror("Error","Email Is Already In Use")
            self.clear()



    def AcceptClear(self):
        self.Pwd.delete(0, tk.END)
        self.ConfPass.delete(0, tk.END)
        self.FirstName.delete(0, tk.END)
        self.LastName.delete(0, tk.END)
        self.LoginBox.delete(0, tk.END)

    def clear(self):
        self.Pwd.delete(0, tk.END)
        self.ConfPass.delete(0, tk.END)



class Homepage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.config(bg='Lightblue')

        tk.Label(self, text="Homepage", fg="black", bg="lightblue", font=("Ebrima", 48, "bold")).place(x=650, y=0)

        tk.Label(self, text="Homepage", fg="black", bg="lightblue", font=("Ebrima", 48, "bold")).place(x=700, y=0)
        tk.Button(self, text="Logout", fg="black", bg="white", font=("Ebrima", 12), command=lambda: controller.show_frame(Login)).place(x=0, y=0)

        # Search bar label and input field
        self.search_label = tk.Label(self, text="Search Projects:", fg="black", bg="lightblue", font=("Ebrima", 18))
        self.search_label.place(x=1500, y=10)

        self.search_entry = tk.Entry(self, width=30, font=("Ebrima", 18))
        self.search_entry.place(x=1400, y=50)

        # Search button
        self.search_button = tk.Button(self, text="Search", fg="black", bg="white", font=("Ebrima", 18), command=self.filter_projects)
        self.search_button.place(x=1750, y=50)

        # Display the projects in a listbox (Isn't linked up with anything yet)
        self.project_listbox = tk.Listbox(self, width=25, height=5, font=("Ebrima", 14)) 
        self.project_listbox.place(x=1400, y=90)  # Position the list box just below the search bar
        self.update_project_listbox()

        self.createProjectButton = tk.Button(self, text="Create New Project", fg="black", bg="DeepskyBlue3", font=("Ebrima", 24, "bold"), command=self.popup1)
        self.createProjectButton.place(x=750, y=150)

    def filter_projects(self):
        # Get the text from the search bar
        search_query = self.search_entry.get().lower()

        # Filter projects based on search query
        self.filtered_projects = [project for project in self.projects if search_query in project.lower()]

        # Update the project listbox with filtered results
        self.update_project_listbox()

    def update_project_listbox(self):
        # Clear the current listbox content
        self.project_listbox.delete(0, tk.END)

        # Insert the filtered projects into the listbox
        for project in self.filtered_projects:
            self.project_listbox.insert(tk.END, project)

    def closing(self):
        exit()
        self.createProjectButton = tk.Button(self, text="Create New Project", fg="black", bg="DeepskyBlue3", font=("Ebrima", 24, "bold"), command=self.popup1)
        self.createProjectButton.place(x=750, y=150)

        self.projects = []  # List to store project buttons

    def popup1(self):
        # Creates a popup window for entering a new project name
        popup_window = tk.Toplevel()
        popup_window.title("Create New Project")
        popup_window.geometry("400x300")
        popup_window.configure(bg='lightblue')

        tk.Label(popup_window, text="Enter Project Name:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=10)

        # Entry widget for project name input
        Popup_Enter = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        Popup_Enter.pack(pady=5)

        # Button to create the project when clicked
        self.CreateProject = tk.Button(popup_window, text="Create Project", bg='DeepskyBlue3', fg='midnight blue', font=("Ebrima", 12), command=lambda: self.create_new_project(Popup_Enter.get(), popup_window))

        self.CreateProject = tk.Button(popup_window, text="Create Project", bg='DeepskyBlue3', fg='midnight blue', font=("Ebrima", 12), command=lambda: self.create_new_project(Popup_Enter.get(), popup_window,))

        self.CreateProject = tk.Button(popup_window, text="Create Project", bg='DeepskyBlue3', fg='midnight blue', font=("Ebrima", 12), command=lambda: self.create_new_project(Popup_Enter.get(), popup_window,))

        self.CreateProject.pack(pady=20)

    def create_new_project(self, project_name, popup_window): # The positioning is yet to be tested due to time constraints
        if project_name:

            new_project_button = tk.Button(self, text=project_name, fg="black", bg="DeepskyBlue3", font=("Ebrima", 24, "bold"))

            max_y = 900
            x_offset = 270
            y_offset = 250
            button_spacing_y = 100
            button_spacing_x = 270

            # Calculates the y-position
            y_position = y_offset + len(self.projects) * button_spacing_y

            # Checks if the y-position exceeds y=900, then move to the right
            if y_position > max_y:
                row = (len(self.projects) // (max_y // button_spacing_y))  # Determine which row it should be in
                x_position = x_offset + (row * button_spacing_x)
                y_position = y_offset + ((len(self.projects) % (max_y // button_spacing_y)) * button_spacing_y)
            else:
                x_position = x_offset
                y_position = y_offset + len(self.projects) * button_spacing_y

            new_project_button.place(x=x_position, y=y_position)

            self.projects.append(new_project_button)  # Adds to the list of projects

            popup_window.destroy()

            messagebox.showinfo("Success", f"Project '{project_name}' created successfully!")
        else:
            # In case the user didn't enter anything
            messagebox.showwarning("No Name", "You must provide a project name.")


class Project(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.config(bg='Lightblue')

        # Project Label
        tk.Label(self, text="Project Area", fg="black", bg="lightblue", font=("Ebrima", 48, "bold")).place(x=720, y=0)

        # Progress Bar
        self.progress_label = tk.Label(self, text="Progress:", fg="black", bg="lightblue", font=("Ebrima", 18))
        self.progress_label.place(x=625, y=87)
        
        self.progress_bar = ttk.Progressbar(self, length=300, mode="determinate", maximum=100)
        self.progress_bar.place(x=750, y=100)

        # Task creation area
        self.create_task_button = tk.Button(self, text="Create New Task", fg="black", bg="DeepskyBlue3", font=("Ebrima", 24, "bold"), command=self.popup_task)
        self.create_task_button.place(x=750, y=150)

        self.tasks = []  # List to store task checkboxes
        self.completed_tasks = 0  # Counter for completed tasks

    def popup_task(self):
        # Creates a popup window for entering a new task name
        popup_window = tk.Toplevel(self.master)
        popup_window.title("Create New Task")
        popup_window.geometry("400x300")
        popup_window.configure(bg='lightblue')

        tk.Label(popup_window, text="Enter Task Name:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=10)

        # Entry widget for task name input
        task_name_entry = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        task_name_entry.pack(pady=5)

        # Button to create the task when clicked
        create_task_button = tk.Button(popup_window, text="Create Task", bg='DeepskyBlue3', fg='midnight blue', font=("Ebrima", 12), command=lambda: self.create_new_task(task_name_entry.get(), popup_window))
        create_task_button.pack(pady=20)

    def create_new_task(self, task_name, popup_window):
        if task_name:
            # Create a new checkbox for the task
            task_var = tk.BooleanVar()  # A variable to track the checkbox state

            task_checkbox = tk.Checkbutton(self, text=task_name, var=task_var, font=("Ebrima", 18), bg="lightblue", command=lambda: self.update_progress(task_var))
           
            # Resused method from homepage since it works.
            max_y = 500
            x_offset = 270
            y_offset = 250
            button_spacing_y = 100
            button_spacing_x = 270

            # Calculates the y-position
            y_position = y_offset + len(self.tasks) * button_spacing_y

            # Checks if the y-position exceeds y=500, then move to the right
            if y_position > max_y:
                row = (len(self.tasks) // (max_y // button_spacing_y))  # Determine which row it should be in
                x_position = x_offset + (row * button_spacing_x)
                y_position = y_offset + ((len(self.tasks) % (max_y // button_spacing_y)) * button_spacing_y)
            else:
                x_position = x_offset
                y_position = y_offset + len(self.tasks) * button_spacing_y

            task_checkbox.place(x=x_position, y=y_position)

            self.tasks.append((task_checkbox, task_var))

            popup_window.destroy()

            messagebox.showinfo("Success", f"Task '{task_name}' created successfully!")
        else:
            # In case the user didn't enter anything
            messagebox.showwarning("No Name", "You must provide a task name.")

    def update_progress(self, task_var):
        # This updates the progress bar as tasks are completed
        if task_var.get():
            self.completed_tasks += 1
        else:
            self.completed_tasks -= 1

        # Calculate progress percentage
        total_tasks = len(self.tasks)
        progress_percentage = (self.completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Update the progress bar value
        self.progress_bar["value"] = progress_percentage

        self.TaskButton = tk.Button(self, text="Task 1", fg="black", bg="grey", font=("Ebrima", 24, "bold"))
        self.TaskButton.place(x=270, y=150)


        # Quit button
        tk.Button(self, text="QUIT", command=self.closing).place(x=0, y=0)

    def closing(self):
        exit()

# ---------------------------- IMPORTANT AREA -------------------------------
root = Navigating()
root.wm_title("SafeNest Banking")
root.state("zoomed")
root.geometry("1920x1080")
root.mainloop()
