# ===============================================================
# EXAMPLE 0: MyDataclass (Your Original Code with Beginner Comments)
# ===============================================================

from dataclasses import dataclass
from typing import ClassVar

@dataclass
class MyDataclass:
    """
    A simple dataclass with:
    - A class (static) variable: shared by all objects.
    - An instance variable: unique for each object.
    """
    # Class variable (static attribute) that belongs to the class.
    class_variable: ClassVar[int] = 42

    # Instance variable that is unique for every object.
    instance_variable: int 

    # Instance Method: Uses 'self' to work with the object.
    def age(self):
        # Returns the instance variable (age of the object).
        return self.instance_variable

    # Class Method: Uses 'cls' to work with the class itself.
    @classmethod
    def class_age(cls):
        # Returns the class variable.
        return cls.class_variable

    # Static Method: Does not use 'self' or 'cls'; acts like a normal function.
    @staticmethod
    def static_age():
        # Returns the class variable directly via the class name.
        return MyDataclass.class_variable

    # Another Static Method: Adds two numbers.
    @staticmethod
    def sum_num(a, b):
        return a + b

# Testing MyDataclass:
your_data = MyDataclass(18)
print("MyDataclass instance method 'age':", your_data.age())           # Output: 18
print("MyDataclass class method 'class_age':", MyDataclass.class_age())   # Output: 42
print("MyDataclass static method 'static_age':", MyDataclass.static_age())# Output: 42
print("MyDataclass static method 'sum_num':", MyDataclass.sum_num(10, 20)) # Output: 30

# ===============================================================
# EXAMPLE 1: Book Library Dataclass
# ===============================================================

from typing import List

@dataclass
class Book:
    """
    A Book dataclass that:
    - Has instance variables for title, author, and year.
    - Uses a class variable to store all books in a library.
    """
    # Class variable: A list that stores all Book instances.
    library: ClassVar[List['Book']] = []
    
    # Instance variables for each Book.
    title: str
    author: str
    year: int = 2020  # Default year if not provided

    def __post_init__(self):
        """
        __post_init__ is automatically called after __init__.
        Here, we add the new Book instance to the library.
        """
        Book.library.append(self)
    
    def description(self):
        """
        Instance method that returns a description of the book.
        """
        return f"'{self.title}' by {self.author} ({self.year})"
    
    @classmethod
    def total_books(cls):
        """
        Class method to return the total number of books in the library.
        """
        return len(cls.library)
    
    @staticmethod
    def is_classic(year):
        """
        Static method to check if a book is a classic.
        A book is considered a classic if it was published before 1970.
        """
        return year < 1970

# Creating Book instances:
book1 = Book("1984", "George Orwell", 1949)
book2 = Book("Python Programming", "John Doe", 2021)

# Using instance method:
print("\nBook Description:", book1.description())  # Output: '1984' by George Orwell (1949)
print("Book Description:", book2.description())      # Output: 'Python Programming' by John Doe (2021)

# Using class method:
print("Total books in library:", Book.total_books()) # Output: Total books in library: 2

# Using static method:
print("Is '1984' a classic?", Book.is_classic(book1.year))  # Output: True

# ===============================================================
# EXAMPLE 2: Rectangle Dataclass
# ===============================================================

@dataclass
class Rectangle:
    """
    A Rectangle dataclass that demonstrates:
    - Instance variables: length and width.
    - A class variable for the unit of measurement.
    """
    # Class variable for the unit of measurement, shared by all Rectangle instances.
    unit: ClassVar[str] = "cm"
    
    # Instance variables:
    length: float
    width: float
    
    def area(self):
        """
        Instance method to calculate the area of the rectangle.
        """
        return self.length * self.width
    
    @classmethod
    def change_unit(cls, new_unit: str):
        """
        Class method to change the measurement unit for all rectangles.
        """
        cls.unit = new_unit
    
    @staticmethod
    def perimeter(length: float, width: float):
        """
        Static method to calculate the perimeter of a rectangle.
        Does not depend on any instance or class data.
        """
        return 2 * (length + width)

# Creating a Rectangle instance:
rect = Rectangle(5, 3)
print("\nRectangle Area:", rect.area(), Rectangle.unit)  # Output: Area: 15 cm
print("Rectangle Perimeter (static):", Rectangle.perimeter(5, 3))  # Output: Perimeter: 16

# Changing the class variable (unit) using the class method:
Rectangle.change_unit("inches")
print("New unit for rectangle:", Rectangle.unit)  # Output: New unit: inches

# ===============================================================
# EXAMPLE 3: Person Dataclass
# ===============================================================

@dataclass
class Person:
    """
    A Person dataclass that demonstrates:
    - Instance variables for name and age.
    - An instance method to return a greeting.
    - A class method to return a general message.
    - A static method to calculate the birth year.
    """
    # Class variable: Default country for all Person objects.
    default_country: ClassVar[str] = "Unknown"
    
    # Instance variables:
    name: str
    age: int

    def greet(self):
        """
        Instance method that returns a greeting including the person's name and age.
        """
        return f"Hello, my name is {self.name} and I am {self.age} years old."

    @classmethod
    def general_info(cls):
        """
        Class method that returns a general information message using the class variable.
        """
        return f"All persons are from {cls.default_country} by default."

    @staticmethod
    def calculate_birth_year(age, current_year):
        """
        Static method that calculates the birth year given an age and the current year.
        """
        return current_year - age

# Creating Person instances:
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)

# Using instance method:
print("\nPerson Greeting:", person1.greet())  # Output: Hello, my name is Alice and I am 30 years old.
print("Person Greeting:", person2.greet())      # Output: Hello, my name is Bob and I am 25 years old.

# Using class method:
print("General Info:", Person.general_info())   # Output: All persons are from Unknown by default.

# Using static method to calculate birth year:
print("Alice's birth year:", Person.calculate_birth_year(person1.age, 2025))  # Output: 1995 (if current year is 2025)
print("Bob's birth year:", Person.calculate_birth_year(person2.age, 2025))    # Output: 2000 (if current year is 2025)
