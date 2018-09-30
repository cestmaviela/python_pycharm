#构造函数例子

class Person():
    #对Persion类进行实例化的时候
    #姓名要确定
    #年龄要确定
    #地址要确定
    def __init__(self):
       self.name = "NoName"
       self.age = 18
       self.address ="home"
       print("In init func")

#实例化一个人
P = Person(e,c)
