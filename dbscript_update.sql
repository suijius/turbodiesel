ALTER TABLE `ext_code` DROP COLUMN `alias` 
, DROP INDEX `alias` ;

ALTER TABLE `ext_code` CHANGE COLUMN `datasource_id` `code_id` INT(11) NOT NULL AUTO_INCREMENT  ;

ALTER TABLE `page` ADD COLUMN `code_id` INT(11) NULL DEFAULT NULL  AFTER `title` ;

ALTER TABLE `ext_code` ADD COLUMN `is_global` TINYINT NOT NULL DEFAULT 0  AFTER `code` ;


42 revision:

ALTER TABLE `td`.`reversion_version` MODIFY COLUMN `serialized_data` LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE `td`.`reversion_version` MODIFY COLUMN `object_repr` LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;


ALTER TABLE `td`.`nature_additionresult` ADD COLUMN `student` INTEGER AFTER `id`;
ALTER TABLE `td`.`nature_additionresult` MODIFY COLUMN `date` DATETIME DEFAULT NULL;

ALTER TABLE `page` DROP COLUMN `lft`,
 DROP COLUMN `rght`,
 DROP COLUMN `tree_id`,
 DROP COLUMN `level`;
 

 ALTER TABLE `ext_workflow` ADD COLUMN `description` VARCHAR(1000) NOT NULL AFTER `name`;

INSERT INTO `application` ('name', 'alias', 'image'); VALUES (`Общие ресурсы`, `common`, `/media/common.png`)

UPDATE `application` SET `application_id`=0 WHERE `application_id`='X';
update FROM `entity` set `application_id` = 0 where `application_id` = 1;


 ALTER TABLE `application` ADD COLUMN `title` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL AFTER `image`;
 update application set title=name;

ALTER TABLE `application` ADD COLUMN `default` INT NULL DEFAULT '0'  AFTER `title` ;
ALTER TABLE `entity` ADD COLUMN `service` INT NULL DEFAULT '0'  AFTER `application_id` ;



