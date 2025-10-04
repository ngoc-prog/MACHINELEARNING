from Review.Product import Product
from Review.products import ListProduct

lp=ListProduct()
lp.add_products(Product(100,"Product 1",200,10))
lp.add_products(Product(14,"Product 2",20,100))
lp.add_products(Product(150,"Product 3",10,40))
lp.add_products(Product(200,"Product 4",340,80))
lp.add_products(Product(400,"Product 5",220,200))
print("List of Products:")
lp.print_product()
lp.desc_sort_products()
print("List of Products after descending sort:")
lp.print_product()




