DROP TABLE IF EXISTS user;
CREATE TABLE user (
	id INT(11) NOT NULL auto_increment,
	email VARCHAR(40) NOT NULL,
        track INT(11),
	PRIMARY KEY (id)
);

DROP TABLE IF EXISTS keyword;
CREATE TABLE keyword (
        id INT(11) NOT NULL auto_increment,
        data VARCHAR(100) NOT NULL,
        updated_at DATETIME,
        PRIMARY KEY (id)
);

DROP TABLE IF EXISTS tracking;
CREATE TABLE tracking (
        id INT(11) NOT NULL auto_increment,
	user_id INT(11),
	keyword_id INT(11),
	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (keyword_id) REFERENCES keyword(id),
        PRIMARY KEY (id)
);

