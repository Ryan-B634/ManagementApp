import tkinter as tk
from tkinter import messagebox, ttk
import pymongo  # Database
from pymongo import MongoClient  # Database
import re   # Regular Expression to validate email
import tkcalendar  # For task and project deadlines
from tkcalendar import Calendar

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

        for F in [Login, SignUp, Homepage, Project]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # For testing, show Project page (change as needed)
        self.show_frame(Project)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Bring the frame to the top
#---------------------------- IMPORTANT CLASS END ----------------------------

def validate_login(email_entry, password_entry, controller):
    username = email_entry.get()
    password = password_entry.get()

    client = MongoClient("mongodb://localhost:27017")
    mydb = client["Users"]
    mycol = mydb["UserInfo"]

    user = mycol.find_one({"Email": username, "Password": password})

    if user is None:
        print("Invalid username or password.")
        messagebox.showerror("Login Failed", "Invalid username or password.")
    else:
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        controller.show_frame(Homepage)

# ---------------------------- LOGIN PAGE ----------------------------
class Login(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='Lightblue')

        tk.Label(self, text="Management Application", fg="Black", bg="lightblue", font=("Ebrima", 48, "bold")).place(x=590, y=0)
        tk.Label(self, text="Login", fg="Black", bg="lightblue", font=("Ebrima", 32, "bold")).place(x=900, y=100)
        tk.Button(self, text="Sign up", fg="Black", bg="DeepskyBlue1", font=("Ebrima", 18), height=-4, command=lambda: controller.show_frame(SignUp)).place(x=920, y=700)

        tk.Label(self, text="Enter Email:", fg="Black", bg="lightblue", font=("Ebrima", 24, "bold")).place(x=610, y=285)
        self.LoginEmail = tk.Entry(self, width=45, font=("Ebrima", 13, "bold"))
        self.LoginEmail.place(x=800, y=300)

        tk.Label(self, text="Enter Password:", fg="Black", bg="lightblue", font=("Ebrima", 24, "bold")).place(x=547, y=485)
        self.LoginPassword = tk.Entry(self, font=("Ebrima", 13, "bold"), width=45, show="*")
        self.LoginPassword.place(x=800, y=500)

        self.show_password_button = tk.Button(self, text="👁", fg="Black", bg="lightblue", border=0, font=("Ebrima", 18), command=self.toggle_password)
        self.show_password_button.place(x=1250, y=487)

        tk.Button(self, text="Login", fg="Black", bg="DeepskyBlue1", font=("Ebrima", 18), height=-4,
                  command=lambda: validate_login(self.LoginEmail, self.LoginPassword, controller)).place(x=935, y=600)

    def toggle_password(self):
        if self.LoginPassword.cget('show') == "*":
            self.LoginPassword.config(show="")
            self.show_password_button.config(text="Hide")
        else:
            self.LoginPassword.config(show="*")
            self.show_password_button.config(text="Show")

