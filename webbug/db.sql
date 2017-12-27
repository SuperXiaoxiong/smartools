create database webbbug
use webbug

create table webbug(
 `ip` VARCHAR(100) not null,
 `port` INT unsigned,
 `osman`  VARCHAR(200) not null,
 `encode` VARCHAR(100) not null,
 `lang` VARCHAR(100) not null
);


//add filed id ,time , useragent

ALTER TABLE webbug ADD useragent VARCHAR(200);
//ALTER TABLE webbug ADD time DATETIME;
//alter table webbug modify column `time` TIMESTAMP ;
ALTER TABLE webbug ADD time TIMESTAMP;
alter table webbug add id int auto_increment primary key; 