# Version 0.2
# To Do:
# Backend
# Task System
# Rest of Pages

import tkinter as tk
from tkinter import messagebox
import pymongo
from pymongo import MongoClient

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
    def __init__(self, parent, controller, master=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, master, *args, **kwargs)
        self.master = master
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

        # Quit button
        tk.Button(self, text="QUIT", command=self.closing).place(x=0, y=0)

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
    def __init__(self, parent, controller, master=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, master, *args, **kwargs)
        self.master = master
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
        tk.Button(self, text="SignUp", fg="Black", bg="white", font=("Times", 24),
                  command=lambda: validate_signup(
                      self.SignUpEmail.get(),
                      self.SignUpPassword.get(),
                      self.SignUpConfirmPassword.get(),
                      controller)).place(x=885, y=900)

        # Quit button
        tk.Button(self, text="QUIT", command=self.closing).place(x=0, y=0)

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

    def closing(self):
        exit()



# Update validate_signup to correctly handle the entries
def validate_signup(email, password, confirm_password, controller):
    if not email or not password or not confirm_password:
        messagebox.showerror("Sign Up Failed", "All fields are required.")
        return
    elif password != confirm_password and len(password) < 8:
        messagebox.showerror("Sign Up Failed", "Passwords do not match.")
        return
    else:
        messagebox.showinfo("Sign Up Successful", "Account created successfully!")  # Shows success message
        controller.show_frame(Homepage)  # Navigate to Homepage

class Homepage(tk.Frame):
    def __init__(self, parent, controller, master=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, master, *args, **kwargs)
        self.master = master
        self.config(bg='Lightblue')

        tk.Label(self, text="Homepage", fg="black", bg="lightblue", font=("Ebrima", 48, "bold")).place(x=650, y=0)

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
