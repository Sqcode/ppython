import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
class Shape:     # 图形基类(叮当猫各部件（形状）共有的属性)
    def __init__(self, qp, QRect, QColor=QColor("#07bbee")):     # 构造方法参数：形状，位置坐标，颜色, color="#07bbee"
        self.qp = qp                  #qpainter()的实例
        self.rect = QRect             # 坐标（x1, y1, x2, y2）
        self.color = QColor               #颜色
        self.qp.setPen(QPen(Qt.black, 3))  #边线
 
 
class Liner:     #直线类
    def __init__(self, qp, QRect):
        self.qp = qp
        self.rect = QRect
        self.width = 1
 
class Arc:    #弧线类
    def __init__(self, qp, QRect, startAngle, spanAngle):
        self.qp = qp
        self.rect = QRect
        self.startAngle = startAngle
        self.spanAngle = spanAngle
 
class eyeball(Shape):    #眼珠
    def draw(self):
        self.qp.setBrush(self.color)       #设置画刷
        self.qp.drawEllipse(self.rect)       #画圆形x,y,w,h  120, 25, 160, 160
 
class mouth(Arc):
    def draw(self):
        self.qp.drawArc(self.rect,self.startAngle,self.spanAngle)  #后面两个参数分别为 起始角与跨度角
 
class beard(Liner):    #中央竖线
    def draw(self):
        self.qp.drawLine(self.rect)
 
class Beards:         #胡须组合
    def __init__(self, qp, start_point):        # w,h 宽、高
        self.qp = qp                            # 
        self.start_point = start_point          #起始坐标
 
        self.bd0 = beard(self.qp, self.bd0_cacu())
        self.bd1 = beard(self.qp, self.bd1_cacu())
        self.bd2 = beard(self.qp, self.bd2_cacu())
        self.bd00 = beard(self.qp, self.bd00_cacu())
        self.bd11 = beard(self.qp, self.bd11_cacu())
        self.bd22 = beard(self.qp, self.bd22_cacu())
 
    def draw(self):                # 绘制
        self.bd1.draw()
        self.bd0.draw()
        self.bd2.draw()
        self.bd11.draw()
        self.bd00.draw()
        self.bd22.draw()
 
    def bd0_cacu(self):             # 计算胡须的坐标
        x1 = self.start_point[0] - 40
        y1 = self.start_point[1] - 5
        x2 = x1 - 58
        y2 = y1 - 20
        return QLineF(x1, y1, x2, y2)
 
    def bd1_cacu(self):             # 计算中间胡须的坐标
        x1 = self.start_point[0] - 40
        y1 = self.start_point[1] + 5
        x2 = x1 -65
        y2 = y1
        return QLineF(x1, y1, x2, y2)
 
    def bd2_cacu(self):             # 计算胡须的坐标
        x1 = self.start_point[0] - 40
        y1 = self.start_point[1] + 15
        x2 = x1 -58
        y2 = y1 + 20
        return QLineF(x1, y1, x2, y2)
 
    def bd00_cacu(self):             # 计算胡须的坐标
        x1 = self.start_point[0] + 40
        y1 = self.start_point[1] - 5
        x2 = x1 + 58
        y2 = y1 - 20
        return QLineF(x1, y1, x2, y2)
 
    def bd11_cacu(self):             # 计算胡须的坐标
        x1 = self.start_point[0] + 40
        y1 = self.start_point[1] + 5
        x2 = x1 + 65
        y2 = y1
        return QLineF(x1, y1, x2, y2)
 
    def bd22_cacu(self):             # 计算胡须的坐标
        x1 = self.start_point[0] + 40
        y1 = self.start_point[1] + 15
        x2 = x1 + 58
        y2 = y1 + 20
        return QLineF(x1, y1, x2, y2)
 
