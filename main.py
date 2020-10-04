import subprocess as sp
import pymysql
import pymysql.cursors



def add_hotel():      
    """
    Add a new hotel
    """
    if True:
        #Takes Hotel's details
        try:
            print("Enter Hotel Details: ")
            id = input("Hotel ID: ")
            name = input("Name: ")
            managerid = input("Manager ID: ")
            #Check if Manager exists in the database
            if not manager_exists(managerid):
                manager_flag = input("No such Manager exists , would you like to add a new manager(0/1)?: ")
                if manager_flag:
                    hireAnEmployee()
                else:
                    print("\n Sorry cannot insert")
                    return
            stars = input("Stars: ")
            locationid = addLocation()
            print(locationid)
            query = "INSERT INTO HOTEL VALUES ('%s','%s','%s','%s','%s')"%(id,name,managerid,locationid['ID'],stars)
            print(query)
            cur.execute(query)
            con.commit()
        except Exception as e:
            con.rollback()
            print("Failed to insert new hotel")
            query = "DELETE FROM LOCATION WHERE ID='%s'"%(locationid['ID'])
            cur.execute(query)
            con.commit()
            print("Deleted Location")
            print(e)

def addLocation():
    '''
    Add a new location and return the ID
    '''
    try:
        street = input("Street: ")
        city = input("City: ")
        country = input("Country: ")
        zipcode = input("Zipcode: ")
        query = "INSERT INTO LOCATION (STREET,CITY,COUNTRY,ZIPCODE) VALUES ('%s','%s','%s','%s')"%(street,city,country,zipcode)
        print(query)
        cur.execute(query)
        con.commit()
        cur.execute("SELECT ID FROM LOCATION WHERE STREET='%s' AND CITY='%s' AND COUNTRY='%s' AND ZIPCODE='%s'"%(street,city,country,zipcode))
        locationid = cur.fetchone()
        return locationid
    except Exception as e:
        con.rollback()
        print("Failed to insert location\n")
        print(e)  
        
def hireAnEmployee():
    try:
        # Takes emplyee details as input
        row = {}
        print("Enter new employee's details: ")
        name = (input("Name (Fname Minit Lname): ")).split(' ')
        row["FNAME"] = name[0]
        row["LNAME"] = name[1]
        row["ID"] = input("Input id: ")
        if emp_exists(id) and emp_fired(id):
            query = "UPDATE EMPLOYEE SET STATUS='Currently Employed' WHERE ID=%s"%(row["ID"])
            return
        row["DOB"] = input("Birth Date (YYYY-MM-DD): ")
        row["EMAIL"] = input("email: ")
        row["JOINDATE"] = input("joining date (YYYY-MM-DD): ")
        row["SALARY"] = int(input("Salary: "))
        row["STATUS"] = "currently employed"
        row["PHONE"] = int(input("Enter 6 digit phone: "))
        hotelid = input("Hotel ID: ")
        if not hotel_exists(hotelid):
            print("No Such hotel exists")
            return
        query = "INSERT INTO EMPLOYEE (FNAME, LNAME, ID, DOB, EMAIL, JOINDATE, SALARY, STATUS, PHONE) VALUES('%s','%s', %s, '%s', '%s', '%s', %s, '%s',%s)" % (row["FNAME"], row["LNAME"], row["ID"], row["DOB"], row["EMAIL"], row["JOINDATE"], row["SALARY"], row["STATUS"],row["PHONE"])
        print(query)
        cur.execute(query)
        con.commit()
        print("Inserted Into Employee Database")
        position = input("Enter the position of the employee (supervisor/service_staff/manager): ")
        if position == "supervisor":
            add_supervisor(row["ID"])
        elif position == "service_staff":
            add_service_staff(row["ID"])
        elif position == "manager":
            add_manager(row["ID"])
        belongs_to(hotelid,id)
        
    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(e)

    return

