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
	IN p_username VARCHAR(40),
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
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(IN p_username VARCHAR(40)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;

CREATE TABLE `tbl_post` (
    `post_id` INT(11) NOT NULL AUTO_INCREMENT,
    `post_title` VARCHAR(45) DEFAULT NULL,
    `post_description` VARCHAR(500) DEFAULT NULL,
    `post_user_id` BIGINT DEFAULT NULL,
    `post_date` DATETIME DEFAULT NULL,
    PRIMARY KEY (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

# Procedure to add a new post
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_newPost`(
    IN p_title VARCHAR(45),
    IN p_description VARCHAR(500),
    IN p_user_id BIGINT
)
BEGIN
    INSERT INTO tbl_post(
        post_title,
        post_description,
        post_user_id,
        post_date
    )
    VALUES
    (
        p_title,
        p_description,
        p_user_id,
        NOW()
    );
END$$
DELIMITER ;

# Procedure to retrieve a post
DELIMITER $$
CREATE PROCEDURE `sp_getPostByUser` (
    IN p_user_id BIGINT
)
BEGIN
    SELECT * FROM tbl_post WHERE post_user_id = p_user_id;
END$$
DELIMITER ;