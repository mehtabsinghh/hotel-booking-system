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
    def __init__(self, email, parent=None):
        # Initialize the Login window
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # Set the title and fixed window size
        self.setWindowTitle('Login Window')
        self.setFixedWidth(480)
        self.setFixedHeight(620)
        
        # Connect buttons to their respective functions
        self.loginButton.clicked.connect(self.login_function)
        self.signupHereButton.clicked connect(self.goto_create)
        
        # Make the password field display dots for security
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
    def login_function(self):
        # Function to validate user input and login
        global email
        email = self.email_field.text()
        password = self.password_field.text()
        
        if len(email) == 0 or len(password) == 0:
            # Check if either the email or password is empty
            self.login_text.setText("Please input all fields")
        else:
            # Check for invalid characters in email and password
            invalid_chars = "\"'`;&<>”‘’"
            if any(char in invalid_chars for char in email) or any(char in invalid_chars for char in password):
                self.login_text.setText("Invalid characters used in email or password")
                return
            
            # Establish a connection to the SQL database
            conn = sqlite3.connect("D:\MY folder\hotelDB.db")
            cur = conn.cursor()
            
            # Retrieve the password associated with the provided email
            query = 'SELECT password FROM USERS WHERE email = \'' + email + "\'"
            cur.execute(query)
            result_pass = cur.fetchone()
            
            if result_pass is None:
                # Check if the email doesn't exist
                self.login_text.setText("Email has not been registered")
            elif result_pass[0] == password:
                # Check if the password matches
                self.login_text.setText("Successfully logged in")
                w1.hide()
                w3.show()
                self.email_field.setText("")
                self.password_field.setText("")
                self.login_text.setText("")
            else:
                self.login_text.setText("Incorrect username or password")
                
    def goto_create(self):
        # Function to open the create account window
        w1.hide()
        w2.show()
                
class SignUp(QtWidgets.QMainWindow, window2):
    def __init__(self, parent=None):
        # Initialize the SignUp window
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # Set the title and fixed window size
        self.setWindowTitle('Signup Window')
        self.setFixedWidth(480)
        self.setFixedHeight(620)
        
        # Connect buttons to their respective functions
        self.signupButton.clicked.connect(self.signup_function)
        self.backButton.clicked.connect(self.back_to_login)
        
        # Make the password fields display dots for security
        self.passwordSignup_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPass_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
    def signup_function(self):
        # Function to create a user account and insert it into the database
        email = self.usernameSignUp_field.text()
        password = self.passwordSignup_field.text()
        confirm_password = self.confirmPass_field.text()
        
        if len(email) == 0 or len(password) == 0 or len(confirm_password) == 0:
            # Check if any of the fields are empty
            self.signup_text.setText("Please input all fields")
        else:
            # Check for invalid characters in email and password
            invalid_chars = "\"'`;&<>”‘’"
            if any(char in invalid_chars for char in email) or any(char in invalid_chars for char in password) or any(char in invalid_chars for char in confirm_password):
                self.signup_text.setText("Invalid characters used in email or password")
                return
            
            if password != confirm_password:
                # Compare password and confirm password
                self.signup_text.setText("Passwords do not match")
                return
            
            # Establish a connection to the SQL database
            conn = sqlite3.connect("D:\MY folder\hotelDB.db")
            cur = conn.cursor()
            
            check_query = 'SELECT email FROM USERS WHERE email=?'
            cur.execute(check_query, (email,))
            
            if cur.fetchone():
                # Check if email already exists
                self.signup_text.setText("Email already exists, please use a different one")
                return
            
            # Insert email and password into the database
            query = 'INSERT INTO USERS (email, password) VALUES (?, ?)'
            cur.execute(query, (email, password))
            conn.commit()
            self.signup_text.setText("Account successfully registered")
            w2.hide()
            w1.show()
            
    def back_to_login(self):
        # Function to go back to the login window
        w2.hide()
        w1.show()

