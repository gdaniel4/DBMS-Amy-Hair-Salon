import datetime
from datetime import date
import random
import json
import flask
from flask import jsonify
from flask import request, make_response
from flask import redirect, url_for
from flask.templating import render_template
import pandas as pd
from pandas.core.frame import DataFrame
import pyodbc
from pyodbc import Error
def create_connection(Driver, Server, db_name, Trsuted_Connection, MARS_Connection): # Create conneciton with sql 
    connection = None
    try:
        connection = pyodbc.connect(
            Driver=Driver,
            Server=Server, #Server name of the server when you connect to the SQL management
            database=db_name, #Database Name
            Trusted_Connection = Trsuted_Connection,
            MultipleActiveResultsSets = True,
            MARS_Connection=MARS_Connection
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query): # Excute code to sql 
    cursor = connection.cursor()
    try:
        cursor.execute(query).fetchall()
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query): # Excute to read in python 
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


#connection = create_connection("{SQL SERVER}","DESKTOP-0BGENB5\MSSQLSERVER02","Version2", "Yes" ) # Connects the database in sql
connection = create_connection("{SQL SERVER}","GABE-LAPTOP001\MSSQLSERVER01","was","Yes","Yes") # Connects the database in sql

#Set up app name
app = flask.Flask(__name__) #Set app
app.config["DEBUG"] = True #Debug

@app.route('/Customer/',methods = ['GET'])
def Customer():
    query = "SELECT * FROM Customer"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return jsonify(result)
   
    """
    connection = create_connection("{SQL SERVER}","GABE-LAPTOP001\MSSQLSERVER01","was", "Yes" ) # Connects the database in sql
    cursor = connection.cursor()
    cmd = "SELECT * FROM Customer"    
    results = cursor.execute(cmd).fetchall()
    df = pd.read_sql(cmd,connection)
    return df, results
    """

    """
    query = "SELECT * FROM Customer"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)
    """
    
    
@app.route('/Customer/add',methods = ['POST'])
def AddCustomer():
    request_data = request.get_json()
    State = request_data['State']
    Country = request_data['Country']
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    CustomerHomeNumber = request_data['CustomerHomeNumber']
    CustomerCellNumber = request_data['CustomerCellNumber']
    CustomerStatusID = '1'
    CustomerStrike = '0'
    StrikeComment = "None"
    query = "INSERT INTO Customer (CustomerFirstName,CustomerLastName,CustomerHomeNumber,CustomerCellNumber,StateID,CountryID,CustomerStatusID,CustomerStrike,StrikeComment) VALUES ('{}','{}','{}','{}',(SELECT State.StateID FROM State WHERE StateInitial = '{}'),(SELECT Country.CountryID FROM Country WHERE CountryName = '{}'),'{}','{}','{}')".format(CustomerFirstName,CustomerLastName,CustomerHomeNumber,CustomerCellNumber,State,Country,CustomerStatusID,CustomerStrike,StrikeComment)
    execute_query(connection,query)
    return 'Added Customer'

@app.route('/Customer/update/<int:id>',methods = ['PUT'])
def UpdateCustomer(id):
    request_data = request.get_json()
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    CustomerHomeNumber = request_data['CustomerHomeNumber']
    CustomerCellNumber = request_data['CustomerCellNumber']
    State = request_data['State']
    Country = request_data['Country']
    CustomerStatus = request_data['Status']
    CustomerStrike = request_data['CustomerStrike']
    StrikeComment = request_data['StrikeComment']
    query = "UPDATE Customer SET CustomerFirstName = '{}',CustomerLastName = '{}',CustomerHomeNumber = '{}',CustomerCellNumber = '{}',StateID = (SELECT State.StateID FROM State WHERE StateInitial = '{}'),CountryID = (SELECT Country.CountryID FROM Country WHERE CountryName = '{}'),CustomerStatusID = (SELECT CustomerStatusID FROM CustomerStatus WHERE StatusDescription = '{}'),CustomerStrike = '{}',StrikeComment = '{}' WHERE CustomerID = '{}'".format(CustomerFirstName,CustomerLastName,CustomerHomeNumber,CustomerCellNumber,State,Country,CustomerStatus,CustomerStrike,StrikeComment,id)
    execute_query(connection,query)
    return 'Updated Customer'

@app.route('/Customer/update/<int:id>',methods = ['GET'])
def CustomerByID(id):
    query = "SELECT CustomerID,CustomerFirstName,CustomerLastName,CustomerHomeNumber,CustomerCellNumber,State.StateInitial,Country.CountryInitial,CustomerStatus.StatusDescription,CustomerStrike,StrikeComment FROM Customer JOIN State ON State.StateID = Customer.StateID JOIN Country ON Country.CountryID = Customer.CountryID JOIN CustomerStatus ON CustomerStatus.CustomerStatusID = Customer.CustomerStatusID WHERE CustomerID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Customer/delete/<int:id>', methods = ['DELETE'])
def DeleteCustomer(id):
    query = "DELETE FROM Customer WHERE CustomerID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/Customer')

@app.route('/Appointment/',methods = ['GET'])
def Appointment():
    query = "SELECT * FROM Appointment"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Appointment/add',methods = ['POST'])
def AddAppointment():
    request_data = request.get_json()
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    AppointmentDate = request_data['AppointmentDate']
    AppointmentTime = request_data['AppointmentTime']
    ServiceName = request_data['ServiceName']
    query = "INSERT INTO Appointment (CustomerID,EmployeeID,AppointmentDate,AppointmentTime) VALUES ((SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}'),(SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'),'{}','{}')".format(CustomerFirstName,CustomerLastName,EmployeeFirstName,EmployeeLastName,AppointmentDate,AppointmentTime)
    execute_query(connection,query)
    query = "INSERT INTO AppointmentService (AppointmentID,ServiceID,AppointmentDate) VALUES ((SELECT AppointmentID FROM Appointment WHERE CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}') and AppointmentDate = '{}'),(SELECT ServiceID FROM Service WHERE ServiceName = '{}'),'{}')".format(CustomerFirstName,CustomerLastName,AppointmentDate,ServiceName,AppointmentDate)
    execute_query(connection,query)
    return ' Added Appointment'

@app.route('/Appointment/update/<int:id>',methods = ['GET'])
def ShowUpdateAppointment(id):
    query = "SELECT * FROM Appointment WHERE AppointmentID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Appointment/update/<int:id>',methods = ['PUT'])
def UpdateAppointment(id):
    request_data = request.get_json()
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    AppointmentDate = request_data['AppointmentDate']
    AppointmentTime = request_data['AppointmentTime']
    query = "UPDATE Appointment SET CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' AND CustomerLastName = '{}'),EmployeeID = (SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' AND EmployeeLastName = '{}'),AppointmentDate = '{}',AppointmentTime = '{}' WHERE AppointmentID = '{}'".format(CustomerFirstName,CustomerLastName,EmployeeFirstName,EmployeeLastName,AppointmentDate,AppointmentTime,id)
    execute_query(connection,query)
    return 'Updated Service'

@app.route('/Appointment/delete/<int:id>', methods = ['DELETE'])
def DeleteAppointment(id):
    query = "DELETE FROM Appointment WHERE AppointmentID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/Appointment')

@app.route('/AppointmentService/',methods = ['GET'])
def AppointmentService():
    query = "SELECT * FROM AppointmentService"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/AppointmentService/add',methods = ['POST'])
def AddAppointmentService():
    request_data = request.get_json()
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    AppointmentDate = request_data['AppointmentDate']
    ServiceName = request_data['ServiceName']
    query = "INSERT INTO AppointmentService (AppointmentID,ServiceID,AppointmentDate) VALUES ((SELECT AppointmentID FROM Appointment WHERE CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}') and AppointmentDate = '{}'),(SELECT ServiceID FROM Service WHERE ServiceName = '{}'),'{}')".format(CustomerFirstName,CustomerLastName,AppointmentDate,ServiceName,AppointmentDate)
    execute_query(connection,query)
    return 'Added Appointment Service'

