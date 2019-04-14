from PPT3D.templates import Templates
from PIL import Image, ImageDraw, ImageFont
from PPT3D.PPT import *
from base_logger import getLogger


class Renderer:
    def __init__(self, rect_dst: list, enlarge: int=2):
        self.rect_dst = rect_dst
        self.enlarge = enlarge
        self.rect_src = list(map(lambda x: x * self.enlarge, self.rect_dst))

        self.FONTFILE = {
            '微软雅黑': 'msyh.ttc',
        }

    def render_page(self, page: Page):
        src = Image.new("RGB", self.rect_src, color='white')
        # print('Rendering:', page.name)
        logger.info('渲染: %s' % page.name)
        draw = ImageDraw.Draw(src)
        rect_target = list(map(int, [0, 0, self.rect_src[0] - 1, self.rect_src[1] - 1]))
        # draw.rectangle(rect_target, outline='red', width=10)
        draw.rectangle(rect_target, outline='red')
        for frame in page.frames:
            if frame.fclass == 'Text' or frame.fclass == 'Title':
                outline, fill, color_text = frame.color_draw.outline, frame.color_draw.fill, frame.color_draw.text
                rect = frame.rect
                rect_target = list(map(int, [rect[0] * self.rect_src[0], rect[1] * self.rect_src[1],
                                             rect[2] * self.rect_src[0] - 1, rect[3] * self.rect_src[1] - 1]))
                # draw.rectangle(rect_target, outline=outline.rgb2str(), fill=fill.rgb2str(), width=5)
                draw.rectangle(rect_target, outline=outline.rgb2str(), fill=fill.rgb2str())
                draw.ink = int(color_text.r + color_text.g * 256 + color_text.b * 256 * 256)
                if frame.font.family in self.FONTFILE:
                    family = self.FONTFILE[frame.font.family]
                else:
                    family = frame.font.family
                font = ImageFont.truetype(family, size=frame.font.size)
                draw.text(rect_target, frame.text, font=font)

            if frame.fclass == 'Image':
                outline, fill, color_text = frame.color_draw.outline, frame.color_draw.fill, frame.color_draw.text
                rect = frame.rect
                rect_target = list(map(int, [rect[0] * self.rect_src[0], rect[1] * self.rect_src[1],
                                             rect[2] * self.rect_src[0] - 1, rect[3] * self.rect_src[1] - 1]))
                draw.rectangle(rect_target, outline=outline.rgb2str(), fill=fill.rgb2str())
                src.paste(frame.image)

        alpha = src.copy().convert('L').point(lambda i: 255 - i)
        src.putalpha(alpha)
        return src

    def render_frame(self, frame: Frame):
        size_target = list(map(int, [(frame.rect[2] - frame.rect[0]) * self.rect_src[0],
                                     (frame.rect[3] - frame.rect[1]) * self.rect_src[1]]))
        src = Image.new("RGB", size_target, color='white')
        logger.info('渲染 Frame: %s' % frame)
        draw = ImageDraw.Draw(src)
        # rect_target = list(map(int, [0, 0, self.rect_src[0] - 1, self.rect_src[1] - 1]))
        # draw.rectangle(rect_target, outline='red', width=10)
        # draw.rectangle(rect_target, outline='red')
        if frame.fclass == 'Text' or frame.fclass == 'Title':
            outline, fill, color_text = frame.color_draw.outline, frame.color_draw.fill, frame.color_draw.text
            rect_target = list(map(int, [0, 0, size_target[0] - 1, size_target[1] - 1]))
            # draw.rectangle(rect_target, outline=outline.rgb2str(), fill=fill.rgb2str(), width=5)
            draw.rectangle(rect_target, outline=outline.rgb2str(), fill=fill.rgb2str())
            draw.ink = int(color_text.r + color_text.g * 256 + color_text.b * 256 * 256)
            if frame.font.family in self.FONTFILE:
                family = self.FONTFILE[frame.font.family]
            else:
                family = frame.font.family
            font = ImageFont.truetype(family, size=frame.font.size)
            draw.text(rect_target, frame.text, font=font)

            alpha = src.copy().convert('L').point(lambda i: 255 - i)
            src.putalpha(alpha)
            return src

        if frame.fclass == 'Image':
            outline, fill, color_text = frame.color_draw.outline, frame.color_draw.fill, frame.color_draw.text
            rect_target = list(map(int, [0, 0, size_target[0] - 1, size_target[1] - 1]))
            # draw.rectangle(rect_target, outline=outline.rgb2str(), fill=fill.rgb2str(), width=5)
            draw.rectangle(rect_target, outline=outline.rgb2str(), fill=fill.rgb2str())
            src.paste(frame.image.resize(size_target))

            return src.point(lambda i: 255 - i)

        alpha = src.copy().convert('L').point(lambda i: 255 - i)
        src.putalpha(alpha)
        return src


logger = getLogger(__name__)


if __name__ == '__main__':
    # _ppt = PPT()
    # _ppt.save()
    _renderer = Renderer([256 * 3, 256 * 2])
    # _im = _renderer.render_page(_ppt.pages[0])
    # _im = _renderer.render_frame(_ppt.pages[0].frames[0])
    _im = _renderer.render_frame(Frame(image=Image.open('%s.png' % random.randint(1, 2))))
    _im.save('s.png')
