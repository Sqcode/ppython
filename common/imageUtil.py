import numpy as np
import cv2, os, time, sys
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageEnhance
import matplotlib.pylab as plt
from shapely.geometry import LineString
from watermarker.marker import add_mark
import exp
from util import file_exist, JarProjectPath

def mask(dir, text='sqc'):
    """
    file： 待添加水印的照片；
    mark： 使用哪些字作为水印；
    out： 添加水印后保存的位置；
    color： 水印字体的颜色，默认颜色#8B8B1B；
    size： 水印字体的大小，默认50；
    opacity： 水印字体的透明度，默认0.15；
    space： 水印字体之间的间隔, 默认75个空格；
    angle： 水印字体的旋转角度，默认30度；
    接下来，我们仅用一行代码，给图片添加水印。
    """
    path, file = os.path.split(dir)[:2]
    # print(path, file)

    add_mark(
        # 待加水印的图片的位置
        file=dir,
        # 输出文件存放的位置
        out=f"{path}/mask",
        # 需要加的水印的内容
        mark=text,
        # 字体的透明度，默认为0.15
        opacity=0.2,
        # 文字倾斜的角度，默认值是30
        angle=45,
        # 文字之间的间隔，默认是75个空格
        space=30,
        # 文字的颜色
        # color="#FFC814",
        # 文字的大小，默认是50
        size=50)

# 俩图片相加
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

# 展示图
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

# 获取 图片中的线条
def get_lines(filepath):
    """
    :param filepath: 图片路径，获取图片中的线条，作为基准线
    """
    if not os.path.exists(filepath):
        raise exp.MyException('路径不存在 %s' % filepath)

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

# 是否相交
def is_crosses(line1, line2):
    """
    判断2条线是否相交
    """
    if LineString(line1).crosses(LineString(line2)):
        return True
    return False

def compare_images(path_one, path_two, diff_save_location=f"{JarProjectPath.project_root_path()}/files/diff_{str(round(time.time() * 1000))}.jpg"):
    """
    比较图片，如果有不同则生成展示不同的图片
 
    @参数一: path_one: 第一张图片的路径
    @参数二: path_two: 第二张图片的路径
    @参数三: diff_save_location: 不同图的保存路径
    """
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
    try: 
        diff = ImageChops.difference(image_one, image_two)
        if diff.getbbox() is None:
        # 图片间没有任何不同则直接退出
            print("【+】We are the same!")
        else:
            diff.save(diff_save_location)
    except ValueError as e:
        text = ("表示图片大小和box对应的宽度不一致，参考API说明：Pastes another image into this image."
                "The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, "
                "right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted "
                "image must match the size of the region.使用2纬的box避免上述问题")
        print("【{0}】{1}".format(e,text))
    return diff_save_location

def printImage(dir, char_lst=' .:-=+*#%@'):
    """
    通过灰度值，将图片以字符打印
    """
    im = Image.open(dir)
    h = im.height
    w = im.width

    #resize = im.resize((150, 150))
    #w = resize.width
    # resize.show()
    gray = im.convert('L')
    # gray.show()
    scale = w // 100  #图片缩放100长度
    print(w, w//50, scale)
    char_lst = char_lst  #要替换的字符
    # char_lst = ' @'  #要替换的字符
    char_len = len(char_lst)  #替换字符的长度
    # print(char_len)
    try:
        for y in range(0, h, scale):  #根据缩放长度 遍历高度
            # print(y)
            for x in range(0, w, scale):  #根据缩放长度 遍历宽度
                choice = gray.getpixel((x, y)) * char_len // 255  #获取每个点的灰度  根据不同的灰度填写相应的 替换字符
                # print(choice, char_len, choice == char_len)
                if choice == char_len:
                    choice = char_len - 1
                sys.stdout.write(char_lst[choice])  #写入控制台
            sys.stdout.write('\n')
            # sys.stdout.write('----------------------------------')
            sys.stdout.flush()
    except ValueError:
        print('图片缩放长度100，异常')
    except IndexError:
        print('image index out of range')

def enhance(dir):
    """
    ImageEnhance提供了一些类，可以用于图像增强。
    所有的增强类都实现了一个接口，这个接口包括一个方法enhancer.enhance(factor)。
    该方法返回增强过的图像。factor为1时，返回原图像拷贝，factor越大，增强效果越显著。
    """
    im = Image.open(dir)
    # enhancer = ImageEnhance.Sharpness(im)
    # enhancer.enhance(0.0).show("Sharpness %f" % 0.0)
    # enhancer.enhance(10.0).show("Sharpness %f" % 10.0)

    # 锐度，增强因子为1.0是原始图片
    # 锐度增强
    enh_sha = ImageEnhance.Sharpness(im)
    sharpness = 10.0
    image_sharped = enh_sha.enhance(sharpness)
    # print(os.path.abspath(dir), os.path.dirname(dir), os.path.splitext(dir), os.path.basename(dir))
    #np, suf = os.path.splitext(dir)[:2]
    n, f = os.path.basename(dir).split('.')[:2]
    # print(n,f)
    out_path = os.path.join(os.path.dirname(dir), n+'_'+str(round(time.time()*1000))+'.'+f)
    # out_path = os.path.join(os.path.dirname(dir), 'bak'+os.path.splitext(dir)[1])
    # print(out_path)
    image_sharped.save(out_path)
    return out_path

if __name__ == "__main__":
    
    path = "C:/Users/dyjx/Desktop/ocr/kd/demo1_fuben.bmp"
    path_new = "C:/Users/dyjx/Desktop/ocr/kd/test1.bmp"
    path = r'static/pig.jpg'
    path1 = r'static/biu.jpg'
    path2 = r'static/biubiu.jpg'
    path3 = r'static/blove.jpg'
    path4 = r'static/logo.png'
    path5 = r'images/jietu.png'
    path6 = 'C:/Users/dyjx/Desktop/py/images/1629353489174/sf_3.png'

    compare_images(path1, path2)
    # enhance(path)
    # printImage(path1)
    # mask(path2)

    # get_lines(path6)

    # plt_show([cv2.imread(path), cv2.imread(path1)], ['path'])

    # a = img_add(path3, path4)
    # b = img_add(path4, path3)
    # plt_show([a, b], ['3+4', '4+3'])

    #path = "C:/Users/dyjx/Desktop/ocr/kd/kd1.jpg"
    # path = "C:/Users/dyjx/Desktop/ocr/kd/demo1_fuben.bmp"
