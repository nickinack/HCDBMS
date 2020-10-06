import subprocess as sp
import pymysql
import pymysql.cursors
# import datetime
from datetime import datetime
from tabulate import tabulate


def add_hotel():
    """
    Add a new hotel
    """
    # if True:
    if True:
        # Takes Hotel's details
        try:
            print("Enter Hotel Details: ")
            id = input("Hotel ID: ")
            name = input("Name: ")
            managerid = input("Manager ID: ")
            maanger_flag = ""
            # Check if Manager exists in the database
            if not manager_exists(managerid):
                manager_flag = input(
                    "No such Manager exists , would you like to add a new manager(0/1)?: ")
                if manager_flag:
                    hireAnEmployee(id)
                else:
                    print("\n Sorry cannot insert")
                    return
            stars = input("Stars: ")
            locationid = addLocation()
            print(locationid)
            query = "INSERT INTO HOTEL VALUES ('%s','%s','%s','%s','%s')" % (
                id, name, managerid, locationid['ID'], stars)
            # print(query)
            cur.execute(query)
            con.commit()
            if manager_flag:
                belongs_to(id, managerid)
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
        while street == "":
            street = input("Street cannot be empty. Street: ")
        city = input("City: ")
        while city == "":
            city = input("City cannot be empty. City: ")
        country = input("Country: ")
        while country == "":
            country = input("Country cannot be empty. Country: ")
        zipcode = input("Zipcode: ")
        while zipcode == "":
            zipcode = input("Zipcode cannot be empty. Zipcode: ")
        query = "INSERT INTO LOCATION (STREET,CITY,COUNTRY,ZIPCODE) VALUES ('%s','%s','%s','%s')" % (
            street, city, country, zipcode)
        # print(query)
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


def hireAnEmployee(hotelid_default=None):
    try:
        # Takes emplyee details as input
        row = {}
        print("Enter new employee's details: ")
        name = (input("Name (Fname Minit Lname): ")).split(' ')
        row["FNAME"] = name[0]
        row["LNAME"] = name[1]
        row["ID"] = int(input("Input id: "))
        if emp_exists(row["ID"]) and emp_fired(row["ID"]):
            query = "UPDATE EMPLOYEE SET STATUS='Currently Employed' WHERE ID=%s" % (
                row["ID"])
            return
        row["DOB"] = input("Birth Date (YYYY-MM-DD): ")
        row["EMAIL"] = input("email: ")
        row["JOINDATE"] = input("joining date (YYYY-MM-DD): ")
        row["SALARY"] = int(input("Salary: "))
        row["STATUS"] = "currently employed"
        row["PHONE"] = int(input("Enter 6 digit phone: "))
        hotelid = int(input("Hotel ID: "))
        if not hotel_exists(hotelid) and hotelid_default is None:
            print("No Such hotel exists")
            return
        query = "INSERT INTO EMPLOYEE (FNAME, LNAME, ID, DOB, EMAIL, JOINDATE, SALARY, STATUS, PHONE) VALUES('%s','%s', %s, '%s', '%s', '%s', %s, '%s',%s)" % (
            row["FNAME"], row["LNAME"], row["ID"], row["DOB"], row["EMAIL"], row["JOINDATE"], row["SALARY"], row["STATUS"], row["PHONE"])
        # print(query)
        cur.execute(query)
        con.commit()
        print("Inserted Into Employee Database")
        position = input(
            "Enter the position of the employee (supervisor/service_staff/manager): ")
        if position == "supervisor":
            add_supervisor(row["ID"])
        elif position == "service_staff":
            add_service_staff(row["ID"])
        elif position == "manager":
            add_manager(row["ID"])
        
        if hotel_exists(hotelid):
            belongs_to(hotelid, row["ID"])

        year, month = int(row["JOINDATE"].split('-')[0]), int(row["JOINDATE"].split('-')[1])

        create_finances_if_not_exist(hotelid, month, year)

        finance_exp_update = "UPDATE FINANCES SET EMP_EXP = EMP_EXP + %d WHERE HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
            row["SALARY"], hotelid, month, year
        )
        cur.execute(finance_exp_update)
        con.commit()

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

        if manager_exists(id):
            query = "DELETE FROM MANAGER WHERE ID=%s" % (id)
            position = "Manager"
            if manages_supervisor(id):
                input_flag = input(
                    "Manager is currently managing list of supervisors; would you like to change the manager for these supervisors (yes/no)?: ")
                if input_flag == "yes":
                    change_supervsior_manager(id)
                else:
                    return
            if manages_hotel(id):
                input_flag = input(
                    "Manager manages the hotel; would you like to change the manager for the hotel (yes/no)?: ")
                if input_flag == "yes":
                    change_hotel_manager(id)
                else:
                    return

        if service_staff_exists(id):
            query = "DELETE FROM SERVICE STAFF WHERE ID=%s" % (id)
            position = "Service staff"
            if service_staff_room_exists(id):
                input_flag = input(
                    "Service staff is currently involved with room cleaning services; would you like to change the service staff for these rooms (yes/no): ")
                if input_flag == "yes":
                    change_room_service_staff(id)
                else:
                    return

        if supervisor_exists(id):
            query = "DELETE FROM SUPERVISOR WHERE ID=%s" % (id)
            position = "Supervisor"
            if supervises_service_staff(id):
                input_flag = input(
                    "Supervisor is supervising some service staff members; would you like to change the service staff for these employees (yes/no)?: ")
                if input_flag == "yes":
                    change_supervisor_service_staff(id)
                else:
                    return
            if supervises_clubs(id):
                input_flag = input(
                    "Supervisor is supervising clubs; would you like to change the supervisor for the clubs associated (yes/no)?: ")
                if input_flag == "yes":
                    pass
                else:
                    return

        changeEmpStatus(id)
        cur.execute(query)
        con.commit()
        print(position, " fired; records still present with status fired")

    except Exception as e:
        con.rollback()
        print("Failed to remove employee \n")
        print(e)


def changeEmpStatus(id):
    try:
        query = "UPDATE EMPLOYEE SET STATUS='FIRED' WHERE ID=%s" % (id)
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
        while dept == "":
            dept = input("Department cannot be empty. Department: ")
        query = "INSERT INTO SUPERVISOR VALUES (%s,%s,'%s')" % (
            id, managerid, dept)
        cur.execute(query)
        con.commit()
        print("Inserted into supervisor table successfully")
    except Exception as e:
        print("Failed to add supervisor")
        query = "DELETE FROM EMPLOYEE WHERE ID=%s" % (id)
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
        while dept == "":
            dept = input("Department cannot be empty. Department: ")
        query = "INSERT INTO SERVICE_STAFF VALUES (%s,%s,'%s')" % (
            id, superid, dept)
        cur.execute(query)
        con.commit()
        print("Inserted into service staff successfully")
    except Exception as e:
        print("Failed to add service staff")
        query = "DELETE FROM EMPLOYEE WHERE ID=%s" % (id)
        cur.execute(query)
        con.commit()
        print(e)


