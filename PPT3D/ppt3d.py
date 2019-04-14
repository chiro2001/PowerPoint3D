from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from PPT3D.glfw import *
import base64
from win32api import GetSystemMetrics
import sys
from PPT3D.settings import Settings
from PPT3D.renderer import Renderer
from PPT3D.PPT import *
from PPT3D.templates import Templates
from PIL import Image
from base_logger import getLogger


class Motion:
    def __init__(self, ppt: PPT):
        self.distance = 3
        self.x, self.y, self.z = 0, 0, self.distance
        self.facing = 0
        self.target = 0
        # 0 - 静止, 1 - 活动
        self.status = 1
        self.ppt = ppt

    def click(self):
        if self.status == 1:
            if self.target == len(self.ppt.pages) - 1:
                self.target = 0
            else:
                self.target += 1
            return
        if self.target == len(self.ppt.pages) - 1:
            self.target = 0
        else:
            self.target += 1
        self.x, self.y, self.z = self.ppt.pages[self.facing].position.json()
        self.status = 1

    def mouse(self, button, mode, x, y):
        if button == GLUT_LEFT_BUTTON and mode == GLUT_DOWN:
            logger.info('按下鼠标 (%s, %s)' % (x, y))
            self.click()

    def keyboard(self, key, x, y):
        # Special Key 处理
        if key in [GLUT_KEY_UP, GLUT_KEY_DOWN, GLUT_KEY_LEFT, GLUT_KEY_RIGHT]:
            if key in [GLUT_KEY_DOWN, GLUT_KEY_RIGHT]:
                self.click()
            elif key in [GLUT_KEY_UP, GLUT_KEY_LEFT]:
                # TODO: 向前
                pass
            return
        if type(key) is int:
            return

        # 切换全屏模式
        if key == b'f':
            glutFullScreenToggle()
            return

        # key = key.decode().lower()
        if key in [b' ', b'\r']:
            self.click()
        else:
            print(key)

        if key in [b'\x1b', b'q']:
            sys.exit()

    def timer(self):
        if self.status == 1:
            # facing = self.ppt.pages[self.facing].position
            target = self.ppt.pages[self.target].position
            self.x += (target.x - self.x) / 10
            self.y += (target.y - self.y) / 10
            self.z += (target.z - self.z) / 10

            if abs(self.x - target.x) <= 0.0002:
                self.facing = self.target
                self.x, self.y, self.z = self.ppt.pages[self.facing].position.json()
                self.status = 0

        self.set_look_at()

    def set_look_at(self):
        gluLookAt(self.x * 5, self.y * 5, self.z * 5 + self.distance,
                  self.x * 5, self.y * 5, self.z * 5 + self.distance - 1,
                  0, 1, 0)


