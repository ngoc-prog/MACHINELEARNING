from project_retail.connectors.employee_connector import EmployeeConnector

# Tạo kết nối với cơ sở dữ liệu
ec = EmployeeConnector()
ec.connect()

# Thử đăng nhập
em = ec.login("bin@gmail.com", 456)
if em is None:
    print("Login failed")
else:
    print(em)

# Hiển thị tất cả nhân viên
print("Test - All employees:")
employees = ec.get_list_employee()
for emp in employees:
    print(emp)

    # Kiểm tra nhân viên có ID=4
    print("-----------ID=4-----------")
    id = 4
    emp = ec.get_detail(id)
    if emp is not None:
        print("FOUND ID=", id)
        print(emp)
    else:
        print("NOT FOUND ID=", id)