class head(Shape):   # 头
    def draw(self):
        ##实例：x1，y1，x2，y2，即渐变的起始点和终止点
        linearGradient = QLinearGradient(420, 0, 100, 280) 
        #线性渐变色的效果，以整个图形区间为100%，
        #分成多段设置颜色，各颜色按百分比分配。
        linearGradient.setColorAt(0.1, Qt.white)   #10%处白色 
        linearGradient.setColorAt(0.2, self.color)   #60%处绿色 #07bbee
        linearGradient.setColorAt(0.8, self.color)   #60%处绿色 #07bbee
        linearGradient.setColorAt(1.0, Qt.black)       #100%处黑色
        self.qp.setBrush(linearGradient)       #设置画刷
        # self.qp.setBrush(self.color)
        # qp.drawRoundedRect(120, 25, 160, 160, 40, 40, Qt.RelativeSize)  #画圆角矩形x1,y1,x2,y2,圆角的角度
        self.qp.drawEllipse(self.rect)       #画圆形x,y,w,h  120, 25, 160, 160
 
class nose(Shape):    #鼻子
    def draw(self):
        RadialGradient = QRadialGradient(265, 144, 6, 265, 144)  #辐射渐变
        #参数分别为中心坐标，半径长度和焦点坐标,
        #如果需要对称那么中心坐标和焦点坐标要一致  #c93300
        #辐射渐变色的效果，以整个图形区间为100%，
        #分成多段设置颜色，各颜色按百分比分配。
        RadialGradient.setColorAt(0.0, Qt.white)   #10%处白色 
        RadialGradient.setColorAt(1.0, self.color)   #60%处绿色 #07bbee
        # RadialGradient.setColorAt(1.0, Qt.black)   #100%处黑色
        self.qp.setPen(QPen(Qt.black, 2))            #边线
        self.qp.setBrush(RadialGradient)       #设置画刷
        self.qp.drawRoundedRect(self.rect, 80, 80, Qt.RelativeSize)  #画圆角矩形x,y,w,h,圆角的角度
 
class face(Shape):
    def draw(self):
        self.qp.setPen(Qt.NoPen)           #无边线
        self.qp.setBrush(self.color)       #设置画刷
        self.qp.drawEllipse(self.rect)     #画圆形x,y,w,h  120, 25, 160, 160
 
class eye(Shape):    #眼框
    def draw(self):
        self.qp.setBrush(self.color)       #设置画刷
        self.qp.drawRoundedRect(self.rect, 90, 90, Qt.RelativeSize)  #画圆角矩形x1,y1,x2,y2,圆角的角度
 