class MainWindow(QtWidgets.QMainWindow, window3):
    def __init__(self, parent=None):
        # Initialize the MainWindow
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        loadUi("main_window.ui", self)  # Load the GUI file.

        # Set the title and initialize the table
        self.setWindowTitle('Main Window')
        self.hoteltable()
        self.tableWidget.clicked.connect(self.openhotel)
        self.tableWidget.setColumnWidth(0, 600)

        # Connect buttons to their functions
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
        # Log the user out
        w3.hide()
        w1.show()

    def showhelp(self):
        # Show the help window
        w6.show()

    def hoteltable(self):
        # Load the table with information from the database
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query = 'SELECT * FROM HOTELS'
        results = cur.execute(query)
        self.tableWidget.setRowCount(5)
        for i, row in enumerate(results):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(row[4]))

    def openhotel(self, index):
        # Open the hotel based on the clicked row
        row = index.row()
        hotelName = self.tableWidget.item(row, 0).text()
        if hotelName == "montcalm royal":
            w4.show()
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
        # Search for a hotel in the table
        search = self.searchText.text().lower()
        if any(char in "\"'`/;&<>”‘’" for char in search):
            self.searchLabel.setText("Invalid characters used")
            return
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query = 'SELECT hotel_name FROM HOTELS WHERE hotel_name=?'
        cur.execute(query, (search,))
        result = cur.fetchone()
        if result is None:
            self.searchLabel.setText("Hotel not found")
            return
        self.searchLabel.setText("Hotel found")
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(result[0]))

    def wififilter(self):
        # Filter hotels with WiFi
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query = 'SELECT hotel_name FROM HOTELS WHERE wifi=1'
        cur.execute(query)
        results = cur.fetchall()
        self.tableWidget.setRowCount(0)
        for i, rows in enumerate(results):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(rows[0]))

    def roomservicefilter(self):
        # Filter hotels with room service
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query = 'SELECT hotel_name FROM HOTELS WHERE room_service=1'
        cur.execute(query)
        results = cur.fetchall()
        self.tableWidget.setRowCount(0)
        for i, rows in enumerate(results):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(rows[0]))

    def petsfilter(self):
        # Filter hotels allowing pets
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query = 'SELECT hotel_name FROM HOTELS WHERE pets=1'
        cur.execute(query)
        results = cur.fetchall()
        self.tableWidget.setRowCount(0)
        for i, rows in enumerate(results):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(rows[0]))

        def clearsearchfunction(self):
        # Clear any searches or filters applied to the table
        self.tableWidget.setRowCount(0)
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query = 'SELECT * FROM HOTELS'
        results = cur.execute(query)
        self.tableWidget.setRowCount(len(results))
        for i, row in enumerate(results):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(row[3]))

    def recommendationsfunction(self):
        # Recommend hotels to users based on their history
        self.tableWidget.setRowCount(0)
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query1 = 'SELECT id FROM USERS WHERE email=?'
        cur.execute(query1, (email,))
        uniqueID = cur.fetchone()
        query2 = '''SELECT DISTINCT H.*
                    FROM HOTELS H
                    INNER JOIN USER_BOOKINGS UB
                    ON H.hotel_name = UB.hotel_name
                    WHERE UB.id = ?;'''
        cur.execute(query2, (uniqueID[0],))
        result = cur.fetchall()
        for i, rows in enumerate(result):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(rows[0]))

    def weatherFetcher(self):
        # Retrieve weather information from the internet for London
        apiKey = "[Enter API KEY HERE]"
        baseUrl = "https://api.openweathermap.org/data/2.5/weather"
        requestsUrl = f"{baseUrl}?appid={apiKey}&q=london"
        response = requests.get(requestsUrl)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = round(data["main"]["temp"] - 273.15, 2)
            print("Weather: ", weather)
            print("Temperature: ", temperature, "celsius")
            self.weatherText.setText(f"""Weather: {weather} 
                                         Temperature: {temperature}°C""")
        else:
            self.weatherText.setText("An error has occurred")
            
class MontcalmRoyal(QtWidgets.QMainWindow, window4):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Set window title
        self.setWindowTitle('Montcalm Royal')

        # Connect buttons to their functions
        self.montcalmBackButton.clicked.connect(self.goback)
        self.bookdateButton.clicked connect(self.makebooking)
        self.graphButton.clicked.connect(self.showgraph)

    def showgraph(self):
        # Display a monthly visits graph
        graph = Graph(hotelname="montcalm royal", parent=self)
        graph.show()

    def goback(self):
        # Return to the main window
        w3.show(), w4.hide()

    def createPDF(self, dateString, costPerNight, email):
        # Create a PDF for booking confirmation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Montcalm Royal", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Montcalm_Royal_Booking_Confirmation.pdf")

    def makebooking(self):
        # Insert booking into the SQL database
        selectedDate = self.dateEdit.date()
        dateString = selectedDate.toString('dd-MM-yyyy')
        currentDate = datetime.now()
        if selectedDate < currentDate:
            self.bookingLabel.setText("Invalid date")
            return
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query1 = 'SELECT id FROM USERS WHERE email=?'
        cur.execute(query1, (email,))
        uniqueID = cur.fetchone()
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="montcalm royal"'
        cur.execute(cpnQuery)
        costPerNight = cur.fetchone()
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)'
        try:
            cur.execute(query2, (uniqueID[0], "montcalm royal", dateString, costPerNight[0]))
            conn.commit()
            self.bookingLabel.setText("Booking confirmed")
            self.createPDF(dateString, costPerNight, email)
        except sqlite3.IntegrityError:
            self.bookingLabel.setText("Duplicate bookings are not allowed")
            
