import tkinter as tk
from tkinter import Menu
from tkinter import ttk
# 菜单列

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('演示窗口')
        self.root.geometry("500x200+1100+150")
        # 创建主菜单实例
        self.menubar = Menu(self.root)
        # 显示菜单,将root根窗口的主菜单设置为menu
        self.root.config(menu=self.menubar)
        self.interface()

    def interface(self):
        """"界面编写位置"""
        # 在 menubar 上设置菜单名，并关联一系列子菜单
        self.menubar.add_cascade(label="文件", menu=self.papers())
        self.menubar.add_cascade(label="查看", menu=self.about())

    def papers(self):
        """
        fmenu = Menu(self.menubar): 创建子菜单实例
        tearoff=1: 1的话多了一个虚线,如果点击的话就会发现,这个菜单框可以独立出来显示
        fmenu.add_separator(): 添加分隔符"--------"
        """
        fmenu = Menu(self.menubar, tearoff=0)
        # 创建单选框
        for item in ['新建', '打开', '保存', '另存为']:
            fmenu.add_command(label=item)

        return fmenu

    def about(self):
        amenu = Menu(self.menubar, tearoff=0)
        # 添加复选框
        for item in ['项目复选框', '文件扩展名', '隐藏的项目']:
            amenu.add_checkbutton(label=item)

        return amenu

# Drop-down box
def drop_down_box(gui):
    """"界面编写位置"""
    values = ['1', '2', '3', '4']
    drop_down = ttk.Combobox(
        master = gui.root,  # 父容器
        height=10,  # 高度,下拉显示的条目数量
        width=20,  # 宽度
        state='',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled(禁止输入选择)
        cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=('', 15),  # 字体、字号
        textvariable='',  # 通过StringVar设置可改变的值
        values=values,  # 设置下拉框的选项
        )
    drop_down.grid(padx=150)


if __name__ == '__main__':
    gui = GUI()
    drop_down_box(gui)
    gui.root.mainloop()
