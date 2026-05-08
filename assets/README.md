# JRPG 对话素材准备

我已把你指定的 6 个角色整理成统一的处理流程：

- 毛猛达
- 陈国庆
- 姚祺儿
- 李九松
- 嫩娘
- 朱桢

## 目录说明

- `assets/raw/`：按人物分文件夹放原始剧照（建议每个角色放 2~5 张备选）。
- `assets/portraits/`：导出的透明背景、统一尺寸 PNG。
- `assets/source_log.csv`：记录素材来源与授权说明，便于后续管理。

## 原图放置方式

每个人物都有自己的文件夹。你只需要把照片放进对应文件夹里，脚本会自动处理该人物文件夹里的所有支持图片。

```text
assets/raw/
  毛猛达/
    01.jpg
    02.jpg
  陈国庆/
    01.jpg
  姚祺儿/
    01.png
  李九松/
    01.webp
  嫩娘/
    01.jpg
  朱桢/
    01.jpg
```

支持格式：`.jpg`、`.jpeg`、`.png`、`.webp`。

## 批量处理命令

先安装依赖：

```bash
pip install pillow rembg onnxruntime
```

执行处理：

```bash
python scripts/prepare_character_assets.py --size 768
```

处理完成后，会在 `assets/portraits/` 下按人物生成文件夹，并保留原图文件名输出 PNG，例如：

```text
assets/portraits/
  mao_mengda/
    01.png
    02.png
  chen_guoqing/
    01.png
  yao_qier/
    01.png
  li_jiusong/
    01.png
  nen_niang/
    01.png
  zhu_zhen/
    01.png
```

## 来源记录

请把每张图的来源 URL、截图时间、使用限制记录到 `assets/source_log.csv`。

> 提醒：剧照通常受版权保护。建议仅用于学习/原型演示，正式发布前请确认授权。
