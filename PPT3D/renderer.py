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
            draw.rectangle(frame['rect'], outline=outline, fill=fill)
            draw.ink = int(color_text[0] + color_text[1] * 256 + color_text[2] * 256 * 256)
            if frame['font']['family'] in self.FONTFILE:
                family = self.FONTFILE[frame['font']['family']]
            else:
                family = frame['font']['family']
            font = ImageFont.truetype(family, size=frame['font']['size'])
            draw.text([0, 0], frame['text'], font=font)
        return src


if __name__ == '__main__':
    _temp = Templates()
    _renderer = Renderer([256, 256])
    for _template in _temp.get():
        _img = _renderer.render(_template)
        _img.save('s.png')
