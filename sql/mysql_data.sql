DROP TABLE IF EXISTS `employee_total_days`;
DROP TABLE IF EXISTS `employee_leave_days`;

CREATE OR REPLACE TABLE `employee` (
  `employee_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `position` varchar(20) NOT NULL CHECK(`position` in ('junior engineer', 'senior engineer', 'chief engineer', 'team leader')),
  `specialization` SET('BA', 'OACI', 'O365', 'Core') NOT NULL DEFAULT '',
  `team_number` TINYINT(1) NOT NULL DEFAULT 1,
  `expert` TINYINT(1) NOT NULL DEFAULT 0,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE OR REPLACE TABLE `employee_total_days` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `employee_id` INT(11) NOT NULL,
  `total_days` TINYINT(4) NOT NULL,
  `year` SMALLINT(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_employee_total_days` (`employee_id`, total_days),
  CONSTRAINT `FK_employee_total_days` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;


CREATE OR REPLACE TABLE `employee_leave_days` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `employee_id` INT(11) NOT NULL,
  `leave_days` TINYINT(4) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `FK_employee_leave_days` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

CREATE OR REPLACE TABLE `user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL UNIQUE,
  `password` VARCHAR(128) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `roles` SET('read:users','write:users','read:employees', 'write:employees') NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

INSERT INTO `employee`(`full_name`, `position`, `specialization`, `team_number`, `expert`, `email`)
    VALUES ('Иванов', 'junior engineer', 'Core,BA', 1, 0, 'mail@mail.ru');
INSERT INTO `employee_total_days`(`employee_id`, `total_days`, `year`)
    VALUES (1, 28, 2020);
INSERT INTO `employee_leave_days`(`employee_id`, `leave_days`, `start_date`, `end_date`)
    VALUES(1, 5, '2020-01-06', '2020-01-12');

INSERT INTO `user`(`username`, `password`, `email`, `roles`)
    VALUES('admin', '$2b$12$HSz0inPMP6loSguyp5KPl.MZh/RaV/0klbUMCU9h6peIIyn/P4fQq', 'admin@mail.com', 'read:users,write:users');
INSERT INTO `user`(`username`, `password`, `email`, `roles`)
    VALUES('user', '$2b$12$nZKuiZrbSedpTwQrhDn6hey6S38fr5oVEYuM5QAodBrsNpCq3v9WO', 'user@mail.com', 'read:employees,write:employees');

