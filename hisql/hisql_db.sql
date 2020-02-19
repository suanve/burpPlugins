/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 100407
 Source Host           : localhost:3306
 Source Schema         : hisql_db

 Target Server Type    : MySQL
 Target Server Version : 100407
 File Encoding         : 65001

 Date: 15/11/2019 17:30:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for info
-- ----------------------------
DROP TABLE IF EXISTS `info`;
CREATE TABLE `info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL COMMENT '用户名',
  `request_body` text DEFAULT NULL COMMENT '请求主体',
  `method` varchar(255) DEFAULT NULL COMMENT '请求方式',
  `domain` varchar(255) DEFAULT NULL COMMENT '域名',
  `type` varchar(255) DEFAULT NULL COMMENT '类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
