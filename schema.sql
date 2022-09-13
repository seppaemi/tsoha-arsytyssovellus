CREATE TABLE users (
	 id SERIAL PRIMARY KEY,
	 username TEXT UNIQUE,
	 password TEXT,
	 is_admin BOOLEAN
);

CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    region_id INTEGER REFERENCES regions,
    sent_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE info (
	id SERIAL PRIMARY KEY,
	day DATE,
	time TIME,
	message_id INTEGER REFERENCES messages,
	location TEXT
);

CREATE TABLE images (
	id SERIAL PRIMARY KEY,
	name TEXT,
	data BYTEA,
	message_id INTEGER REFERENCES messages
);