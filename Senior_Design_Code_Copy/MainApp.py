"""
Programmer: Chris Blanks
Last Edited: 11/3/2018
Project: Automated Self-Serving System
Purpose: This script defines the MainApp class that runs everything.
"""

#Standard library imports
import tkinter as tk
import os
import datetime

#My scripts
from CustomerWindow import CustomerWindow
from EmployeeWindow import EmployeeWindow
import DrinkProfile as dp_class
from LoginWindow import LoginWindow
from KeyboardWindow import KeyboardWindow


def runMainApplication():
    """Basic run of application."""
    root = tk.Tk()
    main_app = MainApp(master= root)
    root.mainloop()


class MainApp:

    #class member variables
    isEmployeeMode= False
    isValidLogin = False
    drink_profile_directory = "/Users/Cabla/Documents/PYTHON_MODULES/SENIOR_DESIGN_CODE/drink_profiles"
    config_file_path = "/Users/Cabla/Documents/PYTHON_MODULES/SENIOR_DESIGN_CODE/system_info/config.txt"
    drink_names = []
    
    def __init__(self,master):
        self.master = master
        self.writeToLog("Running main application")
        self.drink_objects = self.getDrinks()
        self.createMainWindow()
        self.selectWindow()
        
        self.retrieveConfigurationInformation()
        self.cleanOldDrinksFromConfig()


    def selectWindow(self):
        """Determines what window is open."""
        #input mode until GPIO pin is setup to trigger employee mode
        selection = int(input("Press 1 to enter employee mode."))

        if selection == 1:
            self.isEmployeeMode = True
            #self.launchKeyboardWindow()
            self.launchLoginWindow()           
        else:
            self.isEmployeeMode = False
            self.master.withdraw()
            self.createCustomerWindow()


    def createMainWindow(self):
        """Displays main window elements. """
        self.master.geometry("200x200")
        self.main_title = tk.Label(self.master,text="Root Window")
        self.main_title.grid()

        self.customer_window_btn = tk.Button(self.master,text="customer window"
                                             ,command= lambda window="customer": self.relaunchWindow(window))
        self.customer_window_btn.grid()
        self.employee_window_btn = tk.Button(self.master,text="employee window"
                                             ,command= lambda window="employee": self.relaunchWindow(window))
        self.employee_window_btn.grid()

        
    def relaunchWindow(self,window):
        """ Relaunches the selected window."""
        if window == "customer":
            self.isEmployeeMode = False
            self.master.withdraw()
            self.createCustomerWindow()
        elif window == "employee":
            self.isEmployeeMode = True
            self.master.withdraw()
            #self.launchKeyboardWindow()
            self.launchLoginWindow()
        else:
            print("What the heck?")

        
    def createCustomerWindow(self):
        """Creates separate customer window."""
        self.customer_top_lvl = tk.Toplevel(self.master)
        self.customer_window = CustomerWindow(self)

        
    def createEmployeeWindow(self,isAdminMode):
        """Creates separate employee window """
        self.employee_top_lvl = tk.Toplevel(self.master)
        self.employee_window = EmployeeWindow(self,isAdminMode)

    
    def launchLoginWindow(self):
        """Launches login window when employee mode is selected."""
        self.login_top_lvl = tk.Toplevel(self.master)
        self.login_window = LoginWindow(self)

        
    def launchKeyboardWindow(self):
        """Launches a top level window that contains a keyboard that can deliver
        input to processes that need it."""
        self.keyboard_top_lvl = tk.Toplevel(self.master)
        self.keyboard_window = KeyboardWindow(self)

        
    def getDrinks(self):
        """Retrieves a list of active Drink objects."""
        temp = []
        os.chdir(self.drink_profile_directory)
        drink_profile_names = os.listdir(os.getcwd())
        for name in drink_profile_names:
            path_builder = self.drink_profile_directory +"/"+ name
            os.chdir(path_builder)
            drink = dp_class.DrinkProfile(path_builder +"/"+ os.listdir(os.getcwd())[1])
            if drink.isActive == "1":
                drink.name = (drink.name).replace(" ","_")
                drink.addDrinkToConfig()
                temp.append(drink)
        #go back to SENIOR_DESIGN_CODE directory
        os.chdir("..")
        os.chdir("..")
        return temp


    def retrieveConfigurationInformation(self):
        """Retrieves configuration info (e.g. drink names) from config file """
        f = open(self.config_file_path,'r+')
        lines = f.read().splitlines()
        #print("'{}' contents:\n".format((f.name).split("/")[-1]),'\n'.join(lines))

        line_number = 1
        for line in lines:
            if line_number == 1:
                if line.split()[1] == '0':
                    print("Config file is not locked.\n\n")
                else:
                    self.isLocked = True
                    print("Config file is locked.\n\n")
            if line_number == 2:
                drinks = line.split(" ")
                for i in range(len(drinks)-1):
                    self.drink_names.append(drinks[i+1])
            line_number+=1        
        f.close()


    def updateConfigurationFile(self,item_to_update,updated_value= None):
        """ """
        f = open(self.config_file_path,"r+")
        lines = f.read().splitlines()
        f.seek(0)

        line_headers = ["locked ","active_drink_list ","system_status "]
        line_to_edit = 0
        
        if item_to_update == "data_lock":
            line_to_edit = 1
        if item_to_update == "drink_list":
            line_to_edit = 2
        if item_to_update == "system_status":
            line_to_edit = 3

        line_number = 1
        for line in lines:
            if line_number == line_to_edit and updated_value != None:
               line = line_headers[line_to_edit - 1] + updated_value
               f.write(line+"\n")
            else:
                f.write(line+"\n")
            if line_number == 3:
                break
            line_number+=1

        f.close()


    def cleanOldDrinksFromConfig(self):
        """Updates the active drinks in the config file."""
        cleaned_list_of_names = ""
        loaded_drink_object_names = []
        for drink in self.drink_objects:
            loaded_drink_object_names.append((drink.name).replace("_"," "))
        for config_name in self.drink_names:
            if config_name.replace("_"," ") in loaded_drink_object_names:
                cleaned_list_of_names = cleaned_list_of_names + config_name + " "
        self.updateConfigurationFile("drink_list",cleaned_list_of_names)
        self.writeToLog("Cleaned Config file.")
                
               
    def writeToLog(self, message):
        """Writes messages into the log.txt file."""
        self.todays_log = "system_info/log_files/log_on_"+str(datetime.date.today())+".txt"
        log = open(self.todays_log,"a")
        full_msg = str(datetime.datetime.now()) +" : " + message
        log.write(full_msg + "\n")
        log.close()

    
    def addUserToLogin(self,user_type,username,password):
        """Creates a new user in the user_login file. Ex: self.addUserToLogin("R","Lei","Zhang")"""
        file = open("system_info/user_login.txt","r+")
        lines = file.read().splitlines()
        file.seek(0)
        print(lines)
        line_num = 1
        if user_type == "A":
            for line in lines:
                if "ADMIN USER" in line:
                    line = line +"\n"+ username +" "+ password
                if "END" in line:
                    file.write(line)
                    print("END:" + line)
                    break
                file.write(line+"\n")
                print("Add lines: "+line)
        else:
            for line in lines:
                if "REGULAR USER" in line:
                    line = line +"\n"+ username +" "+ password
                if "END" in line:
                    file.write(line)
                    print(line)
                    break
                file.write(line+"\n")
                print(line)
        file.seek(0)
        print(file.readlines())
        file.flush()
        file.close()

        msg = "Added "+username+ "account to login."
        self.writeToLog(msg)        

    def deleteUserFromLogin(self, username, password):
        """Deletes a user in the user_login file (besides the original admin account)."""
        file = open("system_info/user_login.txt","r+")
        lines = file.read().splitlines()
        file.seek(0)
        print(lines)
        login_combo = username +" " + password
        for line in lines:
            if "END" in line:
                file.write("END")
                break
            if not login_combo in line:
                file.write(line+"\n")
                print("delete lines: "+line)
            else:
                pass
        file.truncate()
        file.flush()
        file.close()

        msg = "Removed "+username+ "account from login."
        self.writeToLog(msg)  

            
if __name__ == "__main__":
    runMainApplication()