def add_manager(id):
    '''
    Add a manager
    '''
    try:
        query = "INSERT INTO MANAGER (ID) VALUES(%d)" % (id)
        cur.execute(query)
        con.commit()
        print("Inserted into Manager table")
    except Exception as e:
        con.rollback()
        print("Failed to insert into manager table")
        query = "DELETE FROM EMPLOYEE WHERE ID=%s" % (id)
        cur.execute(query)
        con.commit()
        print(e)


def belongs_to(hotelid, empid):
    '''
    Implement Belongs to relationship
    '''
    # print("Belongs to")
    try:
        query = "INSERT INTO BELONGS_TO(HOTELID, EMPID) VALUES (%s,%s)" % (hotelid, empid)
        # print(query)
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
        new_managerid = input(
            "Select the new manager ID to whom you want to assign these supervisors to: ")
        if (not manager_exists(new_managerid)) or (not emp_exists(new_managerid)) or (emp_fired(new_managerid)):
            print("New manager ID invalid")
            return
        query = "UPDATE SUPERVISOR SET MANAGERID=%s WHERE MANAGERID=%s" % (
            new_managerid, id)
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
        new_managerid = input(
            "Select the new manager ID who will be taking care of the hotel: ")
        if (not manager_exists(new_managerid)) or (not emp_exists(new_managerid)) or (emp_fired(new_managerid)):
            print("New Manager ID invalid")
            return
        query = "UPDATE HOTEL SET MANAGERID=%s WHERE MANAGERID=%s" % (
            new_managerid, id)
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
        new_service_staff_id = input(
            "Enter the new service staff ID who will be taking care of the rooms: ")
        if (not service_staff_exists(new_service_staff_id)) or (not emp_exists(new_service_staff_id)) or (emp_fired(new_service_staff_id)):
            print("New Service staff ID is invalid")
        query = "UPDATE SERVICE_STAFF_ROOM SET SERVICE_STAFF_ID=%s WHERE SERVICE_STAFF_ID=%s" % (
            new_service_staff_id, id)
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
        new_supid = input(
            "Enter te new supervisor ID who will be supervising service staff: ")
        if (not supervisor_exists(new_supid)) or (not emp_exists(new_supid)) or (emp_fired(new_supid)):
            print("New Supervisor ID is invalid")
            return
        query = "UPDATE SERVICE_STAFF SET SUPID=%s WHERE SUPID=%s" % (
            new_supid, id)
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
        new_supid = input(
            "Enter te new supervisor ID who will be supervising clubs: ")
        if (not supervisor_exists(new_supid)) or (not emp_exists(new_supid)) or (emp_fired(new_supid)):
            print("New Supervisor ID is invalid")
            return
        query = "UPDATE CLUBS SET SUPID=%s WHERE SUPID=%s" % (new_supid, id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Failed to change Supervisor \n")
        print(e)


def modify_manager_for_one_supervisor(id):
    '''
    Modifies manager for one supervisor
    '''
    try:
        managerid = input("Enter the new manager id for the supervisor: ")
        if (not manager_exists(managerid)) or (not emp_exists(managerid)) or (emp_fired(managerid)):
            print("Manager does not exist in the database / is fired \n")
            return

        query = "UPDATE SUPERVISOR SET MANAGERID=%s WHERE ID=%s" % (
            managerid, id)
        cur.execute(query)
        con.commit()
        print("Successully modified the manager for supervisor \n")
    except Exception as e:
        print("Failed to modify \n")
        print(e)


def modify_supervisor_for_one_service_staff(id):
    '''
    Modifies supervisor of one service staff member
    '''
    try:
        supid = input("Enter the new supervisor id for the service staff: ")
        if (not supervisor_exists(id)) or (not emp_fired(supid)) or (emp_fired(supid)):
            print("Supervisor does not exis in the database / is fired")
            return

        query = "UPDATE SERVICE_STAFF SET SUPID=%s WHERE ID=%s" % (supid, id)
        cur.execute(query)
        con.commit()
        print("Successfully modieifed the supervisor for the service staff \n")
    except Exception as e:
        print("Failed to modify \n")
        print(e)


def modify_service_staff_for_one_room():
    '''
    Modifies service staff for one room
    '''
    try:
        id = int(input("Enter employee ID: "))
        if (not service_staff_exists(id)) or (not emp_exists(id)) or (emp_fired(id)):
            print("Employee does not exist / is not service staff / is fired")
        hotelid = "SELECT HOTELID FROM BELONGS_TO WHERE EMPID=%s" % (id)
        roomno = int(input("Enter Room number: "))
        if not (room_hotel_exists(roomno, hotelid)):
            print("Room does not exist in the hotel in which the employee works at \n")
            return
        query = "UPDATE SERVICE_STAFF_ROOM SET SERVICE_STAFF_ID=%s WHERE ROOMNO=%s AND HOTELID=%s" % (
            id, roomno, hotelid)
        cur.execute(query)
        con.commit()
    except Exception as e:
        print("Failed to modify service staff details for the room \n")
        print(e)


def modify_employee():
    '''
    Modify an employee details (other than pkey)
    '''
    try:
        id = int(input("Enter the ID of employee: "))
        print("The following is the list of attributes you can change in an employee: ")
        position = ""
        if manager_exists(id):
            position = "manager"
        elif supervisor_exists(id):
            position = "supervisor"
        elif service_staff_exists(id):
            position = "service_staff"
        print("e1. Fname")
        print("e2. Lname")
        print("e3. Phone")
        print("e4. Email")
        print("e5. DOB")
        print("e6. Salary")
        if position == "supervisor":
            print("e7. Department: ")
            print("e8. ManagerID: ")
        if position == "service_staff":
            print("e7. Supervisor")
            print("e8. Department")

        attr = input("Enter the attribute you want to change: ")
        attr_dict = {
            "e1": "Fname",
            "e2": "Lname",
            "e3": "Phone",
            "e4": "Email",
            "e5": "DOB",
            "e6": "SALARY"
        }

        query = ""
        if not (attr == "e7" or attr == "e8"):
            change = input("Enter the new value for the attribute: ")
            query = "UPDATE EMPLOYEE SET %s='%s' WHERE ID=%s" % (
                attr_dict[attr], change, id)
            # print(query)

        elif (attr == "e7" or attr == "e8"):
            if position == "supervisor" and attr == "e7":
                change = input("Enter the new value for department: ")
                query = "UPDATE SUPERVISOR SET DEPT='%s' WHERE ID=%s" % (
                    change, id)

            if position == "supervisor" and attr == "e8":
                modify_manager_for_one_supervisor(id)
                return

            if position == "service_staff" and attr == "e7":
                modify_supervisor_for_one_service_staff(id)
                return

            if position == "service_staff" and attr == "e8":
                change = input("Enter nrew value for department")
                query = "UPDATE SERVICE_STAFF SET DEPT='%s' WHERE ID=%s" % (
                    change, id)

        cur.execute(query)
        con.commit()
        print("Successfully modified detals\n")

    except Exception as e:
        print("Failed to insert into database \n")
        print(e)

'''
Helper functions start
'''


def manager_exists(id):
    query = "SELECT ID FROM MANAGER WHERE ID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def supervisor_exists(id):
    query = "SELECT ID FROM SUPERVISOR WHERE ID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def service_staff_exists(id):
    query = "SELECT ID FROM SERVICE_STAFF WHERE ID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def populate_exp_profits(hotelid, month, year):
    print("here")
    query = "SELECT ELEC_BILL, HOTEL_BILL, EMP_EXP, SERVICE_EXP, TOTAL_INCOME FROM FINANCES WHERE HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
            hotelid, month, year
        )
    cur.execute(query)
    exp_res = cur.fetchone()

    total_exp = exp_res["ELEC_BILL"] + exp_res["HOTEL_BILL"] + \
        exp_res["SERVICE_EXP"] + exp_res["EMP_EXP"]

    query = "SELECT TOTAL_EXP FROM EXPENDITURE WHERE ELEC_BILL = %d AND HOTEL_BILL = %d  AND EMP_EXP = %d \
        AND SERVICE_EXP = %d AND TOTAL_INCOME = %d" % (
            exp_res["ELEC_BILL"], exp_res["HOTEL_BILL"], exp_res["EMP_EXP"],
            exp_res["SERVICE_EXP"], exp_res["TOTAL_INCOME"]
        )
    cur.execute(query)

    res = cur.fetchone()
    print("First res: ")
    print(res)
    if res is None:
        print("inserting into exp")
        query = "INSERT INTO EXPENDITURE (ELEC_BILL, HOTEL_BILL, EMP_EXP, SERVICE_EXP, TOTAL_INCOME, TOTAL_EXP) \
            VALUES (%d, %d, %d, %d, %d, %d)" % (
                exp_res["ELEC_BILL"], exp_res["HOTEL_BILL"], exp_res["EMP_EXP"],
                exp_res["SERVICE_EXP"], exp_res["TOTAL_INCOME"], total_exp
            )
        cur.execute(query)
        con.commit()

    query = "SELECT * FROM PROFIT WHERE TOTAL_EXP = %d AND TOTAL_INCOME = %d" % (
        total_exp, exp_res["TOTAL_INCOME"]
    )
    cur.execute(query)

    if cur.fetchone() is None:
        query = "INSERT INTO PROFIT (TOTAL_EXP, TOTAL_INCOME, TOTAL_PROFIT) VALUES (%d, %d, %d)" % (
            total_exp, exp_res["TOTAL_INCOME"], exp_res["TOTAL_INCOME"] - total_exp
        )
        cur.execute(query)
        con.commit()


