from PIL import Image, ImageFont
import PIL
import random
import os
import json
import base64
import io
import zipfile


class Font:
    def __init__(self, family: str='微软雅黑', size: int=48*2):
        self.family = family
        self.size = size

    def get_font(self):
        font = ImageFont.truetype(self.family, self.size)
        return font

    def load(self, font):
        self.family = font['family']
        self.size = font['size']
        return self

    def json(self):
        js = {'family': self.family, 'size': self.size}
        return js


class Color:
    def __init__(self, r, g, b, enable: bool=True):
        self.r, self.g, self.b = r, g, b
        self.enable = enable

    # None表示透明
    def _rgb2str(self, r, g, b):
        if type(r) is float:
            r, g, b = list(map(lambda x: int(x * 256), [r, g, b]))
        if not (0 <= r < 256 and 0 <= g < 256 and 0 <= b < 256):
            return None
        if self.enable is False:
            return None
        res = '#%02X%02X%02X' % (r, g, b)
        return res

    def rgb2str(self):
        return self._rgb2str(self.r, self.g, self.b)

    def str2rgb(self, res: str):
        res = res.split('#')[-1]
        if len(res) != 2 * 3:
            self.r, self.g, self.b = 0, 0, 0
            return
        self.r, self.g, self.b = int(res[0:2], 16), int(res[2:4], 16), int(res[4:6], 16)
        return

    def load(self, color):
        if color is None:
            self.r, self.g, self.b = 0, 0, 0
            self.enable = False
            return
        self.r, self.g, self.b = color[0], color[1], color[2]
        return self

    def json(self):
        if self.enable:
            return [self.r, self.g, self.b]
        return None


class ColorDraw:
    def __init__(self, outline: Color=None, fill: Color=None, text: Color=None):
        self.outline, self.fill, self.text = outline, fill, text
        if self.text is None:
            self.text = Color(0, 0, 0)
        if self.outline is None:
            self.outline = Color(255, 0, 0, enable=True)
        if self.fill is None:
            self.fill = Color(0, 0, 0, enable=False)

    def json(self):
        return {'outline': self.outline.json(),
                'fill': self.fill.json(),
                'text': self.text.json()}

    def load(self, color):
        self.outline = Color(0, 0, 0).load(color['outline'])
        self.fill = Color(0, 0, 0).load(color['fill'])
        self.text = Color(0, 0, 0).load(color['text'])
        if self.text is None:
            self.text = Color(0, 0, 0)
        if self.outline is None:
            self.outline = Color(0, 0, 0, enable=False)
        if self.fill is None:
            self.fill = Color(0, 0, 0, enable=False)
        return self


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def load(self, vec):
        self.x, self.y, self.z = vec[0], vec[1], vec[2]
        return self

    def json(self):
        return [self.x, self.y, self.z]


Rect = list


class Frame:
    def __init__(self,
                 fclass: str='Text',
                 rect: Rect=None,
                 text: str='这是一个文本框',
                 image: Image=None,
                 font: Font=None,
                 color_draw: ColorDraw=None,
                 floating: float=0.0
                 ):
        self.fclass, self.rect, self.text, self.font, self.color_draw, self.floating = \
            fclass, rect, text, font, color_draw, floating
        self.image = image
        if self.rect is None:
            # 目标上下浮动
            self.rect = list(map(lambda x: random.sample([-1, 1], 1)[0] * random.random() * 0.04 + x,
                                 [0.1, 0.45]))
            self.rect.append(self.rect[0] + 0.8)
            self.rect.append(self.rect[1] + 0.15)
        if self.image is not None:
            self.fclass = 'Image'
            self.text = '图像'
            self.rect = [0, 0]
            if self.image.size[0] > self.image.size[1]:
                self.rect.append(1)
                self.rect.append(self.image.size[1] / self.image.size[0])
            else:
                self.rect.append(self.image.size[0] / self.image.size[1])
                self.rect.append(1)
            # self.rect[0] -= 0.5 * (1 - self.rect[0])
            # self.rect[1] -= 0.5 * (1 - self.rect[1])
            # self.rect[2] -= 0.5 * (1 - self.rect[2])
            # self.rect[3] -= 0.5 * (1 - self.rect[3])

            # self.rect = [0, -0.5, 1, 0.5]

            # self.rect[1] = 0
            # self.rect[3] = 1

        if self.font is None:
            self.font = Font()
        if self.color_draw is None:
            self.color_draw = ColorDraw()

    def load(self, frame):
        self.fclass = frame['class']
        self.rect = frame['rect']
        self.text = frame['text']
        self.font = Font().load(frame['font'])
        self.color_draw = ColorDraw().load(frame['color'])
        if 'image' in frame:
            data = base64.b64decode(frame['image'])
            stream = io.BytesIO(data)
            self.image = Image.open(stream)
        return self

    def json(self):
        res = {
            'class': self.fclass,
            'rect': self.rect,
            'text': self.text,
            'font': self.font.json(),
            'color': self.color_draw.json()
        }
        if self.image is not None:
            stream = io.BytesIO()
            self.image.save(stream, format='PNG')
            stream.seek(0)
            res['image'] = base64.b64encode(stream.read()).decode()
        return res

    def __str__(self):
        return '<Frame %s %s %s>' % (self.fclass, str(list(map(lambda x: float('%.4s' % x), self.rect))), self.text)


