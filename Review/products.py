class ListProduct:
    def __init__(self):
        self.products=[]
    def add_products(self,p):
        self.products.append(p)
    def print_product(self):
        for p in self.products:
            print(p)
    def desc_sort_products(self):
        for i in range(0,len(self.products)):
            for j in range(i+1,len(self.products)):
                pi=self.products[i]
                pj=self.products[j]
                if pi.price < pj.price:
                    self.products[j]=pi
                    self.products[i]=pj

