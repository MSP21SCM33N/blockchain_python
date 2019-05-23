
def print_func(name, age):
    print(name + " " + age)


def decades_lived(age):
    print("Decades lived: %d " %(int(age)// 10))

name = input("Please enter your name: ")
age = input("Please enter your age: ")


print_func(name, age)
decades_lived(age)