@app.route('/AppointmentService/update/<int:id>',methods = ['PUT'])
def UpdateAppointmentService(id):
    request_data = request.get_json()
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    AppointmentDate = request_data['AppointmentDate']
    ServiceName = request_data['ServiceName']
    query = "UPDATE AppointmentService SET AppointmentID = (SELECT AppointmentID FROM Appointment WHERE CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}') and AppointmentDate = '{}'), ServiceID = (SELECT ServiceID FROM Service WHERE ServiceName = '{}'), AppointmentDate = '{}' WHERE AppointmentServiceID = '{}'".format(CustomerFirstName,CustomerLastName,AppointmentDate,ServiceName,AppointmentDate,id)
    execute_query(connection,query)
    return 'Update Appointment Service'

@app.route('/AppointmentService/update/<int:id>',methods = ['GET'])   
def GetAppointmentService(id):
    query = "SELECT AppointmentServiceID, Appointment.AppointmentID, Customer.CustomerID, Customer.CustomerFirstName, Customer.CustomerLastName, Service.ServiceID, Service.ServiceName, AppointmentService.AppointmentDate FROM AppointmentService JOIN Appointment ON Appointment.AppointmentID = AppointmentService.AppointmentID JOIN Service ON Service.ServiceID = AppointmentService.ServiceID JOIN Customer ON Customer.CustomerID = Appointment.CustomerID WHERE AppointmentServiceID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/AppointmentService/delete/<int:id>', methods = ['DELETE'])
def DeleteAppointmentService(id):
    query = "DELETE FROM AppointmentService WHERE AppointmentServiceID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/AppointmentService')

@app.route('/EmployeeSchedule/',methods = ['GET'])
def EmployeeSchedule():
    query = "SELECT * FROM EmployeeSchedule"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/EmployeeSchedule/add',methods = ['POST'])
def AddEmployeeSchedule():
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    ClockIn = request_data['ClockIn']
    ClockOut = request_data['ClockOut']
    DayofWeek = request_data['DayofWeek']
    Day = datetime.datetime.strptime(DayofWeek, "%Y-%m-%d")
    Day = Day.strftime('%A')
    query = "INSERT INTO EmployeeSchedule (EmployeeID,DaysofOperationID,EmployeeFirstName,EmployeeLastName,DayofWeek,ClockIn,ClockOut) VALUES ((SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'),(SELECT DaysofOperationID FROM DaysofOperation WHERE DayName = '{}'),'{}','{}','{}','{}','{}')".format(EmployeeFirstName,EmployeeLastName,Day,EmployeeFirstName,EmployeeLastName,DayofWeek,ClockIn,ClockOut)
    execute_query(connection,query)
    return 'Added EmployeeSchedule'

@app.route('/EmployeeSchedule/update/<int:id>',methods = ['PUT'])
def UpdateEmployeeSchedule(id):
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    ClockIn = request_data['ClockIn']
    ClockOut = request_data['ClockOut']
    DayofWeek = request_data['Date']
    Day = datetime.datetime.strptime(DayofWeek, "%m/%d/%Y")
    Day = Day.strftime('%A')
    query = "UPDATE EmployeeSchedule SET EmployeeID = (SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'), DaysofOperationID = (SELECT DaysofOperationID FROM DaysofOperation WHERE DayName = '{}'), EmployeeFirstName = '{}', EmployeeLastName = '{}', DayofWeek = '{}', ClockIn = '{}', ClockOut = '{}' WHERE ScheduleID = '{}')".format(EmployeeFirstName,EmployeeLastName,Day,EmployeeFirstName,EmployeeLastName,DayofWeek,ClockIn,ClockOut,id)
    execute_query(connection,query)
    return 'Updated EmployeeSchedule'

@app.route('/EmployeeSchedule/update/<int:id>',methods = ['GET'])
def GetEmployeeSchedule(id):
    query = "SELECT * FROM EmployeeSchedule WHERE ScheduleID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/EmployeeSchedule/delete/<int:id>', methods = ['DELETE'])
def DeleteEmployeeSchedule(id):
    query = "DELETE FROM EmployeeSchedule WHERE ScheduleID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/EmployeeSchedule')

@app.route('/AcquiredSkill/',methods = ['GET'])
def AcquiredSkill():
    query = "SELECT * FROM AcquiredSkill"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/AcquiredSkill/add',methods = ['POST'])
def AddAcquiredSkill():
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    Skill = request_data['SkillName']
    DateAcq = request_data['DateAcq']
    AcqSkillInstitution = request_data['AcqSkillInstitution']
    AcqSkillState = request_data['AcqSkillState']
    query = "INSERT INTO AcquiredSkill (EmployeeID,SkillID,DateAcq,SkillName,AcqSkillInstitution,AcqSkillState) VALUES ((SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'),(SELECT SkillID FROM Skill WHERE SkillName = '{}'),'{}','{}','{}','{}')".format(EmployeeFirstName,EmployeeLastName,Skill,DateAcq,Skill,AcqSkillInstitution,AcqSkillState)
    execute_query(connection,query)
    return 'Added Acquired Skill'

@app.route('/AcquiredSkill/update/<int:id>', methods = ['PUT'])
def UpdateAcquiredSkill(id):
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    SkillName = request_data['SkillName']
    DateAcq = request_data['DateAcq']
    AcqSkillInstitution = request_data['AcqSkillInstitution']
    AcqSkillState = request_data['AcqSkillState']
    query = "UPDATE AcquiredSkill SET EmployeeID = (SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'), SkillID = (SELECT SkillID FROM Skill WHERE SkillName = '{}'), DateAcq = '{}', SkillName = '{}', AcqSkillInstitution = '{}', AcqSkillState = '{}' WHERE AcquiredSkillID = '{}'".format(EmployeeFirstName,EmployeeLastName,SkillName,DateAcq,SkillName,AcqSkillInstitution,AcqSkillState,id)
    execute_query(connection,query)
    return 'Updated Acquired Skill'

@app.route('/AcquiredSkill/update/<int:id>',methods = ['GET'])
def GetAcquiredSkill(id):
    query ="SELECT AcquiredSkillID,Employee.EmployeeID,Employee.EmployeeFirstName,Employee.EmployeeLastName,SkillID,DateAcq,SkillName,AcqSkillInstitution,AcqSkillState FROM AcquiredSkill JOIN Employee ON Employee.EmployeeID = AcquiredSkill.EmployeeID WHERE AcquiredSkillID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/AcquiredSkill/delete/<int:id>', methods = ['DELETE'])
def DeleteAcquiredSkill(id):
    query = "DELETE FROM AcquiredSkill WHERE AcquiredSkillID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/AcquiredSkill')


@app.route('/RequiredSkill/',methods = ['GET'])
def RequiredSkill():
    query = "SELECT * FROM RequiredSkill"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/RequiredSkill/add',methods = ['POST'])
def AddRequiredSkill():
    request_data = request.get_json()
    ServiceName = request_data['ServiceName']
    SkillName = request_data['SkillName']
    query = "INSERT INTO RequiredSkill (ServiceID, SkillID,SkillName,ServiceName) VALUES ((SELECT ServiceID FROM Service WHERE ServiceName = '{}'),(SELECT SkillID FROM Skill WHERE SkillName = '{}'),'{}','{}')".format(ServiceName,SkillName,SkillName,ServiceName)
    execute_query(connection,query)
    return 'Added Required Skill'

@app.route('/RequiredSkill/update/<int:id>', methods = ['PUT'])
def UpdateRequiredSkill(id):
    request_data = request.get_json()
    ServiceName = request_data['ServiceName']
    SkillName = request_data['SkillName']
    query = "UPDATE RequiredSkill SET ServiceID = (SELECT ServiceID FROM Service WHERE ServiceName = '{}'), SkillID = (SELECT SkillID FROM Skill WHERE SkillName = '{}'), SkillName = '{}', ServiceName = '{}' WHERE RequiredSkillID = '{}'".format(ServiceName,SkillName,SkillName,ServiceName,id)
    execute_query(connection,query)
    return 'Updated Required Skill'

@app.route('/RequiredSkill/update/<int:id>',methods = ['GET'])
def GetRequiredSkill(id):
    query = "SELECT * FROM RequiredSkill WHERE RequiredSkillID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/RequiredSkill/delete/<int:id>', methods = ['DELETE'])
