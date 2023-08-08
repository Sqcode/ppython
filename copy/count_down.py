## import library
from tkinter import *
import time
from datetime import datetime,timedelta

##########fun to start countdown########
def countdown():
 #now = datetime.now()
 #end = datetime((year_set).get(),(month_set).get(),(day_set).get(),(hour_set).get(),(min_set).get(),(sec_set).get(),00);
 global seconds_now
 now = time.time()
 lt_ = time.strptime(f'{(year_set).get()} {(month_set).get()} {(day_set).get()} {(hour_set).get()} {(min_set).get()} {(sec_set).get()}', '%Y %m %d %H %M %S')
 end = time.mktime(lt_)
 times=int (end-now)
  #.total_seconds());
 while times > -1:
  minute,second = (times // 60 , times % 60)
  
  hour = 0
  if minute > 60:
   hour , minute = (minute // 60 , minute % 60)
  
  day=0
  if hour>24:
    day,hour=(hour//24,hour%24) 
   
  sec.set(second)
  mins.set(minute)
  hrs.set(hour)
  days.set(day)
  root.update()
  time.sleep(1)
 
  times -= 1
  
################GUI to display window ##########################
root = Tk()
root.geometry('450x300')
root.resizable(0,0)
root.config(bg ='blanched almond')
root.title('倒计时')
Label(root, text = '倒计时' , font = 'arial 20 bold', bg ='papaya whip').pack()
start = Button(root, text='START', bd ='5', command = countdown, bg = 'antique white', font = 'arial 10 bold').place(x=150, y=210)
 
############GUI to display current time#######################
Label(root, font ='arial 15 bold', text = ' 当前时间：', bg = 'papaya whip').place(x = 40 ,y = 70)
 
#######################GUI to set the future time ##########
Label(root, font ='arial 15 bold', text = ' 到达时间：', bg = 'papaya whip').place(x = 40 ,y = 110)
#set year
year_set = StringVar()
Entry(root, textvariable =year_set , width = 4, font = 'arial 12').place(x=175, y=115)
Label(root, font ='arial 15', text = '-', bg = 'papaya whip').place(x = 215 ,y = 110)
year_set.set('2021')
 
#set month
month_set= StringVar()
Entry(root, textvariable =month_set, width =2, font = 'arial 12').place(x=235, y=115)
Label(root, font ='arial 15', text ='-', bg = 'papaya whip').place(x = 260 ,y = 110)
month_set.set('10')
 
#set day
day_set= StringVar()
Entry(root, textvariable =day_set, width =2, font = 'arial 12').place(x=275, y=115)
day_set.set('01')
 
# set hour
hour_set= StringVar()
Entry(root, textvariable =hour_set, width =2, font = 'arial 12').place(x=305, y=115)
Label(root, font ='arial 15', text = ':', bg = 'papaya whip').place(x = 330 ,y = 110)
hour_set.set('00')
 
# set min
min_set= StringVar()
Entry(root, textvariable =min_set, width =2, font = 'arial 12').place(x=345, y=115)
Label(root, font ='arial 15', text = ':', bg = 'papaya whip').place(x = 370 ,y = 110)
min_set.set('00')
 
# set sec
sec_set= StringVar()
Entry(root, textvariable =sec_set, width =2, font = 'arial 12').place(x=385, y=115)
sec_set.set('00')
 
#######################GUI to display timer countdown ##########
Label(root, font ='arial 15 bold', text = ' 倒计时：', bg ='papaya whip').place(x = 40 ,y = 150)
#storing seconds
sec = StringVar()
Entry(root, textvariable = sec, width = 2, font = 'arial 12').place(x=325, y=155)
Label(root, font ='arial 15', text = '秒', bg = 'papaya whip').place(x = 350 ,y = 150)
sec.set('00')
 
#storing minutes
mins= StringVar()
Entry(root, textvariable = mins, width =2, font = 'arial 12').place(x=275, y=155)
Label(root, font ='arial 15', text = '分', bg = 'papaya whip').place(x = 300 ,y = 150)
mins.set('00')
 
# storing hours
hrs= StringVar()
Entry(root, textvariable = hrs, width =2, font = 'arial 12').place(x=225, y=155)
Label(root, font ='arial 15', text = '时', bg = 'papaya whip').place(x = 250 ,y = 150)
hrs.set('00')
 
# storing days
days= StringVar()
Entry(root, textvariable = days, width =2, font = 'arial 12').place(x=175, y=155)
Label(root, font ='arial 15', text = '天', bg = 'papaya whip').place(x = 200 ,y = 150)
days.set('00')
 
#########fun to display current time#############
def clock():
 clock_time = time.strftime('%Y-%m-%d %H:%M:%S %p')
 curr_time.config(text = clock_time)
 curr_time.after(1000, clock)
 
curr_time =Label(root, font ='arial 15 bold', text = '', fg = 'gray25' ,bg ='papaya whip')
curr_time.place(x = 175 , y = 70)
clock()

root.mainloop()