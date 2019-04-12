from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PPT3D.glfw import *
from win32api import GetSystemMetrics
import sys
from PPT3D.settings import Settings
from PPT3D.renderer import Renderer
from PPT3D.templates import Templates


class PPT3D:

    def __init__(self):

        # 初始化组件
        self.settings = Settings()
        self.renderer = Renderer()
        self.templates = Templates()

        # 取得屏幕大小
        self.zoom_window = 0.5
        self.rect_screen = list(map(int, [GetSystemMetrics(0), GetSystemMetrics(1)]))
        self.rect_window = list(map(int, [self.rect_screen[0] * self.zoom_window,
                                          self.rect_screen[1] * self.zoom_window]))
        # print(self.rect_screen)

        # 初始化glfw
        if not glfwInit():
            sys.exit()
        # 打开抗锯齿
        glfwWindowHint(GLFW_SAMPLES, 16)
        # 打开窗口
        self.window = glfwCreateWindow(self.rect_window[0], self.rect_window[1], str.encode("Hello World"), None, None)
        if not self.window:
            glfwTerminate()
            sys.exit()

        # 设置窗口上下文
        glfwMakeContextCurrent(self.window)

        # 设置键盘处理函数
        glfwSetKeyCallback(self.window, self.keyboard)

        self.glut_init()

    def glut_init(self):
        # 打开抗锯齿开关
        glEnable(GL_MULTISAMPLE)

    def keyboard(self, window, key, scancode, action, mods):
        if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
            glfwSetWindowShouldClose(window, 1)

    def mainloop(self):
        while not glfwWindowShouldClose(self.window):
            # Render here
            width, height = glfwGetFramebufferSize(self.window)
            ratio = width / float(height)
            glViewport(0, 0, width, height)
            glClear(GL_COLOR_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-ratio, ratio, -1, 1, 1, -1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glRotatef(glfwGetTime() * 50, 0, 0, 1)
            glBegin(GL_TRIANGLES)
            glColor3f(1, 0, 0)
            glVertex3f(-0.6, -0.4, 0)
            glColor3f(0, 1, 0)
            glVertex3f(0.6, -0.4, 0)
            glColor3f(0, 0, 1)
            glVertex3f(0, 0.6, 0)
            glEnd()

            # Swap front and back buffers
            glfwSwapBuffers(self.window)

            # Poll for and process events
            glfwPollEvents()

        glfwTerminate()
