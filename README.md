# HD Card Generator

基于模板的卡片图片生成服务。通过 HTML 叠加文字到背景模板图上，使用 Playwright 截图输出 PNG。支持 HTTP API 和 CLI 两种使用方式。

## 工作原理

```
title + tutor  -->  HTML 模板（文字叠加到背景图上）  -->  Playwright 截图  -->  PNG
```

## Docker 部署（推荐）

### 构建镜像

```bash
docker build -t hd-card-generator .
```

### 启动服务

```bash
docker run -d -p 8000:8000 hd-card-generator
```

### 调用 API

```bash
curl -X POST http://localhost:8000/render \
  -H "Content-Type: application/json" \
  -d '{"title": "COMP1100 期中考试", "tutor": "Tutor Ruby"}' \
  --output card.png
```

### API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/render` | 生成卡片，返回 PNG 图片 |
| GET | `/health` | 健康检查 |

**POST /render 请求体：**

```json
{
  "title": "COMP1100 期中考试",
  "tutor": "Tutor Ruby"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 大标题文字 |
| `tutor` | string | Tutor 名字 |

**响应：** `image/png` 二进制图片流

## CLI 使用

### 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

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

### CLI 配置格式

```json
{
  "title": "COMP1100 期中考试",
  "tutor": "Tutor Ruby",
  "template": "templates/template.png",
  "output": "output/card.png"
}
```

## 自定义模板

- 替换 `templates/template.png` 为你自己的背景图
- 编辑 `template.html` 调整文字位置、字号、颜色等 CSS 样式
- HTML 使用 Google Fonts（Noto Sans SC）确保中文渲染正常

## 项目结构

```
hd-card-generator/
├── app.py               # FastAPI 服务
├── render.py            # 核心渲染逻辑 + CLI 入口
├── template.html        # HTML 模板（含占位符）
├── Dockerfile           # Docker 构建文件
├── requirements.txt     # Python 依赖
├── templates/
│   └── template.png     # 背景模板图片
├── config.json          # CLI 默认配置
├── examples/            # CLI 批量配置示例
│   ├── card_comp1100.json
│   └── card_acct3101.json
└── output/              # CLI 生成结果（已 gitignore）
```
