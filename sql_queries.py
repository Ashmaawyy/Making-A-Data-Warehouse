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
    artist varchar(20),
    auth varchar(20),
    firstName varchar(20),
    gender varchar(5),
    itemInSession int,
    lastName varchar(20),
    lengh double precision,
    level varchar(4),
    location varchar(20),
    method varchar(3),
    page varchar(8),
    regestration double precision,
    sessionId int,
    song varchar(50),
    status int,
    ts bigint,
    userAgent varchar(50),
    userId int
);
""")

staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS staging_songs
(
    num_songs int,
    artist_id varchar(),
    artist_latitude double precision,
    artist_longitude double precision,
    artist_location varchar(),
    artist_name varchar(),
    song_id varchar(),
    title varchar(),
    duration double precision
);
""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users
(
    user_id int PRIMARY KEY NOT NULL,
    first_name varchar,
    last_name varchar,
    gender varchar,
    level varchar NOT NULL DEFAULT 'free',
    CONSTRAINT check_level CHECK (level = 'free' OR level = 'paid')
);
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs
(
    song_id varchar PRIMARY KEY NOT NULL,
    title varchar(),
    artist_id varchar(),
    year int,
    duration double precision
);
""")

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists
(
    artist_id varchar PRIMARY KEY NOT NULL,
    name varchar(),
    location varchar(),
    latitude double precision,
    longitude double precision
);
""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time
(
    start_time timestamp PRIMARY KEY NOT NULL,
    hour int,
    day int,
    week int,
    month int,
    year int,
    weekday int
);
""")

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id IDENTITY(0,1) PRIMARY KEY NOT NULL,
    start_time timestamp NOT NULL,
    user_id int NOT NULL,
    level varchar NOT NULL,
    song_id varchar(),
    artist_id varchar(),
    session_id int,
    location varchar(),
    user_agent varchar(),
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

songplay_table_insert = (""" INSERT INTO songplays (start_time,
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
