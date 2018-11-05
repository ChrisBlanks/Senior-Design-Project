"""
Programmer: Chris Blanks
Last Edited: 11/3/2018
Project: Automated Self-Serving System
Purpose: This script defines the EmployeeWindow Class.
"""

import tkinter as tk
from tkinter import messagebox

from AppWindow import AppWindow

class EmployeeWindow(AppWindow):
    
    operation_instructions_file_path = """/Users/Cabla/Documents/PYTHON_MODULES/SENIOR_DESIGN_CODE/system_info/instructions_4_employee.txt"""

    def __init__(self,main_app_instance, isAdminMode = False):
        AppWindow.__init__(self)
        
        self.master = main_app_instance.employee_top_lvl
        self.frame = tk.Frame(self.master)
        self.parent_menu = tk.Menu(self.frame)
        self.master.config(menu= self.parent_menu)
        self.main_app = main_app_instance
        
        self.isAdminMode = isAdminMode

        self.configureWindow()
        self.frame.grid()
        
        self.createHelpMenu()
        self.displayDrinkOptionsInGUI() #Method from AppWindow

        
    def configureWindow(self):
        """Sets window geometry and limits."""
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth()
                                                  ,self.master.winfo_screenheight()))   
        self.master.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox)

        if self.isAdminMode:
            self.setupAdminMenuBar()
        else:
            self.setupOptionsMenuBar()


    def setupAdminMenuBar(self):
        """Provides extra features in the menu bar for full control of the app."""
        print("Admin status.")
        self.setupOptionsMenuBar()

        self.admin_menu = tk.Menu(self.parent_menu,tearoff=0)
        self.parent_menu.add_cascade(label="Admin Options",menu=self.admin_menu)
        
        self.admin_menu.add_command(label="Launch Drink Profile Manager",command= self.createDrinkProfileManager)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Display Log" ,command= self.displayLogFile) #allow option to delete them
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Edit Configuration" ,command= self.editConfigFile)
        self.admin_menu.add_separator()
        self.admin_menu.add_command(label="Edit User Logins" ,command= self.editUserLogins)

    
    def setupOptionsMenuBar(self):
        """Provides regular features in the menu bar for employees"""
        print("Employee status.")
        self.options_menu = tk.Menu(self.parent_menu,tearoff=0)
        self.parent_menu.add_cascade(label="Employee Options",menu= self.options_menu)

        self.options_menu.add_command(label="Launch Drink Profile Manager" ,command= self.createDrinkProfileManager)


    def createDrinkProfileManager(self):
        """Allows the employee to add, edit, or delete drink profiles."""
        if self.isAdminMode:
            pass #put in a button for deleting drink profiles plus the add and edit
            #should update config file here
        else:
            pass #put in buttons for adding and editing drink profiles

    
    def displayLogFile(self):
        """Displays the most recent log file."""
        file = open(self.main_app.todays_log,'r')
        lines = file.readlines()
        file.close()
        msg = " ".join(lines)
        
        top = tk.Toplevel()
        top.title("Current Log File:")
        #top.geometry("350x230")

        scroll = tk.Scrollbar(top,orient= tk.VERTICAL)
        scroll.grid(row=0,column=1,sticky="ns")
        
        canvas = tk.Canvas(top,width=600,
                           height=500,
                           scrollregion=(0,0,2000,2000))
        canvas.grid(row=0,column=0,sticky="nsew")

        scroll.config(command=canvas.yview)
        canvas.config(yscrollcommand = scroll.set)
        canvas.create_text((0,0),text=msg,anchor="nw") #top left and anchored to the right

        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
    

    def editConfigFile(self):
        """Allows editing of the contents in the configuration file. """
        pass #Will be defined at a later time

    
    def editUserLogins(self):
        """Displays current registered users. Allows for adding or deleting users."""
        pass

    
    def deployExitMessageBox(self):
        if messagebox.askokcancel("Quit","Are you sure?"):
            self.isAdminMode = False
            self.master.destroy()
            self.main_app.master.deiconify()