def DeleteRequiredSkill(id):
    query = "DELETE FROM RequiredSkill WHERE RequiredSkillID = {}".format(id)
    execute_query(connection,query)
    return redirect('/RequiredSkill')


@app.route('/EmployeeRole/', methods = ['GET'])
def EmployeeRole():
    query = "SELECT * FROM EmployeeRole"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)


@app.route('/EmployeeRole/add', methods = ['POST'])
def AddEmployeeRole():
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    RoleTitle = request_data['RoleTitle']
    YearofRole = request_data['YearofRole']
    query = "INSERT INTO EmployeeRole (EmployeeID,RoleID,YearofRole) VALUES ((SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'),(SELECT RoleID FROM Role WHERE RoleTitle = '{}'),'{}')".format(EmployeeFirstName,EmployeeLastName,RoleTitle,YearofRole)
    execute_query(connection,query)
    return 'Add Employee Role'

@app.route('/EmployeeRole/update/<int:id>', methods = ['PUT'])
def UpdateEmployeeRole(id):
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    RoleTitle = request_data['RoleTitle']
    YearofRole = request_data['YearofRole']
    query = "UPDATE EmployeeRole SET EmployeeID = (SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'), RoleID = (SELECT RoleID FROM Role WHERE RoleTitle = '{}'), YearofRole = '{}' WHERE EmployeeRoleID = '{}'".format(EmployeeFirstName,EmployeeLastName,RoleTitle,YearofRole,id)
    execute_query(connection,query)
    return 'Updated Employee Role'

@app.route('/EmployeeRole/update/<int:id>',methods = ['GET'])
def GetEmployeeRolel(id):
    query = "SELECT Employee.EmployeeFirstName,Employee.EmployeeLastName,Role.RoleTitle,YearofRole FROM EmployeeRole JOIN Employee ON Employee.EmployeeID = EmployeeRole.EmployeeID JOIN Role ON Role.RoleID = EmployeeRole.RoleID WHERE EmployeeRoleID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)



@app.route('/EmployeeRole/delete/<int:id>', methods = ['DELETE'])
def DeleteEmployeeRole(id):
    query = "DELETE FROM EmployeeRole WHERE EmployeeRoleID = {}".format(id)
    execute_query(connection,query)
    return redirect('/EmployeeRole')


@app.route('/Satisfaction/', methods = ['GET'])
def Satisfaction():
    query = "SELECT * FROM Satisfaction"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Satisfaction/add', methods = ['POST'])
def AddSatisfaction():
    request_data = request.get_json()
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    AppointmentDate = request_data['AppointmentDate']
    AppointmentSatisfaction = request_data['AppointmentSatisfaction']
    Comment = 'None'
    query = "INSERT INTO Satisfaction (AppointmentID,EmployeeID,SatisfactionMeaningID,AppointmentSatisfaction,Comments) VALUES ((SELECT AppointmentID FROM Appointment WHERE CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}') and AppointmentDate = '{}'),(SELECT EmployeeID FROM Appointment WHERE CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}') and AppointmentDate = '{}'),(SELECT SatisfactionMeaningID FROM SatisfactionMeaning WHERE AppointmentSatisfaction = '{}'),'{}','{}')".format(CustomerFirstName,CustomerLastName,AppointmentDate,CustomerFirstName,CustomerLastName,AppointmentDate,AppointmentSatisfaction,AppointmentSatisfaction,Comment)
    execute_query(connection,query)
    return 'Added Satisfaction'

@app.route('/Satisfaction/update/<int:id>', methods = ['GET'])
def GetSatisfaction(id):
    query = "SELECT SatisfactionID, Appointment.AppointmentID, Appointment.AppointmentDate,Customer.CustomerFirstName, Customer.CustomerLastName, Employee.EmployeeID, Employee.EmployeeFirstName, Employee.EmployeeLastName, AppointmentSatisfaction, Comments FROM Satisfaction JOIN Appointment ON Appointment.AppointmentID = Satisfaction.AppointmentID JOIN Customer ON Customer.CustomerID = Appointment.CustomerID JOIN Employee ON Employee.EmployeeID = Satisfaction.EmployeeID WHERE SatisfactionID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Satisfaction/update/<int:id>', methods = ['PUT'])
def UpdateSatisfaction(id):
    request_data = request.get_json()
    CustomerFirstName = request_data['CustomerFirstName']
    CustomerLastName = request_data['CustomerLastName']
    AppointmentDate = request_data['AppointmentDate']
    AppointmentSatisfaction = request_data["AppointmentSatisfaction"]
    Comments = request_data["Comments"]
    query = "UPDATE Satisfaction SET AppointmentID = (SELECT AppointmentID FROM Appointment WHERE CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}') and AppointmentDate = '{}'), EmployeeID = (SELECT EmployeeID FROM Appointment WHERE CustomerID = (SELECT CustomerID FROM Customer WHERE CustomerFirstName = '{}' and CustomerLastName = '{}') and AppointmentDate = '{}'), SatisfactionMeaningID = (SELECT SatisfactionMeaningID FROM SatisfactionMeaning WHERE AppointmentSatisfaction = '{}'), AppointmentSatisfaction = '{}', Comments = '{}' WHERE SatisfactionID = '{}'".format(CustomerFirstName,CustomerLastName,AppointmentDate,CustomerFirstName,CustomerLastName,AppointmentDate,AppointmentSatisfaction,AppointmentSatisfaction,Comments,id)
    execute_query(connection,query)
    return 'Updated Satisfaction'

@app.route('/Satisfaction/delete/<int:id>', methods = ['DELETE'])
def DeleteSatisfaction(id):
    query = "DELETE FROM Satisfaction WHERE SatisfactionID = {}".format(id)
    execute_query(connection,query)
    return redirect('/EmployeeRole')



@app.route('/EmployeeTimeOff/', methods = ['GET'])
def EmployeeTimeOff():
    query = "SELECT * FROM EmployeeTimeOff"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/EmployeeTimeOff/add',methods = ['POST'])
def AddEmployeeTimeOff():
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    StartTimeOffDate = request_data['StartTimeOffDate']
    AvailabilityDate = request_data['AvailabilityDate']
    Reason = request_data['Reason']
    query = "INSERT INTO EmployeeTimeOff (EmployeeID, StartTimeOffDate, AvailabilityDate,Reason) VALUES ((SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'),'{}','{}','{}')".format(EmployeeFirstName,EmployeeLastName,StartTimeOffDate,AvailabilityDate,Reason)
    execute_query(connection,query)
    return 'Added Employee Time Off'

@app.route('/EmployeeTimeOff/update/<int:id>',methods = ['PUT'])
def UpdateEmployeeTimeOff(id):
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    StartTimeOffDate = request_data['StartTimeOffDate']
    AvailabilityDate = request_data['AvailabilityDate']
    Reason = request_data['Reason']
    query = "UPDATE EmployeetimeOff SET EmployeeID = (SELECT EmployeeID FROM Employee WHERE EmployeeFirstName = '{}' and EmployeeLastName = '{}'), StartTimeOffDate = '{}', AvailabilityDate = '{}', Reason = '{}'".format(EmployeeFirstName,EmployeeLastName,StartTimeOffDate,AvailabilityDate,Reason)
    execute_query(connection,query)
    return 'Updated Employee Time Off'

@app.route('/EmployeeTimeOff/update/<int:id>', methods = ['GET'])
def GetEmployeeTimeOff(id):
    query = "SELECT Employee.EmployeeFirstName,Employee.EmployeeLastName,StartTimeOffDate,AvailabilityDate,Reason FROM EmployeeTimeOff JOIN Employee ON Employee.EmployeeID = EmployeeTimeOff.EmployeeID WHERE EmployeeTimeOffID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)


@app.route('/EmployeeTimeOff/delete/<int:id>', methods = ['DELETE'])
def DeleteEmployeeTimeOff(id):
    query = "DELETE FROM EmployeeTimeOff WHERE EmployeeTimeOffID = {}".format(id)
    execute_query(connection,query)
    return redirect('/EmployeeTimeOff')


@app.route('/ServiceInclusion/', methods = ['GET'])
def ServiceInclusion():
    query = "SELECT * FROM ServiceInclusion"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/ServiceInclusion/add',methods = ['POST'])
