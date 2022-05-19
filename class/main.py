# f = open('file.txt','r')
# file = f.readlines()
# newList = []
# for line in file :
#     if line[-1] == '\n' :
#         newList.append(line[:-1])
#     else :
#         newList.append(line)
# print(newList)

# file = open('write.txt','w')
#
# file.write('python')
#
# file.close()

class Dog(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def speak(self):
        print("My name is",self.name,"I am ",self.age)
    def add_weight(self,weight):
        self.weight = weight

loc = Dog('loc',15)
loc.speak()

class Cat(object) :
    def __init__(self,name,age,color):
        super().__init__(name,age)
        self.color = color

class Vehicle() :
    def __init__(self,price,gas,color):
        self.price = price
        self.gas = gas
        self.color = color
    def fillUpTank(self):
        self.gas = 100
    def emptyGas(self):
        self.gas = 0
    def gasLeft(self):
        self.gas = gas

class Car(Vehicle):
    def __init__(self,price,gas,color,speed):
        super().__init__(price,gas,color)
        self.speed = speed
    def beep(self):
        print("Beep beep beep")

class Truck(Car):
    def __init__(self,price,gas,color,tires):
        super().__init__(price,gas,color)
        self.tires = tires
    def beep(self):
        print("Honk Honk")

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.coords = (self.x,self.y)
    def move(self,x,y):
        self.x += x
        self.y += y
    def lenght(self):
        import math
        return math.sqrt(self.x**2 + self.y**2)
    def __gt__(self, p):
        return self.lenght() > p.lenght()
    def __ge__(self, p):
        return self.lenght() >= p.lenght()
    def __lt__(self, p):
        return self.lenght() < p.lenght()
    def __le__(self,p):
        return self.lenght() <= p.lenght()
    def __eq__(self, p):
        return self.x == p.x and self.y == p.y


    def __add__(self, p):
        return Point(self.x + p.x,self.y + p.y)
    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)
    def __mul__(self, p):
        return self.x*p.x + self.y*p.y
    def __str__(self):
        return "(" + str(self.x)  + "," + str(self.y) + ")"
# p1 = Point(1,3)
# p2 = Point(2,4)
# p3 = Point(3,6)
# p4 = Point(4,9)
#
# print(p1==p2,p2>p1,p1<=p2)

#OOP

class Student():
    def __init__(self,name,age,grade):
        self.name = name
        self.age = age
        self.grade = grade
    def get_grade(self):
        return self.grade

class Course():
    def __init__(self,name,max_student):
        self.name = name
        self.max_student = max_student
        self.students = []
    def add_student(self,student):
        if len(self.students) < self.max_student :
            self.students.append(student)
            return True
        return False
    def get_avarage_grade(self):
        value = 0
        for student in self.students :
            value += student.get_grade()
        return value/len(self.students)

S1 = Student('Loc','22',90)
S2 = Student('Panh','25',10)
course = Course("Math",30)
course.add_student(S1)
course.add_student(S2)
print(course.students[0].name)
print(course.get_avarage_grade())


class Person():
    population = 50
    def __init__(self,name,age):
        self.name = name
        self.age = age
    @classmethod
    def getPopulation(cls):
        return cls.population
    @staticmethod
    def isAdult(age):
        return age >= 18

# Map function

li = [1,2,3,4,5,6,7,8,9,10]
def func(x) :
    return x**x

newList = []
for x in li :
    newList.append(func(x))

# print(newList)
# print(list(map(func,li)))
# print([func(x) for x in li if x%2==0 ])

#filter function

def addOne(x) :
    return x + 1
def isOdd(x):
    return x%2 != 0

li = [1,2,3,4,5,6,7,8,9,10]
b = list(filter(isOdd,li))
# print(b)

c = list(map(addOne,filter(isOdd,li)))
# print(c)

# Lambda function

def add(x):
    func1 = lambda x : x + 1
    return func1(x) + 1
func3 = lambda x,y = 4 : x +y
print(add(2))
print(func3(2))

li = [1,2,3,4,5,6,7,8,9,10]

d = list(map(lambda x: x + 1,li))
e = list(filter(lambda x: x%2 ==0,li))
print(d)
print(e)

# Collections

import collections
from collections import Counter

# Counter

c = Counter('gallad')
# print(c)
c = Counter(['a','a','b','c','c'])
# print(c)
e = Counter({'a':1,'b':2})
# print(e)
d = Counter(cats = 4,dogs = 2)

# print(d)
# print(c.most_common(2))
c.subtract(e)
# print(c)
c.update(e)
# print(c)

# Collections/ nametuples

import collections
from collections import namedtuple

Point = namedtuple('Point', 'x y z')
newP = Point(3,4,5)
# print(newP)
# print(newP._asdict())
# print(newP._fields)
newP = newP._replace(y = 6)
# print(newP)
newP = newP._make(['a','b','c'])
# print(newP)

# Collections/ Deque

import collections
from collections import deque

d = deque('hello',maxlen = 5)
d.append(1)
d.pop()
d.popleft()
d.clear()
d.extend([2,3,4])
d.extendleft([1,2,3])
d.rotate(-1)

a = [1,2,3,4]

print(a[:-1])