
# 271201

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
    try:
        # Takes emplyee details as input
        row = {}
        print("Enter club's details: ")
        row["HOTELID"] = int(input("HOTELID: "))
        row["TYPE"] = input("TYPE: ")
        row["SERVICE_EXP"] = intinput("Monthly Service expenditure: "))
        row["MONTH"] = int(input("Month: "))
        row["YEAR"] = int(input("Year: "))
        row["TOTAL_INCOME"] = int(input("Monthly total income: "))
        row["COST_PER_HOUR"] = int(input("Cost per hour: "))
        row["SUPID"] = int(input("Supervisor ID: "))

        query = "INSERT INTO CLUBS(HOTELID,  TYPE, SERVICE_EXP, MONTH, YEAR, TOTAL_INCOME, COST_PER_HOUR, SUPID) VALUES('%d', '%s', '%d', '%d', '%d', '%d', '%d', %d, %d)" % (
            row["HOTELID"], row["TYPE"], row["SERVICE_EXP"], row["MONTH"], row["YEAR"], row["TOTAL_INCOME"], row["COST_PER_HOUR"], row["SUPID"])

        print(query)
        cur.execute(query)
        con.commit()

        print("Inserted Into Database")

    except:
        print("oops")