class Heads:         # 头部整体（组合头、脸、眼、鼻、嘴、胡子）
    def __init__(self, qp, start_point,w, h):    # w,h是帽子的宽、高
        self.qp = qp                            # 
        self.start_point = start_point          #起始坐标
        self.w = w
        self.h = h
        self.hd = head(self.qp, self.hd_cacu(), QColor('#07bbee'))      # 例化头
        self.fc = face(self.qp, self.fc_cacu(), Qt.white)      #脸
        self.nos = nose(self.qp, self.nos_cacu(), QColor("#c93300"))    #鼻子
        self.eye0 = eye(self.qp, self.ey0_cacu(), Qt.white)    # 实例化眼0
        self.eye1 = eye(self.qp, self.ey1_cacu(), Qt.white)    #眼1
        self.bds = Beards(self.qp, (260, 185))         #胡须组合的起始位置
        self.bd = beard(self.qp, self.bd_cacu())       #中央竖线
        self.mt = mouth(self.qp, self.mt_cacu(), 230 * 16, 80 * 16)  #弧线的起始角度, 弧线角度（角度*16）
        self.mt2 = mouth(self.qp, self.mt2_cacu(), 230 * 16, 80 * 16)  #弧线的起始角度, 弧线角度（角度*16）
        self.eb0 = eyeball(self.qp, self.eb0_cacu(), Qt.black)   #眼珠0
        self.eb1 = eyeball(self.qp, self.eb1_cacu(), Qt.black)   #眼珠1
 
    def draw(self):                # 绘制
        self.hd.draw()             #调用头方法绘制
        self.fc.draw()             # 调用脸方法绘制
        self.nos.draw()              # 调用底部方法绘制
        self.eye0.draw()
        self.eye1.draw()
        self.bds.draw()
        self.bd.draw()            #调用头方法绘制
        self.mt.draw()
        self.mt2.draw()
        self.eb0.draw()            #眼珠
        self.eb1.draw() 
 
    def eb0_cacu(self):             # 计算眼珠的坐标
        x = self.start_point[0] + self.w / 2 - 25
        y = self.start_point[1] + 70
        w = 12  
        h = 12 
        return QRect(x, y, w, h)
 
    def eb1_cacu(self):             # 计算眼珠的坐标
        x = self.start_point[0] + self.w / 2 + 15
        y = self.start_point[1] + 70
        w = 12  
        h = 12   
        return QRect(x, y, w, h)
 
    def bd_cacu(self):             # 计算中央竖线的坐标
        x1 = self.start_point[0] + self.w / 2
        y1 = self.start_point[1] + 135
        x2 = x1
        y2 = y1 + 95
        return QLineF(x1, y1, x2, y2)
 
    def mt_cacu(self):             # 计算嘴的坐标
        x = self.start_point[0] + 50
        y = self.start_point[1] + 45
        w = 220  
        h = 186  
        return QRect(x, y, w, h)
 
    def mt2_cacu(self):             # 计算嘴的坐标
        x = self.start_point[0] + 60
        y = self.start_point[1] + 49
        w = 200  
        h = 185  
        return QRect(x, y, w, h)
 
    def nos_cacu(self):             # 计算鼻子的坐标
        # r = self.h / 3 / 2
        x = self.start_point[0] + self.w /2 -15
        y = self.start_point[1] + 105
        w = 30  
        h = 30  
        return QRect(x, y, w, h)
 
    def hd_cacu(self):             # 计算头的坐标
        x = self.start_point[0]
        y = self.start_point[1]
        w = self.w  
        h = self.h  
        return QRect(x, y, w, h)
 
    def fc_cacu(self):             # 计算脸的坐标
        x = self.start_point[0] + 35
        y = self.start_point[1] + 65
        w = self.w - 65 
        h = self.h - 100 
        return QRect(x, y, w, h)
 
    def ey1_cacu(self):              # 计算眼1的坐标(圆角矩形)
        x = self.start_point[0] + self.w / 2
        y = self.start_point[1] + 40
        w = 70  
        h = 80 
        return QRect(x, y, w, h)
 
    def ey0_cacu(self):              # 计算眼0的坐标(圆角矩形)
        x = self.start_point[0] + self.w / 2 - 70
        y = self.start_point[1] + 40
        w = 70  
        h = 80 
        return QRect(x, y, w, h)
 
class collar(Shape):    #项圈
    def draw(self):
        linearGradient = QLinearGradient(140, 280, 140, 310) 
        #参数分别为中心坐标，半径长度和焦点坐标,
        #如果需要对称那么中心坐标和焦点坐标要一致  #c93300
        #辐射渐变色的效果，以整个图形区间为100%，
        #分成多段设置颜色，各颜色按百分比分配。
        linearGradient.setColorAt(0.2, QColor("#c40"))     #10%处 
        linearGradient.setColorAt(1.0, QColor("#800400"))   #
        # linearGradient.setColorAt(1.0, Qt.black)   #100%处黑色
        self.qp.setPen(QPen(Qt.black, 2))            #边线
        self.qp.setBrush(linearGradient)       #设置画刷
        self.qpp = QPainterPath()              #路径
        self.qpp.moveTo(self.rect[0] + self.rect[2], self.rect[1] + 20)
        self.qpp.arcTo(self.rect[0] + self.rect[2] - 10, self.rect[1] , 20.0, 20.0, 270.0, 180.0)  #(70, 30, R*2, R*2, 0, 180);(70,30)是起始位置，R是半径,270是起始角度，180是要画的角度
        self.qpp.lineTo(self.rect[0], self.rect[1])
        self.qpp.arcTo(self.rect[0]-10, self.rect[1], 20.0, 20.0, 90.0, 180.0)
        self.qpp.closeSubpath()
        self.qp.drawPath(self.qpp)
 
