import threading

s = 0

def add():
    global s
    for i in range(101):
        s += i
        print('add,s=%d '%s)
            
def subs():
    global s
    for i in range(50, 101):
        s -= i
        print('subs,s=%d '%s)
            
# add()

t = threading.Thread(target=add)
t.start()

t = threading.Thread(target=subs)
t.start()
print(s)

#threading.