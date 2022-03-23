-- Создание базы и пользователя с назначенными правами доступа:
CREATE DATABASE movies;
CREATE USER movies WITH PASSWORD 'movies';
GRANT ALL PRIVILEGES ON DATABASE "movies" to movies;

-- Создание отдельной схемы для контента:
CREATE SCHEMA IF NOT EXISTS content;


CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Жанры кинопроизведений:
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Кинопроизведения:
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate VARCHAR(255),
    file_path VARCHAR(255),
    rating FLOAT,
    type VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);


-- Персона:
CREATE TABLE IF NOT EXISTS content.person (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    full_name VARCHAR(60) NOT NULL,
    birth_date DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Жанры к кинопроизведениям:
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX film_work_genre ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX film_work_person_role ON content.person_film_work (film_work_id, person_id, role);