def hotel_exists(id):
    hotel_query = "SELECT ID FROM HOTEL WHERE ID = %d" % (id)
    cur.execute(hotel_query)
    return cur.fetchone() is not None


def room_hotel_exists(roomno, hotelid):
    room_query = "SELECT * FROM ROOMS WHERE NUMBER = %d AND HOTELID = %d" % (
        roomno, hotelid)
    cur.execute(room_query)
    return cur.fetchone() is not None


def emp_exists(id):
    query = "SELECT ID FROM EMPLOYEE WHERE ID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def emp_fired(id):
    query = "SELECT STATUS FROM EMPLOYEE WHERE ID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() == "FIRED"


def manages_supervisor(id):
    query = "SELECT MANAGERID FROM SUPERVISOR WHERE MANAGERID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def supervises_service_staff(id):
    query = "SELECT ID FROM SUPERVISOR WHERE ID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def service_staff_room_exists(id):
    query = "SELECT SERVICE_STAFF_ID FROM SERVICE_STAFF_ROOM WHERE SERVICE_STAFF_ID=%s" % (
        id)
    cur.execute(query)
    return cur.fetchone is not None


def manages_hotel(id):
    query = "SELECT ID FROM HOTEL WHERE MANAGERID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def create_finances_if_not_exist(hotelid, month, year):
    if not finances_exists(hotelid, month, year):
        print("Please update finances for hotel with ID %d in the month of %d (%d)" % (hotelid, month, year))

        query = "INSERT INTO FINANCES (HOTELID, MONTH, YEAR, elec_bill, hotel_bill) VALUES (%d, %d, %d, %d, %d)" % (
            hotelid, month, year, 0, 0)
        cur.execute(query)
        print("Inserting into finances")
        con.commit()


def finances_exists(hotelid, month, year):
    query = "SELECT * FROM FINANCES WHERE HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
        hotelid, month, year
    )
    cur.execute(query)
    return cur.fetchone() is not None


def supervises_clubs(id):
    query = "SELECT SUPID FROM CLUBS WHERE SUPID=%s" % (id)
    cur.execute(query)
    return cur.fetchone() is not None


def is_room_empty(roomno, hotelid):
    room_status_query = "SELECT STATUS FROM ROOMS WHERE NUMBER = %d AND HOTELID = %d" % (
        roomno, hotelid)
    cur.execute(room_status_query)
    query_res = cur.fetchone()

    if query_res is None:
        return False

    return query_res["STATUS"] == b'\x00'


