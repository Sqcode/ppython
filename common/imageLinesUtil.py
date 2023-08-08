
import numpy as np
import cv2
from PIL import Image
import requests, json
import os
import time
import point
from shapely.geometry import LineString

def req_trweb_ocr(filepath):
    """
    请求识图TrWebOcr，返回识图文字
    """
    url = "http://192.168.179.129:8089/api/tr-run/"
    header = {  # 模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    # data = json.dumps({'name': 'test', 'description':'some test repo'})
    files = {'file': open(path_new, 'rb')}
    r = requests.post(url, files=files, headers=header)
    res = r.json()
    print(res['data'])
    raw_out = res['data']['raw_out']
    # print(type (raw_out))
    # print(raw_out[0][1])
    return res

# im = cv2.imread(path)
# (b, g, r) = image[0, 0]  # 读取(0,0)像素，Python中图像像素是按B,G,R顺序存储的
# print("位置(0,0)处的像素 - 红:%d,绿:%d,蓝:%d" % (r, g, b))  # 显示像素值
# image[0, 0] = (100, 150, 200)  # 更改位置(0,0)处的像素
# (b, g, r) = image[0, 0]  # 再次读取(0,0)像素
# print("位置(0,0)处的像素 - 红:%d,绿:%d,蓝:%d" % (r, g, b))  # 显示更改后的像素值
#cv2.rectangle(im, (23, 56), (164, 82), (0, 0, 255), 1)

'''
    copy original , and tailor a rectangle
'''
# copy original , and tailor a rectangle
# tailor = np.copy(im)
# tailor = tailor[56:56+23, 23:164]
# cv2.imshow('imshow', tailor)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite(path_new, tailor)


# image = Image.open(path)
# box = (23, 219, 505, 90)
# #   从图片上抠下此区域
# region = image.crop(box)
# region = region.transpose(Image.ROTATE_180)
#   查看抠出来的区域
# region.show()
#   将此区域粘回去
# image.paste(region, box)
# image.show()
# print(im.shape[:2])

def image_roi(filepath):
    """
    对一张图，手动roi选择裁剪保存？裁剪识图，返回保存路径
    """
    im = cv2.imread(filepath)
    cv2.imshow('original', im)
    # 选择ROI
    roi = cv2.selectROI(windowName="original", img=im, showCrosshair=True, fromCenter=False)
    x, y, w, h = roi
    print(roi)
    milltime = int(round(time.time() * 1000000))
    # 显示ROI并保存图片
    if roi != (0, 0, 0, 0):
        crop = im[y: y + h, x: x + w]
        # cv2.imshow('crop', crop)
        # cv2.waitKey(0)
        path_new = os.path.abspath(os.path.dirname(filepath)) + '\\' + str(milltime) + '.jpg'
        cv2.imwrite(path_new, crop)
        print('Saved! --- {}'.format(path_new))
        return path_new

'''
    数组测试
'''
# X = np.array([[0 ,1] ,[2 ,3] ,[4 ,5] ,[6 ,7] ,[8 ,9] ,[10 ,11] ,[12 ,13] ,[14 ,15] ,[16 ,17] ,[18 ,19]])
# Y = np.array([[[
#     [0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 3.5005799e-32, 2.2478709e-35, 4.0228995e-36],
#          [1.6642591e-38, 4.6464102e-37, 0.0000000e+00, 2.5087256e-34, 3.6675054e-36, 6.9697912e-38],
#          [0.0000000e+00, 8.9281501e-37, 1.6572484e-35, 0.0000000e+00, 2.6912027e-34, 3.6106460e-36],
#          [5.3464511e-31, 1.5600492e-30, 4.1111328e-33, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00],
#          [3.2492299e-36, 1.0830886e-34, 7.0410645e-30, 0.0000000e+00, 4.3186701e-38, 0.0000000e+00],
#          [1.6074602e-37, 1.1517889e-36, 3.8564700e-34, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00]
#         ]]])
# print(Y[:, 0, :, :])

def lines(filepath):
    im = cv2.imread(filepath)
    # cv2.imshow('origin_img', im)
    h, w = im.shape[:2]
    # height = im.shape[0]  # 高度
    # width = im.shape[1]  # 宽度
    cut_img = im

    gray = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray_img', gray)
    # cv2.waitKey(0)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 118)
    result = cut_img.copy()
    minLineLength = 30  # height/32
    maxLineGap = 10  # height/40
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength, maxLineGap)

    for x1, y1, x2, y2 in lines[0]:
        cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# # 两个回调函数
