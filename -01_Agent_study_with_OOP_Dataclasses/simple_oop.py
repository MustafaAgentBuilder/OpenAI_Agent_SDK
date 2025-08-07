# My Personal Opinion:
# Dataclasses are better than normal OOP (Object-Oriented Programming). 
# Nowadays, the market and developer communities prefer using dataclasses. A big change is that OpenAI is also using dataclasses to create its SDK.
# No need for 'dataclasses' or 'typing' imports in normal OOP for this example.
# In @dataclass, we needed 'from dataclasses import dataclass' and sometimes 'from typing import ClassVar, List'.

# Example 1: MyDataclass
class MyDataclass:
    """
    A simple class with:
    - A class (static) variable: shared by all objects.
    - An instance variable: unique for each object.
    """
    # Class variable: Belongs to the class itself, shared by all instances.
    # Difference: In @dataclass, this was written as 'class_variable: ClassVar[int] = 42'.
    # In normal OOP, we just define it directly without 'ClassVar'.
    class_variable = 42

    # Constructor: This sets up instance variables when you create an object.
    # Difference: In @dataclass, this '__init__' method is automatically made for you based on
    # the instance variables you list (e.g., 'instance_variable: int').
    # In normal OOP, you have to write it yourself.
    def __init__(self, instance_variable: int):
        self.instance_variable = instance_variable  # Unique for each object

    # Instance Method: Uses 'self' to access the object's data.
    # Difference: This stays the same in both @dataclass and normal OOP.
    def age(self):
        return self.instance_variable

    # Class Method: Uses 'cls' to work with the class itself.
    # Difference: No change here; @classmethod works the same in both.
    @classmethod
    def class_age(cls):
        return cls.class_variable

    # Static Method: Doesn’t use 'self' or 'cls'; just a function inside the class.
    # Difference: No change; @staticmethod is the same in both.
    @staticmethod
    def static_age():
        return MyDataclass.class_variable

    # Another Static Method: Adds two numbers.
    @staticmethod
    def sum_num(a, b):
        return a + b

# Example 2: Book
class Book:
    """
    A Book class that:
    - Has instance variables for title, author, and year.
    - Uses a class variable to store all books in a library.
    """
    # Class variable: A list to store all Book objects.
    # Difference: In @dataclass, this was 'library: ClassVar[List["Book"]] = []'.
    # In normal OOP, we define it directly without 'ClassVar'.
    library = []

    # Constructor: Initializes instance variables and adds the book to the library.
    # Difference: In @dataclass, '__init__' is auto-generated, and extra setup (like adding to library)
    # goes in a special '__post_init__' method. In normal OOP, we put all setup in '__init__'.
    def __init__(self, title: str, author: str, year: int = 2020):
        self.title = title    # Instance variable
        self.author = author  # Instance variable
        self.year = year      # Instance variable with a default value
        # This line mimics what '__post_init__' did in @dataclass.
        Book.library.append(self)

    # Instance Method: Describes the book.
    # Difference: No change; instance methods work the same way.
    def description(self):
        return f"'{self.title}' by {self.author} ({self.year})"

    # Class Method: Returns the total number of books.
    # Difference: No change; @classmethod is the same.
    @classmethod
    def total_books(cls):
        return len(cls.library)

    # Static Method: Checks if a book is a classic.
    # Difference: No change; @staticmethod is the same.
    @staticmethod
    def is_classic(year):
        return year < 1970

# Example 3: Rectangle
class Rectangle:
    """
    A Rectangle class that demonstrates:
    - Instance variables: length and width.
    - A class variable for the unit of measurement.
    """
    # Class variable: Unit of measurement for all rectangles.
    # Difference: In @dataclass, this was 'unit: ClassVar[str] = "cm"'.
    # In normal OOP, we define it directly.
    unit = "cm"

    # Constructor: Sets up instance variables.
    # Difference: In @dataclass, '__init__' is auto-made. Here, we write it manually.
    def __init__(self, length: float, width: float):
        self.length = length  # Instance variable
        self.width = width    # Instance variable

    # Instance Method: Calculates the area.
    # Difference: No change here.
    def area(self):
        return self.length * self.width

    # Class Method: Changes the unit for all rectangles.
    # Difference: No change; @classmethod is the same.
    @classmethod
    def change_unit(cls, new_unit: str):
        cls.unit = new_unit

    # Static Method: Calculates perimeter without needing an object.
    # Difference: No change; @staticmethod is the same.
    @staticmethod
    def perimeter(length: float, width: float):
        return 2 * (length + width)

# Example 4: Person
class Person:
    """
    A Person class that demonstrates:
    - Instance variables for name and age.
    - Methods to greet, give general info, and calculate birth year.
    """
    # Class variable: Default country for all Person objects.
    # Difference: In @dataclass, this was 'default_country: ClassVar[str] = "Unknown"'.
    # In normal OOP, we define it directly.
    default_country = "Unknown"

    # Constructor: Initializes instance variables.
    # Difference: In @dataclass, '__init__' is auto-generated. Here, we write it.
    def __init__(self, name: str, age: int):
        self.name = name  # Instance variable
        self.age = age    # Instance variable

    # Instance Method: Returns a greeting.
    # Difference: No change here.
    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

    # Class Method: Gives a general message.
    # Difference: No change; @classmethod is the same.
    @classmethod
    def general_info(cls):
        return f"All persons are from {cls.default_country} by default."

    # Static Method: Calculates birth year.
    # Difference: No change; @staticmethod is the same.
    @staticmethod
    def calculate_birth_year(age, current_year):
        return current_year - age

# Let's test the code to make sure it works!
# Create some objects and call methods.
if __name__ == "__main__":
    # Test MyDataclass
    obj = MyDataclass(25)
    print(f"Instance age: {obj.age()}")              # Output: 25
    print(f"Class age: {MyDataclass.class_age()}")   # Output: 42
    print(f"Static age: {MyDataclass.static_age()}") # Output: 42
    print(f"Sum: {MyDataclass.sum_num(3, 4)}")      # Output: 7

    # Test Book
    book1 = Book("Python 101", "John Doe")
    book2 = Book("OOP Basics", "Jane Smith", 2019)
    print(book1.description())          # Output: 'Python 101' by John Doe (2020)
    print(Book.total_books())           # Output: 2
    print(Book.is_classic(book2.year))  # Output: False

    # Test Rectangle
    rect = Rectangle(5.0, 3.0)
    print(f"Area: {rect.area()} {Rectangle.unit}")      # Output: Area: 15.0 cm
    Rectangle.change_unit("m")
    print(f"New unit: {Rectangle.unit}")                # Output: New unit: m
    print(f"Perimeter: {Rectangle.perimeter(5.0, 3.0)}")# Output: Perimeter: 16.0

    # Test Person
    person = Person("Alice", 30)
    print(person.greet())                              # Output: Hello, my name is Alice and I am 30 years old.
    print(Person.general_info())                       # Output: All persons are from Unknown by default.
    print(f"Birth year: {Person.calculate_birth_year(30, 2023)}")  # Output: Birth year: 1993