def guest_exists(roomno, hotelid, checkin, checkout):
    query = "SELECT * FROM GUESTS WHERE ROOMNO = %d AND HOTELID = %d AND CHECKIN = '%s' AND CHECKOUT = '%s'" % (
        roomno, hotelid, checkin, checkout
    )
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

    # if True:  # try-catch exempted for testing purposes
    try:
        # Takes emplyee details as input
        row = {}
        print("Enter club's details: ")
        row["HOTELID"] = int(input("HOTELID: "))
        row["TYPE"] = input("TYPE: ")
        while row["TYPE"] == "":
            row["TYPE"] = input("Type cannot be empty. Type: ")
        row["SERVICE_EXP"] = int(input("Monthly Service expenditure: "))
        row["MONTH"] = int(input("Month(1-12): "))
        row["YEAR"] = int(input("Year: "))
        row["TOTAL_INCOME"] = int(input("Monthly total income: "))
        row["COST_PER_HOUR"] = int(input("Cost per hour: "))
        row["SUPID"] = int(input("Supervisor ID: "))

        if not (row["MONTH"] >= 1 and row["MONTH"] <= 12):
            print("Incorrect month entered")
            return

        if not hotel_exists(row["HOTELID"]):
            print("Error at add_club(): Hotel does not exist")
            return

        while not supervisor_exists(row["SUPID"]):
            row["SUPID"] = int(input("Incorrect supervisor ID: "))

        club_query = "SELECT * FROM CLUBS WHERE HOTELID = %d AND TYPE = '%s' AND MONTH = %d AND YEAR = %d" % (
            row["HOTELID"], row["TYPE"], row["MONTH"], row["YEAR"]
        )
        cur.execute(club_query)
        clubs_res = cur.fetchone()

        create_finances_if_not_exist(row["HOTELID"], row["MONTH"], row["YEAR"])

        if clubs_res is not None:
            ch = input(
                "Overriding existing club information for the month, continue? (y/n) ")
            if ch != 'y':
                print("Aborting.")
                return
            query = "UPDATE CLUBS SET SUPID = %d, SERVICE_EXP = %d, COST_PER_HOUR = %d, TOTAL_INCOME = %d\
                WHERE TYPE = '%s' AND HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
                    row["SUPID"], row["SERVICE_EXP"], row["COST_PER_HOUR"], row["TOTAL_INCOME"],
                    row["TYPE"], row["HOTELID"], row["MONTH"], row["YEAR"]
                )
            cur.execute(query)
            finance_exp = "UPDATE FINANCES SET SERVICE_EXP = SERVICE_EXP + %d, TOTAL_INCOME = TOTAL_INCOME + %d WHERE HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
                row["SERVICE_EXP"], row["TOTAL_INCOME"], row["HOTELID"], row["MONTH"], row["YEAR"]
            )
            # print(finance_exp)
            cur.execute(finance_exp)
        else:
            query = "INSERT INTO CLUBS(HOTELID,  TYPE, SERVICE_EXP, MONTH, YEAR, TOTAL_INCOME, COST_PER_HOUR, SUPID) \
                VALUES('%d', '%s', '%d', '%d', '%d', '%d', '%d', %d)" % (
                    row["HOTELID"], row["TYPE"], row["SERVICE_EXP"], row["MONTH"],
                    row["YEAR"], row["TOTAL_INCOME"], row["COST_PER_HOUR"], row["SUPID"]
                )
            # print(query)
            cur.execute(query)

            finance_exp = "UPDATE FINANCES SET SERVICE_EXP = SERVICE_EXP + %d, TOTAL_INCOME = TOTAL_INCOME + %d WHERE HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
                row["SERVICE_EXP"], row["TOTAL_INCOME"], row["HOTELID"], row["MONTH"], row["YEAR"]
            )
            # print(finance_exp)
            cur.execute(finance_exp)

        con.commit()
    except Exception as e:
        print("Error adding clubs.")
        print(e)


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

        query_room_type = "SELECT TYPE FROM ROOM_TYPE where RATE = %d and MAX_GUESTS = %d" % (
            row["RATE"], row["MAX_GUESTS"])
        cur.execute(query_room_type)
        room_type = cur.fetchone()

        if room_type is None:
            room_type_insert = "INSERT INTO ROOM_TYPE (RATE, MAX_GUESTS) VALUES (%d, %d)" % (
                row["RATE"], row["MAX_GUESTS"])
            cur.execute(room_type_insert)

            cur.execute(query_room_type)
            con.commit()
            room_type = cur.fetchone()

        row["TYPE"] = room_type["TYPE"]
        print("Final room type = ", row["TYPE"])

        query = "INSERT INTO ROOMS(NUMBER, HOTELID, STATUS, TYPE) VALUES(%d, %d, %d, %d)" % (
            row["NUMBER"], row["HOTELID"], row["STATUS"], row["TYPE"])

        # print(query)
        cur.execute(query)
        con.commit()

        print("Inserted Into Database")

    except Exception as e:
        print("Error while inserting into ROOM: %s", e)


def add_member():
    # if True:
    try:
        row = {}
        print("Enter member details: ")
        row["TIER"] = int(input("Tier(1-5): "))
        row["FNAME"] = input("First name: ")
        row["LNAME"] = input("Last name: ")
        row["EMAILID"] = input("Email: ")
        row["DOB"] = input("Date of birth (YYYY-MM-DD): ")
        row["STAYS"] = int(input("Stays: "))

        while row["TIER"] not in [1, 2, 3, 4, 5]:
            row["TIER"] = int(input("Choose tier(1-5): "))

        query = "INSERT INTO MEMBERS (TIER, FNAME, LNAME, EMAILID, DOB, STAYS) values (%d, '%s', '%s', '%s', \'%s\', %d)" % (
            row["TIER"], row["FNAME"], row["LNAME"], row["EMAILID"], row["DOB"], row["STAYS"])
        # print("Query: ", query)
        cur.execute(query)
        con.commit()
        print("Inserted to database")
    except Exception as e:
        print("Error while add_member(): ", e)