# def HoughLinesP(minLineLength):
#     global minLINELENGTH
#     minLINELENGTH = minLineLength + 1
#     print
#     "minLINELENGTH:", minLineLength + 1
#     tempIamge = scr.copy()
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, minLINELENGTH, 0)
#     for x1, y1, x2, y2 in lines[0]:
#         cv2.line(tempIamge, (x1, y1), (x2, y2), (0, 255, 0), 1)
#     cv2.imshow(window_name, tempIamge)

def get_lines(filepath):
    """
    获取图片中的线条，作为基准线
    """
    gray = cv2.imread(filepath)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # cv2.imwrite(path_new, edges)
    h, w = gray.shape[:2]

    minLineLength = w * 0.9
    # minLineLength = h/32  # height/32
    maxLineGap = h/40  # height/40

    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=80, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=maxLineGap)
    # print(lines.shape)
    I = np.argsort(lines[:, 0, 0])
    lines = lines[I[::1]]
    I = np.argsort(lines[:, 0, 1], kind='mergesort')
    lines = lines[I[::1]]

    '''
    微调间距，使得2条直线相交，去掉相似接近的一条。过滤线条（图片上的虚线，相当于矩形，也会有上下2条边）
    '''
    gap = 1
    line_bak = [[lines[0][0][0], lines[0][0][1] + gap], [lines[0][0][2], lines[0][0][3] - gap]]
    a, b, c = lines.shape
    filter_lines = []
    filter_lines.append([[0,0,w,0]])
    for i in range(a):
        if i > 0:
            line_to = [[lines[i][0][0], lines[i][0][1] - gap], [lines[i][0][2], lines[i][0][3] + gap]]
            flag = is_crosses(line_bak, line_to)
            # print(flag)
            line_bak = [[lines[i][0][0], lines[i][0][1] + gap], [lines[i][0][2], lines[i][0][3] - gap]]
            if flag:
                continue
        filter_lines.append(lines[i])

    text_gap = 1
    for i in range(len(filter_lines)):
        text_gap = text_gap + 1
        # print(filter_lines[i])
        cv2.line(gray, (filter_lines[i][0][0], filter_lines[i][0][1]), (filter_lines[i][0][2], filter_lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        cv2.putText(gray, str(i), (filter_lines[i][0][0], filter_lines[i][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    cv2.imshow('result', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #
    # path_new = os.path.abspath(os.path.dirname(filepath)) + '\\' + str(int(round(time.time() * 1000000))) + '.jpg'
    # cv2.imwrite(path_new, gray)
    return filter_lines

def is_crosses(line1, line2):
    """
    判断2条线是否相交
    """
    if LineString(line1).crosses(LineString(line2)):
        return True
    return False

if __name__ == "__main__":
    #path = "C:/Users/dyjx/Desktop/ocr/kd/kd1.jpg"
    # path = "C:/Users/dyjx/Desktop/ocr/kd/demo1_fuben.bmp"
    path = "C:/Users/dyjx/Desktop/ocr/kd/demo1_fuben.bmp"
    path_new = "C:/Users/dyjx/Desktop/ocr/kd/test1.bmp"

    image_roi(path)
    # lines = get_lines(path)
    # for i in range(len(lines)):
    #     if (i+1)%2==0:
    #         print(i, lines[i-1], lines[i])

    # [[28  85 579  85]]
    # [[29 168 577 168]]
    # [[28 226 578 226]]
    # [[29 372 577 372]]
    # [[29 485 577 485]]
    # [[29 676 577 676]]
    # [[29 734 578 734]]

    # #polyline = [(0, 0), (609, 0), (579,85), (28, 85)]
    # polyline = [(29, 372), (577, 372), (577, 485), (29, 485)]
    # points = []
    # for line in polyline:
    #     if line:
    #         try:
    #             lng, lat = line[:]
    #             points.append(point.Point(float(lng), float(lat)))
    #         except ValueError:
    #             pass

    # flag = point.is_point_in_polygon(point.Point(float(198), float(451)), points)
    # print(flag)
    # #