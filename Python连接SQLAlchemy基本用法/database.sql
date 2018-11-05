-- 1 创建数据库
CREATE DATABASE IF NOT EXISTS user_system
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
-- 2 使用数据库
USE user_system;
-- 3 创建用户表
CREATE TABLE IF NOT EXISTS tb_user (
    `id` int(11) AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `username` varchar(20) NOT NULL UNIQUE COMMENT '用户名',
    `password` varchar(32) NOT NULL COMMENT '密码',
    `reg_time` timestamp NOT NULL DEFAULT current_timestamp COMMENT '注册时间'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_general_ci
COMMENT='用户表';
-- 4 创建签到表
CREATE TABLE IF NOT EXISTS tb_sign (
    `id` int(11) AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` int(11) NOT NULL COMMENT '用户ID',
    `sign_time` timestamp NOT NULL DEFAULT current_timestamp COMMENT '签到时间',
    FOREIGN KEY(`user_id`) REFERENCES `tb_user`(`id`)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_general_ci
COMMENT='签到表';