def add_finances():
   
    # if True:
    try:
        query = "SELECT SUM(SALARY) FROM EMPLOYEE WHERE NOT STATUS='FIRED'"
        cur.execute(query)
        salary_cnt = cur.fetchone()
        row = {}
        print("Enter finance details: ")
        row["HOTELID"] = int(input("HOTEL ID: "))
        row["MONTH"] = int(input("MONTH(0-12): "))
        row["YEAR"] = int(input("YEAR: "))
        row["ELEC_BILL"] = int(input("Electricity bill: "))
        row["HOTEL_BILL"] = int(input("Hotel bill: "))
        row["EMP_EXP"] = int(input("Employee Expenditure: "))
        row["SERVICE_EXP"] = int(salary_cnt["SUM(SALARY)"])
        row["TOTAL_INCOME"] = int(input("Total income: "))

        if not (row["MONTH"] >= 1 and row["MONTH"] <= 12):
            print("Incorrect month entered")
            return

        if not hotel_exists(row["HOTELID"]):
            print("Error while adding finances: No such hotel exists")
            return

        finances_query = "INSERT INTO FINANCES(HOTELID, MONTH, YEAR, ELEC_BILL, HOTEL_BILL, EMP_EXP, SERVICE_EXP, TOTAL_INCOME) values (%d, %d,%d,%d,%d,%d,%d,%d)" % (
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

        populate_exp_profits(row["HOTELID"], row["MONTH"], row["YEAR"])

        con.commit()
        print("Inserted into database")
    except Exception as e:
        print("Error adding to finance.")
        print(e)


def add_service_staff_room():
    """
    Assign a service staff to a room
    """
    # if True:
    try:
        row = {}
        print("Enter room and service staff detail: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["SERVICE_STAFF_ID"] = int(input("Service staff ID: "))

        if not room_hotel_exists(row["ROOMNO"], row["HOTELID"]):
            print("Error assigning service staff: Room does not exist")
            return

        if not service_staff_exists(row["SERVICE_STAFF_ID"]):
            print("Error assigning service staff: Service staff does not exist")
            return

        query = "INSERT INTO SERVICE_STAFF_ROOM (ROOMNO, HOTELID, SERVICE_STAFF_ID) VALUES (%d, %d, %d)" % (
            row["ROOMNO"], row["HOTELID"], row["SERVICE_STAFF_ID"])
        cur.execute(query)
        con.commit()

        print("Successfully assigned")
    except Exception as e:
        print("Error assigning")
        print(e)


def remove_service_staff_room():
    """
    Remove a service staff from a room
    """
    # if True:
    try:
        row = {}
        print("Enter room and service staff detail: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["SERVICE_STAFF_ID"] = int(input("Service staff ID: "))

        if not room_hotel_exists(row["ROOMNO"], row["HOTELID"]):
            print("Error assigning service staff: Room does not exist")
            return

        if not service_staff_exists(row["SERVICE_STAFF_ID"]):
            print("Error assigning service staff: Service staff does not exist")
            return

        relation_exist_query = "SELECT * FROM SERVICE_STAFF_ROOM WHERE ROOMNO = %d AND HOTELID = %d AND SERVICE_STAFF_ID = %d" % (
            row["ROOMNO"], row["HOTELID"], row["SERVICE_STAFF_ID"])
        cur.execute(relation_exist_query)
        if cur.fetchone() is None:
            print("Service staff was not assigned to the room")
            return
        query = "DELETE FROM SERVICE_STAFF_ROOM WHERE ROOMNO = %d AND HOTELID = %d AND SERVICE_STAFF_ID = %d" % (
            row["ROOMNO"], row["HOTELID"], row["SERVICE_STAFF_ID"])
        cur.execute(query)
        con.commit()

        print("Successfully un-assigned")
    except Exception as e:
        print("Error unassigning service staff")
        print(e)


def finance_report():
    '''
    Generates Finance report for a give hotelid , month , year
    '''
    # if True:
    try:
        profit_avg_query = "SELECT AVG(TOTAL_PROFIT) AS AVG_PROFIT FROM PROFIT" 
        cur.execute(profit_avg_query)
        profit_avg = cur.fetchone()["AVG_PROFIT"]
        hotelid = int(input("Enter hotel id: "))
        month = int(input("Enter Month: "))
        year = int(input("Year: "))

        if not (month >= 1 and month <= 12):
            print("Incorrect month entered")
            return
        
        if not finances_exists(hotelid, month, year):
            print("No such Finance entry has been made. \n")
            return

        populate_exp_profits(hotelid, month, year)

        query = "SELECT * FROM FINANCES NATURAL JOIN EXPENDITURE NATURAL JOIN PROFIT WHERE \
                FINANCES.HOTELID=%s AND \
                FINANCES.MONTH=%s AND \
                FINANCES.YEAR=%s " % (hotelid, month, year)
        cur.execute(query)
        finances = cur.fetchone()
        managerid_query = "SELECT MANAGERID , FNAME , LNAME FROM HOTEL JOIN EMPLOYEE WHERE \
                            HOTEL.ID=%s AND \
                            EMPLOYEE.ID=HOTEL.MANAGERID" % (hotelid)
        cur.execute(managerid_query)
        manager_details = cur.fetchone()
        print("------------------------FINANCE REPORT-----------------------\n")
        print("MONTH:                ", month)
        print("YEAR:                 ", year)
        print("HOTELID:              ", hotelid)
        print("MANAGERID:            ", manager_details["MANAGERID"])
        print("MANAGER NAME:         ",
              manager_details["FNAME"], " ", manager_details["LNAME"])
        print("EMPLOYEE EXPENDITURE: ", finances["EMP_EXP"])
        print("SERVICE EXPENDITURE:  ", finances["SERVICE_EXP"])
        print("ELECTRICITY BILL:     ", finances["ELEC_BILL"])
        print("HOTEL BILL:           ", finances["HOTEL_BILL"])
        print("TOTAL EXPENDITURE:    ", finances["TOTAL_EXP"])
        print("TOTAL INCOME:         ", finances["TOTAL_INCOME"])
        print("TOTAL PROFIT:         ", finances["TOTAL_PROFIT"])
        if profit_avg < finances["TOTAL_PROFIT"]:
            print("Hotel profit higher than average")
        print("-------------------------------------------------------------\n")
    except Exception as e:
        print("Failed to generate report \n")
        print(e)

def add_guest():
    # if True:
    try:
        row = {}
        print("Enter Guest details: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["ISMEMBER"] = int(input("Is member(1/0): "))
        row["MEMBERID"] = 0
        if row["ISMEMBER"] == 0:
            row["MEMBERID"] = None
        else:
            row["MEMBERID"] = int(input("Member ID: "))
        row["CHECKIN"] = input("Checkin date (YYYY-MM-DD): ")
        row["CHECKOUT"] = input("Checkout date(YYYY-MM-DD): ")
        row["COST"] = 0
        row["CLUB_HOURS"] = 0

        y_in, m_in, d_in = int(row["CHECKIN"].split('-')[0]), int(row["CHECKIN"].split('-')[1]), int(row["CHECKIN"].split('-')[2])
        y_out, m_out, d_out = int(row["CHECKOUT"].split('-')[0]), int(row["CHECKOUT"].split('-')[1]), int(row["CHECKOUT"].split('-')[2])
        
        if y_out < y_in or (y_out == y_in and m_out < m_in) or (y_out == y_in and m_out == m_in and d_out <= d_in):
            print("Date errors")
            return

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
        update_rooms_status = "UPDATE ROOMS SET STATUS = 1 WHERE NUMBER = %d AND HOTELID = %d" % (
            row["ROOMNO"], row["HOTELID"])
        cur.execute(update_rooms_status)

        if row["ISMEMBER"]:  # increment number of stays
            member_query = "UPDATE MEMBERS SET STAYS = STAYS + 1 WHERE ID = %d" % (
                row["MEMBERID"])
            cur.execute(member_query)
            print("Member stays updated")

        con.commit()

        print("Guest checked in.")
    except Exception as e:
        print("Error checking in guest")
        print(e)


def remove_guest():
    # if True:
    try:
        row = {}
        print("Enter Guest details: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["CHECKIN"] = input("Checkin date: ")
        row["CHECKOUT"] = input("Checkout date: ")

        if not guest_exists(row["ROOMNO"], row["HOTELID"], row["CHECKIN"], row["CHECKOUT"]):
            print("Guest does not exist")
            return

        clear_mr_entry = "DELETE FROM MASTER_RELATIONSHIP WHERE ROOMNO = %d AND HOTELID = %d AND CHECKIN = '%s' AND CHECKOUT = '%s'" % (
            row["ROOMNO"],
            row["HOTELID"],
            row["CHECKIN"],
            row["CHECKOUT"]
        )
        cur.execute(clear_mr_entry)

        #  GENERATE COST
        cost_guest_generation(
            row["ROOMNO"],
            row["HOTELID"],
            row["CHECKIN"],
            row["CHECKOUT"]
        )

        query = "DELETE FROM GUESTS WHERE ROOMNO = %d AND HOTELID = %d AND CHECKIN = '%s' AND CHECKOUT = '%s'" % (
            row["ROOMNO"],
            row["HOTELID"],
            row["CHECKIN"],
            row["CHECKOUT"]
        )
        cur.execute(query)

        update_rooms_status = "UPDATE ROOMS SET STATUS = 0 WHERE NUMBER = %d AND HOTELID = %d" % (
            row["ROOMNO"], row["HOTELID"])
        cur.execute(update_rooms_status)

        con.commit()

        print(update_rooms_status)
        print("Guest successfully checked out. Room emptied.")
    
    except Exception as e:
        print("Error checking out")
        print(e)


def add_guest_club():
    """
    mysql> DESC MASTER_RELATIONSHIP;
    +-----------------+--------------+------+-----+---------+-------+
    | Field           | Type         | Null | Key | Default | Extra |
    +-----------------+--------------+------+-----+---------+-------+
    | ROOMNO          | int          | NO   | PRI | NULL    |       |
    | HOTELID         | int          | NO   | PRI | NULL    |       |
    | CHECKIN         | date         | NO   | PRI | NULL    |       |
    | CHECKOUT        | date         | NO   | PRI | NULL    |       |
    | CLUB_TYPE       | varchar(255) | NO   | PRI | NULL    |       |
    | MONTH           | int          | NO   | PRI | NULL    |       |
    | YEAR            | int          | NO   | PRI | NULL    |       |
    | CLUB_HOURS_USED | int          | YES  |     | NULL    |       |
    +-----------------+--------------+------+-----+---------+-------+
    8 rows in set
    """
    # if True:
    try:
        row = {}
        print("Enter Guest details: ")
        row["ROOMNO"] = int(input("Room number: "))
        row["HOTELID"] = int(input("Hotel ID: "))
        row["CHECKIN"] = input("Checkin date: ")
        row["CHECKOUT"] = input("Checkout date: ")
        print("Enter Club details: ")
        row["CLUB_TYPE"] = input("Club type: ")
        row["CLUB_HOURS_USED"] = int(input("Hours registered for: "))
        # row["MONTH"] = int(input("Month of joining: "))
        # row["YEAR"] = int(input("Year: "))
        row["YEAR"], row["MONTH"] = int(row["CHECKOUT"].split("-")[0]), int(row["CHECKOUT"].split("-")[1])

        if not guest_exists(row["ROOMNO"], row["HOTELID"], row["CHECKIN"], row["CHECKOUT"]):
            print("Invalid guest information")
            return

        club_type_query = "SELECT * FROM CLUBS WHERE HOTELID = %d AND TYPE = '%s'" % (
            row["HOTELID"], row["CLUB_TYPE"])
        cur.execute(club_type_query)

        if cur.fetchone() is None:
            print("Such a club does not exist in the hotel")
            return
        else:
            club_exist_q = "SELECT * FROM CLUBS WHERE HOTELID = %d AND TYPE = '%s' AND MONTH = %d AND YEAR = %d" % (
                row["HOTELID"], row["CLUB_TYPE"], row["MONTH"], row["YEAR"])
            cur.execute(club_exist_q)
            if cur.fetchone() is None:
                print("Club has not been updated.")
                supid = int(input("Enter supervisor ID for this month: "))
                while not supervisor_exists(supid):
                    supid = int(
                        input("Supervisor does not exist. Enter valid ID: "))
                cost_per_hour = int(input("Enter cost per hour for this month: "))
                service_exp = int(input("Enter projected service expenditure: "))

                club_type_query = "INSERT INTO CLUBS (HOTELID, TYPE, MONTH, YEAR, SUPID, COST_PER_HOUR, SERVICE_EXP) VALUES (%d, '%s', %d, %d, %d, %d, %d)" % (
                    row["HOTELID"], row["CLUB_TYPE"], row["MONTH"], row["YEAR"], supid, cost_per_hour, service_exp
                )
                cur.execute(club_type_query)

                create_finances_if_not_exist(row["HOTELID"], row["MONTH"], row["YEAR"])

                finance_exp = "UPDATE FINANCES SET SERVICE_EXP = SERVICE_EXP + %d, TOTAL_INCOME = TOTAL_INCOME + %d WHERE HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
                    service_exp, cost_per_hour * row["CLUB_HOURS_USED"], row["HOTELID"], row["MONTH"], row["YEAR"]
                )
                cur.execute(finance_exp)
                con.commit()

        create_finances_if_not_exist(row["HOTELID"], row["MONTH"], row["YEAR"])

        mr_query = "SELECT * FROM MASTER_RELATIONSHIP WHERE \
                    ROOMNO = %d AND \
                    HOTELID = %d AND \
                    CHECKIN = '%s' AND \
                    CHECKOUT = '%s' AND \
                    CLUB_TYPE = '%s' AND \
                    MONTH = '%d' AND \
                    YEAR = %d" % (
                        row["ROOMNO"],
                        row["HOTELID"],
                        row["CHECKIN"],
                        row["CHECKOUT"],
                        row["CLUB_TYPE"],
                        row["MONTH"],
                        row["YEAR"]
                    )
        cur.execute(mr_query)
        if cur.fetchone() is None:
            mr_query = "INSERT INTO MASTER_RELATIONSHIP(ROOMNO, HOTELID, CHECKIN, CHECKOUT, CLUB_TYPE, MONTH, YEAR, CLUB_HOURS_USED) VALUES (%d, %d, '%s', '%s', '%s', %d, %d, %d)" % (
                row["ROOMNO"],
                row["HOTELID"],
                row["CHECKIN"],
                row["CHECKOUT"],
                row["CLUB_TYPE"],
                row["MONTH"],
                row["YEAR"],
                row["CLUB_HOURS_USED"]
            )
            cur.execute(mr_query)
        else:
            print("Guest has already been registered. Increasing time registered")
            mr_query = "UPDATE MASTER_RELATIONSHIP SET CLUB_HOURS_USED = CLUB_HOURS_USED + %d WHERE \
                        ROOMNO = %d AND \
                        HOTELID = %d AND \
                        CHECKIN = '%s' AND \
                        CHECKOUT = '%s' AND \
                        CLUB_TYPE = '%s' AND \
                        MONTH = '%d' AND \
                        YEAR = %d" % (
                            row["CLUB_HOURS_USED"], row["ROOMNO"], row["HOTELID"],
                            row["CHECKIN"], row["CHECKOUT"], row["CLUB_TYPE"],
                            row["MONTH"], row["YEAR"]
                        )
            cur.execute(mr_query)

        club_rate_query = "SELECT COST_PER_HOUR FROM CLUBS WHERE HOTELID = %d AND TYPE = '%s' AND MONTH = %d AND YEAR = %d" % (
            row["HOTELID"], row["CLUB_TYPE"], row["MONTH"], row["YEAR"]
        )
        cur.execute(club_rate_query)
        club_rate = cur.fetchone()["COST_PER_HOUR"]

        print("Club registered for month = %d and year = %d" %
              (row["MONTH"], row["YEAR"]))
        print("Cost per hour = ", club_rate)

        club_income_update = "UPDATE CLUBS SET TOTAL_INCOME = TOTAL_INCOME + %d \
            WHERE HOTELID = %d AND TYPE = '%s' AND MONTH = %d AND YEAR = %d" % (
                row["CLUB_HOURS_USED"] * club_rate,
                row["HOTELID"], row["CLUB_TYPE"], row["MONTH"], row["YEAR"]
            )
        cur.execute(club_income_update)

        finance_exp = "UPDATE FINANCES SET TOTAL_INCOME = TOTAL_INCOME + %d WHERE HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
            row["CLUB_HOURS_USED"] *
                club_rate, row["HOTELID"], row["MONTH"], row["YEAR"]
        )
        cur.execute(finance_exp)

        con.commit()

        print("Guest successfully registered")
    except Exception as e:
        print("Error registering")
        print(e)


def dispatch():
    """
    Function that maps helper functions to option entered
    """
    print("The following options are possible for employee management")
    print("a. Add an Employee")
    print("b. Fire an Employee")
    print("c. Assign service staff to room")
    print("d. Remove service staff from room")
    print("e. Alter Employee Details")
    print("f. Modify service staff for room")
    ch = input("Enter choice: ")
    if(ch == "a"):
        hireAnEmployee()

    elif(ch == "b"):
        fireAnEmployee()

    elif (ch == "c"):
        add_service_staff_room()

    elif (ch == "d"):
        remove_service_staff_room()

    elif (ch == "e"):
        modify_employee()

    elif (ch == "f"):
        modify_service_staff_for_one_room()

    else:
        print("Error: Invalid Option")


def cost_guest():
    '''
    Get the entire cost of stay and generate the bill for the guest
    '''
    try:
        club_cost = 0
        stay_cost = 0
        member_discount = 0
        date_format = "%Y-%m-%d"
        member_discount_dict = {
            1: 100,
            2: 200,
            3: 300,
            4: 400,
            5: 500
        }
        member_stays_dict = {
            10: 100,
            50: 200,
            100: 500
        }

        roomno = int(input("Enter room number: "))
        hotelid = int(input("Enter HotelID: "))
        checkin = input("Enter Checkin: ")
        checkout = input("Enter Checkout: ")
        if not room_hotel_exists(roomno, hotelid):
            print("Room dosen't exist in the hotel\n")
            return
        if is_room_empty(roomno, hotelid):
            print("Room is empty\n")
            return
        if not guest_exists(roomno, hotelid, checkin, checkout):
            print("No such guest with the matching details exists \n")
            return

        query = "SELECT CLUB_TYPE,CLUB_HOURS_USED,MONTH,YEAR FROM MASTER_RELATIONSHIP WHERE \
                ROOMNO=%s AND \
                HOTELID=%s AND \
                CHECKIN='%s' AND \
                CHECKOUT='%s' " % (roomno, hotelid, checkin, checkout)
        cur.execute(query)
        results = cur.fetchall()

        for result in results:
            query = "SELECT COST_PER_HOUR FROM CLUBS WHERE \
                    HOTELID=%s AND \
                    TYPE='%s' AND \
                    MONTH=%s AND \
                    YEAR=%s" % (hotelid, result["CLUB_TYPE"], result["MONTH"], result["YEAR"])
            cur.execute(query)
            result1 = cur.fetchone()
            club_cost = (
                club_cost + result1["COST_PER_HOUR"] * result["CLUB_HOURS_USED"])

        query = "SELECT TYPE FROM ROOMS WHERE \
                NUMBER=%s AND \
                HOTELID=%s " % (roomno, hotelid)
        cur.execute(query)
        type_result = cur.fetchone()
        type_query = "SELECT RATE FROM ROOM_TYPE WHERE TYPE=%s" % (
            type_result["TYPE"])
        cur.execute(type_query)
        type_cost = cur.fetchone()
        start_date = datetime.strptime(checkin, date_format)
        end_date = datetime.strptime(checkout, date_format)
        stay_days = end_date - start_date
        tot_stays = stay_days.days + 1
        stay_cost = tot_stays * type_cost["RATE"]

        member_check_query = "SELECT IS_MEMBER , MEMBERID FROM GUESTS WHERE \
                            ROOMNO=%s AND \
                            HOTELID=%s AND \
                            CHECKIN='%s' AND \
                            CHECKOUT='%s' " % (roomno, hotelid, checkin, checkout)
        cur.execute(member_check_query)
        member_check = cur.fetchone()
        if not (member_check["MEMBERID"] is None):
            query = "SELECT TIER , STAYS FROM MEMBERS WHERE ID=%s" % (
                member_check["MEMBERID"])
            cur.execute(query)
            member_stats = cur.fetchone()
            member_discount = member_discount + \
                member_discount_dict[member_stats["TIER"]]
            if member_stats["STAYS"] >= 100:
                member_discount = member_discount + member_stays_dict[100]
            elif member_stats["STAYS"] >= 50:
                member_discount = member_discount + member_stays_dict[50]
            elif member_stats["STAYS"] >= 10:
                member_discount = member_discount + member_stays_dict[10]

        print("Your total stay cost is:  ", stay_cost)
        print("Your total club cost is: ", club_cost)
        print("Discount :", member_discount)
        grand_total = stay_cost + club_cost - member_discount
        print("Your grand total is: ", grand_total)

    except Exception as e:
        print("Couldn't generate bill \n")
        print(e)


def cost_guest_generation(roomno, hotelid, checkin, checkout):
    '''
    Get the entire cost of stay and generate the bill for the guest
    '''
    try:
        club_cost = 0
        stay_cost = 0
        member_discount = 0
        date_format = "%Y-%m-%d"
        member_discount_dict = {
            1: 100,
            2: 200,
            3: 300,
            4: 400,
            5: 500
        }
        member_stays_dict = {
            10: 100,
            50: 200,
            100: 500
        }

        if not room_hotel_exists(roomno, hotelid):
            print("Room dosen't exist in the hotel\n")
            return
        if is_room_empty(roomno, hotelid):
            print("Room is empty\n")
            return
        if not guest_exists(roomno, hotelid, checkin, checkout):
            print("No such guest with the matching details exists \n")
            return

        query = "SELECT CLUB_TYPE,CLUB_HOURS_USED,MONTH,YEAR FROM MASTER_RELATIONSHIP WHERE \
                ROOMNO=%s AND \
                HOTELID=%s AND \
                CHECKIN='%s' AND \
                CHECKOUT='%s' " % (roomno, hotelid, checkin, checkout)
        cur.execute(query)
        results = cur.fetchall()

        for result in results:
            query = "SELECT COST_PER_HOUR FROM CLUBS WHERE \
                    HOTELID=%s AND \
                    TYPE='%s' AND \
                    MONTH=%s AND \
                    YEAR=%s" % (hotelid, result["CLUB_TYPE"], result["MONTH"], result["YEAR"])
            cur.execute(query)
            result1 = cur.fetchone()
            club_cost = (
                club_cost + result1["COST_PER_HOUR"] * result["CLUB_HOURS_USED"])

        query = "SELECT TYPE FROM ROOMS WHERE \
                NUMBER=%s AND \
                HOTELID=%s " % (roomno, hotelid)
        cur.execute(query)
        type_result = cur.fetchone()
        type_query = "SELECT RATE FROM ROOM_TYPE WHERE TYPE=%s" % (
            type_result["TYPE"])
        cur.execute(type_query)
        type_cost = cur.fetchone()
        start_date = datetime.strptime(checkin, date_format)
        end_date = datetime.strptime(checkout, date_format)
        stay_days = end_date - start_date
        tot_stays = stay_days.days + 1
        stay_cost = tot_stays * type_cost["RATE"]

        member_check_query = "SELECT IS_MEMBER , MEMBERID FROM GUESTS WHERE \
                            ROOMNO=%s AND \
                            HOTELID=%s AND \
                            CHECKIN='%s' AND \
                            CHECKOUT='%s' " % (roomno, hotelid, checkin, checkout)
        cur.execute(member_check_query)
        member_check = cur.fetchone()
        if not (member_check["MEMBERID"] is None):
            query = "SELECT TIER , STAYS FROM MEMBERS WHERE ID=%s" % (
                member_check["MEMBERID"])
            cur.execute(query)
            member_stats = cur.fetchone()
            member_discount = member_discount + \
                member_discount_dict[member_stats["TIER"]]
            if member_stats["STAYS"] >= 100:
                member_discount = member_discount + member_stays_dict[100]
            elif member_stats["STAYS"] >= 50:
                member_discount = member_discount + member_stays_dict[50]
            elif member_stats["STAYS"] >= 10:
                member_discount = member_discount + member_stays_dict[10]

        print("Your total stay cost is:  ", stay_cost)
        print("Your total club cost is: ", club_cost)
        print("Discount :", member_discount)
        grand_total = stay_cost + club_cost - member_discount
        print("Your grand total is: ", grand_total)

        year, month = int(checkout.split('-')[0]), int(checkout.split('-')[1])

        print("year = %d, month = %d" % (year, month))

        create_finances_if_not_exist(hotelid, month, year)

        finances_income_update = "UPDATE FINANCES SET TOTAL_INCOME = TOTAL_INCOME + %d WHERE \
            HOTELID = %d AND MONTH = %d AND YEAR = %d" % (
                grand_total,
                hotelid, month, year
            )
        cur.execute(finances_income_update)
        con.commit()

    except Exception as e:
        print("Couldn't generate bill \n")
        print(e)

def view_table(rows):
    r = []
    try:
        r.append(list(rows[0].keys()))
    except Exception as e:
        print(e)   
        return
    for row in rows:
        temp = []
        for k in row.keys():
            temp.append(row[k])
        r.append(temp)
    print(tabulate(r, tablefmt="grid", headers="firstrow"))
    print()
    return

def handle_views():
    print("Select from the following to retrieve information: ")
    print("Choose a VIEW option\n\n")
    print("0. Hotels")
    print("1. Employees")
    print("2. Members and guests")
    print("3. Clubs")
    print("4. Rooms")
    print("5. FINANCIAL REPORT")

    choice=int(input("SELECT> "))
    query = ""
    if (choice == 1):
        hId=int(input("Please specify hotelID: "))
        print("1.  Employees")
        print("2. Fired employees")
        print("3.  Service staff")
        print("4.  Supervisors")
        print("5.  Managers")
        chch=int(input("SELECT> "))
        if (chch == 1):
            query = "SELECT * from EMPLOYEE WHERE ID IN(select EMPID from BELONGS_TO where HOTELID=%s)" % (
                hId)
        elif (chch == 2):
            query = "SELECT * from EMPLOYEE WHERE ID IN(select EMPID from BELONGS_TO where HOTELID=%s) and status != 'employed" % (
                hId)
        elif (chch == 3):
            query = "select * from employee where id in (select id from service_staff) and id in (select EMPID from BELONGS_TO where HOTELID=%s)" % (
                hId)
        elif (chch == 4):
            query = "select * from employee where id in (select id from supervisor) and hotelid = %s" %(hId)
        elif (chch == 5):
            query = "select * from employee where id in (select id from MANAGER) and id in (select EMPID from BELONGS_TO where HOTELID=%s)" % (
                hId)
        else:
            print("invalid")

    if (choice == 2):
        hId=int(input("Please specify hotelID: "))
        print("1.  Guests")
        print("2.  Members")
        print("3.  Member guests")
        print("4.  Members of a tier")
        chch=int(input("SELECT> "))
        if (chch == 1):
            query = "select * from GUESTS where HOTELID = %s" % (hId)
        elif (chch == 2):
            query = "select * from MEMBERS"
        elif(chch == 3):
            query = "select * from MEMBERS where ID in (selct MEMBERID from guests where HOTELID = %s and ISMEMBER = 1)" % (
                hId)
        elif (chch == 4):
            tier = input("Enter tier: ")
            query = "select * from MEMBERS where TIER = %s" % (tier)
        else:
            print("invalid")


    if (choice == 3):
        hId=int(input("Please specify hotelID: "))
        print("1. All Clubs")
        print("2. Finance info of clubs of type")
        chch=int(input("SELECT> "))
        if (chch == 1):
            query = "select * from CLUBS where HOTELID = %s" % (hId)
        elif (chch == 2):
            cType = input("Please specify club type: ")
            query = "select * from CLUBS where HOTELID = %s and TYPE = '%s'" % (
                hId, cType)
        else:
            print("invlaid")

    if (choice == 4):
        hId=int(input("Please specify hotelID: "))
        print("1. Rooms of a hotel")
        print("2. Unoccupied rooms of a hotel")
        print("3. Rooms in a hotel currently occupied")
        print("4. Rooms of a certain cost interval")
        chch=int(input("SELECT> "))
        if (chch == 1):
            query = "select * from ROOMS, ROOM_TYPE where HOTELID = %s and ROOMS.TYPE = ROOM_TYPE.TYPE" % (
                hId)
        elif (chch == 2):
            query = "select * from ROOMS where HOTELID = %s and STATUS = 0" % (
                hId)
        elif (chch == 3):
            query = "select * from ROOMS where HOTELID = %s and STATUS = 1" % (
                hId)
        elif (chch == 4):
            lb = int(input("enter lower bound: "))
            ub = int(input("enter upper bound: "))
            query = "select * from ROOMS, ROOM_TYPE where ROOMS.type = ROOM_TYPE.type and hotelid = %s and %s >= rate and %s <= rate" % (
                hId, ub, lb)
        else:
            print("invalid")
    
    if (chch == 5):
        finance_report()



    try:
        cur.execute(query)
    except Exception as e:
        print(e)
    rows = cur.fetchall()
    view_table(rows)


# Global
while(1):
    tmp=sp.call('clear', shell = True)

    # Can be skipped if you want to hard core username and password
    username=input("Username: ")
    password=input("Password: ")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQLl server
        con=pymysql.connect(host = 'localhost',
                              user = username,
                              port = 5005,
                              password = password,
                              db = 'HCDBMS',
                              cursorclass = pymysql.cursors.DictCursor)
        tmp=sp.call('clear', shell = True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp=input("Enter any key to CONTINUE>")

        with con.cursor():
            cur = con.cursor()
            while(1):
                # Here taking example of Employee Mini-world
                print("0. Get data")
                print("1. Manage employees")
                print("2. Add Hotel")
                print("3. Add a Club")
                print("4. Check in a Guest")
                print("5. Check out a Guest")
                print("6. Add a room to a hotel")
                print("7. Guest registering to club")
                print("8. Add monthly finance")
                print("9. Generate profit report")
                print("10. Generate Guest Bill")
                print("11. Add a Member Guest")
                print("20. Logout")
                ch=int(input("Enter choice> "))
                tmp=sp.call('clear', shell = True)
                if ch == 0:
                    handle_views()
                elif ch == 1:
                    dispatch()
                elif ch == 3:
                    add_club()
                elif ch == 2:
                    add_hotel()
                elif ch == 6:
                    add_room()
                elif ch == 7:
                    add_guest_club()
                elif ch == 9:
                    finance_report()
                elif (ch == 11):
                    add_member()
                elif (ch == 8):
                    add_finances()
                elif (ch == 4):
                    add_guest()
                elif (ch == 5):
                    remove_guest()
                elif (ch == 10):
                    cost_guest()
                elif ch == 20:
                    break
                tmp=input("Enter any key to CONTINUE>")

    except:
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
