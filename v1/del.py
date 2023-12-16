class MyClass:
    def __init__(self):
        print("Object created")

    def some_method(self):
        print("Executing some method")

try:
    my_object = MyClass()

    # Your main code here
    my_object.some_method()

    a="a"+325252
except KeyboardInterrupt:
    print("Program interrupted by user")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # This block will be executed no matter what
    # Delete the class object here
    if 'my_object' in locals():
        del my_object
        print("Object deleted")