def fireAnEmployee():
    '''
    Fire an employee
    '''
    try:
        id = input("Enter employee ID: ")
        query = ""
        position = ""
        if not emp_exists(id):
            print("Employee does not exist in the database")
            return

        elif emp_fired(id):
            print("Employee already fired")
            return

        elif manager_exists(id):
            query = "DELETE FROM MANAGER WHERE ID=%s"%(id)
            position = "Manager"
            if manages_supervisor(id):
                input_flag = input("Manager is currently managing list of supervisors; would you like to change the manager for these supervisors (yes/no)?: ")
                if input_flag == "yes":
                    change_supervsior_manager(id)
                else:
                    return
            if manages_hotel(id):
                input_flag = input("Manager manages the hotel; would you like to change the manager for the hotel (yes/no)?: ")
                if input_flag == "yes":
                    change_hotel_manager(id)
                else:
                    return

        elif service_staff_exists(id):
            query = "DELETE FROM SERVICE STAFF WHERE ID=%s"%(id)
            position = "Service staff"
            if service_staff_room_exists(id):
                input_flag = input("Service staff is currently involved with room cleaning services; would you like to change the service staff for these rooms (yes/no): ")
                if input_flag == "yes":
                    change_room_service_staff(id)
                else:
                    return 

        elif supervisor_exists(id):
            query = "DELETE FROM SUPERVISOR WHERE ID=%s"%(id)
            position = "Supervisor"
            if supervises_service_staff(id):
                input_flag = input("Supervisor is supervising some service staff members; would you like to change the service staff for these employees (yes/no)?: ")
                if input_flag == "yes":
                    change_supervisor_service_staff(id)
                else:
                    return
            if supervises_clubs(id):
                input_flag = input("Supervisor is supervising clubs; would you like to change the supervisor for the clubs associated (yes/no)?: ")
                if input_flag == "yes":
                    pass
                else:
                    return

        changeEmpStatus(id)
        cur.execute(query)
        con.commit()
        print(position , " fired; records still present with status fired")
    
    except Exception as e:
        con.rollback()
        print("Failed to remove employee \n")
        print(e)

def changeEmpStatus(id):
    try:
        query = "UPDATE EMPLOYEE SET STATUS='FIRED' WHERE ID=%s"%(id)
        cur.execute(query)
        con.commit()
        print("Successfully changes the employee's status")
    except Exception as e:
        con.rollback()
        print("Failed to change the status of the employee")
        print(e) 

def add_supervisor(id):
    '''
    Add a supervisor
    '''
    try:
        managerid = input("Manager ID: ")
        if not manager_exists(managerid):
            print("No such manager exists")
            return
        dept = input("Department: ")
        query = "INSERT INTO SUPERVISOR VALUES (%s,%s,'%s')"%(id,managerid,dept)
        cur.execute(query)
        con.commit()
        print("Inserted into supervisor table successfully")
    except Exception as e:
        print("Failed to add supervisor")
        query = "DELETE FROM EMPLOYEE WHERE ID=%s"%(id)
        cur.execute(query)
        con.commit()
        print(e)
            
    
def add_service_staff(id):
    '''
    Add a service staff
    '''
    try:
        superid = input("Supervisor ID: ")
        if not supervisor_exists(superid):
            print("No such supervisor exists")
            return
        dept = input("Department: ")
        query = "INSERT INTO SERVICE_STAFF VALUES (%s,%s,'%s')"%(id,superid,dept)
        cur.execute(query)
        con.commit()
        print("Inserted into service staff successfully")
    except Exception as e:
        print("Failed to add service staff")
        query = "DELETE FROM EMPLOYEE WHERE ID=%s"%(id)
        cur.execute(query)
        con.commit()
        print(e)
        

def add_manager(id):
    '''
    Add a manager
    '''
    try:
        query = "INSERT INTO MANAGER (ID) VALUES(%d)"%(id)
        cur.execute(query)
        con.commit()
        print("Inserted into Manager table")
    except Exception as e:
        con.rollback()
        print("Failed to insert into manager table")
        query = "DELETE FROM EMPLOYEE WHERE ID=%s"%(id)
        cur.execute(query)
        con.commit()
        print(e)

