#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk

class LoginForm(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.withdraw()     # hide until ready to show
        self.title("Login")
        self.usernameLabel = ttk.Label(self, text="Username:")
        self.usernameLabel.grid(row=0, column=0, sticky=tk.W, padx="0.75m", pady="0.75m")
        self.usernameEntry = ttk.Entry(self)
        self.usernameEntry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx="0.75m", pady="0.75m")
        self.passwordLabel = ttk.Label(self, text="Password:")
        self.passwordLabel.grid(row=1, column=0, sticky=tk.W, padx="0.75m", pady="0.75m")
        self.passwordEntry = ttk.Entry(self, show="*")
        self.passwordEntry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx="0.75m", pady="0.75m")
        self.loginButton = ttk.Button(self, text="Login")
        self.loginButton.grid(row=2, column=0, padx="0.75m", pady="0.75m")
        self.cancelButton = ttk.Button(self, text="Cancel")
        self.cancelButton.grid(row=2, column=1, padx="0.75m", pady="0.75m")
        self.bind("<Escape>", lambda *args: self.destroy())
        self.deiconify()    # show when widgets are created and laid out
        if self.winfo_viewable():
            self.transient(master)
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

if __name__ == "__main__":
    application = tk.Tk()
    window = LoginForm(application)
    application.protocol("WM_DELETE_WINDOW", application.quit)
    application.mainloop()
