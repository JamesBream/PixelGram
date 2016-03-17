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

CREATE TABLE `PixelGram`.`tbl_post` (
    `post_id` INT(11) NOT NULL AUTO_INCREMENT,
    `post_title` VARCHAR(45) DEFAULT NULL,
    `post_description` VARCHAR(500) DEFAULT NULL,
    `post_user_id` BIGINT DEFAULT NULL,
    `post_date` DATETIME DEFAULT NULL,
    `post_file_path` VARCHAR(200) NULL,
    PRIMARY KEY (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

# Procedure for creating a user from passed in data
USE `PixelGram`;
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
USE `PixelGram`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(IN p_username VARCHAR(40)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;

# Procedure to add a new post
USE `PixelGram`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_newPost`(
    IN p_title VARCHAR(45),
    IN p_description VARCHAR(500),
    IN p_user_id BIGINT,
    IN p_file_path VARCHAR(200)
)
BEGIN
    INSERT INTO tbl_post(
        post_title,
        post_description,
        post_user_id,
        post_date,
        post_file_path
    )
    VALUES
    (
        p_title,
        p_description,
        p_user_id,
        NOW(),
        p_file_path
    );
END$$
DELIMITER ;

# Procedure to retrieve all posts by a user
USE `PixelGram`;
DELIMITER $$
CREATE PROCEDURE `sp_getPostByUser` (
    IN p_user_id BIGINT
)
BEGIN
    SELECT * FROM tbl_post WHERE post_user_id = p_user_id;
END$$
DELIMITER ;

# Procedure to retrieve a post by its post ID and the userID
USE `PixelGram`;
DELIMITER $$
CREATE PROCEDURE `sp_getPostByID` (
    IN p_post_id BIGINT,
    IN p_user_id BIGINT
)
BEGIN
SELECT * FROM tbl_post WHERE post_id = p_post_id and post_user_id = p_user_id;
END$$
DELIMITER ;

# Procedure to update a post
USE `PixelGram`;
DELIMITER $$
CREATE PROCEDURE `sp_updatePost` (
    IN p_title VARCHAR(45),
    IN p_description VARCHAR(500),
    IN p_post_id BIGINT,
    IN p_user_id BIGINT,
    IN p_file_path VARCHAR(200)
)
BEGIN
UPDATE tbl_post SET 
    post_title = p_title, 
    post_description = p_description,
    post_file_path = p_file_path
    WHERE post_id = p_post_id and post_user_id = p_user_id;
END$$
DELIMITER ;

# Procedure to delete posts
USE `PixelGram`;
DELIMITER $$
CREATE PROCEDURE `sp_deletePost` (
    IN p_post_id BIGINT,
    IN p_user_id BIGINT
)
BEGIN
    DELETE from tbl_post where post_id = p_post_id and post_user_id = p_user_id;
END$$
DELIMITER ;

# Procedure to get all posts
USE `PixelGram` ()
DELIMITER $$
CREATE PROCEDURE `sp_getAllPosts`;
BEGIN
    SELECT post_id, post_title, post_description, post_file_path FROM tbl_post;
END$$
DELIMITER ;