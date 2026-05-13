print("hello world")
price = 100
discount = 0.2
product = "Laptop"
product_price = price * (1 - discount)
print(product_price)
print(f"The price of the {product} after discount is: {product_price}")
print("The price of the {} after discount is: {}".format(product, product_price))
print("Total ", product_price, "for the", product)

print(price>50)
print(price<50)
print(price==100)   
print(price!=100)
print(type(price))
age_string = "25"
age = int(age_string)
print(type(age))
print(age)

name = "Alice Smith"
print(name.upper())
print(name.lower())
print(name.title())
print(name.replace("Smith", "Johnson"))
print(name.split())
print(len(name))
join_string = "-".join(name.split())
print(join_string)
print(name[0:5] + name[6:11])
print(name[0:5])
print(name[6:11])
print(name.startswith("Alice"))
print(name.endswith("Smith"))
print(name.find("Smith"))
print("Alice" in name)