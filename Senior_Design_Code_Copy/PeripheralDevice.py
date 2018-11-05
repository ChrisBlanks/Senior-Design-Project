"""
Programmer: Chris Blanks
Last Edited: 10/24/2018
Project: Automated Self-Serving System
Purpose: This script defines the Peripheral Device class.
"""


class PeripheralDevice:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.state = None
        self.buffer = None
        self.communication_method = None
        self.pin_number = None

    def reportStateToMainApp(self):
        pass

    def sendDataToMainApp(self):
        pass

    def startCommunication(self):
        pass

    def terminateCommunication(self):
        pass
