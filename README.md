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
