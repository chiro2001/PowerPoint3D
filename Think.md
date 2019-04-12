# 想法

## 设置

### 储存

json
```
Settings
    display
        distance float
        enlarge float
```

## 模板

### 储存

json
```
Templates[]:
    [0]:
        name str
        frames[]:
            class str ("Title", "Text", "Image")
            text str
            rect [0, 0, 0, 0]
            abs_z float
            font:
                family str
                size int
        
```

## 坐标变换

- 设置模板：范围 [0, 1]
- 储存屏幕大小
- 使用的画布大小：窗口大小/屏幕大小

## 其他

- [GLFW用](https://www.glfw.org/download.html)
