DROP TABLE IF EXISTS IF EXISTS song;
CREATE TABLE song (
	SID SERIAL,
	length INTEGER,
    song_name VARCHAR(128),
    release_year INTEGER,
    lyrics VARCHAR(16384),
    youtube_link VARCHAR(1024),
    spotify_link VARCHAR(1024),
    apple_link VARCHAR(1024),
    PRIMARY KEY (SID)
);

DROP TABLE IF EXISTS person;
CREATE TABLE person (
	PID SERIAL,
	person_name VARCHAR(128),
	gender VARCHAR(1),
	birth_date DATETIME,
	country VARCHAR(128),
	AID INTEGER,
	PRIMARY KEY (PID)
);

DROP TABLE IF EXISTS band;
CREATE TABLE band (
    BID SERIAL,
	formation_year INTEGER,
	AID INTEGER,
	PRIMARY KEY (BID)
);

DROP TABLE IF EXISTS has_members;
CREATE TABLE has_members (
	PID INTEGER,
	BID INTEGER,
	PRIMARY KEY (PID, BID)
);

DROP TABLE IF EXISTS artist;
CREATE TABLE artist (
    AID SERIAL,
	artist_name VARCHAR(128),
    artist_picture_link VARCHAR(1024)
    PRIMARY KEY (AID)
);

DROP TABLE IF EXISTS genre;
CREATE TABLE genre (
	genre_name VARCHAR(128),
	PRIMARY KEY (genre_name)
);

DROP TABLE IF EXISTS record;
CREATE TABLE record (
	RID SERIAL,
	record_cover_link VARCHAR(1024),
	is_single BOOLEAN,
	record_name VARCHAR(128),
	release_year INTEGER,
	PRIMARY KEY (RID)
);

DROP TABLE IF EXISTS similar_to;
CREATE TABLE similar_to (
	SID_1 INTEGER,
	SID_2 INTEGER,
	similarity_score INTEGER,
	PRIMARY KEY (SID_1, SID_2)
);

DROP TABLE IF EXISTS record_songs;
CREATE TABLE record_songs (
	SID INTEGER,
	RID INTEGER,
	PRIMARY KEY (SID, RID)
);

DROP TABLE IF EXISTS song_genre;
CREATE TABLE song_genre (
	SID INTEGER,
	genre_name VARCHAR(128),
	PRIMARY KEY (SID, genre_name)
);

DROP TABLE IF EXISTS record_artist;
CREATE TABLE record_artist (
	RID INTEGER,
	AID INTEGER,
	PRIMARY KEY (RID, AID)
);

DROP TABLE IF EXISTS song_tags;
CREATE TABLE song_tags (
	SID INTEGER,
	tag_name VARCHAR(256),
	PRIMARY KEY (SID, tag_name)
);

DROP TABLE IF EXISTS song_by;
CREATE TABLE song_by (
	SID INTEGER,
	AID INTEGER,
	PRIMARY KEY (SID, AID)
);

DROP TABLE IF EXISTS song_feature;
CREATE TABLE song_feature (
	SID INTEGER,
	AID INTEGER,
	PRIMARY KEY (SID, AID)
);
