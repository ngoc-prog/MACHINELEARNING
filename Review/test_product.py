from Review.Product import Product

p1=Product(100,name="Thuốc lào",quantity=4,price=200)
print(p1)
p2=Product(200,"Thuốc trị hôi nách",5,38)
p1=p2
print("Thông tin của p1=")
print(p1)
p1.name="Thuốc tăng tự trọng"
print("Thông tin của p2=")
print(p2)