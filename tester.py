from PPT3D.ppt3d import PPT3D
from PPT3D.PPT import *

# ppt = PPT().load(filename='save.p3d')
ppt = PPT()
ppt3d = PPT3D(ppt)
ppt3d.mainloop()
