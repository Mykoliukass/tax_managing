# Write a data population script. The script/function should create a document,
# with necessary fields. Values should be auto generated (random number/numbers, int, float,
#  random words etcs.)
# and itteration=0 value how many documents we want to populate the DB.
# For the beggining lets agree that we want to create a database people, with collection
# employees . Fields: name,surname,age,years employed.

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict
from faker import Faker
from random import randint, uniform
from datetime import datetime


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    print(f"Printed result: {result}")
    return str(result.inserted_id)


def calculate_age(birthdate: str) -> int:
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year
    if today.month < birthdate.month or (
        today.month == birthdate.month and today.day < birthdate.day
    ):
        age -= 1

    return age


def generate_float_number() -> float:
    minimal_salary = 10000.00
    maximal_salary = 9990000.00
    salary = uniform(minimal_salary, maximal_salary)
    return round(salary, 2)


def create_a_person():
    fake = Faker()
    name = fake.first_name()
    surname = fake.last_name()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime(
        "%Y-%m-%d"
    )
    age = calculate_age(date_of_birth)
    salary = generate_float_number()
    return name, surname, date_of_birth, age, salary


if __name__ == "__main__":
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "taxes"
    collection_name = "people"

    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    collection = db[collection_name]
    for _ in range(500):
        name, surname, date_of_birth, age, salary = create_a_person()
        document = {
            "name": name,
            "surname": surname,
            "date_of_birth": date_of_birth,
            "age": age,
            "anual_salary_before_tax": salary,
        }

        inserted_id = insert_document(collection, document)
        print(f"Inserted document with ID: {inserted_id}")
        print(f"This person was inserted into the database: {document}")
