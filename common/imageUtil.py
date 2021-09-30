import numpy as np
import cv2
from PIL import Image
import matplotlib.pylab as plt
from shapely.geometry import LineString
import exp

def img_add(f1, f2, tailor=True):
    """
    ！！！俩图片 必须尺寸相同！！！
    """
    im1 = cv2.imread(f1)
    h1, w1 = im1.shape[:2]

    im2 = cv2.imread(f2)
    h2, w2 = im2.shape[:2]

    
    if tailor:
        # 取 2者的，最少长宽
        h = h1 if h1 < h2 else h2
        w = w1 if w1 < w2 else w2
        # resize = cv2.resize(im, (int(h / 2), int(w / 2)))
        # resize = cv2.resize(im, (0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)  
        im1 = cv2.resize(im1, (h, w))
        im2 = cv2.resize(im2, (h, w))
        
    else:
        if h1 != h2 or w1 != w2:
            raise exp.MyException('图片尺寸不相同，无法合并')
    
    print(im1.shape[:2], im2.shape[:2])
    # print(im1, im2)
    res = cv2.add(im1, im2)

    # plt_show([im1, im2, res1, res2], base_cols=4)

    # cv2.imshow("im1", im2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return res

def plt_show(images, titles=[], gray=False, base_cols=3):
    images_len = len(images)
    titles_len = len(titles)
    # images_len = 11
    
    # 计算 是否超出预设的列数，更新列数
    cols = base_cols if images_len > base_cols else images_len
    # 计算 需要多少行，取余+整除
    rows = (1 if images_len > cols and images_len % cols > 0 else 0) + int(images_len / cols)

    # print(f'默认一行{cols}张，余{images_len % cols}张, 需要{rows}行')


    for i in range(images_len):
        # 多少行，多少列
        plt.subplot(rows, cols, i+1)
        # print(isinstance(titles[i], list))
        if gray:
            plt.imshow(images[i], 'gray')
        else: 
            b, g, r = cv2.split(images[i])
            srcImage_new = cv2.merge([r, g, b])
            plt.imshow(srcImage_new)
        
        if titles_len >= images_len or i < titles_len:
            plt.title(titles[i])
        else:
            plt.title(i)
        
        plt.xticks([])
        plt.yticks([])

    plt.show()

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
    #avator
    path = r'static/pig.jpg'
    path1 = r'static/biu.jpg'
    path2 = r'static/biubiu.jpg'
    path3 = r'static/blove.jpg'
    path4 = r'static/logo.png'

    # plt_show([cv2.imread(path), cv2.imread(path1)], ['path'])

    a = img_add(path3, path4)
    # b = img_add(path4, path3)
    # plt_show([a, b], ['3+4', '4+3'])

    #path = "C:/Users/dyjx/Desktop/ocr/kd/kd1.jpg"
    # path = "C:/Users/dyjx/Desktop/ocr/kd/demo1_fuben.bmp"
    path = "C:/Users/dyjx/Desktop/ocr/kd/demo1_fuben.bmp"
    path_new = "C:/Users/dyjx/Desktop/ocr/kd/test1.bmp"
