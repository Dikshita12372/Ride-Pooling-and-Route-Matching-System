-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 28, 2026 at 02:26 PM
-- Server version: 8.0.46
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ride_pooling`
--

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
CREATE TABLE IF NOT EXISTS `ratings` (
  `rating_id` int NOT NULL AUTO_INCREMENT,
  `ride_id` int NOT NULL,
  `driver_id` int NOT NULL,
  `passenger_id` int NOT NULL,
  `rating` int NOT NULL,
  `review` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`rating_id`),
  UNIQUE KEY `ride_id` (`ride_id`,`passenger_id`),
  KEY `driver_id` (`driver_id`),
  KEY `passenger_id` (`passenger_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `rides`
--

DROP TABLE IF EXISTS `rides`;
CREATE TABLE IF NOT EXISTS `rides` (
  `ride_id` int NOT NULL AUTO_INCREMENT,
  `driver_id` int NOT NULL,
  `source` varchar(150) NOT NULL,
  `destination` varchar(150) NOT NULL,
  `ride_date` date NOT NULL,
  `ride_time` time NOT NULL,
  `total_seats` int NOT NULL,
  `available_seats` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `route` text,
  `status` enum('AVAILABLE','FULL','COMPLETED','CANCELLED') NOT NULL DEFAULT 'AVAILABLE',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ride_id`),
  KEY `driver_id` (`driver_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rides`
--

INSERT INTO `rides` (`ride_id`, `driver_id`, `source`, `destination`, `ride_date`, `ride_time`, `total_seats`, `available_seats`, `price`, `route`, `status`, `created_at`) VALUES
(1, 1, 'Kurla', 'Kharghar', '2026-10-28', '03:05:00', 3, 2, 80.00, 'Kurla → Kharghar', 'AVAILABLE', '2026-08-30 14:20:58'),
(2, 3, 'Kharghar', 'Kurla', '2026-11-26', '06:30:00', 4, 4, 75.00, 'Kharghar→ Vashi→Chembur→Kurla', 'AVAILABLE', '2026-08-30 15:29:37'),
(3, 1, 'Kurla', 'Vashi', '2026-09-13', '10:36:00', 3, 3, 40.00, 'Kurla → Chembur → Mankhurd → Vashi', 'AVAILABLE', '2026-08-30 17:44:13'),
(4, 3, 'kurla', 'vashi', '2026-09-15', '10:30:00', 3, 3, 50.00, 'kurla → tilaknagar → chembur → govandi → vashi', 'AVAILABLE', '2026-08-31 03:54:37'),
(5, 3, 'Dombivli', 'Kurla', '2026-10-20', '12:10:00', 2, 2, 50.00, 'Dombivli → kopar → thane → ghatkopar → Kurla', 'AVAILABLE', '2026-09-05 03:57:39'),
(6, 3, 'Pune', 'Vashi', '2026-10-10', '03:45:00', 3, 2, 45.00, 'Pune → Wakad → Urse → Lonavala → Khopoli → Panvel → Vashi', 'AVAILABLE', '2026-09-07 04:01:10');

-- --------------------------------------------------------

--
-- Table structure for table `ride_requests`
--

DROP TABLE IF EXISTS `ride_requests`;
CREATE TABLE IF NOT EXISTS `ride_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `ride_id` int NOT NULL,
  `passenger_id` int NOT NULL,
  `status` enum('PENDING','ACCEPTED','REJECTED','CANCELLED') NOT NULL DEFAULT 'PENDING',
  `requested_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`request_id`),
  UNIQUE KEY `ride_id` (`ride_id`,`passenger_id`),
  KEY `passenger_id` (`passenger_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ride_requests`
--

INSERT INTO `ride_requests` (`request_id`, `ride_id`, `passenger_id`, `status`, `requested_at`) VALUES
(1, 1, 3, 'ACCEPTED', '2026-08-30 14:37:46'),
(2, 2, 1, 'REJECTED', '2026-08-30 15:31:23'),
(3, 6, 2, 'ACCEPTED', '2026-09-07 04:02:21');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('USER','ADMIN') NOT NULL DEFAULT 'USER',
  `phone` varchar(15) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `role`, `phone`, `created_at`) VALUES
(1, 'safdsf', 'abc@gmail.com', '254316', 'USER', '23514', '2026-08-30 13:58:48'),
(2, 'Dikshita', 'dikshita@gmail.com', '1234567', 'USER', '9086524567', '2026-08-30 14:30:09'),
(3, 'Dikshita Sanghani', 'qaz@gmail.com', '123456', 'USER', '9078657892', '2026-08-30 14:37:14');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`ride_id`) REFERENCES `rides` (`ride_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`driver_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ratings_ibfk_3` FOREIGN KEY (`passenger_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `rides`
--
ALTER TABLE `rides`
  ADD CONSTRAINT `rides_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `ride_requests`
--
ALTER TABLE `ride_requests`
  ADD CONSTRAINT `ride_requests_ibfk_1` FOREIGN KEY (`ride_id`) REFERENCES `rides` (`ride_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ride_requests_ibfk_2` FOREIGN KEY (`passenger_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
