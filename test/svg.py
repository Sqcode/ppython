#! encoding:UTF-8
import cairosvg
import os

def export(fromDir, targetDir, exportType):
    print ("开始执行转换命令...")
    files = os.listdir(fromDir)
    num = 0
    for fileName in files:
        path = os.path.join(fromDir,fileName)
        if os.path.isfile(path) and fileName[-3:] == "svg":
            num += 1
            fileHandle = open(path)
            svg = fileHandle.read()
            fileHandle.close()
            exportPath = os.path.join(targetDir, fileName[:-3] + exportType)
            exportFileHandle = open(exportPath,'w')
            if exportType == "png":
                cairosvg.svg2png(bytestring=svg, write_to=exportPath)
            elif exportType == "pdf":
                cairosvg.svg2pdf(bytestring=svg, write_to=exportPath)
            exportFileHandle.close()
            print ("Success Export ", exportType, " -> " , exportPath)
    print ("已导出 ", num, "个文件")

if __name__ == '__main__':
    svgDir = r'C:\Users\dyjx\Desktop\svgs'
    exportDir = r'C:\Users\dyjx\Desktop\pngs'
    exportFormat = 'png'
    export(svgDir, exportDir, exportFormat)