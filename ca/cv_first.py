import numpy as np
import cv2
import matplotlib.pylab as plt

def draw_img():
    # print('默认一维为数组:', np.arange(5))
    # print('自定义起点一维数组:',np.arange(1, 5))
    # print('自定义起点步长一维数组:',np.arange(2, 10, 2))
    # print('二维数组:', np.arange(8).reshape((2, 4)))
    # print('三维数组:', np.arange(60).reshape((3, 4, 5)))
    # print('指定范围三维数组:',np.random.randint(1, 8, size=(3, 4, 5)))

    # print(np.arange(255))
    arr = np.arange(255)
    # 使用 OpenCV 存储成图片
    cv2.imwrite('first_img.jpg', arr) 

def avg_threshold(img):
    h, w = img.shape
    # # 灰度值总和
    # px_t = 0
    # for i in range(h):
    #     for j in range(w):
    #         px_t += img[i][j]
    # # print(px_t)
    # # 求像素平均值
    # avg_thresh = int(px_t/(h*w))
    
    m = np.reshape(img, [1, w*h])
    # 求平均值来当做阈值，来分割图像
    avg_thresh = m.sum() / (w*h)

    return avg_thresh

def channel():
    im = cv2.imread(path, 0)
    h, w = im.shape
    #im.resize((400,400))
    resize = cv2.resize(im, (int(h / 2), int(w / 2)))
    # resize = cv2.resize(im, (0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)  
    # help(cv2.threshold)

    #retval, dst = cv2.threshold(resize, avg_threshold(im), 255, cv2.THRESH_BINARY_INV)
    retval, dst = cv2.threshold(resize, 150, 255, cv2.THRESH_BINARY_INV)
    # cv2.threshold()

    print(retval)
    cv2.imshow('gray', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def plt_show_demo():
    img = cv2.imread(path, 0)
    threshold = avg_threshold(img)
    ret, thresh1 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(img, threshold, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(img, threshold, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(img, threshold, 255, cv2.THRESH_TOZERO_INV)

    titles = ['Original Image', 'BINARY',
              'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([])
        plt.yticks([])

    plt.show()

def plt_show(images,titles):
    for i in range(len(images)):
        plt.subplot(3, 3, i+1)
        # print(isinstance(titles[i], list))
        if isinstance(titles[i], list):
            # print(titles[i][1])
            if titles[i][1]:
                b, g, r = cv2.split(images[i])
                srcImage_new = cv2.merge([r, g, b])
                plt.imshow(srcImage_new)
        else:
            plt.imshow(images[i], 'gray')
        plt.title(titles[i] if titles[i] else i)
        plt.xticks([])
        plt.yticks([])

    plt.show()

# 局部二值化
def adaptive_threshold(src):
    old_img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)

    # 建立一个 2 行 2 列的图
    plt.subplot(2, 2, 1)
    # 原图
    plt.imshow(old_img, 'gray')
    plt.title("old_img")

    # 灰度图
    plt.subplot(2, 2, 2)
    plt.imshow(gray, 'gray')
    plt.title("gray")

    # 添加第三幅图
    # 平均
    binary1 = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 10)

    plt.subplot(2, 2, 3)
    plt.imshow(binary1, 'gray')
    plt.title("MEAN")

    # 添加第四幅图
    # 高斯处理
    binary2 = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 10)

    plt.subplot(2, 2, 4)
    plt.imshow(binary2, 'gray')
    plt.title("GAUSSIAN")

    # plt.subplots(constrained_layout=True)
    # 自适应整体布局，文字不会覆盖
    plt.tight_layout()
    #plt.subplots_adjust(wspace=20)
    plt.show()

def img_add():
    im1 = cv2.imread(path1)
    im2 = cv2.imread(path2)
    res = cv2.add(im1, im2)
    #res = cv2.add(im2, im1)
    cv2.imshow("add", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def mask_demo():
    # cv.imshow("mask_demo", src)
    # 1. 建立与原图一样大小的 mask 图像，并将所有像素初始化为 0，因此全图成了一张全黑色图。
    # 2. 将 mask 图中的目标区域的所有像素值设置为255,此时目标区域变成了白色。
    mask = np.zeros([300, 300], dtype=np.uint8)
    cv2.circle(mask, (240,60), 50, (255,0,0),-1)
    # cv2.imshow("mask1", mask)
    # mask[高度截取，宽度截取]
    # mask[100:300, 200:400] = 255
    #cv2.imshow("mask2", mask)

    im1 = cv2.imread(path1)
    im2 = cv2.imread(path2)
    # img_add_mask = cv2.add(im1, im1, mask=mask)
    # cv2.imshow("img_add_mask", img_add_mask)

    ret1 = cv2.subtract(im1, im2)
    ret2 = cv2.subtract(im2, im1)
    # cv2.imshow("subtract_demo", ret)

    plt_show([ret1, ret2], ['1-2', '2-1'])

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def onChange(x):
    print('on', x)
    # pass
    # 设置系数
    r = float(x)/100.0
    # 默认情况下 src1 完全展示，逐步过渡到 src2
    img = cv2.addWeighted(img1, r, img2, 1.0-r, 0)
    cv2.imshow("img", img)

def add_weighted():

    img = np.zeros((300, 300, 3), np.uint8)
    cv2.namedWindow("img")
    cv2.createTrackbar('trackbar', "img", 3, 99, onChange)

    r = cv2.getTrackbarPos('trackbar', "img")
    # # 设置系数
    print(r)
    # r = float(r)/100.0
    # # 默认情况下 src1 完全展示，逐步过渡到 src2
    img = cv2.addWeighted(img1, r, img2, 1.0-r, 0)
    cv2.imshow("img", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # while(1):
    #     cv2.imshow("img", img)
    #     # 按键盘上的 esc 退出。
    #     k = cv2.waitKey(1) & 0xFF
    #     if k == 27:
    #         break
    #     # 获取滑动条的值
    #     r = cv2.getTrackbarPos('trackbar', "img")
    #     # 设置系数
    #     # print(r)
    #     r = float(r)/100.0
    #     # 默认情况下 src1 完全展示，逐步过渡到 src2
    #     img = cv2.addWeighted(img1, r, img2, 1.0-r, 0)

    
    # c = cv2.addWeighted(im1, 0.4, im2, 0.6, 0)
    # plt_show([im1,im2,c], ['img1', 'img2', 'add_weighted'])

def gradient():
    step_list = [float(0.02 * x) for x in range(0, 51)]
    print(step_list)
    # cv2.imshow("show", img1)
    for i in step_list:
        res = cv2.addWeighted(img1, i, img2, (1-i), 0)
        cv2.imshow("show", res)
        cv2.waitKey(60)
    
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

def roi():
    img = cv2.imread(path3)
    print(img.shape)
    h, w = img.shape[:2]
    horn = img[70:120, 220:290]
    # horn1 = img[0:200, 100:300]
    # horn2 = img[0:300, 100:400]
    # horn3 = img[0:400, 100:500]
    # horn4 = img[0:500, 100:600]
    # horn5 = img[0:600, 100:700]
    # 犄角转换成灰度图
    gray_horn = cv2.cvtColor(horn, cv2.COLOR_BGR2GRAY)
    # 获取到了犄角的二值化图像
    thresh, mask = cv2.threshold(gray_horn, 160, 255, cv2.THRESH_BINARY)
    # 获取 mask 的反色图像
    mask_inv = cv2.bitwise_not(mask)

    # 打开一个图片
    colors = cv2.imread(path)
    # 选中一块与 mask 相同大小的 ROI
    rows, cols = mask.shape[:2]
    pie_colors = colors[70:120, 220:290]
    # print(pie_colors.shape)
    # print(mask.shape)

    # 选出犄角部分
    img1_bg = cv2.bitwise_and(horn, pie_colors, mask=mask)
    # cv.imshow("img1_bg", img1_bg)
    img2_fg = cv2.bitwise_and(horn, horn, mask=mask_inv)
    # cv.imshow("img2_fg", img2_fg)
    # 两个犄角合并在一起
    add_img = img.copy()  # 对原图像进行拷贝
    dst = cv2.addWeighted(img1_bg, 0.3, img2_fg, 1, 0)
    # cv.imshow("dst", dst)
    add_img[70:120, 220:290] = dst
    # image[60:100, 180:240] = back_horn

    plt_show([horn, gray_horn, mask, mask_inv, img1_bg, img2_fg, dst, img, add_img],
    ["horn", "gray_horn", "mask", "mask_inv", "img1_bg", "img2_fg", "dst", ["img", True], ["add_img", True]])

    # cv2.imshow("horn", horn)
    # # 框选犄角区域
    # image = cv2.rectangle(img, (220, 65), (290, 125),  (0, 0, 255), thickness=2)
    # print(horn.shape)

    # # plt_show([img, image], ['origin', 'horn'])
    # cv2.imshow("horn", image)

    # # 犄角转换成灰度图
    # horn = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # 灰度图在转换成BGR图
    # back_horn = cv2.cvtColor(horn, cv2.COLOR_GRAY2BGR)
    # # image[250:370, 250:350] = back_horn
    # #image[60:100, 180:240]  = back_horn

    # cv2.imshow("Region Of Interest(ROI)", horn)
    # cv2.imshow("horn", image)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

#avator
path = 'C:/Users/dyjx/Desktop/images/pig.jpg'
path1 = 'C:/Users/dyjx/Desktop/images/biu.jpg'
path2 = 'C:/Users/dyjx/Desktop/images/biubiu.jpg'
path3 = 'C:/Users/dyjx/Desktop/images/leimu.png'
path4 = 'C:/Users/dyjx/Desktop/images/leimu.png'
img1 = cv2.imread(path1)
img2 = cv2.imread(path2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
if __name__ == '__main__':
    roi()
    # gradient()
    # add_weighted()
    # mask_demo()
    # img_add()
    # channel()
    # plt_show()
    # adaptive_threshold(cv2.imread(path))