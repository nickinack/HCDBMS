import subprocess as sp
import pymysql
import pymysql.cursors



"""
git checkout -b abhishekh4
git branch
git status
git add .
git push origin abhishekh4
git checkout master
git merge abhishekh4
"""


def add_hotel():
    """
    Add a new hotel
    """
    if True:
        # Takes Hotel's details
        try:
            print("Enter Hotel Details: ")
            id = input("Hotel ID: ")
            name = input("Name: ")
            managerid = input("Manager ID: ")
            # Check if Manager exists in the database

            stars = input("Stars: ")
            locationid = addLocation()
            print(locationid)
            query = "INSERT INTO HOTEL VALUES ('%s','%s','%s','%s','%s')" % (
                id, name, managerid, locationid['ID'], stars)
            print(query)
            cur.execute(query)
            con.commit()
        except Exception as e:
            con.rollback()
            print("Failed to insert new hotel")
            query = "DELETE FROM LOCATION WHERE ID='%s'" % (locationid['ID'])
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
        query = "INSERT INTO LOCATION (STREET,CITY,COUNTRY,ZIPCODE) VALUES ('%s','%s','%s','%s')" % (
            street, city, country, zipcode)
        print(query)
        cur.execute(query)
        con.commit()
        cur.execute("SELECT ID FROM LOCATION WHERE STREET='%s' AND CITY='%s' AND COUNTRY='%s' AND ZIPCODE='%s'" % (
            street, city, country, zipcode))
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
        row["ID"] = int(input("ID: "))
        row["DOB"] = input("Birth Date (YYYY-MM-DD): ")
        row["EMAIL"] = input("email: ")
        row["JOINDATE"] = input("joining date (YYYY-MM-DD): ")
        row["SALARY"] = int(input("Salary: "))
        row["STATUS"] = "currently employed"
        position = input(
            "Enter the position of the employee (supervisor/service_staff/manager")

        query = "INSERT INTO EMPLOYEE (FNAME, LNAME, ID, DOB, EMAIL, JOINDATE, SALARY, STATUS) VALUES(%s,%s, %s, '%s', %s, '%s', %s, %s)" % (
            row["FNAME"], row["LNAME"], row["ID"], row["DOB"], row["EMAIL"], row["JOINDATE"], row["SALARY"], row["STATUS"])

        print(query)
        print("Inserted Into Database")

    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(e)

    return


""" ------ ABHISHEKH ---------"""
def hotel_exists(id):
    hotel_query = "SELECT ID FROM HOTEL WHERE ID = %d" % (id)
    cur.execute(hotel_query)
    return cur.fetchone() is not None


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
        row["STATUS"] = 1
        row["RATE"] = int(input("Room rate: "))
        row["MAX_GUESTS"] = int(input("Max guests allowed: "))

        if not hotel_exists(row["HOTELID"]):
            print("Error at add_room(): Hotel does not exist")
            return

        query_room_type = "SELECT TYPE FROM ROOM_TYPE where RATE = %d and MAX_GUESTS = %d" % (
            row["RATE"], row["MAX_GUESTS"])
        cur.execute(query_room_type)
        room_type = cur.fetchone()

        if room_type is None:
            room_type_insert = "INSERT INTO ROOM_TYPE (RATE, MAX_GUESTS) VALUES (%d, %d)" % (
                row["RATE"], row["MAX_GUESTS"])
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

        query = "INSERT INTO MEMBERS (TIER, FNAME, LNAME, EMAILID, DOB, STAYS) values (%d, '%s', '%s', '%s', \'%s\', %d)" % (
            row["TIER"], row["FNAME"], row["LNAME"], row["EMAILID"], row["DOB"], row["STAYS"])
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


"""
------END ABHISHEKH------
"""


def dispatch():
    """
    Function that maps helper functions to option entered
    """
    print("The following options are possible for employee management")
    print("a. Add an Employee")
    print("b. Fire an Employee")
    ch = input("Enter choice: ")
    if(ch == "a"):
        hireAnEmployee()

    elif(ch == "b"):
        pass

    else:
        print("Error: Invalid Option")


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
                              port=5005,
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
                tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                print("1. Manage employees")
                print("2. Add Hotel")  # Add Hotel
                print("3. Add a Club")  # ABHISHEKH
                print("4. Check in a Guest")
                print("5. Check out a Guest")
                print("6. Add a room to a hotel")  # ABHISHEKH
                print("7. Guest registering to club")
                print("8. Add monthly finance")  # ABHISHEKH
                print("9. Generate profit report")
                print("10. Generate Guest Bill")
                print("11. Add a Member Guest")  # ABHISHEKH
                print("12. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch == 1:
                    dispatch()
                elif ch == 2:
                    add_hotel()
                elif ch == 6:
                    add_room()
                elif (ch == 11):
                    add_member()
                elif (ch == 8):
                    add_finances()
                elif ch == 12:
                    break
                tmp = input("Enter any key to CONTINUE>")

    # except:
    #     tmp = sp.call('clear', shell=True)
    #     print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
    #     tmp = input("Enter any key to CONTINUE>")
