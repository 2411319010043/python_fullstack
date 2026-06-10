# LangChain 综合智能助手项目

这是一个基于 LangChain 搭建的综合智能助手项目。

项目集成了多种能力，包括：

1. 普通聊天
2. 实时天气查询
3. 网页搜索
4. 维基百科查询
5. 图片理解
6. 结构化输出

当用户提出问题时，系统会根据问题类型决定是直接由大模型回答，还是调用对应工具完成任务。  
如果需要统一输出格式，还可以通过 output parser 对回答结果进行二次结构化整理。

## 项目结构

```text
day7-langchain-tools-agent/
├─ agents/        # Agent 组装与调度
├─ examples/      # 各模块单独运行示例
├─ parsers/       # 输出格式化处理
├─ tools/         # 各类工具实现
├─ web/           # Web 页面与后端接口
├─ config.py      # 项目统一配置
├─ requirements.txt
└─ README.md
```

## 各目录说明

### 1. agents

负责创建综合 Agent，把模型和多个工具组合在一起。  
用户提问后， Agent 会判断是直接回答，还是调用天气、搜索、维基百科、图片理解等工具。

### 2. examples

负责单独测试和演示项目中的各个功能。

例如：

- `run_agent.py`：测试综合 Agent
- `run_wikipedia_tool.py`：测试维基百科工具
- `run_output_parsers.py`：测试输出解析器

### 3. parsers

负责对模型已经生成好的自然语言回答进行二次整理，  
把结果统一转换成 JSON 或 XML 等结构化格式。

### 4. tools

负责具体功能实现。

例如：

- `weather_tool.py`：查询实时天气
- `search_tool.py`：网页搜索
- `wikipedia_tool.py`：查询维基百科
- `image_tool.py`：图片理解

### 5. web

负责 Web 应用层，包括前端页面和后端接口。  
用户可以在浏览器中输入问题或图片地址，直接测试整个综合助手项目。

### 6. config.py

负责统一管理项目配置，例如模型名称、API Key、Base URL、天气接口地址等。

## 项目工作流程

```text
1. 用户输入问题
2. 系统判断问题类型
3. 如果是普通问题，直接由模型回答
4. 如果是天气、搜索、维基百科、图片类问题，则调用对应工具
5. 工具执行后，将结果交给模型组织成自然语言回答
6. 如果需要统一格式，再通过 parser 进行二次结构化输出
7. 最终将自然语言结果或结构化结果返回给用户
```

## 环境配置

建议使用 Python 虚拟环境运行本项目。

### 1. 安装依赖

在项目根目录下执行：

```bash
pip install -r requirements.txt
```

### 2. 配置 `.env` 文件

项目运行前需要在根目录下配置 `.env` 文件，常用配置项如下：

```env
OPENAI_API_KEY=你的模型密钥
OPENAI_BASE_URL=你的模型接口地址
OPENAI_MODEL=gpt-4o-mini

GEO_URL=地理编码接口地址
WEATHER_URL=天气接口地址

TAVILY_API_KEY=你的 Tavily 搜索密钥
```

配置项说明：

- `OPENAI_API_KEY`：大模型接口密钥
- `OPENAI_BASE_URL`：模型服务地址
- `OPENAI_MODEL`：项目默认使用的模型名称
- `GEO_URL`：城市转经纬度的接口地址
- `WEATHER_URL`：天气查询接口地址
- `TAVILY_API_KEY`：网页搜索功能需要的密钥

## 运行示例

### 1. 测试综合 Agent

```bash
python -m examples.run_agent
```

### 2. 测试维基百科工具

```bash
python -m examples.run_wikipedia_tool
```

### 3. 测试输出解析器

```bash
python -m examples.run_output_parsers
```

## 启动 Web 页面

在项目根目录下执行：

```bash
python -m uvicorn web.app:app --host 127.0.0.1 --port 8010
```

如果当前环境不是项目使用的虚拟环境，也可以使用：

```bash
D:\Anaconda3\envs\py-fullstack-dev\python.exe -m uvicorn web.app:app --host 127.0.0.1 --port 8010
```

启动成功后，在浏览器中打开：

```text
http://127.0.0.1:8010
```

## 页面测试方式

前端页面提供两个输入项：

1. `question`：用户问题
2. `image_source`：图片路径或公网图片 URL（可选）

使用方式如下：

### 1. 普通聊天

只填写 `question`，例如：

```text
你好，介绍一下你自己
```

### 2. 天气查询

只填写 `question`，例如：

```text
今天北京天气怎么样？
```

### 3. 搜索 / 维基百科

只填写 `question`，例如：

```text
帮我搜索一下 LangChain 最新版本更新了什么
```

或者：

```text
LangChain 是什么
```

### 4. 图片理解

同时填写：

- `question`
- `image_source`

例如：

```text
question:
请描述这张图片里有什么

image_source:
D:\xxx\scene1.jpg
```

也可以使用公网图片 URL。

## 接口说明

### `POST /api/agent`

请求体示例：

```json
{
  "question": "今天北京天气怎么样？",
  "image_source": null
}
```

图片理解示例：

```json
{
  "question": "请描述这张图片里有什么",
  "image_source": "https://example.com/demo.jpg"
}
```

返回结果示例：

```json
{
  "task_type": "weather",
  "answer": "今天北京的天气是晴，温度为27.0°C，风速为9.9 km/h。",
  "structured": {
    "task_type": "weather",
    "summary": "今天北京天气晴，温度为27.0°C，风速为9.9 km/h。",
    "key_points": [
      "天气：晴",
      "温度：27.0°C",
      "风速：9.9 km/h"
    ]
  }
}
```

## Web 模块补充说明

Web 模块提供统一入口：

- 如果用户只输入 `question`，则走综合 Agent
- 如果用户同时提供 `image_source`，则直接走图片理解工具
- 后端最终返回两部分内容：
  - `answer`：自然语言回答
  - `structured`：结构化 JSON 结果

## 项目特点

1. 将多个独立作业整合成一个完整项目
2. 支持工具化调用与 Agent 自动调度
3. 支持自然语言回答与结构化输出两种结果形式
4. 支持本地图片路径和公网图片 URL
5. 支持浏览器页面直接测试功能
