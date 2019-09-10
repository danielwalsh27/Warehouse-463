from collections import OrderedDict

class Rectangle:
        name_ = ""
        length_ = 0
        width_ = 0
        size_ = 0

od = OrderedDict()
length_ = input("Enter Warehouse Length: ")
length = int(length_)
width_ = input("Enter Warehouse Width: ")
width = int(width_)
size = length * width
print("The Total size of the Warehouse is:", size)
print()
userSize = 1

while(True):
    tmp = Rectangle()
    print("Enter a new rectangular package into the warehouse")
    print("*** To exit input enter 0 for length and width***")
    print()
    
    tmp.name_ = input("Enter the Name of the object: ")
    length = input("Enter the Length: ")
    tmp.length_ = int(length)
    width = input("Enter the Width: ")
    tmp.width_ = int(width)
    tmp.size_ = tmp.length_ * tmp.width_
    if(tmp.size_ == 0):
        break
    
    print("The size of the package is:", tmp.size_)
    size = size - tmp.size_
    print("The remaining size of the warehouse is:", size)
    print()
    od[tmp.size_] = tmp

for key, value in sorted(od.items()): 
    print(key, value.name_, value.length_, value.width_, value.size_)
