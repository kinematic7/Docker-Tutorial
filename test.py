from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()


# ----------------------------
# Your original logic
# ----------------------------
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
        self.employees = pd.DataFrame(columns=["name", "age", "employee_id"])

    def add_employee(self, employee):
        new_row = pd.DataFrame([{
            "name": employee.name,
            "age": employee.age,
            "employee_id": employee.employee_id
        }])

        self.employees = pd.concat([self.employees, new_row], ignore_index=True)

    def get_employee_by_id(self, employee_id):
        employee_data = self.employees.loc[
            self.employees["employee_id"] == employee_id
        ]

        if not employee_data.empty:
            return employee_data.iloc[0].to_dict()

        return None

    def get_all_employees(self):
        return self.employees.to_dict(orient="records")

    def group_employees_by_age(self):
        return {
            age: group.to_dict(orient="records")
            for age, group in self.employees.groupby("age")
        }

    def delete_employee_by_id(self, employee_id):
        self.employees = self.employees.loc[
            self.employees["employee_id"] != employee_id
        ]


manager = EmployeeManager()

# ----------------------------
# Request Models
# ----------------------------
class EmployeeRequest(BaseModel):
    name: str
    age: int
    employee_id: str


# ----------------------------
# API Endpoints
# ----------------------------

@app.post("/employees")
def add_employee(emp: EmployeeRequest):
    employee = Employee(emp.name, emp.age, emp.employee_id)
    manager.add_employee(employee)
    return {"message": "Employee added successfully"}


@app.get("/employees")
def get_all():
    return manager.get_all_employees()


@app.get("/employees/{emp_id}")
def get_by_id(emp_id: str):
    return manager.get_employee_by_id(emp_id)


@app.get("/employees/grouped/age")
def group_by_age():
    return manager.group_employees_by_age()


@app.delete("/employees/{emp_id}")
def delete(emp_id: str):
    manager.delete_employee_by_id(emp_id)
    return {"message": "Employee deleted"}