def AddServiceInclusion():
    request_data = request.get_json()
    ServiceName = request_data['ServiceName']
    InclusionName = request_data['InclusionName']
    query = "INSERT INTO ServiceInclusion (ServiceID,InclusionID,InclusionName) VALUES ((SELECT ServiceID FROM Service WHERE ServiceName = '{}'), (SELECT InclusionID FROM Inclusion WHERE InclusionName = '{}'),'{}')".format(ServiceName,InclusionName,InclusionName)
    execute_query(connection,query)
    return 'Added Service Inclusion'

@app.route('/ServiceInclusion/update/<int:id>', methods = ['PUT'])
def UpdateServiceInclusion(id):
    request_data = request.data.get_json()
    ServiceName = request_data['ServiceName']
    InclusionName = request_data['InclusionName']
    query = "UPDATE ServiceInclusion SET ServiceID = (SELECT ServiceID FROM Service WHERE ServiceName = '{}'), InclusionID = (SELECT InclusionID FROM Inclusion WHERE InclusionName = '{}'),'{}' WHERE ServiceInclusion = '{}'".format(ServiceName,InclusionName,InclusionName,id)
    execute_query(connection,query)
    return 'Updated Service Inclusion'


@app.route('/ServiceInclusion/update/<int:id>', methods = ['GET'])
def GETServiceInclusion(id):
    query = "SELECT ServiceInclusionID, Service.ServiceID, Service.ServiceName, InclusionID, InclusionName FROM ServiceInclusion JOIN Service ON Service.ServiceID = ServiceInclusion.ServiceID WHERE ServiceInclusionID ='{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/ServiceInclusion/delete/<int:id>', methods = ['DELETE'])
def DeleteServiceInclusion(id):
    query = "DELETE FROM ServiceInclusion WHERE ServiceInclusionID = {}".format(id)
    execute_query(connection,query)
    return redirect('/ServiceInclusion')


@app.route('/ServiceTool/',methods = ['GET'])
def ServiceTool():
    query = "SELECT * FROM ServiceTool"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/ServiceTool/add',methods = ['POST'])
def AddServiceTool():
    request_data = request.get_json()
    ToolName = request_data['ToolName']
    ServiceName = request_data['ServiceName']
    Quantity = request_data['Quantity']
    Unit = request_data['Unit']
    query = "INSERT INTO ServiceTool (ToolID,ServiceID,Quantity,Unit) VALUES ((SELECT ToolID FROM Tool WHERE ToolName = '{}'),(SELECT ServiceID FROM Service WHERE ServiceName = '{}'),'{}','{}')".format(ToolName,ServiceName,Quantity,Unit)
    execute_query(connection,query)
    return 'Added Service Tool'

@app.route('/ServiceTool/update/<int:id>',methods = ['PUT'])
def UpdateServiceTool(id):
    request_data = request.get_json()
    ToolName = request_data['ToolName']
    ServiceName = request_data['ServiceName']
    Quantity = request_data['Quantity']
    Unit = request_data['Unit']
    query = "UPDATE ServiceTool SET ToolID = (SELECT ToolID FROM Tool WHERE ToolName = '{}'), ServiceID = (SELECT ServiceID FROM Service WHERE ServiceName = '{}'), Quantity = '{}', Unit = '{}' WHERE ServiceToolID = '{}'".format(ToolName,ServiceName,Quantity,Unit,id)
    execute_query(connection,query)
    return 'Update Service Tool'

@app.route('/ServiceTool/update/<int:id>',methods = ['GET'])
def GetServiceTool(id):
    query = "SELECT ServiceToolID, Tool.ToolID, Tool.ToolName, Service.ServiceID, Service.ServiceName, Quantity, Unit FROM ServiceTool JOIN Service ON Service.ServiceID = ServiceTool.ServiceID JOIN Tool ON Tool.ToolID = ServiceTool.ToolID WHERE ServiceToolID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/ServiceTool/delete/<int:id>', methods = ['DELETE'])
def DeleteServiceTool(id):
    query = "DELETE FROM ServiceTool WHERE ServiceToolID = {}".format(id)
    execute_query(connection,query)
    return redirect('/ServiceTool')

@app.route('/ToolManufacturer/', methods = ['GET'])
def ToolManufacturer():
    query = "SELECT * FROM ToolManufacturer"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/ToolManufacturer/add',methods = ['POST'])
def AddToolManufacturer():
    request_data = request.get_json()
    ManufacturerName = request_data['ManufacturerName']
    ToolName = request_data['ToolName']
    ToolManufacturerName = request_data['ToolManufacturerName']
    query = "INSERT INTO ToolManufacturer (ManufacturerID,ToolID,ToolName,ToolManufacturerName) VALUES ((SELECT ManufacturerID FROM Manufacturer WHERE ManufacturerName = '{}'),(SELECT ToolID FROM Tool WHERE ToolName = '{}'),'{}','{}')".format(ManufacturerName,ToolName,ToolName,ToolManufacturerName)
    execute_query(connection,query)
    return 'Add Tool Manufacturer'

@app.route('/ToolManufacturer/update/<int:id>',methods = ['PUT'])
def UpdateToolManufacturer(id):
    request_data = request.get_json()
    ManufacturerName = request_data['ManufacturerName']
    ToolName = request_data['ToolName']
    ToolManufacturerName = request_data['ToolManufacturerName']
    query = "UPDATE ToolManufacturer SET ManufacturerID = (SELECT ManufacturerID FROM Manufacturer WHERE ManufacturerName = '{}'), ToolID = (SELECT ToolID FROM Tool WHERE ToolName = '{}'), ToolName = '{}', ToolManufacturerName = '{}' WHERE ToolManufacturerID = '{}'".format(ManufacturerName,ToolName,ToolName,ToolManufacturerName,id)
    execute_query(connection,query)
    return 'Update Tool Manufacturer'

@app.route('/ToolManufacturer/update/<int:id>', methods = ['GET'])
def GetToolManufacturer(id):
    query = "SELECT ToolManufacturerID, Manufacturer.ManufacturerID, Manufacturer.ManufacturerName, Tool.ToolID, Tool.ToolName, ToolManufacturer.ToolManufacturerName FROM ToolManufacturer JOIN Manufacturer ON Manufacturer.ManufacturerID = ToolManufacturer.ManufacturerID JOIN Tool ON Tool.ToolID = ToolManufacturer.ToolID WHERE ToolManufacturerID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)
    
@app.route('/ToolManufacturer/delete/<int:id>', methods = ['DELETE'])
def DeleteToolManufacturer(id):
    query = "DELETE FROM ToolManufacturer WHERE ToolManufacturerID = {}".format(id)
    execute_query(connection,query)
    return redirect('/ToolManufacturer')

@app.route('/HairServiceProduct/',methods = ['GET'])
def HairServiceProduct():
    query = "SELECT * FROM HairServiceProduct"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/HairServiceProduct/add',methods = ['POST'])
def AddHairServiceProduct():
    request_data = request.get_json()
    ProductName = request_data['ProductName']
    ServiceName = request_data['ServiceName']
    QuantityUsed = request_data['QuantityUsed']
    ProductVolume = request_data['ProductVolume']
    query = "INSERT INTO HairServiceProduct (ProductID,ServiceID,ProductName,QuantityUsed,ProductVolume) VALUES ((SELECT ProductID FROM HairProduct WHERE ProductName = '{}'),(SELECT ServiceID FROM Service WHERE ServiceName = '{}'),'{}','{}','{}')".format(ProductName,ServiceName,ProductName,QuantityUsed,ProductVolume)
    execute_query(connection,query)
    return 'Add Product to Service'

@app.route('/HairServiceProduct/update/<int:id>', methods = ['PUT'])
def UpdateHairServiceProduct(id):
    request_data = request.get_json()
    ProductName = request_data['ProductName']
    ServiceName = request_data['ServiceName']
    QuantityUsed = request_data['QuantityUsed']
    ProductVolume = request_data['ProductVolume']
    query = "UPDATE HairServiceProduct SET ProductID = (SELECT ProductID FROM HairProduct WHERE ProductName = '{}'), ServiceID = (SELECT ServiceID FROM Service WHERE ServiceName = '{}'), ProductName = '{}', QuantityUsed = '{}', ProductVolume = '{}' WHERE ServiceProductID = '{}'".format(ProductName,ServiceName,ProductName,QuantityUsed,ProductVolume,id)
    execute_query(connection,query)
    return 'Update HairServiceProduct'

