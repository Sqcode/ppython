
import os

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

# # 三、os模块
# os.getcwd() # 获取当前工作目录
# os.chdir(“dirname”) # 改变当前脚本工作目录，相当于shell下的cd
# os.curdir # 返回当前目录（‘.’）
# os.pardir # 获取当前目录的父目录字符串名：（’…’）
# os.makedirs(‘dirname1/dirname2’) # 可生成多层递归目录
# os.removedirs(‘dirname1’) # 若目录为空，则删除，并递归到上一级目录，若也为空，删除
# os.mkdir(‘dirname’) # 生成单级目录，相当于mkdir dirname
# os.rmdir(‘dirname’) # 删除单级空目录，不空无法删除。
# os.listdir(‘dirname’) # 列出指定目录下的所有文件和子目录
# os.remove() # 删除一个文件
# os.rename(‘oldname’,‘newname’) # 重命名文件/目录
# os.stat(‘path/filename’) # 获取文件/目录信息
# os.sep # 输出操作系统特定的路径分隔符，win下为“\”，Linux为“/”
# os.linesep # 输出当前平台使用的行终止符，win下为“\t\n”，Linux为“\n”
# os.pathsep # 输出用于分隔文件路径的字符串
# os.name # 输出字符串指示当前使用平台。win->‘nt’；Linux->‘posix’
# os.system(‘bash command’) # 运行shell命令，直接显示
# os.environ # 获取系统环境变量
# os.path.abspath(path) —返回path规范化的绝对路径
# os.path.split(path) # 将path分割成目录和文件名二元组返回
# os.path.dirname(path) # 返回path的目录。其实就是os.path.split的第一个元素
# os.path.basename(path) # 返回path最后的文件名，如果path以\或/结果，就返回空值
# os.path.exists(path) # 如果path存在返回True，否则False
# os.path.isabs(path) # 如果path是绝对路径，返回True
# os.path.isfile(path) # 如果path是一个存在的文件，返回True，否则False。
# os.path.isdir(path) # 如果path是一个存在的目录，返回True。
# os.path.join(path1[,path2[,…]]) # 将多个路径组合后返回
# os.path.getatime(path) # 返回path所指向的文件或目录的最后存取时间
# os.path.getmtime(path) # 返回path所指向的文件或目录的最后修改时间
if __name__ == '__main__':

    # file_dir = r'C:\Users\dyjx\Desktop\ocr\kd'
    # file_name(file_dir)
    # list_name = listdir(file_dir, [])
    print(1)