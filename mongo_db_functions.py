import os, time

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import (
    PyMongoError,
    ConnectionFailure,
    ConfigurationError,
    CollectionInvalid,
    ExecutionTimeout,
    OperationFailure,
    ServerSelectionTimeoutError,
)
from typing import Dict, List, Optional, Union


class MongoCRUD:
    def __init__(
        self, host: str, port: int, database_name: str, collection_name: str
    ) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        try:
            self.collection = self.__connect_to_mongodb()[collection_name]
        except CollectionInvalid as err:
            print(f"Collection creation error: {err}")

    def __connect_to_mongodb(self) -> Union[Database, None]:
        try:
            client = MongoClient(self.host, self.port)
            database = client[self.database_name]
            return database
        except ConnectionFailure as err:
            print(f"Connection failure: {err}")
        except ConfigurationError as err:
            print(f"Configuration error: {err}")

    def find_documents(self, query: Dict) -> Union[List[Dict], None]:
        try:
            documents = self.collection.find(query, {"_id": 0})
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def insert_one_document(self, document: Dict) -> Optional[str]:
        try:
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def insert_many_documents(self, document: Dict) -> Union[str, None]:
        try:
            result = self.collection.insert_many(document)
            return str(result.inserted_ids)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def update_one_document(self, query: Dict, update: Dict) -> Union[int, None]:
        try:
            result = self.collection.update_one(query, {"$set": update})
            return result.modified_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def update_many_documents(self, query: Dict, update: Dict) -> Union[int, None]:
        try:
            result = self.collection.update_many(query, {"$set": update})
            return result.modified_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def delete_one_document(self, query: Dict) -> Union[int, None]:
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def delete_many_documents(self, query: Dict) -> Union[int, None]:
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$eq": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_greater_than(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$gt": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_greater_or_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$gte": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_specified_values(
        self, key: str, values_list: list, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$in": values_list}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_less_than(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$lt": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_less_or_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$lte": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_not_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$ne": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_all_instead_of(
        self, key: str, values_list: list, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$nin": values_list}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_between(
        self, key: str, min_value: int, max_value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$gte": min_value, "$lte": max_value}}
        try:
            documents = self.collection.find(query, parameters).limit(10)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")
