DROP TABLE IF EXISTS `employee_total_days`;
DROP TABLE IF EXISTS `employee_leave_days`;
DROP TABLE IF EXISTS `employee`;

CREATE OR REPLACE TABLE `team` (
  `team_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE OR REPLACE TABLE `employee` (
  `employee_id` INT(11) NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(255) NOT NULL,
  `position` VARCHAR(20) NOT NULL CHECK(`position` in ('junior engineer', 'senior engineer', 'chief engineer', 'team leader')),
  `specialization` SET('BA', 'OACI', 'O365', 'Core') NOT NULL DEFAULT '',
  `team_id` INT(11) NOT NULL,
  `expert` TINYINT(1) NOT NULL DEFAULT 0,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY (`employee_id`),
  CONSTRAINT `FK_employee_team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE OR REPLACE TABLE `employee_total_days` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `employee_id` INT(11) NOT NULL,
  `total_days` TINYINT(4) NOT NULL CHECK(total_days>0),
  `year` SMALLINT(4) NOT NULL CHECK(year>2019),
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_employee_total_days` (`employee_id`, year),
  CONSTRAINT `FK_employee_total_days` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE OR REPLACE TABLE `employee_leave_days` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `employee_id` INT(11) NOT NULL,
  `leave_days` TINYINT(4) NOT NULL CHECK(leave_days>0),
  `start_date` DATE NOT NULL CHECK(year(`start_date`) > 2019),
  `end_date` DATE NOT NULL CHECK(year(`end_date`) > 2019),
  PRIMARY KEY (`id`),
  CONSTRAINT `FK_employee_leave_days` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`) ON DELETE CASCADE,
  CONSTRAINT `CK_end_date_greater_start_date` CHECK (`start_date`<=`end_date`) 

) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;


CREATE OR REPLACE TABLE `user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL UNIQUE,
  `password` VARCHAR(128) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `roles` SET('read:users','write:users','write:teams', 'write:employees', 'write:total_days', 'write:leave_days') NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

INSERT INTO `team`(`name`) VALUES ('Psi');
INSERT INTO `team`(`name`) VALUES ('Alpha');

INSERT INTO `employee`(`full_name`, `position`, `specialization`, `team_id`, `expert`, `email`)
    VALUES ('Иванов', 'team leader', 'Core,BA', 1, 1, 'ivanov@mail.ru');
INSERT INTO `employee`(`full_name`, `position`, `specialization`, `team_id`, `expert`, `email`)
    VALUES ('Петров', 'junior engineer', 'Core,OACI', 1, 0, 'petrov@mail.ru');
INSERT INTO `employee`(`full_name`, `position`, `specialization`, `team_id`, `expert`, `email`)
    VALUES ('Сидоров', 'junior engineer', 'BA,O365', 2, 0, 'sidorov@mail.ru');
INSERT INTO `employee`(`full_name`, `position`, `specialization`, `team_id`, `expert`, `email`)
    VALUES ('Ильин', 'team leader', 'OACI,O365', 2, 1, 'ilyin@mail.ru');

INSERT INTO `employee_total_days`(`employee_id`, `total_days`, `year`)
    VALUES (1, 28, 2020);
INSERT INTO `employee_leave_days`(`employee_id`, `leave_days`, `start_date`, `end_date`) VALUES(1, 5, '2020-01-06', '2020-01-12');
INSERT INTO `employee_leave_days`(`employee_id`, `leave_days`, `start_date`, `end_date`) VALUES(2, 3, '2020-01-15', '2020-01-19');

INSERT INTO `user`(`username`, `password`, `email`, `roles`)
    VALUES('admin', '$2b$12$HSz0inPMP6loSguyp5KPl.MZh/RaV/0klbUMCU9h6peIIyn/P4fQq', 'admin@mail.com', 'write:teams,write:users');
INSERT INTO `user`(`username`, `password`, `email`, `roles`)
    VALUES('user', '$2b$12$nZKuiZrbSedpTwQrhDn6hey6S38fr5oVEYuM5QAodBrsNpCq3v9WO', 'user@mail.com', 'write:teams,write:employees,write:total_days,write:leave_days');

