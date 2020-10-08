-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: HCDBMS
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `BELONGS_TO`
--
DROP DATABASE IF EXISTS HCDBMS;
CREATE DATABASE HCDBMS;
USE HCDBMS;
DROP TABLE IF EXISTS `BELONGS_TO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `BELONGS_TO` (
  `HOTELID` int NOT NULL,
  `EMPID` int NOT NULL,
  PRIMARY KEY (`HOTELID`,`EMPID`),
  KEY `EMPID` (`EMPID`),
  CONSTRAINT `BELONGS_TO_ibfk_1` FOREIGN KEY (`HOTELID`) REFERENCES `HOTEL` (`ID`),
  CONSTRAINT `BELONGS_TO_ibfk_2` FOREIGN KEY (`EMPID`) REFERENCES `EMPLOYEE` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BELONGS_TO`
--

LOCK TABLES `BELONGS_TO` WRITE;
/*!40000 ALTER TABLE `BELONGS_TO` DISABLE KEYS */;
INSERT INTO `BELONGS_TO` VALUES (3,123),(1,1292),(2,1334),(1,2187),(2,2312),(1,6969),(1,7823),(1,8973),(1,9842),(1,9873),(2,9985),(1,80085),(1,98745);
/*!40000 ALTER TABLE `BELONGS_TO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CLUBS`
--

DROP TABLE IF EXISTS `CLUBS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CLUBS` (
  `HOTELID` int NOT NULL,
  `TYPE` varchar(255) NOT NULL,
  `SERVICE_EXP` int NOT NULL DEFAULT '0',
  `MONTH` int NOT NULL,
  `YEAR` int NOT NULL,
  `TOTAL_INCOME` int NOT NULL DEFAULT '0',
  `COST_PER_HOUR` int NOT NULL,
  `SUPID` int NOT NULL,
  PRIMARY KEY (`HOTELID`,`TYPE`,`MONTH`,`YEAR`),
  KEY `SUPID` (`SUPID`),
  CONSTRAINT `CLUBS_ibfk_1` FOREIGN KEY (`SUPID`) REFERENCES `SUPERVISOR` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CLUBS`
--

LOCK TABLES `CLUBS` WRITE;
/*!40000 ALTER TABLE `CLUBS` DISABLE KEYS */;
INSERT INTO `CLUBS` VALUES (1,'burgers',5663,12,2020,845,12,1292),(1,'spa',35,12,2020,780,12,9842);
/*!40000 ALTER TABLE `CLUBS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EMPLOYEE`
--

DROP TABLE IF EXISTS `EMPLOYEE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EMPLOYEE` (
  `ID` int NOT NULL,
  `FNAME` varchar(255) NOT NULL,
  `LNAME` varchar(255) NOT NULL,
  `PHONE` int NOT NULL,
  `EMAIL` varchar(255) NOT NULL,
  `DOB` date NOT NULL,
  `JOINDATE` date NOT NULL,
  `STATUS` varchar(255) NOT NULL,
  `SALARY` int NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `EMAIL` (`EMAIL`),
  UNIQUE KEY `PHONE` (`PHONE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPLOYEE`
--

LOCK TABLES `EMPLOYEE` WRITE;
/*!40000 ALTER TABLE `EMPLOYEE` DISABLE KEYS */;
INSERT INTO `EMPLOYEE` VALUES (112,'K','ubunu',123673,'ubunu@ubunu.org','2001-01-01','2019-01-02','FIRED',12346),(123,'RANDOM','MANAGERCOOLBOIY',345120,'random_manager@coolboy.xyz','2002-03-01','2019-06-01','currently employed',546546),(1292,'not_fnae','tha',458734,'o@tha.ks','1987-12-23','2020-12-23','currently employed',782347),(1313,'bloody','marie',576562,'bloody_marie@halloween.com','2019-12-13','2020-12-04','FIRED',45682),(1334,'temp','staff',476734,'temp@gmail.com','2002-02-03','2019-02-02','currently employed',45643),(2187,'john','boyega',794532,'john.finn@gmail.com','2001-12-23','2020-12-23','currently employed',21871),(2312,'Hama','Watertribe',792303,'hama.waters@yahoo.com','2002-12-23','2020-12-23','currently employed',763783),(6969,'abhi','siv',687622,'abhi.siv@onlyfans.com','2001-12-22','2020-12-23','currently employed',126872),(7823,'doe','john',346783,'dfg@jkjh.com','1987-12-23','2020-12-23','currently employed',390489),(8973,'queer','meave',878312,'proud.meave@vought.com','1992-12-23','2020-12-23','FIRED',823782),(9842,'wendy','mcdonald',128773,'wendy@mcD.com','2001-12-23','2020-12-23','currently employed',876872),(9873,'saru','sen',983213,'saru@gmail.com','2001-12-23','2020-12-23','currently employed',128764),(9985,'staff','temp',123098,'staff@temp.com','2002-03-05','2019-02-02','currently employed',76573),(80085,'karthik','vis',987433,'karkar@queerandproud.com','2001-12-23','2020-12-23','currently employed',42069),(98745,'luke','vader',987402,'luke@saberupmyass.com','1969-12-23','2020-12-23','currently employed',986986);
/*!40000 ALTER TABLE `EMPLOYEE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EXPENDITURE`
--

DROP TABLE IF EXISTS `EXPENDITURE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EXPENDITURE` (
  `ELEC_BILL` int NOT NULL,
  `HOTEL_BILL` int NOT NULL,
  `EMP_EXP` int NOT NULL,
  `SERVICE_EXP` int NOT NULL,
  `TOTAL_EXP` int NOT NULL,
  `TOTAL_INCOME` int NOT NULL,
  PRIMARY KEY (`ELEC_BILL`,`HOTEL_BILL`,`EMP_EXP`,`SERVICE_EXP`,`TOTAL_INCOME`),
  KEY `TOTAL_EXP` (`TOTAL_EXP`,`TOTAL_INCOME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EXPENDITURE`
--

LOCK TABLES `EXPENDITURE` WRITE;
/*!40000 ALTER TABLE `EXPENDITURE` DISABLE KEYS */;
INSERT INTO `EXPENDITURE` VALUES (345,345,3356270,3453,3360413,345327),(345,4564,3356270,345,3361524,345352),(456,4567,3356270,3453,3364746,0),(345,4564,3356270,6008,3367187,346029),(1334,1234,12345,4120053,4134966,1231242);
/*!40000 ALTER TABLE `EXPENDITURE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FINANCES`
--

DROP TABLE IF EXISTS `FINANCES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FINANCES` (
  `HOTELID` int NOT NULL,
  `MONTH` int NOT NULL,
  `YEAR` int NOT NULL,
  `ELEC_BILL` int NOT NULL DEFAULT '0',
  `HOTEL_BILL` int NOT NULL DEFAULT '0',
  `EMP_EXP` int NOT NULL DEFAULT '0',
  `SERVICE_EXP` int NOT NULL DEFAULT '0',
  `TOTAL_INCOME` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`HOTELID`,`MONTH`,`YEAR`),
  KEY `ELEC_BILL` (`ELEC_BILL`,`HOTEL_BILL`,`EMP_EXP`,`SERVICE_EXP`,`TOTAL_INCOME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FINANCES`
--

LOCK TABLES `FINANCES` WRITE;
/*!40000 ALTER TABLE `FINANCES` DISABLE KEYS */;
INSERT INTO `FINANCES` VALUES (2,1,2019,0,0,12346,0,0),(3,3,2019,0,0,34547,0,0),(2,2,2019,0,0,122216,0,0),(3,6,2019,0,0,546546,0,0),(2,12,2020,0,0,809465,0,0),(1,12,2020,345,4564,3356270,6043,346789),(1,11,2020,456,4567,3356270,3453,0);
/*!40000 ALTER TABLE `FINANCES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GUESTS`
--

DROP TABLE IF EXISTS `GUESTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GUESTS` (
  `ROOMNO` int NOT NULL,
  `HOTELID` int NOT NULL,
  `IS_MEMBER` bit(1) NOT NULL,
  `MEMBERID` int DEFAULT NULL,
  `CHECKIN` date NOT NULL,
  `CHECKOUT` date NOT NULL,
  `COST` int NOT NULL,
  `CLUB_HOURS` int DEFAULT NULL,
  PRIMARY KEY (`ROOMNO`,`HOTELID`,`CHECKIN`,`CHECKOUT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GUESTS`
--

LOCK TABLES `GUESTS` WRITE;
/*!40000 ALTER TABLE `GUESTS` DISABLE KEYS */;
INSERT INTO `GUESTS` VALUES (1,1,_binary '\0',NULL,'2020-12-04','2020-12-05',0,0),(2,1,_binary '\0',NULL,'2020-12-02','2020-12-03',0,0);
/*!40000 ALTER TABLE `GUESTS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HOTEL`
--

DROP TABLE IF EXISTS `HOTEL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HOTEL` (
  `ID` int NOT NULL,
  `NAME` varchar(255) NOT NULL,
  `MANAGERID` int NOT NULL,
  `LOCATIONID` int NOT NULL,
  `STARS` int NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `LOCATIONID` (`LOCATIONID`),
  UNIQUE KEY `MANAGERID` (`MANAGERID`),
  CONSTRAINT `HOTEL_ibfk_2` FOREIGN KEY (`MANAGERID`) REFERENCES `MANAGER` (`ID`),
  CONSTRAINT `HOTEL_ibfk_3` FOREIGN KEY (`LOCATIONID`) REFERENCES `LOCATION` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HOTEL`
--

LOCK TABLES `HOTEL` WRITE;
/*!40000 ALTER TABLE `HOTEL` DISABLE KEYS */;
INSERT INTO `HOTEL` VALUES (1,'the grand budapest',2187,16,4),(2,'the Inn',2312,17,4),(3,'HOTEL TULIP GRAND BLUE',123,19,7);
/*!40000 ALTER TABLE `HOTEL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LOCATION`
--

DROP TABLE IF EXISTS `LOCATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LOCATION` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `STREET` varchar(255) DEFAULT NULL,
  `CITY` varchar(255) NOT NULL,
  `COUNTRY` varchar(255) NOT NULL,
  `ZIPCODE` int NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ZIPCODE` (`ZIPCODE`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LOCATION`
--

LOCK TABLES `LOCATION` WRITE;
/*!40000 ALTER TABLE `LOCATION` DISABLE KEYS */;
INSERT INTO `LOCATION` VALUES (16,'12','dagoba','india',201012),(17,'78','fireCity','fireNation',892389),(19,'coolstreet','coolcity','USOFcool',12356771);
/*!40000 ALTER TABLE `LOCATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MANAGER`
--

DROP TABLE IF EXISTS `MANAGER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MANAGER` (
  `ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `MANAGER_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `EMPLOYEE` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MANAGER`
--

LOCK TABLES `MANAGER` WRITE;
/*!40000 ALTER TABLE `MANAGER` DISABLE KEYS */;
INSERT INTO `MANAGER` VALUES (123),(2187),(2312);
/*!40000 ALTER TABLE `MANAGER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MASTER_RELATIONSHIP`
--

DROP TABLE IF EXISTS `MASTER_RELATIONSHIP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MASTER_RELATIONSHIP` (
  `ROOMNO` int NOT NULL,
  `HOTELID` int NOT NULL,
  `CHECKIN` date NOT NULL,
  `CHECKOUT` date NOT NULL,
  `CLUB_TYPE` varchar(255) NOT NULL,
  `MONTH` int NOT NULL,
  `YEAR` int NOT NULL,
  `CLUB_HOURS_USED` int DEFAULT NULL,
  PRIMARY KEY (`ROOMNO`,`HOTELID`,`CHECKIN`,`CHECKOUT`,`CLUB_TYPE`,`MONTH`,`YEAR`),
  KEY `HOTELID` (`HOTELID`,`CLUB_TYPE`,`MONTH`,`YEAR`),
  KEY `HOTELID_2` (`HOTELID`,`MONTH`,`YEAR`),
  CONSTRAINT `MASTER_RELATIONSHIP_ibfk_1` FOREIGN KEY (`ROOMNO`, `HOTELID`, `CHECKIN`, `CHECKOUT`) REFERENCES `GUESTS` (`ROOMNO`, `HOTELID`, `CHECKIN`, `CHECKOUT`),
  CONSTRAINT `MASTER_RELATIONSHIP_ibfk_2` FOREIGN KEY (`ROOMNO`, `HOTELID`) REFERENCES `ROOMS` (`NUMBER`, `HOTELID`),
  CONSTRAINT `MASTER_RELATIONSHIP_ibfk_3` FOREIGN KEY (`HOTELID`, `CLUB_TYPE`, `MONTH`, `YEAR`) REFERENCES `CLUBS` (`HOTELID`, `TYPE`, `MONTH`, `YEAR`),
  CONSTRAINT `MASTER_RELATIONSHIP_ibfk_4` FOREIGN KEY (`HOTELID`, `MONTH`, `YEAR`) REFERENCES `FINANCES` (`HOTELID`, `MONTH`, `YEAR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MASTER_RELATIONSHIP`
--

LOCK TABLES `MASTER_RELATIONSHIP` WRITE;
/*!40000 ALTER TABLE `MASTER_RELATIONSHIP` DISABLE KEYS */;
INSERT INTO `MASTER_RELATIONSHIP` VALUES (1,1,'2020-12-04','2020-12-05','burgers',12,2020,14),(2,1,'2020-12-02','2020-12-03','spa',12,2020,13);
/*!40000 ALTER TABLE `MASTER_RELATIONSHIP` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEMBERS`
--

DROP TABLE IF EXISTS `MEMBERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MEMBERS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `TIER` int NOT NULL,
  `FNAME` varchar(255) DEFAULT NULL,
  `LNAME` varchar(255) DEFAULT NULL,
  `EMAILID` varchar(255) NOT NULL,
  `DOB` date NOT NULL,
  `STAYS` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `EMAILID` (`EMAILID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEMBERS`
--

LOCK TABLES `MEMBERS` WRITE;
/*!40000 ALTER TABLE `MEMBERS` DISABLE KEYS */;
INSERT INTO `MEMBERS` VALUES (4,3,'sflkj','sfkj','sflkj','2020-12-02',4);
/*!40000 ALTER TABLE `MEMBERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PROFIT`
--

DROP TABLE IF EXISTS `PROFIT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PROFIT` (
  `TOTAL_EXP` int NOT NULL,
  `TOTAL_INCOME` int NOT NULL,
  `TOTAL_PROFIT` int NOT NULL,
  PRIMARY KEY (`TOTAL_EXP`,`TOTAL_INCOME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PROFIT`
--

LOCK TABLES `PROFIT` WRITE;
/*!40000 ALTER TABLE `PROFIT` DISABLE KEYS */;
INSERT INTO `PROFIT` VALUES (3360413,345327,-3015086),(3361524,345352,-3016172),(3364746,0,-3364746),(3367187,346029,-3021158),(4134966,1231242,-2903724);
/*!40000 ALTER TABLE `PROFIT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ROOMS`
--

DROP TABLE IF EXISTS `ROOMS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ROOMS` (
  `NUMBER` int NOT NULL,
  `HOTELID` int NOT NULL,
  `STATUS` bit(1) NOT NULL,
  `TYPE` int NOT NULL,
  PRIMARY KEY (`NUMBER`,`HOTELID`),
  KEY `TYPE` (`TYPE`),
  CONSTRAINT `ROOMS_ibfk_1` FOREIGN KEY (`TYPE`) REFERENCES `ROOM_TYPE` (`TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ROOMS`
--

LOCK TABLES `ROOMS` WRITE;
/*!40000 ALTER TABLE `ROOMS` DISABLE KEYS */;
INSERT INTO `ROOMS` VALUES (1,1,_binary '',11),(1,2,_binary '\0',11),(2,1,_binary '',12),(2,2,_binary '\0',14),(3,1,_binary '\0',12),(3,2,_binary '\0',15),(101,1,_binary '\0',13);
/*!40000 ALTER TABLE `ROOMS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ROOM_TYPE`
--

DROP TABLE IF EXISTS `ROOM_TYPE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ROOM_TYPE` (
  `TYPE` int NOT NULL AUTO_INCREMENT,
  `RATE` int NOT NULL,
  `MAX_GUESTS` int NOT NULL,
  PRIMARY KEY (`TYPE`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ROOM_TYPE`
--

LOCK TABLES `ROOM_TYPE` WRITE;
/*!40000 ALTER TABLE `ROOM_TYPE` DISABLE KEYS */;
INSERT INTO `ROOM_TYPE` VALUES (11,700,3),(12,750,4),(13,800,3),(14,1800,5),(15,1200,5);
/*!40000 ALTER TABLE `ROOM_TYPE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SERVICE_STAFF`
--

DROP TABLE IF EXISTS `SERVICE_STAFF`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SERVICE_STAFF` (
  `ID` int NOT NULL,
  `SUPID` int NOT NULL,
  `DEPT` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `SUPID` (`SUPID`),
  CONSTRAINT `SERVICE_STAFF_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `EMPLOYEE` (`ID`),
  CONSTRAINT `SERVICE_STAFF_ibfk_2` FOREIGN KEY (`SUPID`) REFERENCES `SUPERVISOR` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SERVICE_STAFF`
--

LOCK TABLES `SERVICE_STAFF` WRITE;
/*!40000 ALTER TABLE `SERVICE_STAFF` DISABLE KEYS */;
INSERT INTO `SERVICE_STAFF` VALUES (7823,1292,'burgers'),(9985,1334,'spa');
/*!40000 ALTER TABLE `SERVICE_STAFF` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SERVICE_STAFF_ROOM`
--

DROP TABLE IF EXISTS `SERVICE_STAFF_ROOM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SERVICE_STAFF_ROOM` (
  `ROOMNO` int NOT NULL,
  `HOTELID` int NOT NULL,
  `SERVICE_STAFF_ID` int NOT NULL,
  PRIMARY KEY (`ROOMNO`,`HOTELID`,`SERVICE_STAFF_ID`),
  KEY `SERVICE_STAFF_ID` (`SERVICE_STAFF_ID`),
  CONSTRAINT `SERVICE_STAFF_ROOM_ibfk_1` FOREIGN KEY (`ROOMNO`, `HOTELID`) REFERENCES `ROOMS` (`NUMBER`, `HOTELID`),
  CONSTRAINT `SERVICE_STAFF_ROOM_ibfk_2` FOREIGN KEY (`SERVICE_STAFF_ID`) REFERENCES `SERVICE_STAFF` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SERVICE_STAFF_ROOM`
--

LOCK TABLES `SERVICE_STAFF_ROOM` WRITE;
/*!40000 ALTER TABLE `SERVICE_STAFF_ROOM` DISABLE KEYS */;
INSERT INTO `SERVICE_STAFF_ROOM` VALUES (1,2,9985);
/*!40000 ALTER TABLE `SERVICE_STAFF_ROOM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SUPERVISOR`
--

DROP TABLE IF EXISTS `SUPERVISOR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SUPERVISOR` (
  `ID` int NOT NULL,
  `MANAGERID` int NOT NULL,
  `DEPT` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `MANAGERID` (`MANAGERID`),
  CONSTRAINT `SUPERVISOR_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `EMPLOYEE` (`ID`),
  CONSTRAINT `SUPERVISOR_ibfk_2` FOREIGN KEY (`MANAGERID`) REFERENCES `MANAGER` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUPERVISOR`
--

LOCK TABLES `SUPERVISOR` WRITE;
/*!40000 ALTER TABLE `SUPERVISOR` DISABLE KEYS */;
INSERT INTO `SUPERVISOR` VALUES (1292,2187,'pizza'),(1334,2312,'spa'),(9842,2187,'burgers');
/*!40000 ALTER TABLE `SUPERVISOR` ENABLE KEYS */;
UNLOCK TABLES;
