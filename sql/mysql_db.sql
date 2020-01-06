DROP TABLE `employee_total_days`;
DROP TABLE `employee_leave_days`;

CREATE OR REPLACE TABLE `employee` (
  `employee_id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `position` varchar(20) NOT NULL,
  `specialization` VARCHAR(10) DEFAULT '',
  `team_number` TINYINT(1) DEFAULT 1,
  `expert` TINYINT(1) DEFAULT 0,
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

INSERT INTO `employee`(`full_name`, `position`, `specialization`, `team_number`, `expert`)
    VALUES ('Иванов', 'junior engineer', '', 1, 0);
INSERT INTO `employee_total_days`(`employee_id`, `total_days`, `year`)
    VALUES (1, 28, 2020);
INSERT INTO `employee_leave_days`(`employee_id`, `leave_days`, `start_date`, `end_date`)
    VALUES(1, 5, '2020-01-06', '2020-01-12');

