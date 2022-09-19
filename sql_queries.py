import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS users"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= (""" CREATE TABLE IF NOT EXISTS staging_events
(
    artist VARCHAR(20),
    auth VARCHAR(20),
    firstName VARCHAR(20),
    gender VARCHAR(5),
    itemInSession INT,
    lastName VARCHAR(20),
    lengh DOUBLE PRECISION,
    level VARCHAR(4),
    location VARCHAR(20),
    method VARCHAR(3),
    page VARCHAR(8),
    regestration DOUBLE PRECISION,
    sessionId INT,
    song VARCHAR(50),
    status INT,
    ts BIGINT,
    userAgent VARCHAR(50),
    userId INT
);
""")

staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS staging_songs
(
    num_songs INT,
    artist_id VARCHAR(50),
    artist_latitude DOUBLE PRECISION,
    artist_longitude DOUBLE PRECISION,
    artist_location VARCHAR(20),
    artist_name VARCHAR(20),
    song_id VARCHAR(50),
    title VARCHAR(50),
    duration DOUBLE PRECISION
);
""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users
(
    user_id INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    gender VARCHAR(4),
    level VARCHAR(4) NOT NULL DEFAULT 'free',
    CONSTRAINT check_level CHECK (level = 'free' OR level = 'paid')
);
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs
(
    song_id VARCHAR(50) PRIMARY KEY NOT NULL,
    title VARCHAR(50),
    artist_id VARCHAR(50),
    year INT,
    duration DOUBLE PRECISION
);
""")

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists
(
    artist_id VARCHAR(50) PRIMARY KEY NOT NULL,
    name VARCHAR(20),
    location VARCHAR(),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);
""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time
(
    start_time TIMESTAMP PRIMARY KEY NOT NULL,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT
);
""")

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id IDENTITY(0,1) PRIMARY KEY NOT NULL,
    start_time TIMESTAMP NOT NULL,
    user_id INT NOT NULL,
    level VARCHAR(4) NOT NULL,
    song_id VARCHAR(50),
    artist_id VARCHAR(50),
    session_id INT,
    location VARCHAR(20),
    user_agent VARCHAR(50),
    FOREIGN KEY(song_id) REFERENCES songs(song_id),
    FOREIGN KEY(artist_id) REFERENCES artists(artist_id)
);
""")

# STAGING TABLES

staging_events_copy = (""" COPY staging_events
                           FROM {}
                           IAM_ROLE {}
                           REGION 'us-east-1';
                           """).format(config['S3']['LOG_DATA'], *config['IAM_ROLE'].values())

staging_songs_copy = (""" COPY staging_songs
                          FROM {}
                          IAM_ROLE {}
                          REGION 'us-east-1';
                          """).format(config['S3']['SONG_DATA'], *config['IAM_ROLE'].values())

# FINAL TABLES

user_table_insert = (""" INSERT INTO users (user_id, first_name, last_name, gender, level) \
    VALUES (SELECT userId, firstName, lastName, gender, level
            FROM staging_events
            WHERE page = 'NextSong';) 
            ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = (""" INSERT INTO songs (song_id, artist_id, title, duration, year) \
    VALUES (SELECT song_id, artist_id, title, duration, year
            FROM staging_songs;) ON CONFLICT DO NOTHING;
""")

artist_table_insert = (""" INSERT INTO artists (artist_id, latitude, longitude, location, name) \
    VALUES (SELECT artist_id, artist_latitude, artist_longitude, artist_location, artist_name
            FROM staging_songs;) ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = (""" INSERT INTO time (start_time, hour, day, week, month, year, weekday) \
    VALUES (SELECT TO_TIMESTAMP(ls), DATE_PART(hour, TO_TIMESTAMP(ls)), DATE_PART(day, TO_TIMESTAMP(ls)), DATE_PART(week, TO_TIMESTAMP(ls)), DATE_PART(month, TO_TIMESTAMP(ls)), DATE_PART(year, TO_TIMESTAMP(ls)), DATE_PART(weekday, TO_TIMESTAMP(ls))
            FROM staging_events
            WHERE page = 'NextSong';) ON CONFLICT (start_time)
    DO UPDATE SET start_time = EXCLUDED.start_time;
""")

songplay_table_insert = (""" INSERT INTO songplays
(
    start_time,
    user_id,
    level,
    session_id,
    location,
    user_agent,
    song_id,
    artist_id) \
    VALUES (SELECT TO_TIMESTAMP(ls), userId, level, sessionId, location, userAgent
            FROM staging_events
            WHERE page = 'NextSong';) \
    ON CONFLICT DO NOTHING;
""")

# QUERY LISTS

create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create, user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
    songplay_table_create]

drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop]

copy_table_queries = [
    staging_events_copy,
    staging_songs_copy]

insert_table_queries = [
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
    songplay_table_insert]
