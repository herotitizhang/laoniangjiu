# JRPG 对话素材准备

我已把你指定的 6 个角色整理成统一的处理流程：

- 毛猛达
- 陈国庆
- 姚祺儿
- 李九松
- 嫩娘
- 朱桢

## 目录说明

- `assets/raw/`：放原始剧照（建议每个角色放 2~5 张备选）。
- `assets/portraits/`：导出的透明背景、统一尺寸 PNG。
- `assets/source_log.csv`：记录素材来源与授权说明，便于后续管理。

## 推荐命名

把原图命名为“人物名_序号”，例如：

- `毛猛达_01.jpg`
- `陈国庆_01.jpg`
- `姚祺儿_01.jpg`
- `李九松_01.jpg`
- `嫩娘_01.jpg`
- `朱桢_01.jpg`

## 批量处理命令

先安装依赖：

```bash
pip install pillow rembg onnxruntime
# 若只做尺寸统一可不装 rembg
```

执行处理：

```bash
python scripts/prepare_character_assets.py --size 768
```

处理完成后，会在 `assets/portraits/` 生成以下文件：

- `mao_mengda.png`
- `chen_guoqing.png`
- `yao_qier.png`
- `li_jiusong.png`
- `nen_niang.png`
- `zhu_zhen.png`

## 来源记录

请把每张图的来源 URL、截图时间、使用限制记录到 `assets/source_log.csv`。

> 提醒：剧照通常受版权保护。建议仅用于学习/原型演示，正式发布前请确认授权。


## rembg 缺失时的行为

若未安装 `rembg`，脚本不会报错退出，而是自动降级为：

- 保留原图内容（不抠透明背景）
- 仍会统一尺寸并导出 PNG

可显式关闭抠图：

```bash
python scripts/prepare_character_assets.py --size 768 --disable-rembg
```
