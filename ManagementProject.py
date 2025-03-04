import tkinter as tk
from tkinter import messagebox, ttk
import pymongo  # Database
from pymongo import MongoClient  # Database
import re   # Regular Expression to validate email
import tkcalendar  # For task and project deadlines
from tkcalendar import Calendar # For date picking in task management
from PIL import Image, ImageTk # For backgrounds of popups and frames.

client = MongoClient("mongodb://localhost:27017/")
db = client["Users"]
mycol = db['UserInfo']
projects_collection = db["projects"]
tasks_collection = db["tasks"]

# ---------------------------- IMPORTANT CLASS -------------------------------
class Navigating(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.wm_title("SysManage")

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

#---------------------------- TOOLTIP CLASS FOR TASKS ----------------------------
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # Create a new window for the tooltip
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Removes window decorations
        self.tooltip_window.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        # Tooltip content (task data)
        label = tk.Label(self.tooltip_window, text=self.text, font=("Ebrima", 10), bg="lightyellow", bd=1, relief="solid")
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()

def validate_login(email_entry, password_entry, controller):
    username = email_entry.get()
    password = password_entry.get()


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

        # Load background image
        self.bg_image = Image.open("tkinterbackground.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080))  # Adjust size if needed
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and set the image
        self.canvas = tk.Canvas(self, width=1920, height=1080)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.canvas.pack(fill="both", expand=True)

        # Add the title text to the canvas
        self.canvas.create_text(960, 50, text="SysManage", fill="White", font=("Ebrima", 48, "bold"), anchor="center")
        
        # Labels as text on the canvas
        self.canvas.create_text(725, 300, text="Enter Email:", fill="White", font=("Ebrima", 24, "bold"))
        self.canvas.create_text(700, 500, text="Enter Password:", fill="White", font=("Ebrima", 24, "bold"))

        self.LoginEmail = tk.Entry(self, width=45, font=("Ebrima", 13, "bold"))
        self.LoginPassword = tk.Entry(self, font=("Ebrima", 13, "bold"), width=45, show="*")

        self.show_password_button = tk.Button(self, text="👁", fg="white", bg="midnightblue", border=0, font=("Ebrima", 18), command=self.toggle_password)

        # Place entry fields and button on canvas as windows
        self.canvas.create_window(1050, 300, window=self.LoginEmail)
        self.canvas.create_window(1050, 500, window=self.LoginPassword)
        self.canvas.create_window(1350, 500, window=self.show_password_button)

        login_button = tk.Button(self, text="Login", fg="white", bg="midnightblue", font=("Ebrima", 18), height=1, command=lambda: validate_login(self.LoginEmail, self.LoginPassword, controller))
        signup_button = tk.Button(self, text="Sign up", fg="white", bg="midnightblue", font=("Ebrima", 18), height=1, command=lambda: controller.show_frame(SignUp))
        self.canvas.create_window(960, 600, window=login_button)
        self.canvas.create_window(960, 700, window=signup_button)

    def toggle_password(self):
        # Toggle password visibility
        if self.LoginPassword.cget('show') == '*':
            self.LoginPassword.config(show='')
        else:
            self.LoginPassword.config(show='*')


    def toggle_password(self):
        if self.LoginPassword.cget('show') == "*":
            self.LoginPassword.config(show="")
            self.show_password_button.config(text="👁")
        else:
            self.LoginPassword.config(show="*")
            self.show_password_button.config(text="👁")

# ---------------------------- SIGN UP PAGE ----------------------------
class SignUp(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller # Needed in order to automatically redirect user to login page after successful signup

        # Load background image
        self.bg_image = Image.open("tkinterbackground.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080))  # Adjust size if needed
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and set the image
        self.canvas = tk.Canvas(self, width=1920, height=1080)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.canvas.pack(fill="both", expand=True)

        # Add the title text to the canvas
        self.canvas.create_text(960, 50, text="Sign Up", fill="White", font=("Ebrima", 48, "bold"), anchor="center")
        
        # Labels as text on the canvas
        self.canvas.create_text(700, 200, text="Enter Email:", fill="White", font=("Ebrima", 24, "bold"))
        self.canvas.create_text(675, 400, text="Enter Password:", fill="White", font=("Ebrima", 24, "bold"))
        self.canvas.create_text(650, 600, text="Confirm Password:", fill="White", font=("Ebrima", 24, "bold"))
        
        self.SignUpEmail = tk.Entry(self, width=45, font=("Ebrima", 13, "bold"))
        self.SignUpPassword = tk.Entry(self, width=45, font=("Ebrima", 13, "bold"), show="*")
        self.SignUpConfirmPassword = tk.Entry(self, width=45, font=("Ebrima", 13, "bold"), show="*")
        
        self.show_password_button = tk.Button(self, text="👁", fg="white", bg="midnightblue", border=0, font=("Ebrima", 18), command=self.toggle_password)
        self.show_confirm_password_button = tk.Button(self, text="👁", fg="white", bg="midnightblue", border=0, font=("Ebrima", 18), command=self.toggle_confirm_password)
        
        # Place entry fields and buttons on canvas as windows
        self.canvas.create_window(1050, 200, window=self.SignUpEmail)
        self.canvas.create_window(1050, 400, window=self.SignUpPassword)
        self.canvas.create_window(1350, 400, window=self.show_password_button)
        self.canvas.create_window(1050, 600, window=self.SignUpConfirmPassword)
        self.canvas.create_window(1350, 600, window=self.show_confirm_password_button)
        
        signup_button = tk.Button(self, text="Sign Up", fg="white", bg="midnightblue", font=("Ebrima", 18), height=1, command=self.addUser)
        back_button = tk.Button(self, text="Back To Login", fg="white", bg="midnightblue", font=("Ebrima", 18), height=1, command=lambda: controller.show_frame(Login))
        
        self.canvas.create_window(960, 750, window=signup_button)
        self.canvas.create_window(960, 850, window=back_button)

    def toggle_password(self):
        if self.SignUpPassword.cget('show') == "*":
            self.SignUpPassword.config(show="")
            self.show_password_button.config(text="👁")
        else:
            self.SignUpPassword.config(show="*")
            self.show_password_button.config(text="👁")

    def toggle_confirm_password(self):
        if self.SignUpConfirmPassword.cget('show') == "*":
            self.SignUpConfirmPassword.config(show="")
            self.show_confirm_password_button.config(text="👁")
        else:
            self.SignUpConfirmPassword.config(show="*")
            self.show_confirm_password_button.config(text="👁")
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
                            NewUser = [{"Email": self.User, "Password": self.Pwd,"Admin":"No"}]
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

        # Load background image
        self.bg_image = Image.open("tkinterbackground.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080))  # Adjust size if needed
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and set the image
        self.canvas = tk.Canvas(self, width=1920, height=1080)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.canvas.pack(fill="both", expand=True)

        # Add the title text to the canvas
        self.canvas.create_text(960, 50, text="Homepage", fill="White", font=("Ebrima", 48, "bold"), anchor="center")
        
        # Logout button
        logout_button = tk.Button(self, text="Logout", fg="white", bg="midnightblue", font=("Ebrima", 18), command=lambda: controller.show_frame(Login))
        self.canvas.create_window(50, 25, window=logout_button)

        self.projects = []  
        self.filtered_projects = self.projects

       
        # Search bar and button
        self.search_entry = tk.Entry(self, width=20, font=("Ebrima", 18))
        self.canvas.create_window(1675, 30, window=self.search_entry)
        self.search_button = tk.Button(self, text="Search", fg="white", bg="midnightblue", font=("Ebrima", 18), command=self.filter_projects)
        self.canvas.create_window(1870, 30, window=self.search_button)

        # Project Listbox
        self.project_listbox = tk.Listbox(self, width=35, height=10, font=("Ebrima", 14))
        self.canvas.create_window(1725, 200, window=self.project_listbox)
        self.update_project_listbox()

        # Bind selection event
        self.project_listbox.bind("<<ListboxSelect>>", self.on_select)

        # Create project button
        self.createProjectButton = tk.Button(self, text="Create New Project", fg="white", bg="midnightblue", font=("Ebrima", 18, "bold"), command=self.popup1)
        self.canvas.create_window(960, 150, window=self.createProjectButton)


    def get_projects_from_db(self):
        """Fetch the projects from MongoDB."""
        projects_cursor = projects_collection.find() 
        projects = list(projects_cursor)  
        return projects

    def save_project_to_db(self, project):
        """Save the new project to MongoDB."""
        # Insert the new project into the MongoDB collection
        projects_collection.insert_one(project)
        print(f"Project '{project['name']}' saved to database.")
    

    def on_select(self, event):
        """Open the selected project when clicked."""
        selected_index = self.project_listbox.curselection()
        if selected_index:
            selected_project = self.project_listbox.get(selected_index[0])  
            print(f"Selected Project: {selected_project}")  
            self.controller.show_frame(Project)  # Open project page

    def update_project_listbox(self):
        """Update the project list based on search results from MongoDB."""
        self.project_listbox.delete(0, tk.END)
        # Retrieve projects from MongoDB
        projects = self.get_projects_from_db()
        self.projects = projects  
        for project in self.projects:
            self.project_listbox.insert(tk.END, project['name'])

    def filter_projects(self):
        """Filter the project list based on search input."""
        search_term = self.search_entry.get().lower()
        filtered_projects = [p for p in self.projects if search_term in p['name'].lower()]
        self.filtered_projects = filtered_projects
        self.update_project_listbox()


    def popup1(self):
        popup_window = tk.Toplevel()
        popup_window.title("Project Management")
        popup_window.geometry("600x400")

        # Load background image
        bg_image = Image.open("tkinterbackground.jpg")
        bg_image = bg_image.resize((600, 400))  # Adjust size if needed
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a canvas and set the image
        canvas = tk.Canvas(popup_window, width=600, height=400)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.pack(fill="both", expand=True)
        popup_window.bg_photo = bg_photo  # Keep reference to avoid garbage collection

        # Title
        canvas.create_text(300, 40, text="Project Management", fill="White", font=("Ebrima", 20, "bold"))

        # Create project section
        canvas.create_text(300, 100, text="Enter Project Name:", fill="White", font=("Ebrima", 14))
        Popup_Enter = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        create_project_button = tk.Button(popup_window, text="Create Project", bg='midnightblue', fg='white', font=("Ebrima", 12),
                                          command=lambda: self.create_new_project(Popup_Enter.get(), popup_window))
        
        canvas.create_window(300, 130, window=Popup_Enter)
        canvas.create_window(300, 170, window=create_project_button)

        # Delete project section
        canvas.create_text(300, 220, text="Enter Project Name to Delete:", fill="White", font=("Ebrima", 14))
        delete_project_entry = tk.Entry(popup_window, width=30, font=("Ebrima", 12, 'bold'))
        delete_project_button = tk.Button(popup_window, text="Delete Project", bg='midnightblue', fg='white', font=("Ebrima", 12),
                                          command=lambda: self.delete_project(delete_project_entry.get(), popup_window))
        
        canvas.create_window(300, 250, window=delete_project_entry)
        canvas.create_window(300, 290, window=delete_project_button)

    def create_new_project(self, project_name, popup_window):
        if project_name:
            new_project = {
                "name": project_name
            }
            # Store the project in MongoDB
            self.save_project_to_db(new_project)

            # Create a new frame inside the project area for this project
            new_project_button = tk.Button(self, text=project_name, fg="white", bg="midnightblue", font=("Ebrima", 20, "bold"), command=lambda: self.controller.show_frame(Project)) 

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
            popup_window.destroy()
            messagebox.showinfo("Success", f"Project '{project_name}' created successfully!")
        else:
            messagebox.showwarning("No Name", "You must provide a project name.")


    def delete_project(self, project_name, popup_window):
        if project_name:
            # Delete project from MongoDB
            self.delete_project_from_db(project_name)
            
            # Remove project button
            for widget in self.winfo_children():
                if isinstance(widget, tk.Button) and widget.cget("text") == project_name:
                    widget.destroy()
                    break
            
            messagebox.showinfo("Success", f"Project '{project_name}' deleted successfully!")
            popup_window.destroy()
        else:
            messagebox.showwarning("No Name", "You must provide a project name to delete.")

# ---------------------------- PROJECT PAGE (Task Management) ----------------------------
class Project(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        # Load background image
        self.bg_image = Image.open("tkinterbackground.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and set the image
        self.canvas = tk.Canvas(self, width=1920, height=1080)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.canvas.pack(fill="both", expand=True)

        # Title
        self.canvas.create_text(960, 50, text="Project Area", fill="White", font=("Ebrima", 48, "bold"), anchor="center")

        # Progress Bar
        self.canvas.create_text(800, 150, text="Progress:", fill="White", font=("Ebrima", 18))
        self.progress_bar = ttk.Progressbar(self, length=300, mode="determinate", maximum=100)
        self.canvas.create_window(1100, 150, window=self.progress_bar)

        # "Add Task" Button
        self.create_task_button = tk.Button(self, text="Add Task", fg="white", bg="midnightblue", font=("Ebrima", 24, "bold"), command=self.popup_task)
        self.canvas.create_window(800, 250, window=self.create_task_button)

        self.delete_task_button = tk.Button(self, text="Delete Task", fg="white", bg="midnightblue", font=("Ebrima", 24, "bold"), command=self.popup_delete)
        self.canvas.create_window(1100, 250, window=self.delete_task_button)

        # Scrollable task area
        self.task_canvas = tk.Canvas(self, bg="midnightblue", width=800, height=400)
        self.task_scroll = ttk.Scrollbar(self, orient="vertical", command=self.task_canvas.yview)
        self.task_canvas.configure(yscrollcommand=self.task_scroll.set)
        self.task_frame = tk.Frame(self.task_canvas, bg="midnightblue")
        self.task_canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.task_frame.bind("<Configure>", lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))

        self.canvas.create_window(960, 500, window=self.task_canvas)
        self.canvas.create_window(1370, 500, window=self.task_scroll)

        # Home Button
        self.homeButton = tk.Button(self, text="Home", fg="gold", bg="red4", font=("Ebrima", 14, "bold"), command=lambda: controller.show_frame(Homepage))
        self.canvas.create_window(37, 24, window=self.homeButton)

        self.tasks = []

    def popup_task(self):
        popup_window = tk.Toplevel()
        popup_window.title("Create A Task")
        popup_window.geometry("800x750")
        
        # Load and set background image
        bg_image = Image.open("tkinterbackground.jpg")
        bg_image = bg_image.resize((800, 750))
        bg_photo = ImageTk.PhotoImage(bg_image)

        canvas = tk.Canvas(popup_window, width=800, height=750)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.pack(fill="both", expand=True)
        popup_window.bg_photo = bg_photo

        # Task Title
        canvas.create_text(400, 50, text="Task Title:", fill="white", font=("Ebrima", 14))
        task_title_entry = tk.Entry(popup_window, width=40, font=("Ebrima", 12, 'bold'))
        canvas.create_window(400, 80, window=task_title_entry)

        # Task Description
        canvas.create_text(400, 130, text="Task Description:", fill="white", font=("Ebrima", 14))
        task_description_entry = tk.Entry(popup_window, width=40, font=("Ebrima", 12, 'bold'))
        canvas.create_window(400, 160, window=task_description_entry)

        # Assign to Team Member
        canvas.create_text(400, 200, text="Assign to Team Member:", fill="white", font=("Ebrima", 14))
        team_members = ["Alice", "Bob", "Charlie"]  # Example team members
        assignee_combobox = ttk.Combobox(popup_window, font=("Ebrima", 12), values=team_members)
        assignee_combobox.set("Select Member")  # Set default text
        canvas.create_window(400, 230, window=assignee_combobox)

        # Assign to Project
        canvas.create_text(400, 270, text="Assign to Project:", fill="white", font=("Ebrima", 14))
        project_combobox = ttk.Combobox(popup_window, font=("Ebrima", 12), values=["No projects available"])
        project_combobox.set("Select Project")
        canvas.create_window(400, 300, window=project_combobox)

        # Start Date
        canvas.create_text(215, 325, text="Start Date:", fill="white", font=("Ebrima", 14))
        start_date_calendar = Calendar(popup_window, selectmode='day')
        canvas.create_window(200, 430, window=start_date_calendar)

        # End Date
        canvas.create_text(605, 325, text="End Date:", fill="white", font=("Ebrima", 14))
        end_date_calendar = Calendar(popup_window, selectmode='day')
        canvas.create_window(600, 430, window=end_date_calendar)

        # Priority Level
        canvas.create_text(400, 530, text="Priority Level:", fill="white", font=("Ebrima", 14))
        priority_combobox = ttk.Combobox(popup_window, values=["Low", "Medium", "High"], font=("Ebrima", 12))
        canvas.create_window(400, 560, window=priority_combobox)

        # Completion Status
        canvas.create_text(400, 600, text="Completion Status:", fill="white", font=("Ebrima", 14))
        status_combobox = ttk.Combobox(popup_window, values=["In-Progress", "Completed"], font=("Ebrima", 12))
        canvas.create_window(400, 630, window=status_combobox)

        # Assign Task Button
        assign_button = tk.Button(popup_window, text="Assign Task", bg='gold', fg='black', font=("Ebrima", 12, 'bold'), command=lambda: self.create_new_task(
            task_title_entry.get(),
            task_description_entry.get(),
            assignee_combobox.get(),
            project_combobox.get(),
            start_date_calendar.get_date(),
            end_date_calendar.get_date(),
            priority_combobox.get(),
            status_combobox.get(),
            popup_window
        ))
        canvas.create_window(400, 670, window=assign_button)

    def popup_delete(self):
        delete_window = tk.Toplevel()
        delete_window.title("Delete a Task")
        delete_window.geometry("600x400")

        # Load background image
        bg_image = Image.open("tkinterbackground.jpg")
        bg_image = bg_image.resize((600, 400))  # Adjust size if needed
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a canvas and set the image
        canvas = tk.Canvas(delete_window, width=600, height=400)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.pack(fill="both", expand=True)
        delete_window.bg_photo = bg_photo  # Keep reference to avoid garbage collection

        # Title
        canvas.create_text(300, 40, text="Delete a Task", fill="White", font=("Ebrima", 20, "bold"))

        # Create project section
        canvas.create_text(300, 100, text="Enter task Name:", fill="White", font=("Ebrima", 14))
        Delete_Enter = tk.Entry(delete_window, width=30, font=("Ebrima", 12, 'bold'))
        create_project_button = tk.Button(delete_window, text="Delete Task", bg='midnightblue', fg='white', font=("Ebrima", 12), command=lambda: self.delete_task(Delete_Enter.get(), delete_window))
        
        canvas.create_window(300, 130, window=Delete_Enter)
        canvas.create_window(300, 170, window=create_project_button)



    def create_new_task(self, title, description, assignee, project, start_date, end_date, priority, status, popup_window):
        if title:
            task_data = { # For MongoDB
                "title": title,
                "description": description,
                "assignee": assignee,
                "project": project,
                "start_date": start_date,
                "end_date": end_date,
                "priority": priority,
                "status": status
            }
            # Save task to MongoDB
            self.save_task_to_db(task_data)

            # Create a new frame inside the task area for this task
            task_item_frame = tk.Frame(self.task_frame, bg="white", bd=1, relief="solid")
            task_item_frame.pack(fill="x", pady=2, padx=2)

            task_var = tk.BooleanVar()  # Created a BooleanVar for the task completion

            task_checkbox = tk.Checkbutton(
                task_item_frame, text=title, variable=task_var, font=("Ebrima", 14),
                bg="white", command=self.update_progress  # Ensure this updates progress
            )
            task_checkbox.pack(side="left", padx=5)

            # Display the task dates
            dates_label = tk.Label(task_item_frame, text=f"{start_date} to {end_date}", font=("Ebrima", 10), bg="white")
            dates_label.pack(side="left", padx=5)

            tooltip_text = f"Title: {title}\nDescription: {description}\nAssignee: {assignee}\nProject: {project}\nStart Date: {start_date}\nEnd Date: {end_date}\nPriority: {priority}\nStatus: {status}"

            # Attach the tooltip to the task item frame
            Tooltip(task_item_frame, tooltip_text)

            # Store task data in a list
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
        completed = sum(1 for task in self.tasks if task["var"].get())  # Count checked tasks
        total = len(self.tasks)
        progress_percentage = (completed / total * 100) if total > 0 else 0
        self.progress_bar["value"] = progress_percentage

    def popup_edit(self, task):
        # Create the edit window (popup)
        edit_window = tk.Toplevel()
        edit_window.title("Edit Task")
        edit_window.geometry("800x750")

        # Load and set background image for the popup
        bg_image = Image.open("tkinterbackground.jpg")
        bg_image = bg_image.resize((800, 750))
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        canvas = tk.Canvas(edit_window, width=800, height=750)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.pack(fill="both", expand=True)
        edit_window.bg_photo = bg_photo

        canvas.create_text(400, 10, text="Task you wish to edit:", fill="white", font=("Ebrima", 14))
        first_title_entry = tk.Entry(edit_window, width=40, font=("Ebrima", 12, 'bold'))  
        canvas.create_window(400, 30, window=first_title_entry)

        # Task Title
        canvas.create_text(400, 50, text="Task Title:", fill="white", font=("Ebrima", 14))
        task_title_entry = tk.Entry(edit_window, width=40, font=("Ebrima", 12, 'bold'))  
        canvas.create_window(400, 80, window=task_title_entry)

        # Task Description
        canvas.create_text(400, 130, text="Task Description:", fill="white", font=("Ebrima", 14))
        task_description_entry = tk.Entry(edit_window, width=40, font=("Ebrima", 12, 'bold'))
        canvas.create_window(400, 160, window=task_description_entry)

        # Assign to Team Member
        canvas.create_text(400, 200, text="Assign to Team Member:", fill="white", font=("Ebrima", 14))
        team_members = ["Alice", "Bob", "Charlie"]  # Example team members
        assignee_combobox = ttk.Combobox(edit_window, font=("Ebrima", 12), values=team_members)
        canvas.create_window(400, 230, window=assignee_combobox)

        # Assign to Project
        canvas.create_text(400, 270, text="Assign to Project:", fill="white", font=("Ebrima", 14))
        project_combobox = ttk.Combobox(edit_window, font=("Ebrima", 12), values=["No projects available"])
        canvas.create_window(400, 300, window=project_combobox)

        # Start Date
        canvas.create_text(215, 325, text="Start Date:", fill="white", font=("Ebrima", 14))
        start_date_calendar = Calendar(edit_window, selectmode='day')
        canvas.create_window(200, 430, window=start_date_calendar)

        # End Date
        canvas.create_text(605, 325, text="End Date:", fill="white", font=("Ebrima", 14))
        end_date_calendar = Calendar(edit_window, selectmode='day')
        canvas.create_window(600, 430, window=end_date_calendar)

        # Priority Level
        canvas.create_text(400, 530, text="Priority Level:", fill="white", font=("Ebrima", 14))
        priority_combobox = ttk.Combobox(edit_window, values=["Low", "Medium", "High"], font=("Ebrima", 12))
        canvas.create_window(400, 560, window=priority_combobox)

        # Completion Status
        canvas.create_text(400, 600, text="Completion Status:", fill="white", font=("Ebrima", 14))
        status_combobox = ttk.Combobox(edit_window, values=["In-Progress", "Completed"], font=("Ebrima", 12))
        canvas.create_window(400, 630, window=status_combobox)

        # Save changes button
        save_button = tk.Button(edit_window, text="Save Changes", bg='gold', fg='black', font=("Ebrima", 12, 'bold'),
                                command=lambda: self.save_task_changes(task, first_title_entry.get(), task_title_entry.get(), task_description_entry.get(),
                                                                        assignee_combobox.get(), project_combobox.get(),
                                                                        start_date_calendar.get_date(), end_date_calendar.get_date(),
                                                                        priority_combobox.get(), status_combobox.get(), edit_window))
        canvas.create_window(400, 670, window=save_button)


    def save_task_changes(self, task, first_title, title, description, assignee, project, start_date, end_date, priority, status, edit_window):
        if title:
            task_found = False
            # Deleting the old task
            for existing_task in self.tasks:
                if existing_task["checkbox"].cget('text') == first_title:  # Compare with the initial title
                    existing_task["frame"].destroy()
                    self.tasks.remove(existing_task)
                    task_found = True
                    break

            if task_found:
                messagebox.showinfo("Success", f"Task '{first_title}' changed successfully!")
            else:
                messagebox.showwarning("Not Found", f"Task '{first_title}' not found.")
        else:
            messagebox.showwarning("No Title", "You must provide a task title to delete.")

        if title:  # If title is provided, save the new task
            task_data = {  # For MongoDB
                "title": title,
                "description": description,
                "assignee": assignee,
                "project": project,
                "start_date": start_date,
                "end_date": end_date,
                "priority": priority,
                "status": status
            }

            # Create a new frame inside the scrollable task area for this task
            task_item_frame = tk.Frame(self.task_frame, bg="white", bd=1, relief="solid")
            task_item_frame.pack(fill="x", pady=2, padx=2)

            task_var = tk.BooleanVar()  # Created a BooleanVar for the task completion

            task_checkbox = tk.Checkbutton(
                task_item_frame, text=title, variable=task_var, font=("Ebrima", 14),
                bg="white", command=self.update_progress  # Ensure this updates progress
            )
            task_checkbox.pack(side="left", padx=5)

            # Display the task dates
            dates_label = tk.Label(task_item_frame, text=f"{start_date} to {end_date}", font=("Ebrima", 10), bg="white")
            dates_label.pack(side="left", padx=5)

            tooltip_text = f"Title: {title}\nDescription: {description}\nAssignee: {assignee}\nProject: {project}\nStart Date: {start_date}\nEnd Date: {end_date}\nPriority: {priority}\nStatus: {status}"

            # Attach the tooltip to the task item frame
            Tooltip(task_item_frame, tooltip_text)

            # Store task data in a list
            self.tasks.append({"frame": task_item_frame, "var": task_var, "checkbox": task_checkbox})

            # Add an edit button to the task frame
            task_edit_button = tk.Button(task_item_frame, text="Edit", fg="white", bg="midnightblue", font=("Ebrima", 12, "bold"), command=lambda: self.popup_edit(title))
            task_edit_button.pack(side="right", padx=5)

            edit_window.destroy()
            messagebox.showinfo("Success", f"Task '{title}' is the new name of '{first_title}'!")
        else:
            messagebox.showwarning("No Title", "You must provide a task title.")

# ---------------------------- MAIN APPLICATION -------------------------------
root = Navigating()
root.wm_title("SysManage")
root.state("zoomed")
root.geometry("1920x1080")
root.mainloop()