class Page:
    def __init__(self,
                 name: str='默认幻灯片',
                 position: Vec3=None,
                 size: list=None,
                 display: bool=True):
        self.frames = []
        self.display = display
        self.position = position
        self.size = size
        self.name = name
        if self.position is None:
            self.position = Vec3(0, 0, 0)
        if self.size is None:
            # 默认16:9分辨率
            self.size = [1024, 576]

        # 添加一个默认文本框
        # self.frames.append(Frame())
        # self.frames.append(Frame(image=Image.open('i.jpg')))

    def load(self, page):
        self.name = page['name']
        self.display = page['display']
        self.position = Vec3(0, 0, 0).load(page['position'])
        self.frames = []
        for frame in page['frames']:
            self.frames.append(Frame().load(frame))
        return self

    def json(self):
        frames = []
        for frame in self.frames:
            frames.append(frame.json())
        return {
            'name': self.name,
            'display': self.display,
            'position': self.position.json(),
            'frames': frames
        }


class PPT:
    def __init__(self):
        # 储存页面
        self.pages = []
        # 图片，下标就是索引号
        # self.images = []

        # 初始化一个页面
        # page = Page()
        # page.position.load([random.random() * 0.5 for i in range(3)])
        # self.pages.append(page)

        # for i in range(30):
        #     page = Page()
        #     # page.frames.append(Frame(image=Image.open('%s.png' % (i % 2 + 1))))
        #     page.frames.append(Frame())
        #     page.frames[0] = Frame(image=Image.open('%s.png' % (i % 2 + 1)))
        #     page.position.load([random.random() * 12.8 for i in range(3)])
        #     page.position.x += i
        #     self.pages.append(page)

    def load(self, ppt: dict=None, filename: str=None):
        if filename is not None:
            ppt = self.load_file(filename)
        if ppt is None:
            raise ValueError
        self.pages = []
        for page in ppt['pages']:
            self.pages.append(Page().load(page))
        return self

    def load_file(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError
        if not zipfile.is_zipfile(filename):
            raise ValueError
        with zipfile.ZipFile(filename, 'r') as f:
            try:
                with f.open('data.json', 'r') as fp:
                    data = fp.read()
                    ppt = json.loads(data)
                    return ppt
            except FileNotFoundError:
                raise FileNotFoundError

    def save(self, filename: str='save.p3d'):
        pages = []
        for page in self.pages:
            pages.append(page.json())
        ppt = {
            'pages': pages
        }
        # with open(filename, 'w') as f:
        #     f.write(json.dumps(ppt))
        with zipfile.ZipFile(filename, 'w') as f:
            with f.open('data.json', 'w') as fp:
                fp.write(json.dumps(ppt).encode())


if __name__ == '__main__':
    _ppt = PPT()
    # _ppt.save()
    _ppt.load(filename='save.p3d')
    # print(_ppt.pages[0].frames[0].json())
