"""
Programmer: Chris Blanks
Last Edited: 11/3/2018
Project: Automated Self-Serving System
Purpose: This script defines the Drink Class.
"""


import tkinter as tk
from tkinter import messagebox
import os

class LoginWindow:

    #class member variables
    login_file_path = "/Users/Cabla/Documents/PYTHON_MODULES/SENIOR_DESIGN_CODE/system_info/user_login.txt"
    failed_attempt_limit = 3
    
    
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.main_app.master.withdraw()
        
        self.master = self.main_app.login_top_lvl
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        
        self.configureWindow()

        self.attempt_number = 1
        self.isAdminAccount = False
        self.isRegularUser = False

    def configureWindow(self):
        """Creates the login window."""
        self.master.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox)
        self.master.geometry("250x80")
        
        self.login_title= tk.Label(self.frame,text="Employee Login")
        
        self.username_label = tk.Label(self.frame,text="Username:",font=("Times","12","bold italic"))
        self.username_label.grid(row=1,column=1)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1,column=2)

        self.password_label = tk.Label(self.frame,text="Password:",font=("Times","12","bold italic"))
        self.password_label.grid(row=2,column=1)
        self.password_entry = tk.Entry(self.frame)
        self.password_entry.grid(row=2,column=2)

        self.login_btn = tk.Button(self.frame,text="Login",bg="green"
                                   ,fg="white",command= self.testUserLogin)
        self.login_btn.grid(row=1,column= 3,rowspan=2,columnspan=2,padx=3,sticky="nsew")
        #Put a logo under the pass label

    def testUserLogin(self):
        """Tests whether the user's login matches. Sends"""
        self.searchForLoginMatch()
        
        if self.main_app.isValidLogin:
            self.main_app.isEmployeeMode = True
            if self.isRegularUser == False:
                self.isAdminAccount = True      
            self.main_app.isValidLogin = False  #value rest
            self.master.destroy()
            self.main_app.createEmployeeWindow(self.isAdminAccount)
        else:
            
            print("Invalid credentials! ",self.failed_attempt_limit-self.attempt_number,
                  " attempt(s) left")
            self.attempt_number +=1
            
        if self.attempt_number > 3:
            self.main_app.isEmployeeMode = False
            self.main_app.writeToLog("Failed login")
            self.master.destroy()
            self.main_app.createCustomerWindow()
            self.main_app.master.deiconify()

    def searchForLoginMatch(self):
        """Searches for a matching user login."""

        username = self.username_entry.get()
        password = self.password_entry.get()
        
        file = open(self.login_file_path,'r+')
        lines = file.read().splitlines()

        for line in lines:
            if line.split()[0] == username and line.split()[1] == password:
                self.main_app.writeToLog(username + " logged in")
                self.main_app.isValidLogin = True
                break
            if line.split()[0] == "REGULAR" and line.split()[1] == "USERS":
                self.isRegularUser = True
                
        file.close()

    def deployExitMessageBox(self):
        if messagebox.askokcancel("Quit","Are you sure?"):
            self.master.destroy()
            self.main_app.master.deiconify()
