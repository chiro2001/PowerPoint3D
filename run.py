from PPT3D.ppt3d import *
from PPT3D.PPT import *
from PIL import Image
import getopt
import sys


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
***help***
'''


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'h', [])
    if len(args) == 0:
        print(help_str)
        sys.exit()
    for name, val in opts:
        if '-h' == name:
            print(help_str)
            sys.exit()

    if len(args) == 0:
        print(help_str)
        sys.exit()

    _filename = args[0]

    main(_filename)
