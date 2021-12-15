
import os, sys

def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        # print(root) #当前目录路径  
        # print(dirs) #当前路径下所有子目录  
        print(files) #当前路径下所有非目录子文件  

def file_name_for(file_dir, suffix):   
    L = []   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == suffix:  
                L.append(os.path.join(root, file))  
    return L

def listdir(path, list_name):  
    for file in os.listdir(path): 
        # print(file)
        file_path = os.path.join(path, file)
        # n, suffix = os.path.splitext(file_path)[:2]
        n, suffix = os.path.splitext(file)[:2]
        # print(n, suffix)
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        elif suffix =='.jpg':  
            list_name.append(n)

    return list_name

if __name__ == '__main__':

    file_dir = r'C:\Users\dyjx\Desktop\ocr\kd'
    file_name(file_dir)
    # list_name = listdir(filepath, [])
    # print(list_name)


# from selenium import webdriver

# url = 'https://s.weibo.com/top/summary'
# option = webdriver.ChromeOptions()
# option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
# driver = webdriver.Chrome(chrome_options=option)
# driver.get(url)
# # 网页源码
# page = driver.page_source
# print(page)
# # 关闭浏览器
# driver.close()
