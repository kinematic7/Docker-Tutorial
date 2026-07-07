import pandas as pd
from pymongo import MongoClient

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id

class EmployeeManager:
    def __init__(self):
        # 1. Connect to MongoDB inside your cluster using your Service name
        # Format: mongodb://<username>:<password>@<service-name>:<port>/
        connection_string = "mongodb://admin:late2dine@localhost:27017/"
        
        self.client = MongoClient(connection_string)
        self.db = self.client["company"]          # Database name
        self.collection = self.db["employees"]    # Collection name
        
        self.employees = pd.DataFrame(columns=["name", "age", "employee_id"])

    def fetch_from_db(self):
        # 2. Fetch the documents (excluding the MongoDB internal _id)
        mongo_docs = list(self.collection.find({}, {"_id": 0}))
        
        # 3. Load them straight into your Pandas DataFrame
        self.employees = pd.DataFrame(mongo_docs)

if __name__ == "__main__":
    manager = EmployeeManager()
    manager.fetch_from_db()
    print(manager.employees)