class PPT3D:

    def __init__(self, ppt: PPT, fullscreen=False):

        # 初始化内容
        self.ppt = ppt

        # 初始化组件
        self.settings = Settings()
        # self.renderer = Renderer()
        self.templates = Templates()
        self.motion = Motion(self.ppt)

        # 显示相关
        # Frame数量
        self.num_frame = 0

        # 取得屏幕大小
        self.zoom_window = 0.5
        self.rect_screen = list(map(int, [GetSystemMetrics(0), GetSystemMetrics(1)]))
        self.rect_window = list(map(int, [self.rect_screen[0] * self.zoom_window,
                                          self.rect_screen[1] * self.zoom_window]))
        self.rect_page = list(map(lambda x: x / 3000, self.rect_screen))
        self.size_room = [5, 5, 5]
        # print(self.rect_screen)

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE)
        glutInitWindowSize(self.rect_window[0], self.rect_window[1])
        self.window = glutCreateWindow('Hello PyOpenGL')
        glutDisplayFunc(self.draw)
        glutMouseFunc(self.motion.mouse)
        glutKeyboardFunc(self.motion.keyboard)
        glutSpecialFunc(self.motion.keyboard)
        glutIdleFunc(self.draw)

        if fullscreen:
            glutFullScreen()

        self.glut_init(self.rect_window[0], self.rect_window[1])

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.motion.timer()

        # 第一组eyex, eyey,eyez 相机在世界坐标的位置
        # 第二组centerx,centery,centerz 相机镜头对准的物体在世界坐标的位置
        # 第三组upx,upy,upz 相机向上的方向在世界坐标中的方向

        # glutWireTeapot(5)
        # glutSolidTeapot(5)
        # glLoadIdentity()
        glTranslate(-self.rect_page[0] / 1 * self.size_room[0], -self.rect_page[1] / 1 * self.size_room[1], 0)

        index_frame = 0

        # for index in range(self.num_frame):
        for index in range(len(self.ppt.pages)):
            page = self.ppt.pages[index]
            # glTranslate(page.position.x + (self.rect_page[0] * self.size_room[0] + 0.5) * index,
            #             page.position.y,
            #             page.position.z)
            glTranslate(page.position.x,
                        page.position.y,
                        page.position.z)
            # print(page.json())

            for i in range(len(page.frames)):
                frame = page.frames[i]
                # 开始绘制这个Frame，同时设置纹理映射
                glBindTexture(GL_TEXTURE_2D, index_frame)
                index_frame += 1
                vec_target = [self.size_room[0] * page.position.x + frame.rect[0],
                              self.size_room[1] * page.position.y + frame.rect[1],
                              self.size_room[2] * page.position.z]
                # 绘制四边形
                glBegin(GL_QUADS)
                glTexCoord2f(0.0, 0.0)
                glVertex3f(vec_target[0],
                           vec_target[1],
                           vec_target[2])
                glTexCoord2f(1.0, 0.0)
                # glVertex3f(self.size_room[0] * (page.position.x + self.rect_page[0]),
                #            self.size_room[1] * page.position.y,
                #            self.size_room[2] * page.position.z)
                glVertex3f(vec_target[0] + self.size_room[0] * (frame.rect[2] - frame.rect[0]),
                           vec_target[1],
                           vec_target[2])
                glTexCoord2f(1.0, 1.0)
                # glVertex3f(self.size_room[0] * (page.position.x + self.rect_page[0]),
                #            self.size_room[1] * (page.position.y + self.rect_page[1]),
                #            self.size_room[2] * page.position.z)
                glVertex3f(vec_target[0] + self.size_room[0] * (frame.rect[2] - frame.rect[0]),
                           vec_target[1] + self.size_room[1] * (frame.rect[3] - frame.rect[1]),
                           vec_target[2])
                glTexCoord2f(0.0, 1.0)
                # glVertex3f(self.size_room[0] * page.position.x,
                #            self.size_room[1] * (page.position.y + self.rect_page[1]),
                #            self.size_room[2] * page.position.z)
                glVertex3f(vec_target[0],
                           vec_target[1] + self.size_room[1] * (frame.rect[3] - frame.rect[1]),
                           vec_target[2])
                glEnd()

        # 刷新屏幕，产生动画效果
        glutSwapBuffers()

    # 加载纹理
    def load_texture(self):
        renderer = Renderer(self.rect_window)
        # for index in range(len(self.ppt.pages)):
        #     # TODO: Frame渲染
        #     page = self.ppt.pages[index]
        #     img_page = renderer.render_page(page)
        #     img_page = img_page.convert('RGBA')
        #     width, height = img_page.size
        #     img = img_page.tobytes('raw', 'RGBA', 0, -1)
        #
        #     glGenTextures(2)
        #     glBindTexture(GL_TEXTURE_2D, index)
        #     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
        #                  width, height, 0, GL_RGBA,
        #                  GL_UNSIGNED_BYTE, img)
        #     glTexParameterf(GL_TEXTURE_2D,
        #                     GL_TEXTURE_WRAP_S, GL_CLAMP)
        #     glTexParameterf(GL_TEXTURE_2D,
        #                     GL_TEXTURE_WRAP_T, GL_CLAMP)
        #     glTexParameterf(GL_TEXTURE_2D,
        #                     GL_TEXTURE_WRAP_S, GL_REPEAT)
        #     glTexParameterf(GL_TEXTURE_2D,
        #                     GL_TEXTURE_WRAP_T, GL_REPEAT)
        #     glTexParameterf(GL_TEXTURE_2D,
        #                     GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #     glTexParameterf(GL_TEXTURE_2D,
        #                     GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        #
        #     glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        #     # 加载透明图片
        #     # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

        for index in range(len(self.ppt.pages)):
            page = self.ppt.pages[index]
            for frame in page.frames:
                img_frame = renderer.render_frame(frame)
                img_frame = img_frame.convert('RGBA')
                width, height = img_frame.size
                img = img_frame.tobytes('raw', 'RGBA', 0, -1)

                glGenTextures(2)
                glBindTexture(GL_TEXTURE_2D, self.num_frame)
                self.num_frame += 1
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                             width, height, 0, GL_RGBA,
                             GL_UNSIGNED_BYTE, img)
                glTexParameterf(GL_TEXTURE_2D,
                                GL_TEXTURE_WRAP_S, GL_CLAMP)
                glTexParameterf(GL_TEXTURE_2D,
                                GL_TEXTURE_WRAP_T, GL_CLAMP)
                glTexParameterf(GL_TEXTURE_2D,
                                GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D,
                                GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D,
                                GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameterf(GL_TEXTURE_2D,
                                GL_TEXTURE_MIN_FILTER, GL_NEAREST)

                # # 分文字内容和图片内容处理
                # if frame.fclass in ['Text', 'Title']:
                #     glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)
                # # 加载不透明图片
                # elif frame.fclass in ['Image']:
                #     print(frame.fclass)
                #     glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)

                glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)

    def glut_init(self, width, height):
        if glGetIntegerv(GL_SAMPLE_BUFFERS) == 1 and glGetIntegerv(GL_SAMPLES) > 1:
            logger.debug('支持多采样抗锯齿，打开抗锯齿开关')
            glEnable(GL_MULTISAMPLE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_BLEND)
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.9)

        # glEnable(GL_FOG)
        # glFogfv(GL_FOG_COLOR, [0.5, 0.5, 0.5])
        # glFogf(GL_FOG_START, 1.0)
        # glFogf(GL_FOG_END, 15.0)
        # glFogi(GL_FOG_MODE, GL_LINEAR)
        # glHint(GL_FOG_HINT, GL_DONT_CARE)

        glEnable(GL_DEPTH_TEST)

        self.load_texture()
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        # 背面剔除，消隐
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_FASTEST)
        glLoadIdentity()
        gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # if glutGameModeGet(GLUT_GAME_MODE_ACTIVE):
        #     glutLeaveGameMode()

    def mainloop(self):
        glutMainLoop()


logger = getLogger(__name__)
