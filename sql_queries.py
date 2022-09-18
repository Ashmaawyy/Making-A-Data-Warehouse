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
()
""")

staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS staging_songs
()
""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users
(user_id int PRIMARY KEY NOT NULL,
first_name varchar,
last_name varchar,
gender varchar,
level varchar NOT NULL DEFAULT 'free',
CONSTRAINT check_level CHECK (level = 'free' OR level = 'paid'));
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs
(song_id varchar PRIMARY KEY NOT NULL,
title varchar,
artist_id varchar,
year int,
duration decimal);
""")

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists
(artist_id varchar PRIMARY KEY NOT NULL,
name varchar,
location varchar,
latitude decimal,
longitude decimal);
""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time
(start_time timestamp PRIMARY KEY NOT NULL,
hour int,
day int,
week int,
month int,
year int,
weekday int);
""")

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays
(songplay_id SERIAL PRIMARY KEY NOT NULL,
start_time timestamp NOT NULL,
user_id int NOT NULL,
level varchar NOT NULL,
song_id varchar,
artist_id varchar,
session_id int,
location varchar,
user_agent varchar,
FOREIGN KEY(song_id) REFERENCES songs(song_id),
FOREIGN KEY(artist_id) REFERENCES artists(artist_id));
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
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id)
    DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = (""" INSERT INTO songs (artist_id, song_id, title, duration, year) \
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
""")

artist_table_insert = (""" INSERT INTO artists (artist_id, latitude, longitude, location, name) \
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = (""" INSERT INTO time (start_time, hour, day, week, month, year, weekday) \
    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time)
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
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
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