# ---------------------------- SIGN UP PAGE ----------------------------
class SignUp(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='Lightblue')
        self.controller = controller

        tk.Label(self, text="Sign Up", fg="Black", bg="lightblue", font=("Ebrima", 48, "bold")).place(x=830, y=0)
        tk.Button(self, text="Back To Login", fg="Black", bg="white", font=("Ebrima", 24), command=lambda: controller.show_frame(Login)).place(x=1550, y=0)

        tk.Label(self, text="Enter Email", fg="Black", bg="lightblue", font=("Ebrima", 24, "bold")).place(x=850, y=200)
        self.SignUpEmail = tk.Entry(self, width=45)
        self.SignUpEmail.place(x=800, y=300)

        tk.Label(self, text="Enter Password", fg="Black", bg="lightblue", font=("Ebrima", 24, "bold")).place(x=830, y=400)
        self.SignUpPassword = tk.Entry(self, width=45, show="*")
        self.SignUpPassword.place(x=800, y=500)

        self.show_password_button = tk.Button(self, text="Show", fg="Black", bg="white", font=("Ebrima", 18), command=self.toggle_password)
        self.show_password_button.place(x=1250, y=500)

        tk.Label(self, text="Confirm Password", fg="Black", bg="lightblue", font=("Ebrima", 24, "bold")).place(x=800, y=600)
        self.SignUpConfirmPassword = tk.Entry(self, width=45, show="*")
        self.SignUpConfirmPassword.place(x=800, y=700)

        self.show_confirm_password_button = tk.Button(self, text="Show", fg="Black", bg="white", font=("Ebrima", 18), command=self.toggle_confirm_password)
        self.show_confirm_password_button.place(x=1250, y=700)

        tk.Button(self, text="SignUp", fg="Black", bg="white", font=("Ebrima", 24), command=self.addUser).place(x=885, y=900)

    def toggle_password(self):
        if self.SignUpPassword.cget('show') == "*":
            self.SignUpPassword.config(show="")
            self.show_password_button.config(text="Hide")
        else:
            self.SignUpPassword.config(show="*")
            self.show_password_button.config(text="Show")

    def toggle_confirm_password(self):
        if self.SignUpConfirmPassword.cget('show') == "*":
            self.SignUpConfirmPassword.config(show="")
            self.show_confirm_password_button.config(text="Hide")
        else:
            self.SignUpConfirmPassword.config(show="*")
            self.show_confirm_password_button.config(text="Show")

    def addUser(self):
        client = MongoClient("mongodb://localhost:27017")
        mydb = client["Users"]
        mycol = mydb["UserInfo"]

        self.User = self.SignUpEmail.get()
        self.Pwd = self.SignUpPassword.get()
        self.ConfPwd = self.SignUpConfirmPassword.get()

        EmailRE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        Exist = mycol.find_one({"Email": self.User})
        specialchar = re.compile("[$&+,:;=?@#|'<>.-^*()%!]")
        def contains_special_characters(string):
            return bool(specialchar.search(string))
        if Exist is None:
            if EmailRE.match(self.User):
                if self.Pwd == self.ConfPwd:
                    if len(self.Pwd) >= 8:
                        if contains_special_characters(self.Pwd):
                            NewUser = [{"Email": self.User, "Password": self.Pwd}]
                            mycol.insert_many(NewUser)
                            messagebox.showinfo("Success", "User Registered Successfully.")
                            self.AcceptClear()
                            self.controller.show_frame(Login)
                        else:
                            messagebox.showerror("Error", "Password Must Contain At Least one Special Character")
                            self.clear()
                    else:
                        messagebox.showerror("Error", "Password Must Be At Least 8 Characters")
                        self.clear()
                else:
                    messagebox.showerror("Error", "Passwords Do Not Match")
                    self.clear()
            else:
                messagebox.showerror("Error", "Please Enter A Valid Email")
                self.clear()
        else:
            messagebox.showerror("Error", "Email Is Already In Use")
            self.clear()

    def AcceptClear(self):
        self.SignUpEmail.delete(0, tk.END)
        self.SignUpPassword.delete(0, tk.END)
        self.SignUpConfirmPassword.delete(0, tk.END)

    def clear(self):
        self.SignUpConfirmPassword.delete(0, tk.END)
        self.SignUpPassword.delete(0, tk.END)