@app.route('/HairServiceProduct/update/<int:id>', methods = ['GET'])
def GetUpdateHairServiceProduct(id):
    query = "SELECT ServiceProductID, HairProduct.ProductID, HairProduct.ProductName, Service.ServiceID, Service.ServiceName, QuantityUsed, HairServiceProduct.ProductVolume FROM HairServiceProduct JOIN HairProduct ON HairProduct.ProductID = HairServiceProduct.ProductID JOIN Service ON Service.ServiceID = HairServiceProduct.ServiceID WHERE ServiceProductID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/HairServiceProduct/delete/<int:id>', methods = ['DELETE'])
def DeleteHairServiceProduct(id):
    query = "DELETE FROM HairServiceProduct WHERE ServiceProductID = {}".format(id)
    execute_query(connection,query)
    return redirect('/HairServiceProduct')


@app.route('/HairProductManufacturer/',methods = ['GET'])
def HairProductManufacturer():
    query = "SELECT * FROM HairProductManufacturer"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/HairProductManufacturer/add',methods = ['POST'])
def AddHairProductManufacturer():
    request_data = request.get_json()
    ProductName = request_data['ProductName']
    ManufacturerName = request_data['ManufacturerName']
    HairProductManufacturerName = request_data['HairProductManufacturerName']
    query = "INSERT INTO HairProductManufacturer (ProductID,ManufacturerID,ProductName,HairProductManufacturerName) VALUES ((SELECT ProductID FROM HairProduct WHERE ProductName = '{}'), (SELECT ManufacturerID FROM Manufacturer WHERE ManufacturerName = '{}'), '{}','{}')".format(ProductName,ManufacturerName,ProductName,HairProductManufacturerName)
    execute_query(connection,query)
    return 'Add Hair Product Manufaccturer'

@app.route('/HairProductManufacturer/update/<int:id>', methods = ['PUT'])
def UpdateHairProductManucafacturer(id):
    request_data = request.get_json()
    ProductName = request_data['ProductName']
    ManufacturerName = request_data['ManufacturerName']
    HairProductManufacturerName = request_data['HairProductManufacturerName']
    query = "UPDATE HairProductManufacturer SET ProductID = (SELECT ProductID FROM HairProduct WHERE ProductName = '{}'), ManufacturerID = (SELECT ManufacturerID FROM Manufacturer WHERE ManufacturerName = '{}'), ProductName = '{}', HairProductManufacturerName = '{}' WHERE HairProductManufacturerID = '{}'".format(ProductName,ManufacturerName,ProductName,HairProductManufacturerName,id)
    execute_query(connection,query)
    return 'Update Hair Product Manufaccturer'

@app.route('/HairProductManufacturer/update/<int:id>', methods = ['GET'])
def GetHairProductManufacturer(id):
    query = "SELECT HairProductManufacturerID, HairProduct.ProductID, HairProduct.ProductName, Manufacturer.ManufacturerID, Manufacturer.ManufacturerName, HairProductManufacturer.HairProductManufacturerName FROM HairProductManufacturer JOIN HairProduct ON HairProduct.ProductID = HairProductManufacturer.ProductID JOIN Manufacturer ON Manufacturer.ManufacturerID = HairProductManufacturer.ManufacturerID WHERE HairProductManufacturerID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/HairProductManufacturer/delete/<int:id>', methods = ['DELETE'])
def DeleteHairProductManufacturer(id):
    query = "DELETE FROM HairProductManufacturer WHERE HairProductManufacturerID = {}".format(id)
    execute_query(connection,query)
    return redirect('/HairProductManufacturer')

    
@app.route('/Employee/',methods = ['GET'])
def Employee():
    query = "SELECT * FROM Employee"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)


@app.route('/Employee/add',methods = ['POST'])
def AddEmployee():
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    RankTitle = request_data['RankTitle']
    EmployeeHomeNumber = request_data['EmployeeHomeNumber']
    EmployeeCellNumber = request_data['EmployeeCellNumber']
    Country = request_data['Country']
    State = request_data['State']
    EmployeeStreetName = request_data['EmployeeStreetName']
    EmployeeCity = request_data['EmployeeCity']
    EmployeeZipCode = request_data['EmployeeZipCode']
    HireDate = request_data['HireDate']
    EmployeeStatus = request_data['EmployeeStatus']
    query = "INSERT INTO Employee (EmployeeFirstName,EmployeeLastName,EmployeeRankID,EmployeeHomeNumber,EmployeeCellNumber,CountryID,StateID,EmployeeStreetName,EmployeeCity,EmployeeZipCode,HireDate,EmployeeStatusID) VALUES ('{}','{}',(SELECT EmployeeRankID FROM EmployeeRank WHERE RankTitle = '{}'),'{}','{}',(SELECT CountryID FROM Country WHERE CountryName = '{}'),(SELECT StateID FROM State WHERE StateInitial = '{}'),'{}','{}','{}','{}',(SELECT EmployeeStatusID FROM EmployeeStatus WHERE StatusDescription = '{}'))".format(EmployeeFirstName,EmployeeLastName,RankTitle,EmployeeHomeNumber,EmployeeCellNumber,Country,State,EmployeeStreetName,EmployeeCity,EmployeeZipCode,HireDate,EmployeeStatus)
    execute_query(connection,query)
    return 'Add Employee'

@app.route('/Employee/update/<int:id>',methods = ['PUT'])
def UpdateEmployee(id):
    request_data = request.get_json()
    EmployeeFirstName = request_data['EmployeeFirstName']
    EmployeeLastName = request_data['EmployeeLastName']
    RankTitle = request_data['RankTitle']
    EmployeeHomeNumber = request_data['EmployeeHomeNumber']
    EmployeeCellNumber = request_data['EmployeeCellNumber']
    Country = request_data['Country']
    State = request_data['State']
    EmployeeStreetName = request_data['EmployeeStreetName']
    EmployeeCity = request_data['EmployeeCity']
    EmployeeZipCode = request_data['EmployeeZipCode']
    HireDate = request_data['HireDate']
    EmployeeStatus = request_data['EmployeeStatus']
    query = "UPDATE Employee SET EmployeeFirstName = '{}',EmployeeLastName = '{}',EmployeeRankID = (SELECT EmployeeRankID FROM EmployeeRank WHERE RankTitle = '{}'),EmployeeHomeNumber = '{}',EmployeeCellNumber = '{}',CountryID = (SELECT CountryID FROM Country WHERE CountryName = '{}'), StateID = (SELECT StateID FROM State WHERE StateInitial = '{}'),EmployeeStreetName = '{}',EmployeeCity = '{}',EmployeeZipCode = '{}',HireDate = '{}',EmployeeStatusID = (SELECT EmployeeStatusID FROM EmployeeStatus WHERE StatusDescription = '{}') WHERE EmployeeID = '{}'".format(EmployeeFirstName,EmployeeLastName,RankTitle,EmployeeHomeNumber,EmployeeCellNumber,Country,State,EmployeeStreetName,EmployeeCity,EmployeeZipCode,HireDate,EmployeeStatus,id)
    execute_query(connection,query)
    return 'Update Employee'

@app.route('/Employee/update/<int:id>',methods = ['GET'])
def GetEmployee(id):
    query = "SELECT EmployeeID,EmployeeFirstName,EmployeeLastName,EmployeeRank.RankTitle, EmployeeHomeNumber, EmployeeCellNumber, Country.CountryID, Country.CountryInitial, State.StateID, State.StateInitial, EmployeeStreetName, EmployeeCity, EmployeeZipCode, HireDate, EmployeeStatus.EmployeeStatusID, EmployeeStatus.StatusDescription FROM Employee JOIN EmployeeRank ON EmployeeRank.EmployeeRankID = Employee.EmployeeRankID JOIN Country ON Country.CountryID  = Employee.CountryID JOIN State ON State.StateID = Employee.StateID JOIN EmployeeStatus ON EmployeeStatus.EmployeeStatusID = Employee.EmployeeStatusID WHERE EmployeeID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Employee/delete/<int:id>', methods = ['DELETE'])