class bell(Shape):    #铃铛
    def draw(self):
        #参数分别为中心坐标，半径长度和焦点坐标,
        #如果需要对称那么中心坐标和焦点坐标要一致  #c93300
        RadialGradient = QRadialGradient(270, 308, 40, 260, 300)  #辐射渐变
        #辐射渐变色的效果，以整个图形区间为100%，
        #分成多段设置颜色，各颜色按百分比分配。
        RadialGradient.setColorAt(0.0, QColor("#f9f12a"))   #10%处白色 
        RadialGradient.setColorAt(0.75, QColor("#e9e11a"))   #60%处绿色 #07bbee
        RadialGradient.setColorAt(1.0, QColor("#a9a100"))   #100%处黑色
        self.qp.setPen(QPen(Qt.black, 2))            #边线
        self.qp.setBrush(RadialGradient)       #设置画刷
        self.qp.drawRoundedRect(self.rect, 90, 90, Qt.RelativeSize)  #画圆角矩形x1,y1,x2,y2,圆角的角度
 
class body(Shape):    #身体
    def draw(self):
        self.qp.setPen(QPen(Qt.black, 2))           #边线
        self.qp.setBrush(self.color)       #设置画刷
        self.qpp = QPainterPath()     #路径
        self.qpp.moveTo(self.rect[0] + 228, self.rect[1] - 15)
        self.qpp.lineTo(self.rect[0] + 230 + 45, self.rect[1] + 25) 
        self.qpp.lineTo(self.rect[0] + 230 + 20, self.rect[1] + 60)
        self.qpp.lineTo(self.rect[0] + 230  - 2, self.rect[1] + 40)
        self.qpp.lineTo(self.rect[0] + 230  - 2, self.rect[1] + 170)
        self.qpp.arcTo(self.rect[0] + 105,self.rect[1] + 170-10, 20, 20, 0, 180)   #中间半圆
        self.qpp.lineTo(self.rect[0] -2, self.rect[1] + 170)
        self.qpp.lineTo(self.rect[0] - 2, self.rect[1] + 40)
        self.qpp.lineTo(self.rect[0] - 20, self.rect[1] + 60)
        self.qpp.lineTo(self.rect[0] - 40, self.rect[1] + 25)
        self.qpp.lineTo(self.rect[0] + 2, self.rect[1] - 14)
        self.qpp.closeSubpath()
        self.qp.drawPath(self.qpp)
 
 
class foot(Shape):    #脚
    def draw(self):
        linearGradient = QLinearGradient(140, 280, 140, 310) 
        linearGradient.setColorAt(0.2, QColor("#c40"))     #10%处 
        linearGradient.setColorAt(1.0, QColor("#800400"))   #
        # linearGradient.setColorAt(1.0, Qt.black)   #100%处黑色
        self.qp.setPen(QPen(Qt.black, 2))            #边线
        # self.qp.setBrush(linearGradient)       #设置画刷
        self.qpp = QPainterPath()              #路径
        self.qpp.moveTo(self.rect[0] + self.rect[2] - 40, self.rect[1] + self.rect[3] - 2)
        self.qpp.arcTo(self.rect[0] + self.rect[2] - 40, self.rect[1] - 2 , 30.0, 30.0, 270.0, 180.0)  #(70, 30, R*2, R*2, 0, 180);(70,30)是起始位置，R是半径,270是起始角度，180是要画的角度
        self.qpp.lineTo(self.rect[0], self.rect[1]-2)
        self.qpp.arcTo(self.rect[0]-15, self.rect[1] - 3, 60.0, 40.0, 90.0, 125.0)
        # self.qpp.arcTo(self.rect[0]-20, self.rect[1] + 26, 20.0, 20.0, 90.0, 30.0)
        self.qpp.closeSubpath()
        self.qp.drawPath(self.qpp)
 
class hand(Shape):    #手
    def draw(self):
        self.qp.setBrush(self.color)       #设置画刷
        self.qp.drawEllipse(self.rect)     #画圆形x,y,w,h  120, 25, 160, 160
 
