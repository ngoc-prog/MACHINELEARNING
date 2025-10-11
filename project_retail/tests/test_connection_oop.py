from project_retail.connectors.employee_connector import EmployeeConnector

ec=EmployeeConnector()
ec.connect()
em=ec.login("bin@gmail.com",456)
if em==None:
    print("Login failed")
else:
    print(em)