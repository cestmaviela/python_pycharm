#继承的语法
#在python中，任何类都有一个共同的父类叫做object
class Persion():
    name = "Noname"
    age = 0
    __score = 0#小名，私有类，只有自己知道
    _petname = "sec"#小名，保护类，可以被子类使用，但不能公用
    def sleep(self):
        print("sleepping......")
    def work(self):
        print("make some money")

#父类写在括号里
class Tearcher(Persion):
    tearcher_id = "9527"
    name = "mingming"
    def make_test(self):
        print("attention")
    def work(self):
        #扩充父类的功能只需要调用父类的函数
        super(Tearcher, self).work()
        self.make_test()

t = Tearcher()
#子类可以继承父类的属性
print(t.name)
print(t._petname)
print(t.age)
print(t.tearcher_id)
print(Tearcher.name)
print("*"*20)
t.work()
