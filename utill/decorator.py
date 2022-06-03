import datetime
import json
'''
class OptionYearDeco:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        context = self.func(*args, **kwargs)
        year = []  # 년도 selector 옵션값 배열
        now_year = int(str(datetime.datetime.now())[:4])  
        for i in range(10):
            if i <6:
                year.append(now_year - i)
            else:
                year.append(now_year + i-5)
        context['option_year'] = sorted(year)
        return context
'''
########

def option_year_deco(func):

    def func_wrapper(*args, **kwargs):
        context = func(*args, **kwargs)

        year = []  # 년도 selector 옵션값 배열
        now_year = int(str(datetime.datetime.now())[:4])  
        for i in range(10):
            if i <6:
                year.append(now_year - i)
            else:
                year.append(now_year + i-5)
        context['option_year'] = sorted(year)
        print("returnnnnnnnnnnnnnnnn",context)
        return context
    return func_wrapper


'''
def p_decorate(func):
   def func_wrapper(*args, **kwargs):
       print(args, kwargs)
       return "<p>{0}</p>".format(func(*args, **kwargs))
   return func_wrapper

class Person(object):
    def __init__(self):
        self.name = "John"
        self.family = "Doe"

    @p_decorate
    def get_class(self):
        return self.name+" "+self.family

my_person = Person()

#print (my_person.get_class())



class exceptionDec(object):
    def __init__(self, flag):
        self.flag = flag
        
    def __call__(self, func):
        decorator_self = self
        
        def wrappee(*args, **kwargs):
            print("teatsaaa", **kwargs)
            try:
                return func(*args,**kwargs)
            except Exception as e:
                print(f'ERR {func.__name__}() : {str(e)}')
                return decorator_self.flag
        return wrappee

class some_class():
    def __init__(self):
        self.resJson = {}
    def setResponse(self, resJson):
        self.resJson = resJson
    @exceptionDec(False)
    def isSuccess(self):
        return self.resJson['code']==0
    @exceptionDec('It is default message')
    def getMessage(self):
        return self.resJson['message']
    @exceptionDec(-1)
    def getItemCnt(self):
        return len(self.resJson['items'])

some = some_class()
# 설정을 안하면, some.setResponse({'code':1, 'message':'smtp error', 'items':[]})
print(some.getMessage())




class TestDeco:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(*args)
        r = self.func(*args)
        r['year'] = 1234
        print(r)
        return r

@TestDeco
def test(a, b):
    context={}
    context['test'] = a
    return context

test(1, 2)
'''