class Travelodge(QtWidgets.QMainWindow, window7):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Set window title
        self.setWindowTitle('Travelodge')

        # Connect buttons to their functions
        self.montcalmBackButton.clicked.connect(self.goback)
        self.bookdateButton.clicked connect(self.makebooking)
        self.graphButton.clicked.connect(self.showgraph)

    def showgraph(self):
        # Display a monthly visits graph for Travelodge hotel
        graph = Graph(hotelname="travelodge", parent=self)
        graph.show()

    def goback(self):
        # Return to the main window from the Travelodge window
        w3.show()
        w7.hide()

    def createPDF(self, dateString, costPerNight, email):
        # Create a PDF document for booking confirmation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Travelodge", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Travelodge_Booking_Confirmation.pdf")  # Save the PDF document

    def makebooking(self):
        # Insert a booking into the SQL database
        global email
        selectedDate = self.dateEdit.date()
        dateString = selectedDate.toString('dd-MM-yyyy')
        currentDate = datetime.now()
        if selectedDate < currentDate:
            self.bookingLabel.setText("Invalid date")
            return
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query1 = 'SELECT id FROM USERS WHERE email=?'
        cur.execute(query1, (email,))
        uniqueID = cur.fetchone()
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="travelodge"'
        cur.execute(cpnQuery)
        costPerNight = cur.fetchone()
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)'
        try:
            cur.execute(query2, (uniqueID[0], "travelodge", dateString, costPerNight[0]))
            conn.commit()
            self.bookingLabel.setText("Booking confirmed")
            self.createPDF(dateString, costPerNight, email)
        except sqlite3.IntegrityError:
            self.bookingLabel.setText("Duplicate bookings are not allowed")
            
class ParkGrand(QtWidgets.QMainWindow, window8):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Set window title
        self.setWindowTitle('Park Grand')

        # Connect buttons to their functions
        self.montcalmBackButton.clicked.connect(self.goback)
        self.bookdateButton.clicked.connect(self.makebooking)
        self.graphButton.clicked.connect(self.showgraph)

    def showgraph(self):
        # Display a monthly visits graph for Park Grand hotel
        graph = Graph(hotelname="park grand", parent=self)
        graph.show()

    def goback(self):
        # Return to the main window from the Park Grand hotel window
        w3.show()
        w4.hide()

    def createPDF(self, dateString, costPerNight, email):
        # Create a PDF document for booking confirmation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Park Grand", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Park_grand_Booking_Confirmation.pdf")  # Save the PDF document

    def makebooking(self):
        # Insert a booking into the SQL database
        global email
        selectedDate = self.dateEdit.date()
        dateString = selectedDate.toString('dd-MM-yyyy')
        currentDate = datetime.now()
        if selectedDate < currentDate:
            self.bookingLabel.setText("Invalid date")
            return
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query1 = 'SELECT id FROM USERS WHERE email=?'
        cur.execute(query1, (email,))
        uniqueID = cur.fetchone()
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="park grand"'
        cur.execute(cpnQuery)
        costPerNight = cur.fetchone()
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)'
        try:
            cur.execute(query2, (uniqueID[0], "park grand", dateString, costPerNight[0]))
            conn.commit()
            self.bookingLabel.setText("Booking confirmed")
            self.createPDF(dateString, costPerNight, email)
        except sqlite3.IntegrityError:
            self.bookingLabel.setText("Duplicate bookings are not allowed")
            
class Canopy(QtWidgets.QMainWindow, window9):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Set window title
        self.setWindowTitle('Canopy')

        # Connect buttons to their functions
        self.montcalmBackButton.clicked.connect(self.goback)
        self.bookdateButton.clicked.connect(self.makebooking)
        self.graphButton.clicked connect(self.showgraph)

    def showgraph(self):
        # Display a monthly visits graph for Canopy hotel
        graph = Graph(hotelname="canopy", parent=self)
        graph.show()

    def goback(self):
        # Return to the main window from the Canopy hotel window
        w3.show()
        w4.hide()

    def createPDF(self, dateString, costPerNight, email):
        # Create a PDF document for booking confirmation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Canopy", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Canopy_Booking_Confirmation.pdf")  # Save the PDF document

    def makebooking(self):
        # Insert a booking into the SQL database
        global email
        selectedDate = self.dateEdit.date()
        dateString = selectedDate.toString('dd-MM-yyyy')
        currentDate = datetime.now()
        if selectedDate < currentDate:
            self.bookingLabel.setText("Invalid date")
            return
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query1 = 'SELECT id FROM USERS WHERE email=?'
        cur.execute(query1, (email,))
        uniqueID = cur.fetchone()
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="canopy"'
        cur.execute(cpnQuery)
        costPerNight = cur.fetchone()
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)'
        try:
            cur.execute(query2, (uniqueID[0], "canopy", dateString, costPerNight[0]))
            conn.commit()
            self.bookingLabel.setText("Booking confirmed")
            self.createPDF(dateString, costPerNight, email)
        except sqlite3.IntegrityError:
            self.bookingLabel.setText("Duplicate bookings are not allowed")

