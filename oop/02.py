#定义一个类，包含名字，年龄属性
class Student():
    name = "dana"
    age = 18

    def say(self):
        self.name = "aaa"
        self.age = 200
    def sayAgain(s):
        print("My name is {0}".format(__class__.name))
        print("My name is xx")
#实例化一个对象
youyou = Student()
youyou.__dict__
print(youyou.name)

print(Student.name)
print(Student.age)

print("*" * 20)
#id可以鉴别出一个变量是否和另外一个变量是同一个变量
print(id(Student.name))
print(id(Student.age))

print("*" * 20)

a = Student()
print(a.name)
print(a.age)
print(id(a.name))
print(id(a.age))


a.name ="mingming"
a.age = 7
print(a.__dict__)
print(a.name)
print(a.age)
print(id(a.name))
print(id(a.age))

print("*" * 40)
#Student.sayAgain()
#a.say()
a.say()
a.sayAgain()