def belongs_to(hotelid , empid):
    '''
    Implement Belongs to relationship
    '''
    try:
        query = "INSERT INTO BELONGS_TO VALUES (%s,%s)"%(hotelid,empid)
        cur.execute(query)
        con.commit()
        print("Successfully added employee to hotel")
    except Exception as e:
        print("Failed to connect employee to hotel")
        print(e)

def change_supervsior_manager(id):
    '''
    Change the manager associated with a supervisor
    '''
    try:
        if (not manager_exists(id)) or (not emp_exists(id)) or (emp_fired(id)):
            print("Manager does not exist in the manager database / is fired")
            return
        new_managerid = input("Select the new manager ID to whom you want to assign these supervisors to: ")
        if (not manager_exists(new_managerid)) or (not emp_exists(new_managerid)) or (emp_fired(new_managerid)):
            print("New manager ID invalid")
            return
        query = "UPDATE SUPERVISOR SET MANAGERID=%s WHERE MANAGERID=%s"%(new_managerid,id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Failed to change manager \n")
        print(e)

def change_hotel_manager(id):
    '''
    Change the hotel manager
    '''
    try:
        if (not manager_exists(id)) or (not emp_exists(id)) or (emp_fired(id)):
            print("Manager does not exist in the manager database / is fired")
            return
        new_managerid = input("Select the new manager ID who will be taking care of the hotel: ")
        if (not manager_exists(new_managerid)) or (not emp_exists(new_managerid)) or (emp_fired(new_managerid)):
            print("New Manager ID invalid")
            return
        query = "UPDATE HOTEL SET MANAGERID=%s WHERE MANAGERID=%s"%(new_managerid,id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Failed to change manager \n")
        print(e)

def change_room_service_staff(id):
    '''
    Change the service staff associated with rooms
    '''
    try:
        if(not service_staff_exists(id)) or (not emp_exists(id)) or (emp_fired(id)):
            print("Service staff does not exist in the service staff database / is fired")
            return
        new_service_staff_id = input("Enter the new service staff ID who will be taking care of the rooms: ")
        if (not service_staff_exists(new_service_staff_id)) or (not emp_exists(new_service_staff_id)) or (emp_fired(new_service_staff_id)):
            print("New Service staff ID is invalid")
        query = "UPDATE SERVICE_STAFF_ROOM SET SERVICE_STAFF_ID=%s WHERE SERVICE_STAFF_ID=%s"%(new_service_staff_id,id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Failed to change Service staff \n")
        print(e)

def change_supervisor_service_staff(id):
    '''
    Change the supervisor for service staff
    '''
    try:
        if (not supervisor_exists(id)) or (not emp_exists(id)) or (emp_fired(id)):
            print("Supervisor does not exist in the supervisor database / is fired")
            return 
        new_supid = input("Enter te new supervisor ID who will be supervising service staff: ")
        if (not supervisor_exists(new_supid)) or (not emp_exists(new_supid)) or (emp_fired(new_supid)):
            print("New Supervisor ID is invalid")
            return
        query = "UPDATE SERVICE_STAFF SET SUPID=%s WHERE SUPID=%s"%(new_supid,id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Failed to change Supervisor \n")
        print(e)

def change_supervisor_club(id):
    '''
    Change the supervisor associated with the club
    '''
    try:
        if (not supervisor_exists(id)) or (not emp_exists(id)) or (emp_fired(id)):
            print("Supervisor does not exist in the supervisor database / is fired")
            return 
        new_supid = input("Enter te new supervisor ID who will be supervising clubs: ")
        if (not supervisor_exists(new_supid)) or (not emp_exists(new_supid)) or (emp_fired(new_supid)):
            print("New Supervisor ID is invalid")
            return
        query = "UPDATE CLUBS SET SUPID=%s WHERE SUPID=%s"%(new_supid,id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Failed to change Supervisor \n")
        print(e)

def modify(table_name , attribute , pkey):
    pass
        

'''
Helper functions start 
'''
def manager_exists(id):
    query = "SELECT ID FROM MANAGER WHERE ID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def supervisor_exists(id):
    query = "SELECT ID FROM SUPERVISOR WHERE ID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def service_staff_exists(id):
    query = "SELECT ID FROM SERVICE_STAFF WHERE ID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def hotel_exists(id):
    hotel_query = "SELECT ID FROM HOTEL WHERE ID = %d" % (id)
    cur.execute(hotel_query)
    return cur.fetchone() is not None

def room_hotel_exists(roomno, hotelid):
    room_query = "SELECT * FROM ROOMS WHERE NUMBER = %d AND HOTELID = %d" % (roomno, hotelid)
    cur.execute(room_query)
    return cur.fetchone() is not None

def is_room_empty(roomno, hotelid):
    room_status_query = "SELECT STATUS FROM ROOMS WHERE NUMBER = %d AND HOTELID = %d" % (roomno, hotelid)
    cur.execute(room_status_query)
    query_res = cur.fetchone()

    if query_res is None:
        return False
    
    return query_res["STATUS"] == b'\x00'

def emp_exists(id):
    query = "SELECT ID FROM EMPLOYEE WHERE ID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def emp_fired(id):
    query = "SELECT STATUS FROM EMPLOYEE WHERE ID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() == "FIRED"

def manages_supervisor(id):
    query = "SELECT MANAGERID FROM SUPERVISOR WHERE MANAGERID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def supervises_service_staff(id):
    query = "SELECT SUPID FROM SUPERVISOR WHERE SUPID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def service_staff_room_exists(id):
    query = "SELECT SERVICE_STAFF_ID FROM SERVICE_STAFF_ROOM WHERE SERVICE_STAFF_ID=%s"%(id)
    cur.execute(query)
    return cur.fetchone is not None

def manages_hotel(id):
    query = "SELECT ID FROM HOTEL WHERE MANAGERID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def supervises_clubs(id):
    query = "SELECT SUPID FROM CLUBS WHERE SUPID=%s"%(id)
    cur.execute(query)
    return cur.fetchone() is not None

def member_exists(id):
    query = "SELECT * FROM MEMBERS WHERE ID = %d" % (id)
    cur.execute(query)
    return cur.fetchone() is not None
'''
Helper functions end
'''

def add_club():
    """
    Add a new club to a hotel
    """
    """
    `HOTELID` int NOT NULL,
    `TYPE` varchar(255) NOT NULL,
    `SERVICE_EXP` int NOT NULL,
    `MONTH` int NOT NULL,
    `YEAR` int NOT NULL,
    `TOTAL_INCOME` int NOT NULL,
    `COST_PER_HOUR` int NOT NULL,
    `SUPID` int NOT NULL,
    PRIMARY KEY (`HOTELID`,`TYPE`,`MONTH`,`YEAR`),
    KEY `SUPID` (`SUPID`),
    CONSTRAINT `CLUBS_ibfk_1` FOREIGN KEY (`SUPID`) REFERENCES `SUPERVISOR` (`ID`)
    """
    if True:  # try-catch exempted for testing purposes
        # Takes emplyee details as input
        row = {}
        print("Enter club's details: ")
        row["HOTELID"] = int(input("HOTELID: "))
        row["TYPE"] = input("TYPE: ")
        row["SERVICE_EXP"] = int(input("Monthly Service expenditure: "))
        row["MONTH"] = int(input("Month: "))
        row["YEAR"] = int(input("Year: "))
        row["TOTAL_INCOME"] = int(input("Monthly total income: "))
        row["COST_PER_HOUR"] = int(input("Cost per hour: "))
        row["SUPID"] = int(input("Supervisor ID: "))

        if not hotel_exists(row["HOTELID"]):
            print("Error at add_club(): Hotel does not exist")
            return
        
        supid_query = "SELECT ID FROM SUPERVISOR WHERE ID = %d" % (row["SUPID"])
        cur.execute(supid_query)
        if cur.fetchone() is None:
            print("Error at add_club(): No supervisor found")
            return

        query = "INSERT INTO CLUBS(HOTELID,  TYPE, SERVICE_EXP, MONTH, YEAR, TOTAL_INCOME, COST_PER_HOUR, SUPID) VALUES('%d', '%s', '%d', '%d', '%d', '%d', '%d', %d)" % (
            row["HOTELID"], row["TYPE"], row["SERVICE_EXP"], row["MONTH"], row["YEAR"], row["TOTAL_INCOME"], row["COST_PER_HOUR"], row["SUPID"])

        print(query)
        cur.execute(query)
        con.commit()

def add_room():
    """
    `NUMBER` int NOT NULL,
    `HOTELID` int NOT NULL,
    `STATUS` bit(1) NOT NULL,
    `TYPE` int NOT NULL,
    PRIMARY KEY (`NUMBER`,`HOTELID`),
    KEY `TYPE` (`TYPE`),
    CONSTRAINT `ROOMS_ibfk_1` FOREIGN KEY (`TYPE`) REFERENCES `ROOM_TYPE` (`TYPE`)
    """
    try:  # try-catch exempted for testing purposes
        # Takes emplyee details as input
        row = {}
        print("Enter room's details: ")
        row["NUMBER"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        # row["STATUS"] = int(input("Status: "))  # Set to empty by default
        row["STATUS"] = 0
        row["RATE"] = int(input("Room rate: "))
        row["MAX_GUESTS"] = int(input("Max guests allowed: "))

        if not hotel_exists(row["HOTELID"]):
            print("Error at add_room(): Hotel does not exist")
            return

        if room_hotel_exists(row["NUMBER"], row["HOTELID"]):
            print("Room already exists in hotel")
            return

        query_room_type = "SELECT TYPE FROM ROOM_TYPE where RATE = %d and MAX_GUESTS = %d" % (row["RATE"], row["MAX_GUESTS"])
        cur.execute(query_room_type)
        room_type = cur.fetchone()

        if room_type is None:
            room_type_insert = "INSERT INTO ROOM_TYPE (RATE, MAX_GUESTS) VALUES (%d, %d)" % (row["RATE"], row["MAX_GUESTS"])
            cur.execute(room_type_insert)

            cur.execute(query_room_type)
            room_type = cur.fetchone()
        
        row["TYPE"] = room_type["TYPE"]
        print("Final room type = ", row["TYPE"])

        query = "INSERT INTO ROOMS(NUMBER, HOTELID, STATUS, TYPE) VALUES(%d, %d, %d, %d)" % (
            row["NUMBER"], row["HOTELID"], row["STATUS"], row["TYPE"])

        print(query)
        cur.execute(query)
        con.commit()

        print("Inserted Into Database")

    except Exception as e:
        print("Error while inserting into ROOM: %s", e)

def add_member():
    if True:
        row = {}
        print("Enter member details: ")
        row["TIER"] = int(input("Tier: "))
        row["FNAME"] = input("First name: ")
        row["LNAME"] = input("Last name: ")
        row["EMAILID"] = input("Email: ")
        row["DOB"] = input("Date of birth (YYYY-MM-DD): ")
        row["STAYS"] = int(input("Stays: "))

        query = "INSERT INTO MEMBERS (TIER, FNAME, LNAME, EMAILID, DOB, STAYS) values (%d, '%s', '%s', '%s', \'%s\', %d)" % (row["TIER"], row["FNAME"], row["LNAME"], row["EMAILID"], row["DOB"], row["STAYS"])
        print("Query: ", query)
        cur.execute(query)
        con.commit()
        print("Inserted to database")
    # except Exception as e:
    #     print("Error while add_member(): ", e)


def add_finances():
    """
        +--------------+------+------+-----+---------+-------+
    | Field        | Type | Null | Key | Default | Extra |
    +--------------+------+------+-----+---------+-------+
    | HOTELID      | int  | NO   | PRI | NULL    |       |
    | MONTH        | int  | NO   | PRI | NULL    |       |
    | YEAR         | int  | NO   | PRI | NULL    |       |
    | ELEC_BILL    | int  | NO   | MUL | NULL    |       |
    | HOTEL_BILL   | int  | NO   |     | NULL    |       |
    | EMP_EXP      | int  | NO   |     | NULL    |       |
    | SERVICE_EXP  | int  | NO   |     | NULL    |       |
    | TOTAL_INCOME | int  | NO   |     | NULL    |       |
    +--------------+------+------+-----+---------+-------+


    mysql> desc EXPENDITURE;
    +--------------+------+------+-----+---------+-------+
    | Field        | Type | Null | Key | Default | Extra |
    +--------------+------+------+-----+---------+-------+
    | ELEC_BILL    | int  | NO   | PRI | NULL    |       |
    | HOTEL_BILL   | int  | NO   | PRI | NULL    |       |
    | EMP_EXP      | int  | NO   | PRI | NULL    |       |
    | SERVICE_EXP  | int  | NO   | PRI | NULL    |       |
    | TOTAL_EXP    | int  | NO   | MUL | NULL    |       |
    | TOTAL_INCOME | int  | NO   | PRI | NULL    |       |
    +--------------+------+------+-----+---------+-------+
    6 rows in set (0.00 sec)

    """
    if True:
        row = {}
        print("Enter finance details: ")
        row["HOTELID"] = int(input("HOTEL ID: "))
        row["MONTH"] = int(input("MONTH: "))
        row["YEAR"] = int(input("YEAR: "))
        row["ELEC_BILL"] = int(input("Electricity bill: "))
        row["HOTEL_BILL"] = int(input("Hotel bill: "))
        row["EMP_EXP"] = int(input("Employee Expenditure: "))
        row["SERVICE_EXP"] = int(input("Service expenditure: "))
        row["TOTAL_INCOME"] = int(input("Total income: "))

        if not hotel_exists(row["HOTELID"]):
            print("Error while adding finances: No such hotel exists")
            return


        #  EXPENDITURE
        expenditure_query_sel = "SELECT TOTAL_EXP FROM EXPENDITURE WHERE ELEC_BILL = %d AND HOTEL_BILL = %d AND SERVICE_EXP = %d AND TOTAL_INCOME = %d AND EMP_EXP = %d" % (
            row["ELEC_BILL"],
            row["HOTEL_BILL"],
            row["SERVICE_EXP"],
            row["TOTAL_INCOME"],
            row["EMP_EXP"]
        )

        cur.execute(expenditure_query_sel)
        total_exp = 0
        expenditure_query_res = cur.fetchone()
        if expenditure_query_res is None:
            total_exp = row["ELEC_BILL"] + row["HOTEL_BILL"] + row["SERVICE_EXP"] + row["TOTAL_INCOME"] + row["EMP_EXP"]
            expenditure_query_ins = "INSERT INTO EXPENDITURE VALUES (%d, %d, %d, %d, %d, %d)" % (row["ELEC_BILL"], row["HOTEL_BILL"], row["EMP_EXP"], row["SERVICE_EXP"], total_exp, row["TOTAL_INCOME"])
            cur.execute(expenditure_query_ins)

            cur.execute(expenditure_query_sel)
            expenditure_query_res = cur.fetchone()
        
        total_exp = expenditure_query_res["TOTAL_EXP"]
        
        #   PROFIT
        profit_query = "SELECT * FROM PROFIT WHERE TOTAL_EXP = %d AND TOTAL_INCOME = %d" % (total_exp, row["TOTAL_INCOME"])
        cur.execute(profit_query)

        if cur.fetchone() is None:
            profit_query = "INSERT INTO PROFIT (TOTAL_EXP, TOTAL_INCOME, TOTAL_PROFIT) VALUES (%d, %d, %d)" % (total_exp, row["TOTAL_INCOME"], total_exp + row["TOTAL_INCOME"])
            cur.execute(profit_query)

        finances_query = "INSERT INTO FINANCES(HOTELID, MONTH, YEAR, ELEC_BILL, HOTEL_BILL, EMP_EXP, SERVICE_EXP, TOTAL_INCOME) values (%d, %d,%d,%d,%d,%d,%d,%d)" %(
            row["HOTELID"],
            row["MONTH"],
            row["YEAR"],
            row["ELEC_BILL"],
            row["HOTEL_BILL"],
            row["EMP_EXP"],
            row["SERVICE_EXP"],
            row["TOTAL_INCOME"]
        )

        cur.execute(finances_query)
        con.commit()
        print("Inserted into database")


def add_service_staff_room():
    """
    Assign a service staff to a room
    """
    if True:
        row = {}
        print("Enter room and service staff detail: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["SERVICE_STAFF_ID"] = int(input("Service staff ID: "))
        
        if not room_hotel_exists(row["ROOMNO"], row["HOTELID"]):
            print("Error assigning service staff: Room does not exist")
            return
        
        if  not service_staff_exists(row["SERVICE_STAFF_ID"]):
            print("Error assigning service staff: Service staff does not exist")
            return
        
        query = "INSERT INTO SERVICE_STAFF_ROOM (ROOMNO, HOTELID, SERVICE_STAFF_ID) VALUES (%d, %d, %d)" % (row["ROOMNO"], row["HOTELID"], row["SERVICE_STAFF_ID"])
        cur.execute(query)
        con.commit()

        print("Successfully assigned")


def remove_service_staff_room():
    """
    Remove a service staff from a room
    """
    if True:
        row = {}
        print("Enter room and service staff detail: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["SERVICE_STAFF_ID"] = int(input("Service staff ID: "))
        
        if not room_hotel_exists(row["ROOMNO"], row["HOTELID"]):
            print("Error assigning service staff: Room does not exist")
            return
        
        if  not service_staff_exists(row["SERVICE_STAFF_ID"]):
            print("Error assigning service staff: Service staff does not exist")
            return
        
        relation_exist_query = "SELECT * FROM SERVICE_STAFF_ROOM WHERE ROOMNO = %d AND HOTELID = %d AND SERVICE_STAFF_ID = %d" % (row["ROOMNO"], row["HOTELID"], row["SERVICE_STAFF_ID"])
        cur.execute(relation_exist_query)
        if cur.fetchone() is None:
            print("Service staff was not assigned to the room")
            return
        query = "DELETE FROM SERVICE_STAFF_ROOM WHERE ROOMNO = %d AND HOTELID = %d AND SERVICE_STAFF_ID = %d" % (row["ROOMNO"], row["HOTELID"], row["SERVICE_STAFF_ID"])
        cur.execute(query)
        con.commit()

        print("Successfully un-assigned")
    # except Exception as e:
    #    print(e)


def add_guest():
    if True:
        row = {}
        print("Enter Guest details: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["ISMEMBER"] = int(input("Is member(1/0): "))
        row["MEMBERID"] = 0
        if row["ISMEMBER"] == 0:
            row["MEMBERID"] = None
        else:
            row["MEMBERID"] = input("Member ID: ")
        row["CHECKIN"] = input("Checkin date: ")
        row["CHECKOUT"] = input("Checkout date: ")
        row["COST"] = 0
        row["CLUB_HOURS"] = 0

        # Check valid room
        if not room_hotel_exists(row["ROOMNO"], row["HOTELID"]):
            print("Error adding guest: No such room found")
            return
        # Check valid member ID
        if row["ISMEMBER"] and (not member_exists(row["MEMBERID"])):
            print("Error adding member guest: Member ID incorrect")
            return
        
        # Check room empty
        if not is_room_empty(row["ROOMNO"], row["HOTELID"]):
            print("Error adding guest: Room is occupied")
            return
        
        if (row["ISMEMBER"]):
            query = "INSERT INTO GUESTS (ROOMNO, HOTELID, IS_MEMBER, MEMBERID, CHECKIN, CHECKOUT, COST, CLUB_HOURS) VALUES (%d, %d, %d, %d, '%s', '%s', %d, %d)" % (
                row["ROOMNO"],
                row["HOTELID"],
                row["ISMEMBER"],
                row["MEMBERID"],
                row["CHECKIN"],
                row["CHECKOUT"],
                row["COST"],
                row["CLUB_HOURS"]
            )
        else:
            query = "INSERT INTO GUESTS (ROOMNO, HOTELID, IS_MEMBER, CHECKIN, CHECKOUT, COST, CLUB_HOURS) VALUES (%d, %d, %d, '%s', '%s', %d, %d)" % (
                row["ROOMNO"],
                row["HOTELID"],
                row["ISMEMBER"],
                row["CHECKIN"],
                row["CHECKOUT"],
                row["COST"],
                row["CLUB_HOURS"]
            )

        cur.execute(query)

        # Set room status as occupied
        update_rooms_status = "UPDATE ROOMS SET STATUS = 1 WHERE NUMBER = %d AND HOTELID = %d" % (row["ROOMNO"], row["HOTELID"])
        cur.execute(update_rooms_status)

        con.commit()


def dispatch():
    """
    Function that maps helper functions to option entered
    """
    print("The following options are possible for employee management")
    print("a. Add an Employee")
    print("b. Fire an Employee")
    print("c. Assign service staff to room")
    print("d. Remove service staff from room")
    ch = input("Enter choice: ")
    if(ch == "a"):
        hireAnEmployee()
   
    elif(ch == "b"):
        fireAnEmployee()

    elif (ch == "c"):
        add_service_staff_room()
    
    elif (ch == "d"):
        remove_service_staff_room()

    else:
        print("Error: Invalid Option")


def handle_views():
    print("Select from the following to retrieve information: ")
    print("Choose a VIEW option\n\n")
    print("0. Hotels")
    print("1. Employees")
    print("2. Members and guests")
    print("3.  Finances")  # SPECIAL CASE
    print("4. Clubs")
    print("5. Rooms")
    print("18. LATEST MEMBERS")
    print("19. FINANCIAL REPORT")

    choice = int(input("SELECT> "))
    query = ""

    if (choice == 1):
        print("1.  Employees")
        print("2.  Fired employees")
        print("3.  Service staff")
        print("4.  Supervisors")
        print("5.  Managers")


    if (choice == 2):
        print("1.  Guests")
        print("2.  Guests in a hotel")
        print("3.  Members")
        print("4.  Member guests")
        print("5.  Members of a tier")
    
    if (choice == 4):
        print("1. All clubs")
        print("2. Clubs of a hotel")
        print("3. Clubs under a supervisor")
        print("4. Clubs of type")

    if (choice == 5):
        print("1. Rooms of a hotel")
        print("2. Unoccupied rooms of a hotel")
        print("3. Rooms in a hotel currently occupied")
        print("4. Guest staying in room")

# Global
while(1):
    tmp = sp.call('clear', shell=True)
    
    # Can be skipped if you want to hard core username and password
    username = input("Username: ")
    password = input("Password: ")

    if True:  # try
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQLl server 
        con = pymysql.connect(host='localhost',
                              user=username,
                              port = 5005,
                              password=password,
                              db='HCDBMS',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                # Here taking example of Employee Mini-world
                print("0. Get data")
                print("1. Manage employees")
                print("2. Add Hotel")  # Add Hotel
                print("3. Add a Club")  # ABHISHEKH
                print("4. Check in a Guest")  # ABHISHEKH
                print("5. Check out a Guest")
                print("6. Add a room to a hotel")  # ABHISHEKH
                print("7. Guest registering to club")
                print("8. Add monthly finance")  # ABHISHEKH
                print("9. Generate profit report")
                print("10. Generate Guest Bill")
                print("11. Add a Member Guest")
                print("20. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch == 0:
                    handle_views()
                elif ch == 1:
                    dispatch()
                elif ch == 2:
                    add_hotel()
                elif ch == 6:
                    add_room()
                elif (ch == 11):
                    add_member()
                elif (ch == 8):
                    add_finances()
                elif (ch == 4):  # TODO: Compute cost
                    add_guest()
                elif ch == 20:
                    break
                tmp = input("Enter any key to CONTINUE>")

    # except:
    #     tmp = sp.call('clear', shell=True)
    #     print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
    #     tmp = input("Enter any key to CONTINUE>")