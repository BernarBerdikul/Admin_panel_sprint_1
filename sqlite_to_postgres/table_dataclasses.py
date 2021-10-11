from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAtField:
    id: str
    created_at: str


@dataclass(frozen=True)
class UpdateAtField(CreateAtField):
    updated_at: str


@dataclass(frozen=True)
class Genre(UpdateAtField):
    name: str
    description: str


@dataclass(frozen=True)
class FilmWork(UpdateAtField):
    title: str
    type: str
    creation_date: str
    rating: str
    file_path: str
    description: str
    certificate: str


@dataclass(frozen=True)
class Person(UpdateAtField):
    full_name: str
    birth_date: str


@dataclass(frozen=True)
class GenreFilmWork(CreateAtField):
    film_work_id: str
    genre_id: str


@dataclass(frozen=True)
class PersonFilmWork(CreateAtField):
    film_work_id: str
    person_id: str
    role: str
