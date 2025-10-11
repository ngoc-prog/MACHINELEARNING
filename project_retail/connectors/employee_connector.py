from project_retail.connectors.connector import Connector
from project_retail.models.employee import Employee


class EmployeeConnector(Connector):
    def login(self,uid,pwd):
        sql = "SELECT * FROM employee " \
              "where Email=%s and Password=%s"
        val = (uid, pwd)
        dataset=self.fetchone(sql,val)
        emp = None
        if dataset != None:
            emp = Employee(dataset[0], dataset[1], dataset[2], dataset[3],
                           dataset[4], dataset[5])
        return emp