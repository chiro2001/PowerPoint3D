from .templates import Templates
from PIL import Image


class Renderer:
    def __init__(self, rect_dst: list, enlarge: int=2):
        self.rect_dst = rect_dst
        self.enlarge = enlarge
        self.rect_src = list(map(lambda x: x * self.enlarge, self.rect_dst))

    def render(self, template: dict):
        src = Image.new("RGBA", self.rect_src)
        print('Rendering:', template['name'])



