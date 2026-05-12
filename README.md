# 老娘舅小天地网页

一个简易的静态网页，结合网上找到的老娘舅风格图片，为阿德哥与阿庆制作可点击的头像互动场景。

## 使用方式

1. 将仓库下载或克隆到本地。
2. 使用任意静态网页服务器（如 VS Code Live Server、`python -m http.server` 等）或直接双击 `index.html` 在浏览器中打开。
3. 点击人物头像即可查看对应角色的性格台词。

## 结构说明

- `index.html`：页面主体结构。
- `styles.css`：页面样式与布局。
- `script.js`：处理头像点击的交互逻辑。

> 页面中引用的图片均来源于互联网公开资源，仅作学习演示使用。


## 角色素材（透明 PNG）预处理

已新增素材处理脚本，可将原始剧照批量转换为统一尺寸、透明背景 PNG。

```bash
python scripts/prepare_character_assets.py --size 768
```

详细说明见 `assets/README.md`。

## 视频场景自动截图

如果你想从整段视频里快速找“好玩表情”，可以用下面这个脚本按场景变化自动导出截图：

```bash
pip install opencv-python numpy
python scripts/extract_scene_frames.py --input path/to/video.mp4 --output-dir assets/scene_frames
```

常用参数：

- `--threshold`：场景变化阈值（默认 `0.40`，越小越容易出图）
- `--min-interval`：相邻截图最小间隔秒数（默认 `1.5`）
- `--max-shots`：最多导出多少张图（默认 `0` 表示不限）

输出文件名会包含序号和时间戳，方便你回到原视频精修挑选。
