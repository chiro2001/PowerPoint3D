import win32com
import win32com.client
import sys
import os

ppt_root = jpg_root = sys.path[0]+"\\"


def ppt2png(pptFileName):

    powerpoint = win32com.client.Dispatch('PowerPoint.Application')

    powerpoint.Visible = True

    ppt_path = ppt_root + pptFileName

    outputFileName = pptFileName[0:-4] + ".pdf"

    ppt = powerpoint.Presentations.Open(ppt_path)
    #保存为图片
    print('save:', jpg_root + pptFileName.rsplit('.')[0] + '.jpg')
    ppt.SaveAs(jpg_root + pptFileName.rsplit('.')[0] + '.jpg', 17)
    #保存为pdf
    # ppt.SaveAs(jpg_root + outputFileName, 32) # formatType = 32 for ppt to pdf

    # 关闭打开的ppt文件
    ppt.Close()
    # 关闭powerpoint软件
    powerpoint.Quit()


for fn in (fns for fns in os.listdir(ppt_root) if fns.endswith(('.ppt', 'pptx'))):
    ppt2png(fn)
#运行结果则会出现pdf和jpg两个格式的文件夹