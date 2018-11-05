"""
Programmer: Chris Blanks
Last Edited: 11/3/2018
Project: Automated Self-Serving System
Purpose: This script defines the CustomerWindow Class.
"""

import tkinter as tk
from tkinter import messagebox

#my scripts
from AppWindow import AppWindow

class CustomerWindow(AppWindow):
    
    operation_instructions_file_path = """/Users/Cabla/Documents/PYTHON_MODULES/SENIOR_DESIGN_CODE/system_info/instructions_4_customer.txt"""
    
    def __init__(self,main_app_instance):
        AppWindow.__init__(self)
        
        self.main_app = main_app_instance
        self.master = self.main_app.customer_top_lvl
        
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        self.parent_menu = tk.Menu(self.frame)
        self.master.config(menu= self.parent_menu)
        
        self.configureWindow()
        
        self.displayDrinkOptionsInGUI() #Method from AppWindow
        self.createHelpMenu()
        

    def configureWindow(self):
        """Sets window geometry and limits."""
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth()
                                                  ,self.master.winfo_screenheight()))
        self.master.resizable(width=False, height=False)
        self.master.overrideredirect(True) #no window options (e.g. resizing)
        self.master.protocol("WM_DELETE_WINDOW",self.deployExitMessageBox) #ALT + F4 will triger this

        
    def deployExitMessageBox(self):
        if messagebox.askokcancel("Quit","Are you sure?"):
            self.master.destroy()
            self.main_app.master.deiconify()

