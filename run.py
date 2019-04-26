from PPT3D.ppt3d import *
from PPT3D.PPT import *
from PIL import Image
import getopt
import sys
from tkinter import Tk, Label, LEFT


def main(filename: str):
    ppt = PPT()

    ppt2img(filename)

    li = os.listdir(TEMP_PATH)
    li.sort()
    for i in li:
        if not i.lower().endswith('.jpg'):
            continue
        im = Image.open(TEMP_PATH + i)
        page = Page()
        page.frames.append(Frame(image=im))
        page.position.load([random.random() * 6.8 for i in range(3)])
        ppt.pages.append(page)

    ppt3d = PPT3D(ppt)
    ppt3d.mainloop()


help_str = '''
3D动态显示ppt文件。需要本地电脑已安装Microsoft Office 2007及以上版本。

用法:

ppt3d [-h] [filename]

参数:

    -h      显示本帮助。
    

版本:

    v0.02   (2019/04/26)
'''


def show_help():
    root = Tk()
    root.title("PowerPoint 3D")
    Label(root, text=help_str, justify=LEFT).pack()
    root.mainloop()
    sys.exit()


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'h', [])
    if len(args) == 0:
        show_help()
    for name, val in opts:
        if '-h' == name:
            show_help()

    if len(args) == 0:
        show_help()

    _filename = args[0]

    logger.warning(_filename)

    main(_filename)
