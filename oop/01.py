"""
定义一个学生类，用来形容学生
"""
#定义一个空的类
class Student():
    #定义一个空类，pass代表直接跳过
    #此处pass必须有
    pass
#定义一个对象
mingming = Student()

#在定义一个类，用来描述学习python的学生
class PythonStudent():
    name = None
    age = 18
    coure =  "Python"
    #需要注意：
    #1.def doHomework的缩进层级
    #2.系统默认有一个self参数
    def  doHomework(self):
        print("I am doing honework.")

        #推荐在函数末尾使用return 语句
        return None
#实例化一个叫做youyou的学生，是一个具体的人
youyou = PythonStudent()
print(youyou.name)
print(youyou.age)
#注意成员函数的调用没有传递进入参数
youyou.doHomework()