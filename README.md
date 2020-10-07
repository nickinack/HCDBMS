# HCDBMS

HCDBMS is a administrator side Hotel Chain database management system made as a part of <i>CS4.301 Data and Applications, Monsoon 2020. </i> The project has been divided into four phases and the details of each of these phases have been shared in this repository. The phases are as follows:

- Requirements document creation
- ER Diagram
- Normalisation
- CLI Phase

# CLI Specifications

We have used MySQL and PyMySQL client library to interact with the SQL Database. We have implemented extensive lists of functional requirements and some of them have been listen below:

- Create a new hotel branch
- Add a club 
- Get detailed financial reports for a given hotel
- Search for rooms given a price range
- Add/Fire and employee
- Add Members
- Provide member discounts depending on the member tier and stays

Key features of our implementation include:

- Extensive update capabilities using the interface.
- Extensive consideration of corner cases.
- Proper constraints specified at both the database and the user interface level.
- Guest details (Name,SSN) have not been taken into consideration to maintain anonymity.

# Running

First clone the repository and then go the respective directory. Install the requirements using:

```bash
pip install requirements.txt
```

Now,feed the dump using the following command:

```bash
mysql -h 127.0.0.1 -u username --port==<port number> -p < dump.sql
```

Finally, run the python code using the following command:

```bash
python3 main.py
```


