#构造函数的概念
class Animal():
    pass

class BuruAnimal(Animal):
    def __init__(self,name):
        print("I am init in BURU {0}".format(name))


class dog(BuruAnimal):
    #__init__就是构造函数
    #每次实例化的时候，第一个被自动调用
    #因为主要工作是进行初始化，所以的命
    def __init__(self):
        print("I am init in dog")

#实例化的时候，括号内的参数要和构造函数匹配
kaka = dog()

class Cat(BuruAnimal):
    pass

#此时应该自动调用构造函数，因为Cat没有定义构造函数，所以查找父类构造函数
#在BuruAnimal中查找到构造函数，则停止向上查找
#在这里出错了如何实现多个参数的输入??????
c = Cat("ruijie")