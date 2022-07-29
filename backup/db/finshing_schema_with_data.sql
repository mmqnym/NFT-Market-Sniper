-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: ebisu_tracker
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `fishing_e`
--

DROP TABLE IF EXISTS `fishing_e`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishing_e` (
  `ID` int NOT NULL,
  `NAME` varchar(32) NOT NULL,
  `LUCKY` int NOT NULL,
  `DESCRIPTION` varchar(200) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishing_e`
--

LOCK TABLES `fishing_e` WRITE;
/*!40000 ALTER TABLE `fishing_e` DISABLE KEYS */;
INSERT INTO `fishing_e` VALUES (1,'七星鰻魚',7,'今天運氣不錯，可能抽獎都會有好結果。'),(2,'伊勢龍蝦',9,'今天運氣好的不得了，像是身處日本10日遊般的爽快，做什麼想必都能有好結果。'),(3,'垃圾',0,'今天的運勢就是垃圾，建議失蹤一天。'),(4,'大正錦鯉',8,'白底為主的吉祥之魚，做任何事想必都能順心如意，但仍需小心一些小細節可能會造成一些負面影響。'),(5,'小魚乾',1,'今天絕對要低調行事、避免與人衝撞，否則可能會被吞掉。'),(6,'年年有魚',5,'看似很吉祥，實則就只是平凡的魚，象徵平凡的每一天，今天也是個平凡的日子呢。'),(7,'廚餘',0,'一坨拉基，今天可能不適合做任何消費。'),(8,'旗魚',5,'今天對你來說可以是好日子也可以是壞日子，遭遇任何事情都能發現最容易攻破的點並擊破，不過卻也有非常大的可能因大意而遍體鱗傷。'),(9,'昭和錦鯉',7,'黑底為主的吉祥之魚，雖說可能今日相對好運，仍須特別注意一些小事可能會壞了今天的好運。'),(10,'木魚',1,'象徵六根清淨，別看盤別逛市集別消費，今天適合出去走走。'),(11,'河豚',5,'外表強硬，但一旦最強大的毒囊被摘除，也就只是一塊肉罷了，今天做什麼事可能都會稍有阻礙，只要找出關鍵點便能化解難關。'),(12,'海豚',7,'海中智者，卻也是慾望最強烈的海底生物，今天做事或許都能輕鬆解決，但須注意不要被過剩的慾望毀了自己的成果。'),(13,'澳洲藍龍',9,'釣到了只有澳洲特有的藍龍蝦，彷彿深海藍寶石一般，今天 Mint NFT 的話，很可能會拿到鑽石相關的特徵歐。'),(14,'福壽螺',0,'你今天的事情可能就像福壽螺一般，滿滿的都是卵，都是一堆小雜事讓你煩到不可開交，建議消失一天。'),(15,'章魚',7,'你今天做什麼都彷彿擁有8隻手般，不費工夫完成各種事情。'),(16,'紅龍魚',10,'今天運氣絕佳，是個 Mint 中大獎的日子。'),(17,'金龍魚',9,'今天運氣非常好，或許 Mint 可以中個2獎。'),(18,'韓國魚',2,'象徵韓國普遍可見的草魚，你今天要避免過於衝動的野心，避免弄巧成拙，一敗塗地。'),(19,'鬥魚',3,'今天可能有那麼一點諸事不順，做任何事情小心翼翼或許能化險為夷。'),(20,'鮪魚',6,'象徵聰明，今天或許能突破一段時間難以突破的關卡。'),(21,'鮭魚',7,'今天或許是逆著趨勢走才能大成功的日子。'),(22,'鯊魚',0,'你今天做的努力可能都會被吞沒，建議休息一日或是順著平日的生活度過。'),(23,'鰈魚',8,'軟中帶脆，今天想必做任何事都能取巧輕鬆迎刃而解。'),(24,'草蝦',3,'你今天的生活就像隨處可見的草蝦一般平凡，不開心也不難過的普通日子。'),(25,'北極甜蝦',7,'無須調味，自然的散發淡淡的香氣與鮮甜，今天做什麼可能都會有種順利的感覺。'),(26,'海草',6,'釣到海草或許你會覺得很衰，可是你有想過海綿寶寶喝海草汁喝得多津津有味嗎?這暗示了今天可能看起來很糟，實則有不少小確幸等著你。'),(27,'珊瑚',3,'將海洋的綠洲破壞的你，今天或許會有點糟，不過畢竟也是綠洲，或許也能收到來自大洋中的恩惠也不一定。'),(28,'黑珍珠之貝',8,'釣到孕育稀有黑珍珠的黑唇貝，今天可能會有不小的好運到來...'),(29,'金魚',5,'外表艷麗、可以在一般環境生存，如同普通人，看似平凡的度過每一日，實則有點弱不禁風，無法承受過大的壓力與糟糕的環境，今天是個普通平凡的一天，不好也不差。'),(30,'油魚',4,'今天可能會是一個外表光鮮亮麗、事事順心的一天，但其實背後可能又付出不小的代價，需要小心注意別樂過頭了。'),(31,'魷魚',3,'今日須注意凡事可能都沒有那麼輕鬆，很容易弄得身心疲累，不過只要小心一點，或許今天不會那麼難過。'),(32,'海龜',6,'今日若沉穩前行，凡事皆可順，然，須避免過於急躁，以免遭受意外的嚴重事故。'),(33,'一般水母',4,'某種意義上象徵著人類最後的食物來源，今日可能會有小確幸發生，需要好好把握，有機會溜掉的可能性!');
/*!40000 ALTER TABLE `fishing_e` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fishing_n`
--

DROP TABLE IF EXISTS `fishing_n`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishing_n` (
  `ID` int NOT NULL,
  `NAME` varchar(32) NOT NULL,
  `LUCKY` int NOT NULL,
  `DESCRIPTION` varchar(200) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishing_n`
--

LOCK TABLES `fishing_n` WRITE;
/*!40000 ALTER TABLE `fishing_n` DISABLE KEYS */;
INSERT INTO `fishing_n` VALUES (1,'蒙古獵鷹',6,'忠貞度極高的蒙古獵鷹，象徵你可以信任近來身邊的合作夥伴，放心一起合作，會有好結果的，不過要小心鷹餓了會反咬人的!拿捏距離還是必要的。'),(2,'青鳥',10,'一生都不一定有機會見證一次的青鳥，有如中大樂透頭獎一般，近期或許會迎來一段非常好的日子。');
/*!40000 ALTER TABLE `fishing_n` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fishing_s`
--

DROP TABLE IF EXISTS `fishing_s`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishing_s` (
  `ID` int NOT NULL,
  `NAME` varchar(32) NOT NULL,
  `LUCKY` int NOT NULL,
  `DESCRIPTION` varchar(200) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishing_s`
--

LOCK TABLES `fishing_s` WRITE;
/*!40000 ALTER TABLE `fishing_s` DISABLE KEYS */;
INSERT INTO `fishing_s` VALUES (1,'大熊',1,'難得一遇糟糕透頂的情況，小心別被抓傷了!短期請守住自己的本分，不要做太多不可預期明確結果的事情。'),(2,'卡哇依牛牛',9,'難得一遇非常可愛的牛牛，近期可能會有一系列好運等著你!或許可以買些大樂透碰碰運氣。');
/*!40000 ALTER TABLE `fishing_s` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fishing_w`
--

DROP TABLE IF EXISTS `fishing_w`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishing_w` (
  `ID` int NOT NULL,
  `NAME` varchar(32) NOT NULL,
  `LUCKY` int NOT NULL,
  `DESCRIPTION` varchar(200) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishing_w`
--

LOCK TABLES `fishing_w` WRITE;
/*!40000 ALTER TABLE `fishing_w` DISABLE KEYS */;
INSERT INTO `fishing_w` VALUES (1,'駱駝',7,'沙漠的人類救星，象徵近日可能會遇到生命或事業上的貴人或好事，協助你度過難關。'),(2,'沙漠之狐',2,'看似可愛的狐狸，實則可能會趁你陷入危機之際偷走你的一切，近日須注意提防小人。');
/*!40000 ALTER TABLE `fishing_w` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-29 12:34:59
