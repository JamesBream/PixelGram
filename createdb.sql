##################
# PixelGram v0.1 #
##################
# Execute to build initial database structures
# Comment 

CREATE DATABASE PixelGram;

CREATE TABLE `PixelGram`.`tbl_user` (
	`user_id` BIGINT NULL AUTO_INCREMENT,
    `user_name` VARCHAR(45) NULL,
	`user_username` VARCHAR(45) NULL,
	`user_password` VARCHAR(66) NULL,
	PRIMARY KEY (`user_id`));

# Procedure for creating a user from passed in data
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
	IN p_name VARCHAR(20),
	IN p_username VARCHAR(20),
	IN p_password VARCHAR(66)
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

# Procedure for validating user login
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(IN p_username VARCHAR(20)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;