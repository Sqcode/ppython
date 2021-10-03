import matplotlib.pyplot as plt  
import jieba  
from wordcloud import WordCloud,ImageColorGenerator   
from PIL import Image
import numpy as np
import re
# 读入txt文本数据
# text = open(r'./files/text_cloud1.txt', "r",encoding="utf-8").read()

result = ['我','你','速度']
# with open(r'./files/text_cloud1.txt', 'r', encoding='utf-8') as f:
#     for line in f:
#         #print(line)
#         # r = re.split(r'\s|:|/',line)
#         # r = [item for item in result if not re.findall(r'\s+|\d+',item) and item]
#         result.append(line)
# print(result)
# # # print(text)
# # 结巴分词
# seg_list = jieba.cut(result,cut_all=False)
# # for i in seg_list:
# #     print(i)
# # print(seg_list)
# # print([i for i in seg_list])
# result = ",".join(seg_list)  
# print(result)

image = Image.open(r'C:\Users\dyjx\Desktop\images\logo.png')
graph = np.array(image)

#生成词云图
#wc = WordCloud(font_path=r"C:\Windows\Fonts\simhei.TTF", background_color='white',max_font_size=50,mask=graph)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
wc = WordCloud(font_path = 'C:\Windows\Fonts\simfang.ttf',max_words=2000,mask = graph,height= 400,width=400,background_color='white',repeat=False,mode='RGBA') #设置词云图对象属性

#generate（文本）从文本生成wordcloud。
wc.generate(",".join(result))
#从背景图片生成颜色值
image_color = ImageColorGenerator(graph)
wc.recolor(color_func=image_color)
#wc.to_file("./images/wordcloud1.png")
#显示图片
plt.figure("词云图")  # 指定所绘图名称
plt.imshow(wc)  # 以图片的形式显示词云
plt.axis("off")  # 关闭图像坐标系
plt.show()