class ResidentCovent(QtWidgets.QMainWindow, window10):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Set window title
        self.setWindowTitle('Resident Covent')

        # Connect buttons to their functions
        self.montcalmBackButton.clicked.connect(self.goback)
        self.bookdateButton.clicked.connect(self.makebooking)
        self.graphButton.clicked.connect(self.showgraph)

    def showgraph(self):
        # Display a monthly visits graph for Resident Covent hotel
        graph = Graph(hotelname="resident covent", parent=self)
        graph.show()

    def goback(self):
        # Return to the main window from the Resident Covent hotel window
        w3.show()
        w4.hide()

    def createPDF(self, dateString, costPerNight, email):
        # Create a PDF document for booking confirmation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=1, align="C")
        pdf.cell(200, 10, txt="Hotel Name: Resident Covent", ln=1, align="L")
        pdf.cell(200, 10, txt="Reservation Date: " + dateString, ln=1, align="L")
        pdf.cell(200, 10, txt="Cost per Night: £" + str(costPerNight[0]), ln=1, align="L")
        pdf.cell(200, 10, txt="Email: " + email, ln=1, align="L")
        pdf.output("Resident_Covent_Booking_Confirmation.pdf")  # Save the PDF document

    def makebooking(self):
        # Insert a booking into the SQL database
        global email
        selectedDate = self.dateEdit.date()
        dateString = selectedDate.toString('dd-MM-yyyy')
        currentDate = datetime.now()
        if selectedDate < currentDate:
            self.bookingLabel.setText("Invalid date")
            return
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()
        query1 = 'SELECT id FROM USERS WHERE email=?'
        cur.execute(query1, (email,))
        uniqueID = cur.fetchone()
        cpnQuery = 'SELECT cpn FROM HOTELS WHERE hotel_name="resident covent"'
        cur.execute(cpnQuery)
        costPerNight = cur.fetchone()
        query2 = 'INSERT INTO USER_BOOKINGS (id, hotel_name, reservation_date, cpn) VALUES (?,?,?,?)'
        try:
            cur.execute(query2, (uniqueID[0], "resident covent", dateString, costPerNight[0]))
            conn.commit()
            self.bookingLabel.setText("Booking confirmed")
            self.createPDF(dateString, costPerNight, email)
        except sqlite3.IntegrityError:
            self.bookingLabel.setText("Duplicate bookings are not allowed")

class Graph(QtWidgets.QMainWindow, window5):
    def __init__(self, hotelname=None, parent=None):
        # Initialize the QMainWindow and set up the UI
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.hotelname = hotelname

        # Create the graph and set the window title
        self.drawgraph(hotelname)
        self.setWindowTitle("Graph")

    def drawgraph(self, hotelname):
        # Create a Figure for the graph
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        
        # Set the canvas as the central widget
        self.setCentralWidget(self.canvas)

        # Set labels for the X and Y axes
        self.ax.set_xlabel("Months")
        self.ax.set_ylabel("Number of Bookings")

        # Initialize empty lists for X and Y data
        x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Connect to the SQLite database
        conn = sqlite3.connect("D:\MY folder\hotelDB.db")
        cur = conn.cursor()

        # Query to fetch the number of bookings for each month
        query = "SELECT substr(reservation_date, 4, 2) as month, count(*) as count FROM USER_BOOKINGS WHERE hotel_name=? group by month"
        cur.execute(query, (hotelname,))
        data = cur.fetchall()

        # Define a dictionary to map month numbers to names
        monthMap = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        # Populate X and Y lists with data from the database query
        x = []
        y = []
        for row in data:
            if row[0]:
                x.append(monthMap[int(row[0])])
                y.append(row[1])

        # Plot the data on the graph
        self.ax.plot(x, y)
        self.canvas.draw()

        
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
app.exec_()                   # Executes the program
