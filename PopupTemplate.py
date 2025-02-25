def popup1(self):
    popup_window = tk.Toplevel(self.master)  # Use the master or controller as the parent
    popup_window.title("Popup Window")
    popup_window.geometry("400x300")
    popup_window.configure(bg='midnight blue') # can be changed

    tk.Label(popup_window, text="This is a label:", bg='midnight blue', fg='white', font=("Ebrima", 14)).pack(pady=10) # Label for Entry
    Popup_Enter = tk.Entry(self,width=30,  font=("Ebrima", 12,'bold')).pack(pady=5) # Entry

    tk.Button(popup_window, text="Button", bg='white', fg='midnight blue', font=("Ebrima", 12),command=lambda: controller.show_frame()).pack(pady=20) # Put frame popup originated from here.