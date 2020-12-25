-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 23, 2019 at 02:08 PM
-- Server version: 10.1.25-MariaDB
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `web_flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `provider`
--

CREATE TABLE `provider` (
  `nama_provider` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `provider`
--

INSERT INTO `provider` (`nama_provider`) VALUES
('3 (Tri)'),
('Indosat Ooredo'),
('Telkomsel'),
('XL Axiata');

-- --------------------------------------------------------

--
-- Table structure for table `pulsa`
--

CREATE TABLE `pulsa` (
  `nominal_pulsa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pulsa`
--

INSERT INTO `pulsa` (`nominal_pulsa`) VALUES
(25000),
(50000),
(100000);

-- --------------------------------------------------------

--
-- Table structure for table `rekaman_transaksi`
--

CREATE TABLE `rekaman_transaksi` (
  `id` int(11) NOT NULL,
  `attempt` varchar(1) NOT NULL,
  `nama_rekaman_transaksi` varchar(100) NOT NULL,
  `id_transaksi` varchar(50) NOT NULL,
  `kode_angka` varchar(1) NOT NULL,
  `y_pred_sv` char(1) NOT NULL,
  `y_pred_sr` char(1) NOT NULL,
  `id_user` varchar(25) NOT NULL,
  `path_rekaman` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rekaman_transaksi`
--