# ---------------------------- HOMEPAGE ----------------------------
class Homepage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.config(bg='Lightblue')

        self.projects = []  
        self.filtered_projects = []

        tk.Label(self, text="Homepage", fg="black", bg="lightblue", font=("Ebrima", 48, "bold")).grid(row=0, column=2, padx=750)
        tk.Button(self, text="Logout", fg="black", bg="white", font=("Ebrima", 12), command=lambda: controller.show_frame(Login)).grid(row=0, column=1)

        self.filtered_projects = self.projects

        self.search_label = tk.Label(self, text="Search Projects:", fg="black", bg="lightblue", font=("Ebrima", 18))
        self.search_label.place(x=1500, y=10)
        self.search_entry = tk.Entry(self, width=30, font=("Ebrima", 18))
        self.search_entry.place(x=1400, y=50)
        self.search_button = tk.Button(self, text="Search", fg="black", bg="DeepskyBlue1", font=("Ebrima", 12), command=self.filter_projects)
        self.search_button.place(x=1750, y=50)

        self.project_listbox = tk.Listbox(self, width=41, height=5, font=("Ebrima", 14))
        self.project_listbox.place(x=1400, y=90)
        self.update_project_listbox()

        self.createProjectButton = tk.Button(self, text="Create New Project", fg="black", bg="DeepskyBlue1", font=("Ebrima", 24, "bold"), command=self.popup1)
        self.createProjectButton.grid(row=1, column=2, padx=20, pady=20)

    def filter_projects(self):
        search_query = self.search_entry.get().lower()
        self.filtered_projects = [project for project in self.projects if search_query in project.lower()]
        self.update_project_listbox()

    def update_project_listbox(self):
        self.project_listbox.delete(0, tk.END)
        for project in self.filtered_projects:
            self.project_listbox.insert(tk.END, project)

    def popup1(self):
        popup_window = tk.Toplevel()
        popup_window.title("Project Management")
        popup_window.geometry("400x400")
        popup_window.configure(bg='lightblue')

        tk.Label(popup_window, text="Enter Project Name:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=10)
        Popup_Enter = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        Popup_Enter.pack(pady=5)
        self.CreateProject = tk.Button(popup_window, text="Create Project", bg='DeepskyBlue1', fg='midnight blue', font=("Ebrima", 12),
                                        command=lambda: self.create_new_project(Popup_Enter.get(), popup_window))
        self.CreateProject.pack(pady=20)

        tk.Label(popup_window, text="Enter project Name to Delete:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=10)
        delete_project_entry = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        delete_project_entry.pack(pady=5)
        delete_project_button = tk.Button(popup_window, text="Delete project", bg='DeepskyBlue1', fg='midnight blue', font=("Ebrima", 12),
                                          command=lambda: self.delete_project(delete_project_entry.get(), popup_window))
        delete_project_button.pack(pady=20)

    def create_new_project(self, project_name, popup_window):
        if project_name:
            new_project_button = tk.Button(self, text=project_name, fg="black", bg="DeepskyBlue1", font=("Ebrima", 24, "bold"),
                                           command=lambda: self.controller.show_frame(Project))
            max_y = 700
            x_offset = 270
            y_offset = 250
            button_spacing_y = 100
            button_spacing_x = 270
            y_position = y_offset + len(self.projects) * button_spacing_y
            if y_position > max_y:
                row = (len(self.projects) // (max_y // button_spacing_y))
                x_position = x_offset + (row * button_spacing_x)
                y_position = y_offset + ((len(self.projects) % (max_y // button_spacing_y)) * button_spacing_y)
            else:
                x_position = x_offset
                y_position = y_offset + len(self.projects) * button_spacing_y
            new_project_button.place(x=x_position, y=y_position)
            self.projects.append((new_project_button, project_name))
            popup_window.destroy()
            messagebox.showinfo("Success", f"Project '{project_name}' created successfully!")
        else:
            messagebox.showwarning("No Name", "You must provide a project name.")

    def delete_project(self, project_name, popup_window):
        if project_name:
            project_found = False
            for new_project_button, stored_project_name in self.projects:
                if stored_project_name == project_name:
                    new_project_button.destroy()
                    self.projects.remove((new_project_button, stored_project_name))
                    project_found = True
                    break
            if project_found:
                messagebox.showinfo("Success", f"Project '{project_name}' deleted successfully!")
            else:
                messagebox.showwarning("Not Found", f"Project '{project_name}' not found.")
            popup_window.destroy()
        else:
            messagebox.showwarning("No Name", "You must provide a project name to delete.")

# ---------------------------- PROJECT PAGE (Task Management) ----------------------------
class Project(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller
        self.config(bg='Lightblue')
        # Initialize MongoDB for tasks
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["TaskDatabase"]
        self.tasks_collection = self.db["Tasks"]

        tk.Label(self, text="Project Area", fg="black", bg="lightblue", font=("Ebrima", 48, "bold")).grid(row=0, column=2, padx=650)
        self.progress_label = tk.Label(self, text="Progress:", fg="black", bg="lightblue", font=("Ebrima", 18))
        self.progress_label.place(x=625, y=87)
        self.progress_bar = ttk.Progressbar(self, length=300, mode="determinate", maximum=100)
        self.progress_bar.place(x=750, y=100)

        # "Add Task" Button opens popup to add a new task
        self.create_task_button = tk.Button(self, text="Add Task", fg="black", bg="DeepskyBlue1", font=("Ebrima", 24, "bold"), command=self.popup_task)
        self.create_task_button.grid(row=1, column=0, pady=20, padx=20, sticky="w")

        # Scrollable task area using Canvas and a Frame
        self.task_canvas = tk.Canvas(self, bg="lightblue", width=800, height=400)
        self.task_canvas.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.task_canvas.yview)
        self.scrollbar.grid(row=2, column=3, sticky="ns")
        self.task_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.task_frame = tk.Frame(self.task_canvas, bg="lightblue")
        self.task_canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.task_frame.bind("<Configure>", lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))

        self.tasks = []  # List to store tasks (each task is a dict with widget references and state)
        self.homeButton = tk.Button(self, text="Home", fg="gold", bg="red4", font=("Ebrima", 10, "bold"), command=lambda: controller.show_frame(Homepage))
        self.homeButton.grid(row=0, column=1)

    def popup_task(self):
        popup_window = tk.Toplevel()
        popup_window.title("Create A Task")
        popup_window.geometry("400x750")
        popup_window.configure(bg='lightblue')

        tk.Label(popup_window, text="Task Title:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        task_title_entry = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        task_title_entry.pack(pady=5)

        tk.Label(popup_window, text="Task Description:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        task_description_text = tk.Text(popup_window, width=30, height=4, font=("Ebrima", 12))
        task_description_text.pack(pady=5)

        tk.Label(popup_window, text="Assign Task to Team Member:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        team_members = ["Alice", "Bob", "Charlie", "David"]
        assignee_combobox = ttk.Combobox(popup_window, values=team_members, font=("Ebrima", 12))
        assignee_combobox.pack(pady=5)

        tk.Label(popup_window, text="Assign Task to Project:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        # Get project names from the Homepage projects list (if any)
        project_names = [proj[1] for proj in self.controller.frames[Homepage].projects]
        project_combobox = ttk.Combobox(popup_window, values=project_names, font=("Ebrima", 12))
        project_combobox.pack(pady=5)

        tk.Label(popup_window, text="Task Start Date:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        start_date_calendar = Calendar(popup_window, selectmode='day', year=2025, month=3, day=1)
        start_date_calendar.pack(pady=5)

        tk.Label(popup_window, text="Task End Date:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        end_date_calendar = Calendar(popup_window, selectmode='day', year=2025, month=3, day=1)
        end_date_calendar.pack(pady=5)

        tk.Label(popup_window, text="Task Priority Level:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        priority_combobox = ttk.Combobox(popup_window, values=["Low", "Medium", "High"], font=("Ebrima", 12))
        priority_combobox.pack(pady=5)

        tk.Label(popup_window, text="Completion Status:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        status_combobox = ttk.Combobox(popup_window, values=["In-Progress", "Completed"], font=("Ebrima", 12))
        status_combobox.pack(pady=5)

        tk.Button(popup_window, text="Assign Task", bg='DeepskyBlue1', fg='midnight blue', font=("Ebrima", 12),
                  command=lambda: self.create_new_task(
                      task_title_entry.get(),
                      task_description_text.get("1.0", tk.END).strip(),
                      assignee_combobox.get(),
                      project_combobox.get(),
                      start_date_calendar.get_date(),
                      end_date_calendar.get_date(),
                      priority_combobox.get(),
                      status_combobox.get(),
                      popup_window
                  )).pack(pady=10)

        tk.Label(popup_window, text="Enter Task Title to Delete:", bg='lightblue', fg='black', font=("Ebrima", 14)).pack(pady=5)
        delete_title_entry = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        delete_title_entry.pack(pady=5)
        tk.Button(popup_window, text="Delete Task", bg='DeepskyBlue1', fg='midnight blue', font=("Ebrima", 12),
                  command=lambda: self.delete_task(delete_title_entry.get(), popup_window)).pack(pady=10)

    def create_new_task(self, title, description, assignee, project, start_date, end_date, priority, status, popup_window):
        if title:
            # Create a new frame inside the scrollable task area for this task
            task_item_frame = tk.Frame(self.task_frame, bg="white", bd=1, relief="solid")
            task_item_frame.pack(fill="x", pady=2, padx=2)
            task_var = tk.BooleanVar()
            # Task title with a checkbox for completion
            task_checkbox = tk.Checkbutton(task_item_frame, text=title, variable=task_var, font=("Ebrima", 14), bg="white", command=lambda: self.update_progress())
            task_checkbox.pack(side="left", padx=5)
            # Display the task dates
            dates_label = tk.Label(task_item_frame, text=f"{start_date} to {end_date}", font=("Ebrima", 10), bg="white")
            dates_label.pack(side="left", padx=5)
            # Save task to MongoDB
            task_data = {
                "title": title,
                "description": description,
                "assignee": assignee,
                "project": project,
                "start_date": start_date,
                "end_date": end_date,
                "priority": priority,
                "status": status
            }
            self.tasks_collection.insert_one(task_data)
            # Store task widget and state for progress calculation
            self.tasks.append({"frame": task_item_frame, "var": task_var, "checkbox": task_checkbox})
            popup_window.destroy()
            messagebox.showinfo("Success", f"Task '{title}' created successfully!")
        else:
            messagebox.showwarning("No Title", "You must provide a task title.")

    def delete_task(self, title, popup_window):
        if title:
            task_found = False
            for task in self.tasks:
                if task["checkbox"].cget('text') == title:
                    task["frame"].destroy()
                    self.tasks.remove(task)
                    self.tasks_collection.delete_one({"title": title})
                    task_found = True
                    break
            if task_found:
                messagebox.showinfo("Success", f"Task '{title}' deleted successfully!")
            else:
                messagebox.showwarning("Not Found", f"Task '{title}' not found.")
            popup_window.destroy()
        else:
            messagebox.showwarning("No Title", "You must provide a task title to delete.")

    def update_progress(self):
        completed = sum(1 for task in self.tasks if task["var"].get())
        total = len(self.tasks)
        progress_percentage = (completed / total * 100) if total > 0 else 0
        self.progress_bar["value"] = progress_percentage

# ---------------------------- MAIN APPLICATION -------------------------------
root = Navigating()
root.wm_title("Management System")
root.state("zoomed")
root.geometry("1920x1080")
root.mainloop()
