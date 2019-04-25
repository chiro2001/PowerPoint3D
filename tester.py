from PPT3D.ppt3d import *
from PPT3D.PPT import *
from PIL import Image

# ppt = PPT().load(filename='save.p3d')
filename = 'test.pptx'
print(filename)
ppt = PPT()

ppt2img(filename)


# li = os.listdir(TEMP_PATH)
li = os.listdir('imgs\\')
li.sort()
for i in li:
    if not i.lower().endswith('.jpg'):
        continue
    # im = Image.open(TEMP_PATH + i)
    im = Image.open('imgs\\' + i)
    page = Page()
    page.frames.append(Frame(image=im))
    page.position.load([random.random() * 6.8 for i in range(3)])
    ppt.pages.append(page)


ppt3d = PPT3D(ppt)
ppt3d.mainloop()