def DeleteEmployee(id):
    query = "DELETE FROM Employee WHERE EmployeeID = {}".format(id)
    execute_query(connection,query)
    return redirect('/Employee')

@app.route('/EmployeeStatus/',methods = ['GET'])
def EmployeeStatus():
    query = "SELECT * FROM EmployeeStatus"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)


@app.route('/EmployeeStatus/add', methods = ['POST'])
def AddEmployeeStatus():
    request_data = request.get_json()
    EmployeeStatusID = request_data['EmployeeStatusID']
    StatusDescription = request_data["StatusDescription"]
    query = "INSERT into EmployeeStatus (EmployeeStatusID,StatusDescription) VALUES ('{}','{}')".format(EmployeeStatusID, StatusDescription)
    execute_query(connection,query)
    return "Add Employee Status"

@app.route('/EmployeeStatus/update/<int:id>', methods = ['PUT'])
def UpdateEmployeeStatus(id):
    request_data = request.get_json()
    StatusDescription = request_data['StatusDescription']
    query = "UPDATE EmployeeStatus SET StatusDescription = '{}' where EmployeeStatusID = '{}'".format(StatusDescription,id)
    execute_query(connection,query)
  
    return "Update Employee Status"

@app.route('/EmployeeStatus/delete/<int:id>', methods = ['DELETE'])
def DeleteEmployeeStatus(id):
     query = "DELETE from EmployeeStatus WHERE EmployeeStatusID = '{}'".format(id)
     execute_query(connection,query)
     return redirect('/EmployeeStatus')

@app.route('/CustomerStatus/',methods = ['GET'])
def CustomerStatus():
    query = "SELECT * FROM CustomerStatus"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/CustomerStatus/add', methods = ['POST'])
def AddCustomerStatus():
    request_data = request.get_json()
    CustomerStatusID = request_data['CustomerStatusID']
    StatusDescription = request_data['StatusDescription']
    query = "INSERT INTO CustomerStatus (CustomerStatusID,StatusDescription) VALUES ('{}','{}')".format(CustomerStatusID,StatusDescription)
    execute_query(connection,query)
    return 'Added Customer Status'


@app.route('/CustomerStatus/update/<int:id>',methods = ['PUT'])
def UpdateCustomerStatus(id):
    request_data = request.get_json()
    StatusDescription = request_data['StatusDescription']
    query = "UPDATE CustomerStatus SET StatusDescription = '{}' where CustomerID = '{}'".format(StatusDescription,id)
    execute_query(connection,query)  
    return "Updated Customer Status"

@app.route('/CustomerStatus/delete/<int:id>', methods = ['DELETE'])
def DeleteCustomerStatus(id):
    query = "DELETE FROM CustomerStatus WHERE CustomerStatusID = {}".format(id)
    execute_query(connection,query)
    return redirect('/CustomerStatus')

@app.route('/BusinessHours/',methods = ['GET'])
def DayOfOperation():
    query = "SELECT * FROM DaysofOperation"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/BusinessHours/add', methods = ['POST'])
def AddDayOfOperation():
    request_data = request.get_json()
    DaysofOperationID = request_data['DaysfOperationID']
    DayName = request_data['DayName']
    IsActive = request_data['IsActive']
    query = "INSERT into DaysofOperation (DaysofOperationID, DayName, IsActive) VALUES('{}','{}','{}')".format(DaysofOperationID,DayName,IsActive)
    execute_query(connection,query)
    return "Add Day Of Operation"

@app.route('/BusinessHours/update/<int:id>', methods = ['PUT'])
def UpdateDayOfOperation(id):
    request_data = request.get_json()
    DayName = request_data['DayName']
    IsActive = request_data['IsActive']
    query = "UPDATE DaysofOperation SET DayName = '{}' where DaysofOperationID = '{}'".format(DayName,id)
    execute_query(connection,query)
    query = "UPDATE DaysofOperation SET IsActive = '{}' where DaysofOperationID = '{}'".format(IsActive,id)
    execute_query(connection,query)
    return "Updated Day Of Operation"

@app.route('/BusinessHours/delete/<int:id>', methods =['DELETE'])
def DeleteDayOfOperation(id):
    query = "DELETE from DaysofOperation WHERE DaysofOperationID= '{}'".format(id)
    execute_query(connection,query)
    return redirect('/BusinessHours')

@app.route('/Tool/',methods = ['GET'])
def Tool():
    query = "SELECT * FROM Tool"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Tool/add', methods = ['POST'])
def AddTool():
    request_data = request.get_json()
    ToolID = request_data['ToolID']
    ToolName = request_data['ToolName']
    ToolDescription = request_data['ToolDescription']
    query = "INSERT into Tool (ToolID, ToolName, ToolDescription) VALUES('{}','{}','{}')".format(ToolID,ToolName,ToolDescription)
    execute_query(connection,query)
    return "Add Tool"

@app.route('/Tool/update/<int:id>', methods = ['PUT'])
def UpdateTool(id):
    request_data = request.get_json()
    ToolName = request_data['ToolName']
    ToolDescription = request_data['ToolDescription']
    query = "UPDATE Tool SET ToolName = '{}' where ToolID = '{}'".format(ToolName,id)
    execute_query(connection,query)
    query = "UPDATE Tool SET ToolDescription = '{}' where ToolID = '{}'".format(ToolDescription,id)
    execute_query(connection,query)
    return "Updated Day Of Operation"

@app.route('/Tool/delete/<int:id>', methods =['DELETE'])
def DeleteTool(id):
    query = "DELETE from Tool WHERE ToolID= '{}'".format(id)
    execute_query(connection,query)
    return redirect('/Tool')
"""
@app.route('/HairProduct/',methods = ['GET'])
def HairProduct():
    query = "SELECT * FROM HairProduct"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/HairProduct/add',methods = ['POST'])
def AddHairProduct():
    request_data = request.get_json()
    ProductType = request_data['ProductType']
    #Product type color differenciates the product type but it's up to you to add it
    ProductName = request_data['ProductName']
    ProductDescription = request_data['ProductDescription']
    ProductVolume = request_data['ProductVolume']
    query = "INSERT INTO HairServiceProduct (ProductType,ProductName,ProductDescription,ProductVolume) VALUES ((SELECT ProductTypeID FROM ProductType WHERE ProductType = '{}')), ProductName = '{}', ProductDescription = '{}', ProductVolume = '{}'".format(ProductType,ProductName,ProductDescription,ProductVolume)
    execute_query(connection,query)

@app.route('/HairProduct/update/<int:id>', methods = ['PUT'])
def UpdateHairProduct(id):
    request_data = request.get_json()
    ProductType = request_data['ProductType']
    ProductName = request_data['ProductName']
    ProductDescription = request_data['ProductDescription']
    ProductVolume = request_data['ProductVolume']
    query = "UPDATE HairProduct SET ProductTypeID = (SELECT ProductType FROM ProductType WHERE ProductType = '{}'), ProductName = '{}', ProductDescription = '{}', ProductVolume = '{}' WHERE ServiceProductID = '{}'".format(ProductType,ProductName,ProductDescription,ProductVolume,id)
    execute_query(connection,query)

@app.route('/HairProduct/delete/<int:id>', methods = ['DELETE'])
def DeleteHairProduct(id):
    query = "DELETE FROM HairProduct WHERE HairProductID = {}".format(id)
    execute_query(connection,query)
    return redirect('/EmployeeRole')
"""
#COUNTRY

@app.route('/Country/',methods = ['GET'])
def Country():
    query = "SELECT * FROM Country"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Country/add',methods = ['POST'])
def addCountry():
    request_data = request.get_json()
    CountryCode = request_data['CountryCode']
    CountryInitial = request_data['CountryInitial']
    CountryName = request_data['CountryName']
    query = "INSERT INTO Country (CountryCode, CountryInitial, CountryName) VALUES ('{}','{}','{}')".format(CountryCode, CountryInitial, CountryName)
    execute_query(connection,query)
    return 'Add Country'