class chest(Shape):    #白色肚兜
    def draw(self):
        self.color = Qt.white 
        self.qp.setPen(QPen(Qt.black, 2))           #边线
        self.qp.setBrush(self.color)       #设置画刷
        self.qpp = QPainterPath()     #路径
        self.qpp.moveTo(self.rect[0] + 30 , self.rect[1] + 20)
        self.qpp.arcTo(self.rect[0] , self.rect[1] , 170.0, 170.0, 130.0, 280.0)  #(70, 30, R*2, R*2, 0, 180);(70,30)是起始位置，R是半径,270是起始角度，180是要画的角度
        self.qpp.closeSubpath()
        self.qp.drawPath(self.qpp)
 
class half(Shape):    #口袋
    def draw(self):
        self.color = Qt.white
        self.qp.setPen(QPen(Qt.black, 2))           #边线
        self.qp.setBrush(self.color)       #设置画刷
        self.qpp = QPainterPath()     #路径
        self.qpp.moveTo(self.rect[0] , self.rect[1] + 10)
        self.qpp.arcTo(self.rect[0] , self.rect[1] - 55 , self.rect[2], self.rect[3], 180.0, 180.0)  #(70, 30, R*2, R*2, 0, 180);(70,30)是起始位置，R是半径,270是起始角度，180是要画的角度
        self.qpp.closeSubpath()
        self.qp.drawPath(self.qpp)
 
class bellc(Shape):    #铃铛中心
    def draw(self):
        self.qp.setBrush(self.color)       #设置画刷
        self.qp.drawEllipse(self.rect)       #画圆形x,y,w,h  120, 25, 160, 160
 
class bellv(Liner):    #铃铛竖线
    def draw(self):
        self.qp.drawLine(self.rect)
 
class bellh(Liner):    #横线
    # def __init__(self, qp, start_point, w, c=0):
    #     self.qp = qp                            # 
    #     self.start_point = start_point          #起始坐标
    #     self.w = w
    #     self.c = c
 
    def draw(self):
        self.qp.drawLine(self.rect)
 
 
class Bells:                      # 铃铛组合
    def __init__(self, qp, start_point, w, h):    # w,h是铃铛的宽、高
        self.qp = qp                            # 
        self.start_point = start_point          #起始坐标
        self.w = w
        self.h = h
        self.be = bell(self.qp, self.be_cacu(), QColor("#a9a100"))  #铃铛
        self.bec = bellc(self.qp, self.bec_cacu(),Qt.black)         #铃铛中心
        self.belv = bellv(self.qp, self.belv_cacu())      #铃铛竖线
        self.belh1 = bellh(self.qp, self.belh1_cacu()) 
        self.belh2 = bellh(self.qp, self.belh2_cacu()) 
 
    def draw(self):
        self.be.draw()
        self.bec.draw()
        self.belv.draw()
        self.belh1.draw()
        self.belh2.draw()
 
    def belh1_cacu(self):              # 计算铃铛横线的坐标
        x = self.start_point[0] + 2
        y = self.start_point[1] -3
        w = x + 36 
        h = y 
        return QLineF(x, y, w, h)
 
    def belh2_cacu(self):              # 计算铃铛横线的坐标
        x = self.start_point[0] 
        y = self.start_point[1] + 2
        w = x + 40
        h = y 
        return QLineF(x, y, w, h)
 
    def belv_cacu(self):              # 计算铃铛竖线的坐标
        x = self.start_point[0] + 20
        y = self.start_point[1] + 20
        w = x  
        h = y + 8
        return QLineF(x, y, w, h)
 
    def bec_cacu(self):              # 计算铃铛的坐标(圆角矩形)
        x = self.start_point[0] + self.w /2 - 5
        y = self.start_point[1] + 8
        w = 10  
        h = 10
        return QRect(x, y, w, h)
 
    def be_cacu(self):              # 计算铃铛的坐标(圆角矩形)
        x = self.start_point[0] + self.w /2 - 20
        y = self.start_point[1] - 12
        w = 40  
        h = 40
        return QRect(x, y, w, h)
 
