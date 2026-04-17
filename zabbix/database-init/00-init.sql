DROP DATABASE IF EXISTS zabbix;
create database zabbix character set utf8mb4 collate utf8mb4_bin;
GRANT ALL PRIVILEGES ON *.* TO "zabbx"@"%"; FLUSH PRIVILEGES;
SET GLOBAL log_bin_trust_function_creators = 1;