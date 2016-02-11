##################
# PaperLoop v0.1 #
##################
# Execute to build initial database structures
# Comment 

CREATE DATABASE PaperLoop;

CREATE TABLE `PaperLoop`.`tbl_user` (
	`user_id` BIGINT NULL AUTO_INCREMENT,
	`user_username` VARCHAR(45) NULL,
	`user_password` VARCHAR(45) NULL,
	PRIMARY KEY (`user_id`));

# Procedure for creating a user from passed in data
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
	IN p_name VARCHAR(20),
	IN p_username VARCHAR(20),
	IN p_password VARCHAR(20)
)
BEGIN
    # Check whether the user already exists
	IF (select exists (select 1 from tbl_user where user_username = p_username) ) THEN
	
		select 'Username Already Exists!';
	
	ELSE
	
		insert into tbl_user
		(
			user_name,
			user_username,
			user_password
		)
		values
		(
			p_name,
			p_username,
			p_password
		);
		
	END IF;
END$$
DELIMITER ;