-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: quanlykhachsan
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bangsdt`
--

DROP TABLE IF EXISTS `bangsdt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bangsdt` (
  `MaKhach` int(11) NOT NULL,
  `id_SDT` int(11) NOT NULL,
  PRIMARY KEY (`MaKhach`,`id_SDT`),
  KEY `id_SDT` (`id_SDT`),
  CONSTRAINT `bangsdt_ibfk_1` FOREIGN KEY (`MaKhach`) REFERENCES `khach` (`makhach`),
  CONSTRAINT `bangsdt_ibfk_2` FOREIGN KEY (`id_SDT`) REFERENCES `sdt` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bangsdt`
--

LOCK TABLES `bangsdt` WRITE;
/*!40000 ALTER TABLE `bangsdt` DISABLE KEYS */;
INSERT INTO `bangsdt` VALUES (1,1),(1,2);
/*!40000 ALTER TABLE `bangsdt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bangsdtnhanvien`
--

DROP TABLE IF EXISTS `bangsdtnhanvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bangsdtnhanvien` (
  `emp_id` int(11) NOT NULL,
  `id_SDT` int(11) NOT NULL,
  PRIMARY KEY (`emp_id`,`id_SDT`),
  KEY `id_SDT` (`id_SDT`),
  CONSTRAINT `bangsdtnhanvien_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `tai_khoan_nhan_vien` (`emp_id`),
  CONSTRAINT `bangsdtnhanvien_ibfk_2` FOREIGN KEY (`id_SDT`) REFERENCES `sdt` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bangsdtnhanvien`
--

LOCK TABLES `bangsdtnhanvien` WRITE;
/*!40000 ALTER TABLE `bangsdtnhanvien` DISABLE KEYS */;
/*!40000 ALTER TABLE `bangsdtnhanvien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chi_tiet_thue`
--

DROP TABLE IF EXISTS `chi_tiet_thue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `chi_tiet_thue` (
  `MaHopDong` int(11) NOT NULL AUTO_INCREMENT,
  `MaPhong` int(11) NOT NULL,
  `MaKhach` int(11) NOT NULL,
  `NgayBatDau` datetime NOT NULL,
  `SoNgayODuKien` int(11) DEFAULT NULL,
  PRIMARY KEY (`MaHopDong`),
  KEY `MaPhong` (`MaPhong`),
  KEY `MaKhach` (`MaKhach`),
  CONSTRAINT `chi_tiet_thue_ibfk_1` FOREIGN KEY (`MaPhong`) REFERENCES `phong` (`maphong`),
  CONSTRAINT `chi_tiet_thue_ibfk_2` FOREIGN KEY (`MaKhach`) REFERENCES `khach` (`makhach`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_thue`
--

LOCK TABLES `chi_tiet_thue` WRITE;
/*!40000 ALTER TABLE `chi_tiet_thue` DISABLE KEYS */;
INSERT INTO `chi_tiet_thue` VALUES (1,101,1,'2021-11-20 00:00:00',10),(2,102,1,'2021-11-20 00:00:00',5),(3,103,1,'2021-11-20 00:00:00',1);
/*!40000 ALTER TABLE `chi_tiet_thue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `danh_gia_cua_khach`
--

DROP TABLE IF EXISTS `danh_gia_cua_khach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `danh_gia_cua_khach` (
  `MaDanhGia` int(11) NOT NULL AUTO_INCREMENT,
  `MaPhong` int(11) NOT NULL,
  `MaKhach` int(11) NOT NULL,
  `NgayBatDau` datetime NOT NULL,
  `NoiDung` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SoSao` int(11) DEFAULT NULL,
  PRIMARY KEY (`MaDanhGia`),
  KEY `MaPhong` (`MaPhong`),
  KEY `MaKhach` (`MaKhach`),
  CONSTRAINT `danh_gia_cua_khach_ibfk_1` FOREIGN KEY (`MaPhong`) REFERENCES `phong` (`maphong`),
  CONSTRAINT `danh_gia_cua_khach_ibfk_2` FOREIGN KEY (`MaKhach`) REFERENCES `khach` (`makhach`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danh_gia_cua_khach`
--

LOCK TABLES `danh_gia_cua_khach` WRITE;
/*!40000 ALTER TABLE `danh_gia_cua_khach` DISABLE KEYS */;
/*!40000 ALTER TABLE `danh_gia_cua_khach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoa_don`
--

DROP TABLE IF EXISTS `hoa_don`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `hoa_don` (
  `MaHopDong` int(11) NOT NULL,
  `NgayTraPhong` datetime NOT NULL,
  `ThanhTien` int(11) NOT NULL,
  PRIMARY KEY (`MaHopDong`),
  CONSTRAINT `hoa_don_ibfk_1` FOREIGN KEY (`MaHopDong`) REFERENCES `chi_tiet_thue` (`mahopdong`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoa_don`
--

LOCK TABLES `hoa_don` WRITE;
/*!40000 ALTER TABLE `hoa_don` DISABLE KEYS */;
INSERT INTO `hoa_don` VALUES (3,'2021-11-25 00:00:00',1000);
/*!40000 ALTER TABLE `hoa_don` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khach`
--

DROP TABLE IF EXISTS `khach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `khach` (
  `MaKhach` int(11) NOT NULL AUTO_INCREMENT,
  `MaLoaiKhach` int(11) NOT NULL,
  `CMND` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DiaChi` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NgaySinh` datetime DEFAULT NULL,
  PRIMARY KEY (`MaKhach`),
  KEY `MaLoaiKhach` (`MaLoaiKhach`),
  CONSTRAINT `khach_ibfk_1` FOREIGN KEY (`MaLoaiKhach`) REFERENCES `loai_khach` (`maloaikhach`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khach`
--

LOCK TABLES `khach` WRITE;
/*!40000 ALTER TABLE `khach` DISABLE KEYS */;
INSERT INTO `khach` VALUES (1,1,'1','1','2001-01-01 00:00:00');
/*!40000 ALTER TABLE `khach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loai_khach`
--

DROP TABLE IF EXISTS `loai_khach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `loai_khach` (
  `MaLoaiKhach` int(11) NOT NULL AUTO_INCREMENT,
  `LoaiKhach` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`MaLoaiKhach`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loai_khach`
--

LOCK TABLES `loai_khach` WRITE;
/*!40000 ALTER TABLE `loai_khach` DISABLE KEYS */;
INSERT INTO `loai_khach` VALUES (1,'NoiDia'),(2,'NuocNgoai');
/*!40000 ALTER TABLE `loai_khach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loai_phong`
--

DROP TABLE IF EXISTS `loai_phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `loai_phong` (
  `MaLoaiPhong` int(11) NOT NULL AUTO_INCREMENT,
  `LoaiPhong` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DonGia` int(11) NOT NULL,
  PRIMARY KEY (`MaLoaiPhong`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loai_phong`
--

LOCK TABLES `loai_phong` WRITE;
/*!40000 ALTER TABLE `loai_phong` DISABLE KEYS */;
INSERT INTO `loai_phong` VALUES (1,'A',150),(2,'B',170),(3,'C',200);
/*!40000 ALTER TABLE `loai_phong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phong`
--

DROP TABLE IF EXISTS `phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `phong` (
  `MaPhong` int(11) NOT NULL AUTO_INCREMENT,
  `MaLoaiPhong` int(11) NOT NULL,
  `GhiChu` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TinhTrang` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL,
  `HinhAnh` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`MaPhong`),
  KEY `MaLoaiPhong` (`MaLoaiPhong`),
  CONSTRAINT `phong_ibfk_1` FOREIGN KEY (`MaLoaiPhong`) REFERENCES `loai_phong` (`maloaiphong`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phong`
--

LOCK TABLES `phong` WRITE;
/*!40000 ALTER TABLE `phong` DISABLE KEYS */;
INSERT INTO `phong` VALUES (101,1,NULL,'IU',NULL),(102,1,NULL,'IU',NULL),(103,3,NULL,'FR',NULL);
/*!40000 ALTER TABLE `phong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sdt`
--

DROP TABLE IF EXISTS `sdt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sdt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `LoaiSDT` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SDT` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sdt`
--

LOCK TABLES `sdt` WRITE;
/*!40000 ALTER TABLE `sdt` DISABLE KEYS */;
INSERT INTO `sdt` VALUES (1,'Riêng','0823582541'),(2,'Vợ','0823658741');
/*!40000 ALTER TABLE `sdt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tai_khoan_admin`
--

DROP TABLE IF EXISTS `tai_khoan_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tai_khoan_admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `emp_id` int(11) NOT NULL,
  PRIMARY KEY (`admin_id`),
  KEY `emp_id` (`emp_id`),
  CONSTRAINT `tai_khoan_admin_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `tai_khoan_nhan_vien` (`emp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tai_khoan_admin`
--

LOCK TABLES `tai_khoan_admin` WRITE;
/*!40000 ALTER TABLE `tai_khoan_admin` DISABLE KEYS */;
INSERT INTO `tai_khoan_admin` VALUES (1,1);
/*!40000 ALTER TABLE `tai_khoan_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tai_khoan_khach`
--

DROP TABLE IF EXISTS `tai_khoan_khach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tai_khoan_khach` (
  `MaKhach` int(11) NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`MaKhach`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `tai_khoan_khach_ibfk_1` FOREIGN KEY (`MaKhach`) REFERENCES `khach` (`makhach`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tai_khoan_khach`
--

LOCK TABLES `tai_khoan_khach` WRITE;
/*!40000 ALTER TABLE `tai_khoan_khach` DISABLE KEYS */;
INSERT INTO `tai_khoan_khach` VALUES (1,'khach','b\' ,\\xb9b\\xacY\\x07[\\x96K\\x07\\x15-#Kp\'');
/*!40000 ALTER TABLE `tai_khoan_khach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tai_khoan_nhan_vien`
--

DROP TABLE IF EXISTS `tai_khoan_nhan_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tai_khoan_nhan_vien` (
  `emp_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`emp_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tai_khoan_nhan_vien`
--

LOCK TABLES `tai_khoan_nhan_vien` WRITE;
/*!40000 ALTER TABLE `tai_khoan_nhan_vien` DISABLE KEYS */;
INSERT INTO `tai_khoan_nhan_vien` VALUES (1,'admin','admin','b\' ,\\xb9b\\xacY\\x07[\\x96K\\x07\\x15-#Kp\'',1),(2,'nhanvien','nhanvien','b\' ,\\xb9b\\xacY\\x07[\\x96K\\x07\\x15-#Kp\'',1);
/*!40000 ALTER TABLE `tai_khoan_nhan_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thong_so_quy_dinh`
--

DROP TABLE IF EXISTS `thong_so_quy_dinh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `thong_so_quy_dinh` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Loai` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `GiaTri` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thong_so_quy_dinh`
--

LOCK TABLES `thong_so_quy_dinh` WRITE;
/*!40000 ALTER TABLE `thong_so_quy_dinh` DISABLE KEYS */;
INSERT INTO `thong_so_quy_dinh` VALUES (1,'Hệ số',1.5),(2,'Tỷ lệ phụ thu',0.25);
/*!40000 ALTER TABLE `thong_so_quy_dinh` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-01  9:55:28
