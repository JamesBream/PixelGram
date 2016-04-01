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
	PRIMARY KEY (`user_id`)
);

CREATE TABLE `PixelGram`.`tbl_post` (
    `post_id` BIGINT NOT NULL AUTO_INCREMENT,
    `post_title` VARCHAR(45) DEFAULT NULL,
    `post_description` VARCHAR(500) DEFAULT NULL,
    `post_user_id` BIGINT DEFAULT NULL,
    `post_date` DATETIME DEFAULT NULL,
    `post_file_path` VARCHAR(200) NULL,
    PRIMARY KEY (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE `PixelGram`.`tbl_likes` (
    `post_id` BIGINT NOT NULL,
    `like_id` BIGINT NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT NULL,
    `post_like` TINYINT NULL DEFAULT 0,
    PRIMARY KEY (`like_id`)
);

# Function to sum the total likes for posts
USE `PixelGram`;
DELIMITER $$
CREATE FUNCTION `getSum` (
    p_post_id BIGINT
) RETURNS BIGINT
BEGIN
    SET @likesum = 0;
    SELECT SUM(post_like) INTO @likesum FROM tbl_likes WHERE post_id = p_post_id;
RETURN @likesum;
END$$
DELIMITER ;

# Function to determine if a user has liked a post
USE `PixelGram`;
DELIMITER $$
CREATE FUNCTION `hasLiked` (
    p_post_id BIGINT,
    p_user_id BIGINT
) RETURNS TINYINT
BEGIN
    SET @likestatus = 0;
    SELECT post_like INTO @likestatus FROM tbl_likes WHERE post_id = p_post_id and user_id = p_user_id;
RETURN @likestatus;
END$$
DELIMITER ;

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
    VALUES(
        p_title,
        p_description,
        p_user_id,
        NOW(),
        p_file_path
    );
    
    SET @last_id = LAST_INSERT_ID();
    
    INSERT INTO tbl_likes(
        post_id,
        user_id,
        post_like
    )
    VALUES(
        @last_id,
        p_user_id,
        0
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
USE `PixelGram`;
DELIMITER $$
CREATE PROCEDURE `sp_getAllPosts` (
    IN p_user_id BIGINT
)
BEGIN
    SELECT post_id, post_title, post_description, post_file_path, getSum(post_id), hasLiked(post_id, p_user_id) FROM tbl_post;
END$$
DELIMITER ;

# Procedure to add/update post likes
USE `PixelGram`
DELIMITER $$
CREATE PROCEDURE `sp_AddUpdateLikes` (
    p_post_id BIGINT,
    p_user_id BIGINT,
    p_like TINYINT
)
BEGIN
    # Update existing like entry if it exists
    IF (SELECT EXISTS (SELECT 1 FROM tbl_likes WHERE post_id = p_post_id AND user_id = p_user_id)) THEN
    
        # Get current like value
        SELECT post_like INTO @curval FROM tbl_likes WHERE post_id = p_post_id AND user_id = p_user_id;
        
        # Toggle like value
        IF @curval = 0 THEN
            UPDATE tbl_likes SET post_like = 1 WHERE post_id = p_post_id AND user_id = p_user_id;
        ELSE
            UPDATE tbl_likes SET post_like = 0 WHERE post_id = p_post_id AND user_id = p_user_id;
        END IF;
        
    ELSE
    
        INSERT INTO tbl_likes(
            post_id,
            user_id,
            post_like
        )
        VALUES(
            p_post_id,
            p_user_id,
            p_like
            );
            
    END IF;
END$$
DELIMITER ;

# Procedure to retrieve post like status
USE `PixelGram`;
DELIMITER $$
CREATE PROCEDURE `sp_getLikeStatus` (
    IN p_post_id BIGINT,
    IN p_user_id BIGINT
)
BEGIN
    SELECT getSum(p_post_id), hasLiked(p_post_id, p_user_id);
END$$
DELIMITER ;