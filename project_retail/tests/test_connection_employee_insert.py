from project_retail.connectors.employee_connector import EmployeeConnector
from project_retail.models.employee import Employee

ec=EmployeeConnector()
ec.connect()

emp=Employee()
emp.Name="Trần Thị Tám"
emp.Email="tamtam@gmail.com"
emp.Phone="09888888"
emp.Password="789"
emp.IsDeleted=0
result=ec.insert_employee(emp)
if result>0:
    print("insert Ok Ok Ok")
else:
    print("insert FAILED")