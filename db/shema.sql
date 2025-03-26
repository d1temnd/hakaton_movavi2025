CREATE TABLE users (
	id INTEGER NOT NULL, 
	telegram_id INTEGER, 
	role VARCHAR, 
	PRIMARY KEY (id)
)

CREATE TABLE invites (
	id INTEGER NOT NULL, 
	telegram_id INTEGER, 
	token VARCHAR, 
	expiration DATETIME, 
	role VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (token)
)