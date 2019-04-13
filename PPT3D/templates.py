import json

samples = [
    # page
    {
        'name': '仅标题',
        'display': True,
        'position': [0, 0, 0],
        'frames': [
            {
                'class': 'Title',
                'rect': [0.1, 0.45, 0.9, 0.55],
                'text': '标题',
                'font': {
                    'family': '微软雅黑',
                    'size': 32,
                },
                'color': {
                    'outline': None,
                    'fill': None,
                    'text': [0, 0, 0],
                }
            },
        ]
    },
    {
        'name': '标题+正文',
        'display': True,
        'position': [0, 0, 0],
        'frames': [
            {
                'class': 'Title',
                'rect': [0.1, 0.15, 0.9, 0.25],
                'text': '标题',
                'font': {
                    'family': '微软雅黑',
                    'size': 64,
                },
                'color': {
                    'outline': '#FF0000',
                    'fill': None,
                    'text': [0, 0, 0],
                }
            },
            {
                'class': 'Text',
                'rect': [0.1, 0.35, 0.9, 0.85],
                'text': '内容',
                'font': {
                    'family': '微软雅黑',
                    'size': 32,
                },
                'color': {
                    'outline': '#FF0000',
                    'fill': None,
                    'text': [0, 0, 0],
                }
            },
        ]
    }
]


class Templates:
    def __init__(self):
        self.FILENAME = 'templates.json'
        self.templates = None
        self.reload()

    def reload(self):
        # try:
        #     with open(self.FILENAME, 'r') as f:
        #         self.templates = json.loads(f.read())
        # except FileNotFoundError:
        #     self.templates = samples
        #     with open(self.FILENAME, 'w') as f:
        #         f.write(json.dumps(self.templates))
        self.templates = samples
        with open(self.FILENAME, 'w') as f:
            f.write(json.dumps(self.templates))

    def get(self, index: int = None):
        if index is None:
            return self.templates
        return self.templates[index]


if __name__ == '__main__':
    _temp = Templates()