class Bodys:                      # 身体组合
    def __init__(self, qp, start_point, w, h):    # w,h是帽子的宽、高
        self.qp = qp                            # 
        self.start_point = start_point          #起始坐标
        self.w = w
        self.h = h
        self.bod = body(self.qp, self.bod_cacu())        #实例化身体
        self.che = chest(self.qp, self.che_cacu())       #实例化白色肚兜
        self.ha = half(self.qp, self.ha_cacu())          #实例化口袋
        self.coll = collar(self.qp, self.col_cacu())     # 实例化项圈
        self.hnd0 = hand(self.qp, self.hnd0_cacu(), Qt.white)      #左手
        self.hnd1 = hand(self.qp, self.hnd1_cacu(), Qt.white)      #左手
        self.ft1 = foot(self.qp, self.ft1_cacu(), Qt.white)      #脚
        self.ft2 = foot(self.qp, self.ft2_cacu(), Qt.white)      #脚
        self.bels = Bells(self.qp, (240, 300), 40, 40)
 
    def draw(self):                # 绘制
        self.bod.draw()             #调用项圈方法绘制
        self.che.draw()
        self.ha.draw()
        self.coll.draw()
        self.hnd0.draw()
        self.hnd1.draw()
        self.ft1.draw()
        self.ft2.draw()
        self.bels.draw()
 
    def ft1_cacu(self):              # 计算脚的坐标
        x1 = self.start_point[0] 
        y1 = self.start_point[1] + 170
        x2 = 120  
        y2 = 30
        return (x1, y1, x2, y2)
 
    def ft2_cacu(self):              # 计算脚的坐标(圆角矩形)
        x1 = self.start_point[0] + 130
        y1 = self.start_point[1] + 170
        x2 = 120  
        y2 = 30
        return (x1, y1, x2, y2)
 
    def hnd0_cacu(self):              # 计算手的坐标(圆角矩形)
        x = self.start_point[0] - 78
        y = self.start_point[1] + 25
        w = 60  
        h = 60
        return QRect(x, y, w, h)
 
    def hnd1_cacu(self):              # 计算手的坐标(圆角矩形)
        x = self.start_point[0] + self.h + 20
        y = self.start_point[1] + 25
        w = 60  
        h = 60
        return QRect(x, y, w, h)
 
    def ha_cacu(self):              # 计算口袋的坐标(圆角矩形)
        x = self.start_point[0] + 48
        y = self.start_point[1] + 40
        w = 130  
        h = 130
        return (x, y, w, h)
 
    def che_cacu(self):              # 计算白色肚兜的坐标(圆角矩形)
        x = self.start_point[0] + 28
        y = self.start_point[1] - 30
        w = 170  
        h = 170
        return (x, y, w, h)
 
    def col_cacu(self):              # 计算项圈的坐标(圆角矩形)
        x1 = self.start_point[0] 
        y1 = self.start_point[1] - 20
        x2 = 230  
        y2 = 20
        return (x1, y1, x2, y2)
 
    def bod_cacu(self):              # 计算身体的坐标
        x = self.start_point[0] 
        y = self.start_point[1] 
        w = 230  
        h = 165 
        return (x, y, w, h)
 
class Example(QWidget):
    def __init__(self, w, h):
        super().__init__()
        self.qp = QPainter()     # 画笔实例
        self.rect = QRect()
        self.color = QColor()
        self.start_point = (100,30)   #头部的起始位置
        self.w = w
        self.h = h
        self.initUI()
        self.heads = Heads(self.qp,self.start_point, 320, 300)  # w,h
        self.bo = Bodys(self.qp, (145,300), 230, 230)  #start_point,w,h
 
    def initUI(self):
        self.setGeometry(100, 300, self.w, self.h)  # 窗口在屏幕上的坐标和大小：x,y,w,h
        self.setWindowTitle('叮当猫')
        self.show()
        # rect = QRect(120, 25, 160, 160)
        # self.hd = head(self.qp, self.rect, self.color)
 
    def paintEvent(self, e):
        self.qp.begin(self)
        self.drawBrushes(self.qp)  #调用方法
        self.qp.end()
 
    def drawBrushes(self, qp):
        self.heads.draw()
        self.bo.draw()
        # brush.setStyle(Qt.Dense1Pattern)   #设置style
        # qp.setBrush(brush)                 #设置画刷
        # self.qp.drawEllipse(self.rect, self.color)       #画矩形x,y,w,h
        
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example(520, 760)       #窗体大小
    sys.exit(app.exec_())