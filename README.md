# HD Card Generator

基于模板的卡片图片生成工具。通过 HTML 叠加文字到背景模板图上，使用 Playwright 截图输出 PNG。

## 工作原理

```
config.json  -->  HTML 模板（文字叠加到背景图上）  -->  Playwright 截图  -->  PNG
```

1. 读取 JSON 配置文件，获取大标题、小标题、Tutor 名字
2. 将配置注入 HTML 模板，文字通过 CSS 定位叠加在背景图上
3. 使用 Playwright（无头 Chromium）按模板原始尺寸截图
4. 输出像素级精准的 PNG 图片

## 安装

```bash
pip install -r requirements.txt
playwright install chromium
```

或使用 uv：

```bash
uv pip install -r requirements.txt
uv run playwright install chromium
```

## 使用方法

### 单张生成

```bash
python render.py
# 使用当前目录下的 config.json

python render.py --config my_card.json
# 指定配置文件
```

### 批量生成

```bash
python render.py --config examples/
# 处理文件夹下所有 .json 配置文件
```

## 配置格式

```json
{
  "title": "COMP1100 期中考试",
  "subtitle": "易错点 & 考前速通卡",
  "tutor": "Tutor Ruby",
  "template": "templates/template.png",
  "output": "output/card.png"
}
```

| 字段 | 说明 |
|------|------|
| `title` | 大标题文字（黄色区域上方，大字） |
| `subtitle` | 小标题文字（大标题下方，中号字） |
| `tutor` | Tutor 名字（底部渐变条区域） |
| `template` | 背景模板图片路径（相对项目根目录） |
| `output` | 输出 PNG 路径（相对项目根目录） |

## 自定义模板

- 替换 `templates/template.png` 为你自己的背景图
- 编辑 `template.html` 调整文字位置、字号、颜色等 CSS 样式
- HTML 使用 Google Fonts（Noto Sans SC）确保中文渲染正常

## 项目结构

```
hd-card-generator/
├── config.json          # 默认配置
├── render.py            # 渲染脚本
├── template.html        # HTML 模板（含占位符）
├── requirements.txt     # Python 依赖
├── templates/
│   └── template.png     # 背景模板图片
├── examples/            # 批量配置示例
│   ├── card_comp1100.json
│   └── card_acct3101.json
└── output/              # 生成结果（已 gitignore）
```