INSERT INTO `rekaman_transaksi` (`id`, `attempt`, `nama_rekaman_transaksi`, `id_transaksi`, `kode_angka`, `y_pred_sv`, `y_pred_sr`, `id_user`, `path_rekaman`) VALUES
(313, '1', 'TRS586188_USR19_2.wav', 'TRS586188', '2', '1', '2', 'USR19', './voices\\transactions\\TRS586188\\1'),
(314, '1', 'TRS586188_USR19_6.wav', 'TRS586188', '6', '1', '9', 'USR19', './voices\\transactions\\TRS586188\\1'),
(315, '1', 'TRS586188_USR19_8.wav', 'TRS586188', '8', '1', '8', 'USR19', './voices\\transactions\\TRS586188\\1'),
(316, '1', 'TRS586188_USR19_4.wav', 'TRS586188', '4', '1', '4', 'USR19', './voices\\transactions\\TRS586188\\1'),
(317, '1', 'TRS586188_USR19_7.wav', 'TRS586188', '7', '1', '7', 'USR19', './voices\\transactions\\TRS586188\\1'),
(318, '2', 'TRS586188_USR19_2.wav', 'TRS586188', '2', '1', '2', 'USR19', './voices\\transactions\\TRS586188\\2'),
(319, '2', 'TRS586188_USR19_6.wav', 'TRS586188', '6', '1', '8', 'USR19', './voices\\transactions\\TRS586188\\2'),
(320, '2', 'TRS586188_USR19_9.wav', 'TRS586188', '9', '0', '9', 'USR19', './voices\\transactions\\TRS586188\\2'),
(321, '2', 'TRS586188_USR19_4.wav', 'TRS586188', '4', '1', '4', 'USR19', './voices\\transactions\\TRS586188\\2'),
(322, '2', 'TRS586188_USR19_5.wav', 'TRS586188', '5', '0', '5', 'USR19', './voices\\transactions\\TRS586188\\2'),
(323, '1', 'TRS138548_USR48_2.wav', 'TRS138548', '2', '1', '2', 'USR48', './voices\\transactions\\TRS138548\\1'),
(324, '1', 'TRS138548_USR48_5.wav', 'TRS138548', '5', '0', '5', 'USR48', './voices\\transactions\\TRS138548\\1'),
(325, '1', 'TRS138548_USR48_8.wav', 'TRS138548', '8', '1', '8', 'USR48', './voices\\transactions\\TRS138548\\1'),
(326, '1', 'TRS138548_USR48_4.wav', 'TRS138548', '4', '1', '4', 'USR48', './voices\\transactions\\TRS138548\\1'),
(327, '1', 'TRS138548_USR48_3.wav', 'TRS138548', '3', '0', '3', 'USR48', './voices\\transactions\\TRS138548\\1'),
(328, '2', 'TRS138548_USR48_4.wav', 'TRS138548', '4', '1', '4', 'USR48', './voices\\transactions\\TRS138548\\2'),
(329, '2', 'TRS138548_USR48_9.wav', 'TRS138548', '9', '1', '9', 'USR48', './voices\\transactions\\TRS138548\\2'),
(330, '2', 'TRS138548_USR48_7.wav', 'TRS138548', '7', '1', '7', 'USR48', './voices\\transactions\\TRS138548\\2'),
(331, '2', 'TRS138548_USR48_2.wav', 'TRS138548', '2', '1', '2', 'USR48', './voices\\transactions\\TRS138548\\2'),
(332, '2', 'TRS138548_USR48_3.wav', 'TRS138548', '3', '1', '3', 'USR48', './voices\\transactions\\TRS138548\\2'),
(333, '1', 'TRS772050_USR47_9.wav', 'TRS772050', '9', '0', '1', 'USR47', './voices\\transactions\\TRS772050\\1'),
(334, '1', 'TRS772050_USR47_3.wav', 'TRS772050', '3', '0', '3', 'USR47', './voices\\transactions\\TRS772050\\1'),
(335, '1', 'TRS772050_USR47_5.wav', 'TRS772050', '5', '0', '4', 'USR47', './voices\\transactions\\TRS772050\\1'),
(336, '1', 'TRS772050_USR47_6.wav', 'TRS772050', '6', '1', '8', 'USR47', './voices\\transactions\\TRS772050\\1'),
(337, '1', 'TRS772050_USR47_2.wav', 'TRS772050', '2', '1', '1', 'USR47', './voices\\transactions\\TRS772050\\1'),
(338, '2', 'TRS772050_USR47_2.wav', 'TRS772050', '2', '0', '1', 'USR47', './voices\\transactions\\TRS772050\\2'),
(339, '2', 'TRS772050_USR47_3.wav', 'TRS772050', '3', '1', '3', 'USR47', './voices\\transactions\\TRS772050\\2'),
(340, '2', 'TRS772050_USR47_5.wav', 'TRS772050', '5', '0', '4', 'USR47', './voices\\transactions\\TRS772050\\2'),
(341, '2', 'TRS772050_USR47_1.wav', 'TRS772050', '1', '1', '1', 'USR47', './voices\\transactions\\TRS772050\\2'),
(342, '2', 'TRS772050_USR47_8.wav', 'TRS772050', '8', '0', '1', 'USR47', './voices\\transactions\\TRS772050\\2');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id_transaksi` varchar(50) NOT NULL,
  `id_user` varchar(25) NOT NULL,
  `no_hp` varchar(12) NOT NULL,
  `nama_provider` varchar(30) NOT NULL,
  `nominal_pulsa` int(11) NOT NULL,
  `waktu_transaksi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status_transaksi` tinyint(1) NOT NULL DEFAULT '2'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`id_transaksi`, `id_user`, `no_hp`, `nama_provider`, `nominal_pulsa`, `waktu_transaksi`, `status_transaksi`) VALUES
('TRS138548', 'USR48', '628211434232', 'Telkomsel', 25000, '2019-06-18 16:18:06', 1),
('TRS586188', 'USR19', '628128608370', 'Telkomsel', 50000, '2019-06-18 16:12:58', 0),
('TRS772050', 'USR47', '628211173938', 'Telkomsel', 25000, '2019-06-18 16:23:32', 0);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` varchar(25) NOT NULL,
  `nama_user` varchar(50) NOT NULL,
  `email_user` varchar(30) NOT NULL,
  `password_user` text NOT NULL,
  `no_hp_user` varchar(13) NOT NULL,
  `saldo_user` int(11) NOT NULL DEFAULT '50000',
  `waktu_user_daftar` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status_pendaftaran_suara` char(1) NOT NULL DEFAULT '0',
  `path_mfcc` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `nama_user`, `email_user`, `password_user`, `no_hp_user`, `saldo_user`, `waktu_user_daftar`, `status_pendaftaran_suara`, `path_mfcc`) VALUES
('USR19', 'Kevin03', 'kevin@gmail.com', '25d55ad283aa40af464c76d713c7ad', '082728288299', 50000, '2019-06-18 16:10:16', '1', './voices\\users\\USR19\\USR19.npz'),
('USR28', 'Bella Lie', 'mz.bellalie@gmail.com', '25d55ad283aa40af464c76d713c7ad', '081212630097', 75000, '2019-06-16 15:28:09', '1', './voices\\users\\USR28\\USR28.npz'),
('USR46', 'Juni Handoko', 'junihandoko@gmail.com', '25d55ad283aa40af464c76d713c7ad', '082184755697', 50000, '2019-06-17 15:01:11', '1', './voices\\users\\USR46\\USR46.npz'),
('USR47', 'Reynaldo', 'aldoboy97@gmail.com', '25d55ad283aa40af464c76d713c7ad', '082111739383', 50000, '2019-06-18 16:21:17', '1', './voices\\users\\USR47\\USR47.npz'),
('USR48', 'Charles Yuliansen', 'yuliansen92@gmail.com', '25d55ad283aa40af464c76d713c7ad', '082114342328', 25000, '2019-06-18 16:16:04', '1', './voices\\users\\USR48\\USR48.npz'),
('USR57', 'Bella', 'bella@ell.com', '25d55ad283aa40af464c76d713c7ad', '9874433', 157000, '2019-06-17 21:25:07', '1', './voices\\users\\USR57\\USR57.npz'),
('USR78', 'Cindy Winata', 'cndywinata@gmail.com', '25d55ad283aa40af464c76d713c7ad', '627282927289', 50000, '2019-06-17 13:38:12', '1', './voices\\users\\USR78\\USR78.npz'),
('USR89', 'Henry', 'henryhalim97@gmail.com', '3d9ddac1a92f2b17f26e783dc42638ff', '081219496238', 25000, '2019-06-17 13:46:44', '1', './voices\\users\\USR89\\USR89.npz');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `provider`
--
ALTER TABLE `provider`
  ADD PRIMARY KEY (`nama_provider`);

--
-- Indexes for table `pulsa`
--
ALTER TABLE `pulsa`
  ADD PRIMARY KEY (`nominal_pulsa`);

--
-- Indexes for table `rekaman_transaksi`
--
ALTER TABLE `rekaman_transaksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_rekamantransaksi_transaksi` (`id_transaksi`),
  ADD KEY `FK_rekamantransaksi_user` (`id_user`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `FK_transaksi_id_user` (`id_user`),
  ADD KEY `FK_transaksi_nama_provider` (`nama_provider`),
  ADD KEY `FK_transaksi_nominal_pulsa` (`nominal_pulsa`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `rekaman_transaksi`
--
ALTER TABLE `rekaman_transaksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=353;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `rekaman_transaksi`
--
ALTER TABLE `rekaman_transaksi`
  ADD CONSTRAINT `FK_rekamantransaksi_transaksi` FOREIGN KEY (`id_transaksi`) REFERENCES `transaksi` (`id_transaksi`),
  ADD CONSTRAINT `FK_rekamantransaksi_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `FK_transaksi_id_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`),
  ADD CONSTRAINT `FK_transaksi_nama_provider` FOREIGN KEY (`nama_provider`) REFERENCES `provider` (`nama_provider`),
  ADD CONSTRAINT `FK_transaksi_nominal_pulsa` FOREIGN KEY (`nominal_pulsa`) REFERENCES `pulsa` (`nominal_pulsa`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
