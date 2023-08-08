#IMPORTS
import os,sys                                                                  # Provides a way of using operating system dependent functionality
import sqlite3                                                                 # Imports all sqlite functions
from sqlite3 import Error                                                      # Imports the Error function so I can see what errors I may encounter
from PyQt5 import QtCore, QtGui, uic                                           # Imports necessary QUI library in order to interact with GUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets #, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests

#CLASSES
class CreateDatabase():
    def __init__ (self, db_file):
        self.db_file = open(r"D:\MY folder\hotelDB.db") # Address of DB file
        
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return -> void
        """
  
        conn = None
        try:                                #In case error occurs, catch it within the try except block
            conn = sqlite3.connect(db_file) #connect() function opens a connection to SQLite database
            return conn                     
        except Error as e:                  #Catches any errors and displays them
            print(e)
    
    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return -> void
        """
        try:
            c = conn.cursor()           #Allows python to execute SQL statments
            c.execute(create_table_sql) #Will create a table in SQL
        except Error as e:              #Catches any errors and displays them
            print(e)
    
    def main(self):
        """ creates the table using SQL statements and create_table procedure
        :return -> void
        """
        database = r"D:\MY folder\hotelDB.db" #Holds the address of the database file to be used
        # SQL statement for USERS table
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS USERS ( 
                                     id integer PRIMARY KEY,
                                     first_name text NOT NULL,
                                     last_name text NOT NULL,
                                     email text NOT NULL,
                                     gender text NOT NULL,
                                     password text NOT NULL
                                    ); """
        
        # SQL statement for linking table, USER_BOOKINGS
        sql_create_user_bookings_table = """CREATE TABLE IF NOT EXISTS USER_BOOKINGS (
                                            id integer PRIMARY KEY,
                                            hotel_name text PRIMARY KEY,
                                            reservation_date text NOT NULL PRIMARY KEY,
                                            FOREIGN KEY (id) REFERENCES USERS(id)
                                            FOREIGN KEY (hotel_name) REFERENCES HOTELS(hotel_name)
                                            UNIQUE (id, hotel_name)
                                          );"""
    
        # SQL statement for HOTELS table
        sql_create_hotels_table = """CREATE TABLE IF NOT EXISTS HOTELS (
                                     hotel_name text PRIMARY KEY,
                                     wifi integer NOT NULL,
                                     room_service integer NOT NULL,
                                     pets integer NOT NULL
                                    );"""
    
        conn = self.create_connection(database) # creates a connection to the database
        # create tables
        if conn is not None: #Checks if there is a connection to a database
            # create projects table
            self.create_table(conn, sql_create_users_table)

            # create tasks table
            self.create_table(conn, sql_create_user_bookings_table)
        
            # create hotels table
            self.create_table(conn, sql_create_hotels_table)
            
            conn.close() # closes the database after the operations are made
           
        else: #If there is no connection to the database it prints an error message
            print("Error! cannot create the database connection.")
        
db = CreateDatabase(None) # Creates the object for the class
db.main()                 # Runs the main() function from the class which creates the database


# WINDOWS

window1 = uic.loadUiType("login_window.ui")[0]
window2 = uic.loadUiType("signup_window.ui")[0]
window3 = uic.loadUiType("main_window.ui")[0]
window4 = uic.loadUiType("montcalm_gui.ui")[0]
window5 = uic.loadUiType("graph.ui")[0]
window6 = uic.loadUiType("helpmenu.ui")[0]
window7 = uic.loadUiType("travelodge_gui.ui")[0]
window8 = uic.loadUiType("parkgrand_gui.ui")[0]
window9 = uic.loadUiType("canopy_gui.ui")[0]
window10 = uic.loadUiType("residentcovent_gui.ui")[0]
#GLOBAL VARIABLES
email = ""



#CLASSES FOR THE WINDOWS

class Login(QtWidgets.QMainWindow, window1):
    def __init__(self,email, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # Set title 
        self.setWindowTitle('Login Window')
        
        # Sets fixed window size
        self.setFixedWidth(480)
        self.setFixedHeight(620)
        
        # Connects button to its function
        self.loginButton.clicked.connect(self.loginfunction)
        self.signupHereButton.clicked.connect(self.gotocreate)
        
        # Makes the password hidden
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
        
    def loginfunction(self):
        '''Validates whether the email and password inputted match and are correct
           return -> void '''
        global email
        email = self.email_field.text() # Creates variable for email inputted in textbox to be fetched and operated on - aouldcott0@telegraph.co.uk 
        password = self.password_field.text() # Creates variable for password inputted in textbox to be fetched and operated on - XO3KbG9
        if len(email) == 0 or len(password) == 0: # Checks if usernames or password is left blank
            self.login_text.setText("Please input all fields") # Outputs a message into GUI notifying the user of the error    
        else: # Runs the else condition which is if the text boxes are not empty
            if any(char in "\"'`;&<>”‘’" for char in email) or any(char in "\"'`;&<>”‘’" for char in password): # Checking for special characters in email and password
                self.login_text.setText("Invalid characters used in email or password") # Outputs a message notifying user has used invalid characters
                return # Exiting the function early if invalid characters are used
            conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
            cur = conn.cursor() # Creates a cursor object to execute the SQL statements
            query = 'SELECT password FROM USERS WHERE email = \''+email+"\'" # SQL statement to be executed when finding password for matching email                                                                       
            cur.execute(query) # Executes the query
            result_pass = cur.fetchone() # Retrieves the first row of the query result and assigns the first column (password) to result_pass 
            if result_pass is None: # Checks if the email does not exist
                self.login_text.setText("Email has not been registered") # Outputs a message that the email not found in the database
            elif result_pass[0] == password: # Checks if the password of the email is the same as the password inputted
                self.login_text.setText("Successfully logged in") # Outputs a message saying user is logged in
                w1.hide(), w3.show() # Hides the login window and displays the main window
                self.email_field.setText("") # Clears the email field
                self.password_field.setText("") # Clears the password field
                self.login_text.setText("")
            else: # Runs the else condition which is if the password doesn't match
                self.login_text.setText("Incorrect username or password") # Outputs that the user has entered the incorrect password
                
    def gotocreate(self):
        '''Opens the create account window'''
        w1.hide(), w2.show() # Shows Signup window and hides login window
             
                
class SignUp(QtWidgets.QMainWindow, window2):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # Set title 
        self.setWindowTitle('Signup Window')
        
        # Connects button to its function
        self.signupButton.clicked.connect(self.signupfunction)
        self.backButton.clicked.connect(self.backtologin)
        
        # Sets fixed window size
        self.setFixedWidth(480)
        self.setFixedHeight(620)
        
        # Makes the password hidden
        self.passwordSignup_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPass_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
    def signupfunction(self):
        '''Creates an account for the user and inserts it into the database
           return -> void'''
        email = self.usernameSignUp_field.text() # Creates variable for email inputted in textbox to be fetched and operated on
        password = self.passwordSignup_field.text() # Creates variable for password inputted in textbox to be fetched and operated on
        confirmPassword = self.confirmPass_field.text() # Creates variable for password inputted in textbox to be fetched and operated on
        if len(email) == 0 or len(password) == 0 or len(confirmPassword) == 0:
            self.signup_text.setText("Please input all fields") # Outputs a message into GUI to notify user to input all fields
        else: # Runs the code if all text fields are inputted
            if any(char in "\"'`;&<>”‘’" for char in email) or any(char in "\"'`;&<>”‘’" for char in password) or any(char in "\"'`;&<>”‘’" for char in confirmPassword): # Checking for special characters in email and password
                self.signup_text.setText("Invalid characters used in email or password") # Outputs a message notifying user has used invalid characters
                return # Exiting the function early if invalid characters are used
            if password != confirmPassword: # Compares password and confirm password box
                self.signup_text.setText("Passwords do not match") # If they do not match outputs a message
                return # Breaks code here
            conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
            cur = conn.cursor() # Creates a cursor object to execute the SQL statements
            checkQuery = 'SELECT email FROM USERS WHERE email=?' # SQL query to check for existing emails
            cur.execute(checkQuery, (email,)) # Executes the query
            if cur.fetchone(): # If email is found runs if condition
                self.signup_text.setText("Email already exists, please use a different one") # Outputs a message saying email already exists
                return # Breaks code here
            query = 'INSERT INTO USERS (email,password) VALUES (?,?)' # SQL statement to insert email and password into the DB
            cur.execute(query, (email, password)) # Executing the query and passing email and password as tuple
            conn.commit() # Committing the changes to the database
            self.signup_text.setText("Account successfully registered") # Outputting a message telling user account has been registered
            w2.hide(), w1.show()
            
    def backtologin(self):
        '''Goes back to the login window'''
        w2.hide(), w1.show() # Shows Login window and hides Signup window
        

class MainWindow(QtWidgets.QMainWindow, window3):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        loadUi("main_window.ui", self) # Loads to GUI file to operate on
       
        # Set title 
        self.setWindowTitle('Main Window')
        
        # Initialising the table
        self.hoteltable()
        self.tableWidget.clicked.connect(self.openhotel)
        self.tableWidget.setColumnWidth(0, 600)
        # Connecting buttons to their functions
        self.searchButton.clicked.connect(self.searchfunction)
        self.wifiButton.clicked.connect(self.wififilter)
        self.roomserviceButton.clicked.connect(self.roomservicefilter)
        self.petsButton.clicked.connect(self.petsfilter)
        self.clearsearchButton.clicked.connect(self.clearsearchfunction)
        self.helpButton.clicked.connect(self.showhelp)
        self.logoutButton.clicked.connect(self.logoutfunction)
        self.recommendationsButton.clicked.connect(self.recommendationsfunction)
        self.weatherButton.clicked.connect(self.weatherFetcher)
        
        
        
    def logoutfunction(self):
        '''Logs the user out the program
           return -> void'''
        w3.hide(), w1.show() # Hides the main window and shows the login window
        
        
    def showhelp(self):
        '''Shows the help window
           return -> void'''
        w6.show()
        
        
    def hoteltable(self):
        '''Loads the table with all the information from the database
           return -> void '''
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query = 'SELECT * FROM HOTELS' # Selects all the rows from the HOTELS table
        results = cur.execute(query) # Executes the query and stores it in results
        self.tableWidget.setRowCount(5) # Sets the row count to 4
        for i,row in enumerate(results): # Using for loop to get index and enumerate function to get items
            self.tableWidget.setItem(i, 0 , QtWidgets.QTableWidgetItem(row[0])) # Adds first row from database to table
            self.tableWidget.setItem(i, 1 , QtWidgets.QTableWidgetItem(row[1])) # Adds second row from database to table
            self.tableWidget.setItem(i, 2 , QtWidgets.QTableWidgetItem(row[2])) # Adds third row from database to table
            self.tableWidget.setItem(i, 3 , QtWidgets.QTableWidgetItem(row[3])) # Adds fourth row from database to table
            self.tableWidget.setItem(i, 4 , QtWidgets.QTableWidgetItem(row[4])) # Adds fourth row from database to table
            
            
    
    
    def openhotel(self, index):
        ''' Opens the hotel depending on what row was clicked
            return -> void '''
        row = index.row()
        hotelName = self.tableWidget.item(row, 0).text() # Fetches the hotel name
        if hotelName == "montcalm royal": # Checking what the name of the row is
            w4.show() # Shows the window
        elif hotelName == "travelodge":
            w7.show()
        elif hotelName == "park grand":
            w8.show()
        elif hotelName == "canopy":
            w9.show()
        else:
            w10.show()
        w3.close()
        
        
    def searchfunction(self):
        ''' Searches for hotel in table
            return -> void '''
        search = self.searchText.text().lower() # Fetches search result and stores it in lower case
        if any(char in "\"'`/;&<>”‘’" for char in search): # Checking for special characters in email and password
                self.searchLabel.setText("Invalid characters used") # Outputs a message notifying user has used invalid characters
                return # Exiting the function early if invalid characters are used
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query = 'SELECT hotel_name FROM HOTELS WHERE hotel_name=?' # SQL statement that finds hotel that matches search
        cur.execute(query, (search,)) # Executes SQL query
        result = cur.fetchone() # Fetches result
        if result is None: # Checks if no items were selected
            self.searchLabel.setText("Hotel not found") # Outputs a message to user
            return # Breaks code here
        self.searchLabel.setText("Hotel found") # Outputs a message to user
        self.tableWidget.setRowCount(0) # Removes all rows
        self.tableWidget.insertRow(0) # Inserts a new row for the search result
        self.tableWidget.setItem(0,0,QtWidgets.QTableWidgetItem(result[0])) # Sets the item in the row to hotel
        
    def wififilter(self):
        '''Filters out hotels and only includes hotels with wifi
           return -> void'''
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query = 'SELECT hotel_name FROM HOTELS WHERE wifi=1' # SQL statement to find hotels with wifi
        cur.execute(query) # Executes query
        results = cur.fetchall() # Fetches hotels
        print(results) # Printing for testing purposes
        self.tableWidget.setRowCount(0) # Removes all rows at position 0
        for i,rows in enumerate(results): # Using for loop to get index and enumerate function to get items in the tuple
            print(i, rows) # Printing for testing purposes
            self.tableWidget.insertRow(i) # Inserts a row
            self.tableWidget.setItem(i, 0 , QtWidgets.QTableWidgetItem(rows[0])) # Adds first row from database to table
                      
    def roomservicefilter(self):
        '''Filters out hotels and only includes hotels with room service
           return -> void'''
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query = 'SELECT hotel_name FROM HOTELS WHERE room_service=1' # SQL statement to find hotels with room service
        cur.execute(query) # Executes query
        results = cur.fetchall() # Fetches hotels
        print(results) # Printing for testing purposes
        self.tableWidget.setRowCount(0) # Removes all rowsat position 0
        for i,rows in enumerate(results): # Using for loop to get index and enumerate function to get items in the tuple
            print(i, rows) # Printing for testing purposes
            self.tableWidget.insertRow(i) # Inserts a row
            self.tableWidget.setItem(i, 0 , QtWidgets.QTableWidgetItem(rows[0])) # Adds first row from database to table
        
    def petsfilter(self):
        '''Filters out hotels and only includes hotels with pets allowed
           return -> void'''
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query = 'SELECT hotel_name FROM HOTELS WHERE pets=1' # SQL statement to find hotels with pets allowed
        cur.execute(query) # Executes query
        results = cur.fetchall() # Fetches hotels
        print(results) # Printing for testing purposes
        self.tableWidget.setRowCount(0) # Removes all rowsat position 0
        for i,rows in enumerate(results): # Using for loop to get index and enumerate function to get items in the tuple
            print(i, rows) # Printing for testing purposes
            self.tableWidget.insertRow(i) # Inserts a row
            self.tableWidget.setItem(i, 0 , QtWidgets.QTableWidgetItem(rows[0])) # Adds first row from database to table
            
    def clearsearchfunction(self):
        ''' Clears any searches or filters applied to the table
            return -> void '''
        self.tableWidget.setRowCount(0) # Removes all rows at position 0
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query = 'SELECT * FROM HOTELS' # Selects all the rows from the HOTELS table
        results = cur.execute(query) # Executes the query and stores it in results
        self.tableWidget.setRowCount(len(result))
        for i,row in enumerate(results): # Using for loop to get index and enumerate function to get items
            self.tableWidget.setItem(i, 0 , QtWidgets.QTableWidgetItem(row[0])) # Adds first row from database to table
            self.tableWidget.setItem(i, 1 , QtWidgets.QTableWidgetItem(row[1])) # Adds second row from database to table
            self.tableWidget.setItem(i, 2 , QtWidgets.QTableWidgetItem(row[2])) # Adds third row from database to table
            self.tableWidget.setItem(i, 3 , QtWidgets.QTableWidgetItem(row[3])) # Adds fourth row from database to table
            
            
    def recommendationsfunction(self):
        ''' Recommends hotel to users
            return -> void '''
        self.tableWidget.setRowCount(0) # Removes all rows at position 0
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query1 = 'SELECT id FROM USERS WHERE email=?' # Query to fetch user ID
        cur.execute(query1, (email,)) # Executes the query
        uniqueID = cur.fetchone() # Fetches the id
        query2 = '''SELECT DISTINCT H.*              
                    FROM HOTELS H
                    INNER JOIN USER_BOOKINGS UB
                    ON H.hotel_name = UB.hotel_name
                    WHERE UB.id = ?;'''
        cur.execute(query2, (uniqueID[0],)) # Executes query
        result = cur.fetchall() # Stores result
        print (result) # Outputting for testing
        for i,rows in enumerate(result): # Using for loop to get index and enumerate function to get items
            print(i, rows) # Printing for testing purposes
            self.tableWidget.insertRow(i) # Inserts a row
            self.tableWidget.setItem(i, 0 , QtWidgets.QTableWidgetItem(rows[0])) # Adds first row from database to table
            
    def weatherFetcher(self):
        '''Retreieves weathers from internet for london
           return -> void'''
        apiKey = "[Enter API KEY HERE]" # API key to access API
        baseUrl = "https://api.openweathermap.org/data/2.5/weather" # URL
        requestsUrl = f"{baseUrl}?appid={apiKey}&q=london" # Passing in parameters to the URL
        response = requests.get(requestsUrl)
        if response.status_code == 200: # Successful connection
            data = response.json() # Stores data in location data
            weather = data['weather'][0]['description'] # Get the weather description from the API response data
            temperature = round(data["main"]["temp"] - 273.15, 2) # Convert the temperature from Kelvin to Celsius and round to 2 decimal places
            print ("Weather: ", weather) # Print the weather to the shell
            print ("Temperature: ", temperature, "celsius") # Print the temperature to the shell
        
            self.weatherText.setText(f"""Weather: {weather}
