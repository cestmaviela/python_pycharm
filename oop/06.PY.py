#构造函数的调用顺序
class A():
    def __init__(self,name):
        print(name)

class B(A):
    name ="haha"
    def __init__(self,name):
        print(name)

class C(B):
    pass

c = C("b")

print(C.__mro__)
print(c.__dict__)

print(issubclass(B,A))
print(issubclass(C,A))
print(issubclass(A,C))

print(getattr(B,"name"))
print(setattr(B,"name","100")