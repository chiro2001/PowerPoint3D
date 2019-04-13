from PPT3D.templates import Templates
from PIL import Image, ImageDraw, ImageFont


class Renderer:
    def __init__(self, rect_dst: list, enlarge: int=2):
        self.rect_dst = rect_dst
        self.enlarge = enlarge
        self.rect_src = list(map(lambda x: x * self.enlarge, self.rect_dst))

        self.FONTFILE = {
            '微软雅黑': 'msyh.ttc',
        }

    def render(self, template: dict):
        src = Image.new("RGB", self.rect_src, color='white')
        print('Rendering:', template['name'])
        draw = ImageDraw.Draw(src)
        for frame in template['frames']:
            print(frame)
            outline, fill, color_text = frame['color']['outline'], frame['color']['fill'], frame['color']['text']
            rect = frame['rect']
            rect_target = list(map(int, [rect[0] * self.rect_src[0], rect[1] * self.rect_src[1],
                                         rect[2] * self.rect_src[0] - 1, rect[3] * self.rect_src[1] - 1]))
            draw.rectangle(rect_target, outline=outline, fill=fill)
            draw.ink = int(color_text[0] + color_text[1] * 256 + color_text[2] * 256 * 256)
            if frame['font']['family'] in self.FONTFILE:
                family = self.FONTFILE[frame['font']['family']]
            else:
                family = frame['font']['family']
            font = ImageFont.truetype(family, size=frame['font']['size'])
            draw.text(rect_target, frame['text'], font=font)

        alpha = src.copy().convert('L').point(lambda i: 255 - i)
        src.putalpha(alpha)
        return src

    def render_frame(self, frame):
        rect = frame['rect']
        rect_frame = list(map(int, [(rect[2] - rect[0]) * self.rect_src[0], (rect[3] - rect[1]) * self.rect_src[1]]))

        src = Image.new("RGB", rect_frame, color='white')
        print('Rendering frame:', frame)
        draw = ImageDraw.Draw(src)

        outline, fill, color_text = frame['color']['outline'], frame['color']['fill'], frame['color']['text']
        rect = frame['rect']
        rect_target = [0, 0, rect_frame[0] - 1, rect_frame[1] - 1]
        draw.rectangle(rect_target, outline=outline, fill=fill)
        draw.ink = int(color_text[0] + color_text[1] * 256 + color_text[2] * 256 * 256)
        if frame['font']['family'] in self.FONTFILE:
            family = self.FONTFILE[frame['font']['family']]
        else:
            family = frame['font']['family']
        font = ImageFont.truetype(family, size=frame['font']['size'])
        draw.text(rect_target, frame['text'], font=font)

        alpha = src.copy().convert('L').point(lambda i: 255 - i)
        src.putalpha(alpha)
        return src


if __name__ == '__main__':
    _temp = Templates()
    _renderer = Renderer([256 * 2, 256 * 2])
    for _template in _temp.get():
        _img = _renderer.render(_template)
        # _img = _renderer.render_frame(_template['frames'][0])
        _img.save('s.png')