Temperature: {temperature}°C""") # Set the weather text in the GUI
        else: # If the API cannot connect, display an error message in the GUI
            self.weatherText.setText("An error has occured")
           
        
       

class MontcalmRoyal(QtWidgets.QMainWindow, window4):
    def __init__(self,parent=None):
            QtWidgets.QMainWindow.__init__(self, parent)
            self.setupUi(self)
            
            #title
            self.setWindowTitle('Montcalm Royal')
            
            # Connecting buttons to their functions
            self.montcalmBackButton.clicked.connect(self.goback)
            self.bookdateButton.clicked.connect(self.makebooking)
            self.graphButton.clicked.connect(self.showgraph)
            
    def showgraph(self):
        '''Shows monthly visits
           return -> void'''
        graph = Graph(hotelname="montcalm royal", parent=self) # Passing hotel name
        graph.show() # Showing the Graph window
            
    def goback(self):
        ''' Takes user back to home page'''
        w3.show(), w4.hide() # Hides the hotel window and opens the main window
        
    def createPDF(self, dateString, costPerNight, email):
        '''Creates a PDF for when a booking is made
           return -> void'''
        pdf = FPDF() # Creates PDF file
        pdf.add_page() # Adds a page
        pdf.set_font("Arial", size=12)
        # Populating the PDF
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Montcalm Royal", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Montcalm_Royal_Booking_Confirmation.pdf") # Stores it in directory under name
    
    def makebooking(self):
        '''Inserts booking into SQL database
           return -> void'''
        global email
        selectedDate = self.dateEdit.date() # Fetches the date entered in date edit
        dateString = selectedDate.toString('dd-MM-yyyy') # Changes string format
        currentDate = datetime.now() # Fetches the current date
        if selectedDate < currentDate: # Checks whether booking date is before current time
            self.bookingLabel.setText("Invalid date") # Outputs a message to GUI
            return # Breaks code here
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query1 = 'SELECT id FROM USERS WHERE email=?' # SQL statement to retrieve user id
        cur.execute(query1, (email,)) # Executes the query
        uniqueID = cur.fetchone() # Fetches the id
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="montcalm royal"' # SQL statement to fetch cost
        cur.execute(cpnQuery) # Executes SQL statement
        costPerNight = cur.fetchone() # Fetches cpn
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)' # Insert into linking table
        try: # Tries to do this
            cur.execute(query2, (uniqueID[0],"montcalm royal", dateString, costPerNight[0])) # Executes SQL statement
            conn.commit() # Commits the changes made
            self.bookingLabel.setText("Booking confirmed") # Output to the GUI saying booking is confirmed
            self.createPDF(dateString, costPerNight, email) # Creating a pdf using this function
        except sqlite3.IntegrityError: # If an error occurs do this instead
            self.bookingLabel.setText("Duplicate bookings are not allowed") # Outputs a messsage GUI
            
class Travelodge(QtWidgets.QMainWindow, window7):
    def __init__(self,parent=None):
            QtWidgets.QMainWindow.__init__(self, parent)
            self.setupUi(self)
            
            #title
            self.setWindowTitle('Travelodge')
            
            # Connecting buttons to their functions
            self.montcalmBackButton.clicked.connect(self.goback)
            self.bookdateButton.clicked.connect(self.makebooking)
            self.graphButton.clicked.connect(self.showgraph)
            
    def showgraph(self):
        '''Shows monthly visits
           return -> void'''
        graph = Graph(hotelname="travelodge", parent=self) # Passing hotel name
        graph.show() # Showing the Graph window
            
    def goback(self):
        ''' Takes user back to home page'''
        w3.show(), w4.hide() # Hides the hotel window and opens the main window
        
    def createPDF(self, dateString, costPerNight, email):
        '''Creates a PDF for when a booking is made
           return -> void'''
        pdf = FPDF() # Creates PDF file
        pdf.add_page() # Adds a page
        pdf.set_font("Arial", size=12)
        # Populating the PDF
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Travelodge", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Travelodge_Booking_Confirmation.pdf") # Stores it in directory under name
    
    def makebooking(self):
        '''Inserts booking into SQL database
           return -> void'''
        global email
        selectedDate = self.dateEdit.date() # Fetches the date entered in date edit
        dateString = selectedDate.toString('dd-MM-yyyy') # Changes string format
        currentDate = datetime.now() # Fetches the current date
        if selectedDate < currentDate: # Checks whether booking date is before current time
            self.bookingLabel.setText("Invalid date") # Outputs a message to GUI
            return # Breaks code here
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query1 = 'SELECT id FROM USERS WHERE email=?' # SQL statement to retrieve user id
        cur.execute(query1, (email,)) # Executes the query
        uniqueID = cur.fetchone() # Fetches the id
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="travelodge"' # SQL statement to fetch cost
        cur.execute(cpnQuery) # Executes SQL statement
        costPerNight = cur.fetchone() # Fetches cpn
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)' # Insert into linking table
        try: # Tries to do this
            cur.execute(query2, (uniqueID[0],"montcalm royal", dateString, costPerNight[0])) # Executes SQL statement
            conn.commit() # Commits the changes made
            self.bookingLabel.setText("Booking confirmed") # Output to the GUI saying booking is confirmed
            self.createPDF(dateString, costPerNight, email) # Creating a pdf using this function
        except sqlite3.IntegrityError: # If an error occurs do this instead
            self.bookingLabel.setText("Duplicate bookings are not allowed") # Outputs a messsage GUI
            
            
class ParkGrand(QtWidgets.QMainWindow, window8):
    def __init__(self,parent=None):
            QtWidgets.QMainWindow.__init__(self, parent)
            self.setupUi(self)
            
            #title
            self.setWindowTitle('Park Grand')
            
            # Connecting buttons to their functions
            self.montcalmBackButton.clicked.connect(self.goback)
            self.bookdateButton.clicked.connect(self.makebooking)
            self.graphButton.clicked.connect(self.showgraph)
            
    def showgraph(self):
        '''Shows monthly visits
           return -> void'''
        graph = Graph(hotelname="park grand", parent=self) # Passing hotel name
        graph.show() # Showing the Graph window
            
    def goback(self):
        ''' Takes user back to home page'''
        w3.show(), w4.hide() # Hides the hotel window and opens the main window
        
    def createPDF(self, dateString, costPerNight, email):
        '''Creates a PDF for when a booking is made
           return -> void'''
        pdf = FPDF() # Creates PDF file
        pdf.add_page() # Adds a page
        pdf.set_font("Arial", size=12)
        # Populating the PDF
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Park Grand", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Park_grand_Booking_Confirmation.pdf") # Stores it in directory under name
    
    def makebooking(self):
        '''Inserts booking into SQL database
           return -> void'''
        global email
        selectedDate = self.dateEdit.date() # Fetches the date entered in date edit
        dateString = selectedDate.toString('dd-MM-yyyy') # Changes string format
        currentDate = datetime.now() # Fetches the current date
        if selectedDate < currentDate: # Checks whether booking date is before current time
            self.bookingLabel.setText("Invalid date") # Outputs a message to GUI
            return # Breaks code here
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query1 = 'SELECT id FROM USERS WHERE email=?' # SQL statement to retrieve user id
        cur.execute(query1, (email,)) # Executes the query
        uniqueID = cur.fetchone() # Fetches the id
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="park grand"' # SQL statement to fetch cost
        cur.execute(cpnQuery) # Executes SQL statement
        costPerNight = cur.fetchone() # Fetches cpn
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)' # Insert into linking table
        try: # Tries to do this
            cur.execute(query2, (uniqueID[0],"park grand", dateString, costPerNight[0])) # Executes SQL statement
            conn.commit() # Commits the changes made
            self.bookingLabel.setText("Booking confirmed") # Output to the GUI saying booking is confirmed
            self.createPDF(dateString, costPerNight, email) # Creating a pdf using this function
        except sqlite3.IntegrityError: # If an error occurs do this instead
            self.bookingLabel.setText("Duplicate bookings are not allowed") # Outputs a messsage GUI


class Canopy(QtWidgets.QMainWindow, window9):
    def __init__(self,parent=None):
            QtWidgets.QMainWindow.__init__(self, parent)
            self.setupUi(self)
            
            #title
            self.setWindowTitle('Canopy')
            
            # Connecting buttons to their functions
            self.montcalmBackButton.clicked.connect(self.goback)
            self.bookdateButton.clicked.connect(self.makebooking)
            self.graphButton.clicked.connect(self.showgraph)
            
    def showgraph(self):
        '''Shows monthly visits
           return -> void'''
        graph = Graph(hotelname="canopy", parent=self) # Passing hotel name
        graph.show() # Showing the Graph window
            
    def goback(self):
        ''' Takes user back to home page'''
        w3.show(), w4.hide() # Hides the hotel window and opens the main window
        
    def createPDF(self, dateString, costPerNight, email):
        '''Creates a PDF for when a booking is made
           return -> void'''
        pdf = FPDF() # Creates PDF file
        pdf.add_page() # Adds a page
        pdf.set_font("Arial", size=12)
        # Populating the PDF
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Canopy", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Canopy_Booking_Confirmation.pdf") # Stores it in directory under name
    
    def makebooking(self):
        '''Inserts booking into SQL database
           return -> void'''
        global email
        selectedDate = self.dateEdit.date() # Fetches the date entered in date edit
        dateString = selectedDate.toString('dd-MM-yyyy') # Changes string format
        currentDate = datetime.now() # Fetches the current date
        if selectedDate < currentDate: # Checks whether booking date is before current time
            self.bookingLabel.setText("Invalid date") # Outputs a message to GUI
            return # Breaks code here
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query1 = 'SELECT id FROM USERS WHERE email=?' # SQL statement to retrieve user id
        cur.execute(query1, (email,)) # Executes the query
        uniqueID = cur.fetchone() # Fetches the id
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="canopy"' # SQL statement to fetch cost
        cur.execute(cpnQuery) # Executes SQL statement
        costPerNight = cur.fetchone() # Fetches cpn
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)' # Insert into linking table
        try: # Tries to do this
            cur.execute(query2, (uniqueID[0],"canopy", dateString, costPerNight[0])) # Executes SQL statement
            conn.commit() # Commits the changes made
            self.bookingLabel.setText("Booking confirmed") # Output to the GUI saying booking is confirmed
            self.createPDF(dateString, costPerNight, email) # Creating a pdf using this function
        except sqlite3.IntegrityError: # If an error occurs do this instead
            self.bookingLabel.setText("Duplicate bookings are not allowed") # Outputs a messsage GUI


class ResidentCovent(QtWidgets.QMainWindow, window10):
    def __init__(self,parent=None):
            QtWidgets.QMainWindow.__init__(self, parent)
            self.setupUi(self)
            
            #title
            self.setWindowTitle('Resident Covent')
            
            # Connecting buttons to their functions
            self.montcalmBackButton.clicked.connect(self.goback)
            self.bookdateButton.clicked.connect(self.makebooking)
            self.graphButton.clicked.connect(self.showgraph)
            
    def showgraph(self):
        '''Shows monthly visits
           return -> void'''
        graph = Graph(hotelname="resident covent", parent=self) # Passing hotel name
        graph.show() # Showing the Graph window
            
    def goback(self):
        ''' Takes user back to home page'''
        w3.show(), w4.hide() # Hides the hotel window and opens the main window
        
    def createPDF(self, dateString, costPerNight, email):
        '''Creates a PDF for when a booking is made
           return -> void'''
        pdf = FPDF() # Creates PDF file
        pdf.add_page() # Adds a page
        pdf.set_font("Arial", size=12)
        # Populating the PDF
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Resident Covent", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Resident_covent_Booking_Confirmation.pdf") # Stores it in directory under name
    
    def makebooking(self):
        '''Inserts booking into SQL database
           return -> void'''
        global email
        selectedDate = self.dateEdit.date() # Fetches the date entered in date edit
        dateString = selectedDate.toString('dd-MM-yyyy') # Changes string format
        currentDate = datetime.now() # Fetches the current date
        if selectedDate < currentDate: # Checks whether booking date is before current time
            self.bookingLabel.setText("Invalid date") # Outputs a message to GUI
            return # Breaks code here
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        query1 = 'SELECT id FROM USERS WHERE email=?' # SQL statement to retrieve user id
        cur.execute(query1, (email,)) # Executes the query
        uniqueID = cur.fetchone() # Fetches the id
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="resident covent"' # SQL statement to fetch cost
        cur.execute(cpnQuery) # Executes SQL statement
        costPerNight = cur.fetchone() # Fetches cpn
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)' # Insert into linking table
        try: # Tries to do this
            cur.execute(query2, (uniqueID[0],"resident covent", dateString, costPerNight[0])) # Executes SQL statement
            conn.commit() # Commits the changes made
            self.bookingLabel.setText("Booking confirmed") # Output to the GUI saying booking is confirmed
            self.createPDF(dateString, costPerNight, email) # Creating a pdf using this function
        except sqlite3.IntegrityError: # If an error occurs do this instead
            self.bookingLabel.setText("Duplicate bookings are not allowed") # Outputs a messsage GUI


class Graph(QtWidgets.QMainWindow, window5):
    def __init__(self, hotelname=None, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.hotelname = hotelname
        self.drawgraph(hotelname)
        self.setWindowTitle("Graph")
        
        
    def drawgraph(self, hotelname):
        '''Draws the graph
           return -> void'''
        self.figure = Figure()  # Create a figure object
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure) # Create a canvas object to display the figure
        self.setCentralWidget(self.canvas) # Add the canvas to the main window
        self.ax.set_xlabel("Months") # Sets x axis label to months
        self.ax.set_ylabel("Number of Bookings") # Sets y axis labels to number of bookings
        x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] # Values for x axis
        y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Values for y axis
        self.ax.bar(x, y)
        conn = sqlite3.connect("D:\MY folder\hotelDB.db") # Establishes a connection to the SQL database
        cur = conn.cursor() # Creates a cursor object to execute the SQL statements
        print(hotelname)
        query = "SELECT substr(reservation_date, 4, 2) as month, count(*) as count FROM USER_BOOKINGS WHERE hotel_name=? group by month" # Fetches months of bookings
        cur.execute(query, (hotelname,)) # Executes the SQL statements
        data = cur.fetchall() # Fetches all the data
        monthMap = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'} #Hashmap
        x = [] # Creates a list for x axis
        y = [] # Creates a list for y axis
        for row in data: # For loop
            if row[0]: 
                x.append(monthMap[int(row[0])]) # Appends items to x list
                y.append(row[1]) # Appends items to x list
        self.ax.plot(x, y)
        self.canvas.draw() # Draws the graph
        
class HelpMenu(QtWidgets.QMainWindow, window6):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("Help box")
        
        
        
        
        

# RUNNING OF THE PROGRAM

app = QApplication(sys.argv)   # Creates a QApplication which is needed in order to display the QWidgets
w1 = Login(None)               # Creates an object for Login class
w2 = SignUp(None)              # Creates an object for SignUp class
w3 = MainWindow(None)
w4 = MontcalmRoyal(None)
w5 = Graph(None)
w6 = HelpMenu(None)
w7 = Travelodge(None)
w8 = ParkGrand(None)
w9 = Canopy(None)
w10 = ResidentCovent(None)
w1.show()                     # Uses the library to fetch the .show() function which displays the window
app.exec_()                    # Executes the program