@app.route('/Country/update/<int:id>',methods = ['PUT'])
def UpdateCountry(id):
    request_data = request.get_json()
    CountryCode = request_data['CountryCode']
    CountryInitial = request_data['CountryInitial']
    CountryName = request_data['CountryName']
    query = "UPDATE Country SET CountryCode = '{}',CountryInitial = '{}',CountryName = '{}' WHERE CountryID = '{}'".format(CountryCode, CountryInitial, CountryName,id)
    execute_query(connection,query)
    return 'Updated Country'

@app.route('/Country/update/<int:id>',methods = ['GET'])
def GETCustomer(id):
    query = "SELECT * FROM Country WHERE CountryID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Country/delete/<int:id>', methods = ['DELETE'])
def DeleteCountry(id):
    query = "DELETE FROM Country WHERE CountryID = {}".format(id)
    execute_query(connection,query)
    return redirect('/Country')

#STATE

@app.route('/State/',methods = ['GET'])
def State():
    query = "SELECT * FROM State"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/State/add',methods = ['POST'])
def addState():
    request_data = request.get_json()
    StateInitial = request_data['StateInitial']
    StateName = request_data['StateName']
    query = "INSERT INTO State (StateInitial, StateName) VALUES ('{}','{}')".format(StateInitial, StateName)
    execute_query(connection,query)
    return ' Add State'
@app.route('/State/update/<int:id>',methods = ['PUT'])
def UpdateState(id):
    request_data = request.get_json()
    StateInitial = request_data['StateInitial']
    StateName = request_data['StateName']
    query = "UPDATE State SET StateInitial = '{}',StateName = '{}' WHERE StateID = '{}'".format(StateInitial, StateName,id)
    execute_query(connection,query)
    return 'Updated State'

@app.route('/State/update/<int:id>',methods = ['GET'])
def GetState(id):
    query = "SELECT * FROM State WHERE StateID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/State/delete/<int:id>', methods = ['DELETE'])
def DeleteState(id):
    query = "DELETE FROM State WHERE StateID = {}".format(id)
    execute_query(connection,query)
    return redirect('/State')

#MANUFACTURER

@app.route('/Manufacturer/',methods = ['GET'])
def Manufacturer():
    query = "SELECT * FROM Manufacturer"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Manufacturer/add',methods = ['POST'])
def addManufacturer():
    request_data = request.get_json()
    ManufacturerName = request_data['ManufacturerName']
    Country = request_data['Country']
    ManufacturerPhoneNumber = request_data['ManufacturerPhoneNumber']
    ManufacturerEmail = request_data['ManufacturerEmail']
    query = "INSERT INTO Manufacturer (ManufacturerName, CountryID, ManufacturerPhoneNumber, ManufacturerEmail) VALUES ('{}',(SELECT CountryID FROM Country WHERE CountryName = '{}'),'{}','{}')".format(ManufacturerName, Country, ManufacturerPhoneNumber, ManufacturerEmail)
    execute_query(connection,query)
    return 'Add Manufacturer'

@app.route('/Manufacturer/update/<int:id>',methods = ['PUT'])
def UpdateManufacturer(id):
    request_data = request.get_json()
    ManufacturerName = request_data['ManufacturerName']
    Country = request_data['Country']
    ManufacturerPhoneNumber = request_data['ManufacturerPhoneNumber']
    ManufacturerEmail = request_data['ManufacturerEmail']
    query = "UPDATE Manufacturer SET ManufacturerName = '{}', CountryID = (SELECT CountryID FROM Country WHERE CountryInitial = '{}'), ManufacturerPhoneNumber = '{}', ManufacturerEmail = '{}' WHERE ManufacturerID = '{}'".format(ManufacturerName, Country, ManufacturerPhoneNumber, ManufacturerEmail,id)
    execute_query(connection,query)
    return 'Update Manufacturer'

@app.route('/Manufacturer/update/<int:id>',methods = ['GET'])
def GetManufacturer(id):
    query = "SELECT ManufacturerID, ManufacturerName, Country.CountryID, Country.CountryName, ManufacturerPhoneNumber, ManufacturerEmail FROM Manufacturer JOIN Country ON Country.CountryID = Manufacturer.CountryID WHERE ManufacturerID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Manufacturer/delete/<int:id>', methods = ['DELETE'])
def DeleteManufacturer(id):
    query = "DELETE FROM Manufacturer WHERE ManufacturerID = {}".format(id)
    execute_query(connection,query)
    return redirect('/Manufacturer')

#EMPLOYEE RANK

@app.route('/EmployeeRank/',methods = ['GET'])
def EmployeeRank():
    query = "SELECT * FROM EmployeeRank"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/EmployeeRank/add',methods = ['POST'])
def addEmployeeRank():
    request_data = request.get_json()
    RankTitle = request_data['RankTitle']
    query = "INSERT INTO EmployeeRank (RankTitle) VALUES ('{}')".format(RankTitle)
    execute_query(connection,query)
    return 'Add Employee Rank'

@app.route('/EmployeeRank/update/<int:id>',methods = ['PUT'])
def UpdateEmployeeRank(id):
    request_data = request.get_json()
    RankTitle = request_data['RankTitle']
    query = "UPDATE EmployeeRank SET RankTitle = '{}' WHERE EmployeeRankID = '{}'".format(RankTitle,id)
    execute_query(connection,query)
    return 'Update Employee Rank'

@app.route('/EmployeeRank/update/<int:id>',methods = ['GET'])
def GetEmployeeRank(id):
    query = "SELECT * FROM EmployeeRank WHERE EmployeeRankID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/EmployeeRank/delete/<int:id>', methods = ['DELETE'])
def DeleteEmployeeRank(id):
    query = "DELETE FROM EmployeeRank WHERE EmployeeRankID = {}".format(id)
    execute_query(connection,query)
    return redirect('/EmployeeRank')

#INCLUSION

@app.route('/Inclusion/',methods = ['GET'])
def Inclusion():
    query = "SELECT * FROM Inclusion"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Inclusion/add',methods = ['POST'])
def addInclusion():
    request_data = request.get_json()
    InclusionName = request_data['InclusionName']
    query = "INSERT INTO Inclusion (InclusionName) VALUES ('{}')".format(InclusionName)
    execute_query(connection,query)
    return 'Add Inclusion'

@app.route('/Inclusion/update/<int:id>',methods = ['PUT'])
def UpdateInclusion(id):
    request_data = request.get_json()
    InclusionName = request_data['InclusionName']
    query = "UPDATE Inclusion SET InclusionName = '{}' WHERE InclusionID = '{}'".format(InclusionName,id)
    execute_query(connection,query)
    return 'Update Inclusion'

@app.route('/Inclusion/update/<int:id>',methods = ['GET'])
def GetInclusion(id):
    query = "SELECT * FROM Inclusion WHERE InclusionID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Inclusion/delete/<int:id>', methods = ['DELETE'])
def DeleteInclusion(id):
    query = "DELETE FROM Inclusion WHERE InclusionID = {}".format(id)
    execute_query(connection,query)
    return redirect('/Inclusion')

@app.route('/Service/',methods = ['GET'])
def Service():
    query = "SELECT * FROM Service"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Service/add', methods = ['POST'])
def AddService():
    request_data = request.get_json()
    ServiceName = request_data['ServiceName']
    TypeofService = request_data['TypeofService']
    ServicePrice = request_data['ServicePrice']
    ServiceDuration = request_data['ServiceDuration']
    ServiceDescription = request_data['ServiceDescription']
    query = "INSERT INTO Service (ServiceName,TypeofService,ServicePrice,ServiceDuration,ServiceDescription) VALUES ('{}','{}','{}','{}','{}')".format(ServiceName, TypeofService, ServicePrice, ServiceDuration, ServiceDescription)
    execute_query(connection,query)
    return 'Added Service'

@app.route('/Service/update/<int:id>',methods = ['GET'])
def ShowUpdateService(id):
    query = "SELECT * FROM Service WHERE ServiceID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Service/update/<int:id>',methods = ['PUT'])
def UpdateService(id):
    request_data = request.get_json()
    ServiceName = request_data['ServiceName']
    TypeofService = request_data['TypeofService']
    ServicePrice = request_data['ServicePrice']
    ServiceDuration = request_data['ServiceDuration']
    ServiceDescription = request_data['ServiceDescription']
    query = "UPDATE Service SET ServiceName = '{}',TypeofService = '{}',ServicePrice = '{}',ServiceDuration = '{}',ServiceDescription = '{}' WHERE ServiceID = '{}'".format(ServiceName,TypeofService,ServicePrice,ServiceDuration,ServiceDescription,id)
    execute_query(connection,query)
    return 'Updated Service'

