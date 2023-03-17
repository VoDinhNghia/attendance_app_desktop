-- open mysql workbench
-- create database attendance
-- open query tab => run row bellow

use `attendance`;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `users` (
  `username` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `users` (`username`, `password`) VALUES
('VoDinhNghia', 'dae09402a60544b9eb8b774a0aaf8176');

CREATE TABLE `label_face` (
  `ID` int(12) NOT NULL,
  `name` varchar(200) CHARACTER SET utf16 COLLATE utf16_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `history_attendance` (
  `ID` int(12) NOT NULL,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `date` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `time` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
COMMIT;