-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: catalog_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add product',7,'add_product'),(26,'Can change product',7,'change_product'),(27,'Can delete product',7,'delete_product'),(28,'Can view product',7,'view_product');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$TmOmF050MiPqHJyEKEX1mR$n9i24LyLUcKl0GChKJgHkGe+fYJ1wrvwlzfrCsfD5nk=',NULL,1,'root','','','',1,1,'2025-11-03 18:32:31.073910'),(2,'pbkdf2_sha256$1000000$e7aRMdLeOCxu6swAEiSNYJ$j/cFvYuJOUIDgyN89nkk7KBl33VE/R/2E5SdqQbdrTs=','2025-11-04 04:51:15.457981',1,'admin','','','',1,1,'2025-11-03 18:33:08.153612');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog_product`
--

DROP TABLE IF EXISTS `catalog_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalog_product` (
  `product_id` bigint NOT NULL AUTO_INCREMENT,
  `sku` varchar(64) NOT NULL,
  `name` varchar(255) NOT NULL,
  `category` varchar(120) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `catalog_product_category_5cf29444` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog_product`
--

LOCK TABLES `catalog_product` WRITE;
/*!40000 ALTER TABLE `catalog_product` DISABLE KEYS */;
INSERT INTO `catalog_product` VALUES (1,'SKU0001','Prod1','Clothing',706.68,1,'2025-11-03 10:00:59.786167','2025-11-03 10:00:59.786271'),(2,'SKU0002','Prod2','Clothing',1560.01,1,'2025-11-03 10:00:59.786354','2025-11-03 10:00:59.786382'),(3,'SKU0003','Prod3','Clothing',1761.00,1,'2025-11-03 10:00:59.786429','2025-11-03 10:00:59.786453'),(4,'SKU0004','Prod4','Books',4946.10,1,'2025-11-03 10:00:59.786496','2025-11-03 10:00:59.786558'),(5,'SKU0005','Prod5','Clothing',1566.09,1,'2025-11-03 10:00:59.786618','2025-11-03 10:00:59.786644'),(6,'SKU0006','Prod6','Books',1950.56,1,'2025-11-03 10:00:59.786689','2025-11-03 10:00:59.786713'),(7,'SKU0007','Prod7','Electronics',1706.45,1,'2025-11-03 10:00:59.786756','2025-11-03 10:00:59.786778'),(8,'SKU0008','Prod8','Clothing',2326.12,1,'2025-11-03 10:00:59.786819','2025-11-03 10:00:59.786839'),(9,'SKU0009','Prod9','Books',2185.89,0,'2025-11-03 10:00:59.786880','2025-11-03 10:00:59.786899'),(10,'SKU0010','Prod10','Electronics',552.02,0,'2025-11-03 10:00:59.786983','2025-11-03 10:00:59.787014'),(11,'SKU0011','Prod11','Electronics',2433.64,0,'2025-11-03 10:00:59.787055','2025-11-03 10:00:59.787076'),(12,'SKU0012','Prod12','Electronics',1909.54,0,'2025-11-03 10:00:59.787119','2025-11-03 10:00:59.787139'),(13,'SKU0013','Prod13','Books',2838.95,0,'2025-11-03 10:00:59.787177','2025-11-03 10:00:59.787196'),(14,'SKU0014','Prod14','Clothing',2963.09,0,'2025-11-03 10:00:59.787235','2025-11-03 10:00:59.787258'),(15,'SKU0015','Prod15','Clothing',3476.19,0,'2025-11-03 10:00:59.787299','2025-11-03 10:00:59.787319'),(16,'SKU0016','Prod16','Books',4869.04,1,'2025-11-03 10:00:59.787360','2025-11-03 10:00:59.787395'),(17,'SKU0017','Prod17','Electronics',2578.35,0,'2025-11-03 10:00:59.787441','2025-11-03 10:00:59.787463'),(18,'SKU0018','Prod18','Books',2342.79,1,'2025-11-03 10:00:59.787505','2025-11-03 10:00:59.787538'),(19,'SKU0019','Prod19','Books',1141.95,0,'2025-11-03 10:00:59.787578','2025-11-03 10:00:59.787600'),(20,'SKU0020','Prod20','Electronics',3757.83,0,'2025-11-03 10:00:59.787639','2025-11-03 10:00:59.787659'),(21,'SKU0021','Prod21','Electronics',3047.84,0,'2025-11-03 10:00:59.787695','2025-11-03 10:00:59.787716'),(22,'SKU0022','Prod22','Electronics',692.25,0,'2025-11-03 10:00:59.787754','2025-11-03 10:00:59.787774'),(23,'SKU0023','Prod23','Electronics',2661.61,1,'2025-11-03 10:00:59.787802','2025-11-03 10:00:59.787812'),(24,'SKU0024','Prod24','Clothing',1594.13,0,'2025-11-03 10:00:59.787833','2025-11-03 10:00:59.787842'),(25,'SKU0025','Prod25','Clothing',1540.51,1,'2025-11-03 10:00:59.787877','2025-11-03 10:00:59.787896'),(26,'SKU0026','Prod26','Electronics',796.49,0,'2025-11-03 10:00:59.787934','2025-11-03 10:00:59.787962'),(27,'SKU0027','Prod27','Electronics',4690.42,0,'2025-11-03 10:00:59.788003','2025-11-03 10:00:59.788025'),(28,'SKU0028','Prod28','Clothing',1156.35,0,'2025-11-03 10:00:59.788065','2025-11-03 10:00:59.788087'),(29,'SKU0029','Prod29','Electronics',699.41,0,'2025-11-03 10:00:59.788128','2025-11-03 10:00:59.788150'),(30,'SKU0030','Prod30','Electronics',4365.09,0,'2025-11-03 10:00:59.788192','2025-11-03 10:00:59.788214'),(31,'SKU0031','Prod31','Clothing',2907.99,0,'2025-11-03 10:00:59.788255','2025-11-03 10:00:59.788277'),(32,'SKU0032','Prod32','Clothing',3928.61,0,'2025-11-03 10:00:59.788318','2025-11-03 10:00:59.788340'),(33,'SKU0033','Prod33','Books',4185.05,1,'2025-11-03 10:00:59.788378','2025-11-03 10:00:59.788397'),(34,'SKU0034','Prod34','Electronics',2573.34,0,'2025-11-03 10:00:59.788438','2025-11-03 10:00:59.788458'),(35,'SKU0035','Prod35','Clothing',3369.38,1,'2025-11-03 10:00:59.788498','2025-11-03 10:00:59.788519'),(36,'SKU0036','Prod36','Books',1693.56,0,'2025-11-03 10:00:59.788613','2025-11-03 10:00:59.788643'),(37,'SKU0037','Prod37','Clothing',1240.83,0,'2025-11-03 10:00:59.788681','2025-11-03 10:00:59.788701'),(38,'SKU0038','Prod38','Clothing',2750.87,0,'2025-11-03 10:00:59.788755','2025-11-03 10:00:59.788778'),(39,'SKU0039','Prod39','Books',1459.14,1,'2025-11-03 10:00:59.788818','2025-11-03 10:00:59.788838'),(40,'SKU0040','Prod40','Electronics',3565.32,0,'2025-11-03 10:00:59.788876','2025-11-03 10:00:59.788896'),(41,'SKU0041','Prod41','Books',3261.28,1,'2025-11-03 10:00:59.788934','2025-11-03 10:00:59.788980'),(42,'SKU0042','Prod42','Electronics',4780.32,1,'2025-11-03 10:00:59.789045','2025-11-03 10:00:59.789066'),(43,'SKU0043','Prod43','Books',2656.59,0,'2025-11-03 10:00:59.789104','2025-11-03 10:00:59.789124'),(44,'SKU0044','Prod44','Books',4494.63,1,'2025-11-03 10:00:59.789161','2025-11-03 10:00:59.789180'),(45,'SKU0045','Prod45','Books',4687.29,1,'2025-11-03 10:00:59.789217','2025-11-03 10:00:59.789237'),(46,'SKU0046','Prod46','Electronics',1447.32,1,'2025-11-03 10:00:59.789276','2025-11-03 10:00:59.789296'),(47,'SKU0047','Prod47','Electronics',4165.48,0,'2025-11-03 10:00:59.789335','2025-11-03 10:00:59.789355'),(48,'SKU0048','Prod48','Electronics',4053.91,0,'2025-11-03 10:00:59.789393','2025-11-03 10:00:59.789413'),(49,'SKU0049','Prod49','Clothing',2985.58,0,'2025-11-03 10:00:59.789449','2025-11-03 10:00:59.789469'),(50,'SKU0050','Prod50','Electronics',1765.79,1,'2025-11-03 10:00:59.789509','2025-11-03 10:00:59.789528'),(51,'SKU0051','Prod51','Clothing',217.88,0,'2025-11-03 10:00:59.789568','2025-11-03 10:00:59.789588'),(52,'SKU0052','Prod52','Clothing',1360.17,1,'2025-11-03 10:00:59.789627','2025-11-03 10:00:59.789647'),(53,'SKU0053','Prod53','Electronics',2754.72,0,'2025-11-03 10:00:59.789718','2025-11-03 10:00:59.789739'),(54,'SKU0054','Prod54','Electronics',995.08,1,'2025-11-03 10:00:59.789807','2025-11-03 10:00:59.789829'),(55,'SKU0055','Prod55','Electronics',1603.29,0,'2025-11-03 10:00:59.789869','2025-11-03 10:00:59.789889'),(56,'SKU0056','Prod56','Books',929.04,0,'2025-11-03 10:00:59.789921','2025-11-03 10:00:59.789932'),(57,'SKU0057','Prod57','Electronics',233.14,1,'2025-11-03 10:00:59.789953','2025-11-03 10:00:59.789964'),(58,'SKU0058','Prod58','Clothing',2010.70,0,'2025-11-03 10:00:59.790000','2025-11-03 10:00:59.790027'),(59,'SKU0059','Prod59','Electronics',2122.83,0,'2025-11-03 10:00:59.790068','2025-11-03 10:00:59.790086'),(60,'SKU0060','Prod60','Clothing',1940.01,1,'2025-11-03 10:00:59.790123','2025-11-03 10:00:59.790142'),(61,'SKU0061','Prod61','Electronics',1092.54,1,'2025-11-03 10:00:59.790179','2025-11-03 10:00:59.790199'),(62,'SKU0062','Prod62','Clothing',2592.24,0,'2025-11-03 10:00:59.790236','2025-11-03 10:00:59.790256'),(63,'SKU0063','Prod63','Electronics',1419.51,0,'2025-11-03 10:00:59.790294','2025-11-03 10:00:59.790314'),(64,'SKU0064','Prod64','Clothing',2810.29,1,'2025-11-03 10:00:59.790353','2025-11-03 10:00:59.790389'),(65,'SKU0065','Prod65','Clothing',241.64,1,'2025-11-03 10:00:59.790428','2025-11-03 10:00:59.790447'),(66,'SKU0066','Prod66','Electronics',1418.88,1,'2025-11-03 10:00:59.790482','2025-11-03 10:00:59.790501'),(67,'SKU0067','Prod67','Electronics',3838.59,1,'2025-11-03 10:00:59.790544','2025-11-03 10:00:59.790613'),(68,'SKU0068','Prod68','Clothing',2884.40,0,'2025-11-03 10:00:59.790699','2025-11-03 10:00:59.790729'),(69,'SKU0069','Prod69','Electronics',4246.76,1,'2025-11-03 10:00:59.790773','2025-11-03 10:00:59.790794'),(70,'SKU0070','Prod70','Electronics',1929.20,1,'2025-11-03 10:00:59.790831','2025-11-03 10:00:59.790852'),(71,'SKU0071','Prod71','Electronics',2733.92,0,'2025-11-03 10:00:59.790889','2025-11-03 10:00:59.790903'),(72,'SKU0072','Prod72','Books',2313.54,1,'2025-11-03 10:00:59.790929','2025-11-03 10:00:59.790948'),(73,'SKU0073','Prod73','Clothing',4809.46,0,'2025-11-03 10:00:59.790985','2025-11-03 10:00:59.791005'),(74,'SKU0074','Prod74','Books',4863.20,1,'2025-11-03 10:00:59.791043','2025-11-03 10:00:59.791063'),(75,'SKU0075','Prod75','Electronics',4674.18,0,'2025-11-03 10:00:59.791101','2025-11-03 10:00:59.791120'),(76,'SKU0076','Prod76','Clothing',3029.55,0,'2025-11-03 10:00:59.791158','2025-11-03 10:00:59.791178'),(77,'SKU0077','Prod77','Clothing',4227.95,1,'2025-11-03 10:00:59.791216','2025-11-03 10:00:59.791234'),(78,'SKU0078','Prod78','Books',4219.35,0,'2025-11-03 10:00:59.791277','2025-11-03 10:00:59.791297'),(79,'SKU0079','Prod79','Electronics',890.94,1,'2025-11-03 10:00:59.791336','2025-11-03 10:00:59.791356'),(80,'SKU0080','Prod80','Clothing',539.60,1,'2025-11-03 10:00:59.791394','2025-11-03 10:00:59.791414'),(81,'SKU0081','Prod81','Electronics',3652.86,0,'2025-11-03 10:00:59.791453','2025-11-03 10:00:59.791474'),(82,'SKU0082','Prod82','Clothing',1133.17,0,'2025-11-03 10:00:59.791512','2025-11-03 10:00:59.791533'),(83,'SKU0083','Prod83','Books',4732.50,0,'2025-11-03 10:00:59.791571','2025-11-03 10:00:59.791591'),(84,'SKU0084','Prod84','Books',2318.32,1,'2025-11-03 10:00:59.791631','2025-11-03 10:00:59.791646'),(85,'SKU0085','Prod85','Books',4916.81,0,'2025-11-03 10:00:59.791668','2025-11-03 10:00:59.791678'),(86,'SKU0086','Prod86','Electronics',2353.02,0,'2025-11-03 10:00:59.791699','2025-11-03 10:00:59.791708'),(87,'SKU0087','Prod87','Electronics',4578.69,1,'2025-11-03 10:00:59.791729','2025-11-03 10:00:59.791739'),(88,'SKU0088','Prod88','Books',4619.06,0,'2025-11-03 10:00:59.791761','2025-11-03 10:00:59.791794'),(89,'SKU0089','Prod89','Electronics',4517.08,1,'2025-11-03 10:00:59.791833','2025-11-03 10:00:59.791851'),(90,'SKU0090','Prod90','Clothing',2823.37,0,'2025-11-03 10:00:59.791888','2025-11-03 10:00:59.791908'),(91,'SKU0091','Prod91','Clothing',2736.84,1,'2025-11-03 10:00:59.791946','2025-11-03 10:00:59.791966'),(92,'SKU0092','Prod92','Books',251.64,0,'2025-11-03 10:00:59.792004','2025-11-03 10:00:59.792033'),(93,'SKU0093','Prod93','Books',704.74,0,'2025-11-03 10:00:59.792074','2025-11-03 10:00:59.792094'),(94,'SKU0094','Prod94','Books',1854.03,1,'2025-11-03 10:00:59.792136','2025-11-03 10:00:59.792156'),(95,'SKU0095','Prod95','Books',4920.60,1,'2025-11-03 10:00:59.792194','2025-11-03 10:00:59.792213'),(96,'SKU0096','Prod96','Clothing',1915.36,1,'2025-11-03 10:00:59.792313','2025-11-03 10:00:59.792348'),(97,'SKU0097','Prod97','Clothing',145.88,1,'2025-11-03 10:00:59.792411','2025-11-03 10:00:59.792433'),(98,'SKU0098','Prod98','Clothing',3434.72,0,'2025-11-03 10:00:59.792473','2025-11-03 10:00:59.792492'),(99,'SKU0099','Prod99','Electronics',540.84,0,'2025-11-03 10:00:59.792530','2025-11-03 10:00:59.792550'),(100,'SKU0100','Prod100','Books',1183.62,0,'2025-11-03 10:00:59.792590','2025-11-03 10:00:59.792610'),(101,'SKU0101','Prod101','Clothing',280.30,0,'2025-11-03 10:00:59.792649','2025-11-03 10:00:59.792670'),(102,'SKU0102','Prod102','Books',3564.14,1,'2025-11-03 10:00:59.792771','2025-11-03 10:00:59.792801'),(103,'SKU0103','Prod103','Electronics',1060.83,0,'2025-11-03 10:00:59.792846','2025-11-03 10:00:59.792868'),(104,'SKU0104','Prod104','Electronics',4362.59,0,'2025-11-03 10:00:59.792909','2025-11-03 10:00:59.792932'),(105,'SKU0105','Prod105','Electronics',2803.75,1,'2025-11-03 10:00:59.792971','2025-11-03 10:00:59.792992'),(106,'SKU0106','Prod106','Electronics',2982.01,1,'2025-11-03 10:00:59.793032','2025-11-03 10:00:59.793052'),(107,'SKU0107','Prod107','Electronics',1372.16,1,'2025-11-03 10:00:59.793092','2025-11-03 10:00:59.793113'),(108,'SKU0108','Prod108','Books',3671.60,0,'2025-11-03 10:00:59.793152','2025-11-03 10:00:59.793173'),(109,'SKU0109','Prod109','Electronics',4253.57,1,'2025-11-03 10:00:59.793213','2025-11-03 10:00:59.793293'),(110,'SKU0110','Prod110','Books',3420.90,0,'2025-11-03 10:00:59.793354','2025-11-03 10:00:59.793380'),(111,'SKU0111','Prod111','Books',2844.57,0,'2025-11-03 10:00:59.793530','2025-11-03 10:00:59.793562'),(112,'SKU0112','Prod112','Electronics',4695.66,1,'2025-11-03 10:00:59.793610','2025-11-03 10:00:59.793652'),(113,'SKU0113','Prod113','Clothing',2219.49,0,'2025-11-03 10:00:59.793727','2025-11-03 10:00:59.793747'),(114,'SKU0114','Prod114','Clothing',696.42,0,'2025-11-03 10:00:59.793772','2025-11-03 10:00:59.793792'),(115,'SKU0115','Prod115','Clothing',1871.21,1,'2025-11-03 10:00:59.793829','2025-11-03 10:00:59.793850'),(116,'SKU0116','Prod116','Books',1200.29,0,'2025-11-03 10:00:59.793878','2025-11-03 10:00:59.793896'),(117,'SKU0117','Prod117','Clothing',2708.81,0,'2025-11-03 10:00:59.793933','2025-11-03 10:00:59.793953'),(118,'SKU0118','Prod118','Electronics',2020.11,0,'2025-11-03 10:00:59.793985','2025-11-03 10:00:59.794006'),(119,'SKU0119','Prod119','Electronics',4412.48,1,'2025-11-03 10:00:59.794056','2025-11-03 10:00:59.794067'),(120,'SKU0120','Prod120','Books',1205.58,0,'2025-11-03 10:00:59.794107','2025-11-03 10:00:59.794121'),(121,'SKU-TEST-2','Another Demo','Clothing',25.00,1,'2025-11-04 11:37:58.322956','2025-11-04 11:37:58.323249');
/*!40000 ALTER TABLE `catalog_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'catalog','product'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-03 18:24:48.234161'),(2,'auth','0001_initial','2025-11-03 18:24:49.906466'),(3,'admin','0001_initial','2025-11-03 18:24:50.379166'),(4,'admin','0002_logentry_remove_auto_add','2025-11-03 18:24:50.407554'),(5,'admin','0003_logentry_add_action_flag_choices','2025-11-03 18:24:50.437156'),(6,'contenttypes','0002_remove_content_type_name','2025-11-03 18:24:50.720346'),(7,'auth','0002_alter_permission_name_max_length','2025-11-03 18:24:50.910447'),(8,'auth','0003_alter_user_email_max_length','2025-11-03 18:24:50.968058'),(9,'auth','0004_alter_user_username_opts','2025-11-03 18:24:50.993621'),(10,'auth','0005_alter_user_last_login_null','2025-11-03 18:24:51.157912'),(11,'auth','0006_require_contenttypes_0002','2025-11-03 18:24:51.167752'),(12,'auth','0007_alter_validators_add_error_messages','2025-11-03 18:24:51.187735'),(13,'auth','0008_alter_user_username_max_length','2025-11-03 18:24:51.381278'),(14,'auth','0009_alter_user_last_name_max_length','2025-11-03 18:24:51.604003'),(15,'auth','0010_alter_group_name_max_length','2025-11-03 18:24:51.669028'),(16,'auth','0011_update_proxy_permissions','2025-11-03 18:24:51.691726'),(17,'auth','0012_alter_user_first_name_max_length','2025-11-03 18:24:51.910942'),(18,'catalog','0001_initial','2025-11-03 18:24:52.040651'),(19,'sessions','0001_initial','2025-11-03 18:24:52.161361');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('mib42qbr8xq0uid90ozgkya9pp4lsngh','.eJxVjMsOwiAQRf-FtSG8GVy69xsIUwapGkhKuzL-uzbpQrf3nHNfLKZtrXEbtMQ5szNT7PS7YZoe1HaQ76ndOp96W5cZ-a7wgw5-7Zmel8P9O6hp1G_tjNElGWtl8gCKEJSWMghBWRgDpGwhCVAkKlWweBSOsgtSi-CNdpa9P7rhNrc:1vG90l:y3GBWEfGZwD0XfZPsidtSIu_WxqYGdoNHFWToiXBbZ8','2025-11-18 04:51:15.473735');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-05  7:34:05
