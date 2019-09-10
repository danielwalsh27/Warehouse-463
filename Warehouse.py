length_ = input("Enter the Length: ")
length = int(length_)
width_ = input("Enter the Width: ")
width = int(width_)
size = length * width
print("The Total size of the Warehouse is:", size)
print()
userSize = 1

while(userSize != 0):
    print("Enter a new rectangular package into the warehouse")
    print("*** To exit input enter 0 for length and width***")
    print()
    length_ = input("Enter the Length: ")
    userLength = int(length_)
    width_ = input("Enter the Width: ")
    userWidth = int(width_)
    userSize = userLength * userWidth
    print("The size of the package is:", userSize)
    size = size - userSize
    print("The remaining size of the warehouse is:", size)
    print()