@app.route('/Service/delete/<int:id>', methods = ['DELETE'])
def DeleteService(id):
    query = "DELETE FROM Service WHERE ServiceID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/Service')

@app.route('/Skill/',methods = ['GET'])
def Skill():
    query = "SELECT * FROM Skill"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

# KEY ERROR WITH 'SkillName'
# FIXED! Check the Postman --> body --> raw and make sure it is in the right format
@app.route('/Skill/add', methods = ['POST'])
def AddSkill():
    request_data = request.get_json()
    SkillName = request_data['SkillName']
    query = "INSERT INTO Skill (SkillName) VALUES ('{}')".format(SkillName)
    execute_query(connection,query)
    return 'Added Skill'


@app.route('/Skill/update/<int:id>',methods = ['PUT'])
def UpdateSkill(id):
    request_data = request.get_json()
    SkillName = request_data['SkillName']
    query = "UPDATE Skill SET SkillName = '{}' WHERE SkillID = '{}'".format(SkillName,id)
    execute_query(connection,query)
    return 'Updated Skill'

@app.route('/Skill/update/<int:id>',methods = ['GET'])
def ShowUpdateskill(id):
    query = "SELECT * FROM Skill WHERE SkillID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Skill/delete/<int:id>', methods = ['DELETE'])
def DeleteSkill(id):
    query = "DELETE FROM Skill WHERE SkillID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/Skill')

@app.route('/Role/',methods = ['GET'])
def Role():
    query = "SELECT * FROM Role"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Role/add', methods = ['POST'])
def AddRole():
    request_data = request.get_json()
    RoleTitle = request_data['RoleTitle']
    RoleDescription = request_data['RoleDescription']
    query = "INSERT INTO Role (RoleTitle,RoleDescription) VALUES ('{}','{}')".format(RoleTitle,RoleDescription)
    execute_query(connection,query)
    return 'Added Role'

@app.route('/Role/update/<int:id>',methods = ['GET'])
def ShowUpdateRole(id):
    query = "SELECT * FROM Role WHERE RoleID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/Role/update/<int:id>',methods = ['PUT'])
def UpdateRole(id):
    request_data = request.get_json()
    RoleTitle = request_data['RoleTitle']
    RoleDescription = request_data['RoleDescription']
    query = "UPDATE Role SET RoleTitle = '{}', RoleDescription = '{}' WHERE RoleID = '{}'".format(RoleTitle,RoleDescription,id)
    execute_query(connection,query)
    return 'Updated Role'

@app.route('/Role/delete/<int:id>', methods = ['DELETE'])
def DeleteRole(id):
    query = "DELETE FROM Role WHERE RoleID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/Role')

@app.route('/SatisfactionMeaning/',methods = ['GET'])
def SatisfactionMeaning():
    query = "SELECT * FROM SatisfactionMeaning"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/SatisfactionMeaning/add', methods = ['POST'])
def AddSatisfactionMeaning():
    request_data = request.get_json()
    AppointmentSatisfaction = request_data['AppointmentSatisfaction']
    SatisfactionMeaning = request_data['SatisfactionMeaning']
    query = "INSERT INTO SatisfactionMeaning (AppointmentSatisfaction,SatisfactionMeaning) VALUES ('{}','{}')".format(AppointmentSatisfaction,SatisfactionMeaning)
    execute_query(connection,query)
    return 'Added Satisfaction Meaning'

@app.route('/SatisfactionMeaning/update/<int:id>',methods = ['GET'])
def ShowUpdateSatisfactionMeaning(id):
    query = "SELECT * FROM SatisfactionMeaning WHERE SatisfactionMeaningID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/SatisfactionMeaning/update/<int:id>',methods = ['PUT'])
def UpdateSatisfactionMeaning(id):
    request_data = request.get_json()
    AppointmentSatisfaction = request_data['AppointmentSatisfaction']
    SatisfactionMeaning = request_data['SatisfactionMeaning']
    query = "UPDATE SatisfactionMeaning SET AppointmentSatisfaction = '{}', SatisfactionMeaning = '{}' WHERE SatisfactionMeaningID = '{}'".format(AppointmentSatisfaction,SatisfactionMeaning,id)
    execute_query(connection,query)
    return 'Updated SatisfactionMeaning'

@app.route('/SatisfactionMeaning/delete/<int:id>', methods = ['DELETE'])
def DeleteSatisfactionMeaning(id):
    query = "DELETE FROM SatisfactionMeaning WHERE SatisfactionMeaningID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/SatisfactionMeaning')

@app.route('/ProductType/',methods = ['GET'])
def ProductType():
    query = "SELECT * FROM ProductType"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/ProductType/add', methods = ['POST'])
def AddProductType():
    request_data = request.get_json()
    ProductType = request_data['ProductType']
    Color = request_data['Color']
    query = "INSERT INTO ProductType (ProductType,Color) VALUES ('{}','{}')".format(ProductType,Color)
    execute_query(connection,query)
    return 'Added ProductType'

@app.route('/ProductType/update/<int:id>',methods = ['GET'])
def ShowUpdateProductType(id):
    query = "SELECT * FROM ProductType WHERE ProductTypeID = '{}'".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/ProductType/update/<int:id>',methods = ['PUT'])
def UpdateProductType(id):
    request_data = request.get_json()
    ProductType = request_data['ProductType']
    Color = request_data['Color']
    query = "UPDATE ProductType SET ProductType = '{}', Color = '{}' WHERE ProductTypeID = '{}'".format(ProductType,Color,id)
    execute_query(connection,query)
    return 'Updated ProductType'

@app.route('/ProductType/delete/<int:id>', methods = ['DELETE'])
def DeleteProductType(id):
    query = "DELETE FROM ProductType WHERE ProductTypeID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/ProductType')

@app.route('/HairProduct/',methods = ['GET'])
def HairProduct():
    query = "SELECT * FROM HairProduct"
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/HairProduct/add', methods = ['POST'])
def AddHairProduct():
    request_data = request.get_json()
    ProductType  = request_data['ProductType']
    Color = request_data['Color']
    ProductName = request_data['ProductName']
    ProductDescription = request_data['ProductDescription']
    ProductVolume = request_data['ProductVolume']
    query = "INSERT INTO HairProduct (ProductTypeID,ProductName,ProductDescription,ProductVolume) VALUES ((SELECT ProductTypeID from ProductType WHERE ProductType='{}' and Color='{}'),'{}','{}','{}')".format(ProductType,Color,ProductName,ProductDescription,ProductVolume)
    execute_query(connection,query)
    return 'Added Hair Product'

@app.route('/HairProduct/update/<int:id>',methods = ['GET'])
def ShowUpdateHairProduct(id):
    query = "SELECT * FROM HairProduct WHERE ProductID = '{}'; SELECT * FROM ProductType".format(id)
    Result = pd.read_sql(query,connection)
    Output = Result.to_dict('records')
    return jsonify(Output)

@app.route('/HairProduct/update/<int:id>',methods = ['PUT'])
def UpdateHairProduct(id):
    request_data = request.get_json()
    ProductType = request_data['ProductType']
    Color = request_data['Color']
    ProductName = request_data['ProductName']
    ProductDescription = request_data['ProductDescription']
    ProductVolume = request_data['ProductVolume']
    query = "UPDATE HairProduct SET ProductTypeID = (SELECT ProductTypeID from ProductType WHERE ProductType='{}' and Color='{}'),ProductName = '{}',ProductDescription = '{}',ProductVolume = '{}' WHERE ProductID = '{}'".format(ProductType,Color,ProductName,ProductDescription,ProductVolume,id)
    execute_query(connection,query)
    return 'Updated Service'

@app.route('/HairProduct/delete/<int:id>', methods = ['DELETE'])
def DeleteHairProduct(id):
    query = "DELETE FROM HairProduct WHERE ProductID = '{}'".format(id)
    execute_query(connection,query)
    return redirect('/HairProduct')

app.run()