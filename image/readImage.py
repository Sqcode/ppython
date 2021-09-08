import cv2
import os
import numpy as np
from PIL import Image
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from watermarker.marker import add_mark
import time


def main(dir):
    if os.path.exists(dir):
        im = cv2.imread(dir)
        print(im.shape)
        # for n in im:
        #     print(n)
    else :
        print('路径不存在')

def pil (dirpath):
    from PIL import Image
    import numpy as np
    img_PIL = Image.open(dirpath)#读取数据
    print("img_PIL:",img_PIL)
    print("img_PIL:",type(img_PIL))
    #将图片转换成np.ndarray格式
    img_PIL = np.array(img_PIL)
    print("img_PIL:",img_PIL.shape)
    print("img_PIL:",type(img_PIL))

def shape(dir):
    """
        通道3，灰度
    """
    im = cv2.imread(dir)
    h, w = im.shape[:2]
    print(im.shape, im.dtype)
    # cv2.namedWindow('origin1111111111')
    cv2.imshow('origin', im)

    #拆分通道
    b, g, r = cv2.split(im)
    #显示原始图像
    cv2.imshow("B", b)
    cv2.imshow("G", g)
    cv2.imshow("R", r)
    #合并通道
    
    b = np.zeros((h, w), dtype=im.dtype)
    r = np.zeros((h, w), dtype=im.dtype)
    # m = cv2.merge([r, g, b])
    m = cv2.merge([b, g, r])
    # cv2.imshow("Merge", m)
    enlarge = cv2.resize(m, (0, 0), fx=0.5, fy=1.5, interpolation=cv2.INTER_CUBIC)  

    cv2.imshow("enlarge", enlarge)

    # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # print(gray.shape, gray.dtype)
    # cv2.imshow('gray', gray)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def printImage(dir):
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
    char_lst = ' .:-=+*#%@'  #要替换的字符
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
    out_path = os.path.join(os.path.dirname(dir), n+'_'+str(round(time.time()*1000))+'.'+f)
    # out_path = os.path.join(os.path.dirname(dir), 'bak'+os.path.splitext(dir)[1])
    print(out_path)
    image_sharped.save(out_path)

def mask(dir):
    add_mark(
        # 待加水印的图片的位置
        file=dir,
        # 输出文件存放的位置
        out="out.jpg",
        # 需要加的水印的内容
        mark="Sun",
        # 字体的透明度，默认为0.15
        opacity=0.2,
        # 文字倾斜的角度，默认值是30
        angle=45,
        # 文字之间的间隔，默认是75个空格
        space=10,
        # 文字的颜色
        color="#FFC814",
        # 文字的大小，默认是50
        size=10
        
         )

if __name__ == '__main__':
    dir = 'C:/Users/dyjx/Desktop/images/me.jpg'
    print(os.path.abspath(__file__), os.path.dirname(__file__), os.path.splitext(__file__), os.path.basename(__file__))

    # enhance(dir)
    # mask(dir)


