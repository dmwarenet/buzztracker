DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id serial PRIMARY KEY,
	email text NOT NULL,
        track integer
);

DROP TABLE IF EXISTS keyword;
CREATE TABLE keyword (
        id serial PRIMARY KEY,
        data text NOT NULL,
        updated_at timestamp
);

DROP TABLE IF EXISTS tracking;
CREATE TABLE tracking (
        id serial PRIMARY KEY,
	users_id integer references users(id),
	keyword_id integer references keyword(id)
);

