from PPT3D.ppt3d import *
from PPT3D.PPT import *
from PIL import Image

# ppt = PPT().load(filename='save.p3d')
filename = 'test.pptx'
filename = os.path.abspath(filename)
print(filename)
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
    ppt.pages.append(page)


ppt3d = PPT3D(ppt)
ppt3d.mainloop()
