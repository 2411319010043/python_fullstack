# what：导入 requests，用来发送 HTTP 请求
# why：真实天气数据来自外部天气 API，需要通过网络请求获取
# how：requests.get(url, params=...) 发送 GET 请求并用 response.json() 解析结果
import requests
# what：把普通函数快速封装成 LangChain Tool
# why：天气查询函数需要变成 Agent 可调用的工具
# how：在函数上方加 @tool
from langchain_core.tools import tool
# what：从项目配置中导入天气相关 API 地址
# why：GEO_URL 和 WEATHER_URL 统一放在 config.py 中读取，避免在工具文件里重复读取 .env
# how：GEO_URL 用于城市转经纬度，WEATHER_URL 用于根据经纬度查询天气
from config import GEO_URL, WEATHER_URL

# 天气查询 Tool

# what：把 Open-Meteo 的 weather_code 转成中文天气描述
# why：API 返回的是数字代码，用户更容易理解中文描述
# how：根据常见 weather_code 分组返回对应中文文本
def weather_code_to_text(code: int) -> str:
    if code == 0:
        return "晴"
    elif code in [1, 2, 3]:
        return "多云"
    elif code in [45, 48]:
        return "有雾"
    elif code in [51, 53, 55, 61, 63, 65]:
        return "有雨"
    elif code in [71, 73, 75]:
        return "有雪"
    else:
        return "未知天气"


# what：get_weather 是天气查询 Tool
# why：Agent 需要一个外部工具来回答实时天气类问题
# how：接收 city 字符串，先查询城市经纬度，再根据经纬度查询真实天气
@tool
def get_weather(city: str) -> str:

    # what：这是 Tool 的 docstring，也就是工具说明。
    # why：Agent / 大模型会根据这段说明判断什么时候调用天气工具。
    # how：写清楚工具用途、输入是什么、返回什么。
    """根据城市名称查询当前天气，返回天气状况和温度。适合回答实时天气相关问题。"""

    # what：构造请求地理编码 API 的参数字典。
    # why：Open-Meteo 的地理编码接口需要知道你要查哪个城市，以及返回几条结果、语言和格式。
    # how：name=city 表示要查询的城市名。count=1 表示只取最相关的 1 个结果。language="zh" 表示返回中文结果。format="json" 表示返回 JSON 格式。
    geo_params = {
        "name": city,
        "count": 1,
        "language": "zh",
        "format": "json",
    }

    # what：向地理编码 API 发送 GET 请求。
    # why：我们需要把城市名转换成经纬度，天气 API 才能查询真实天气。
    # how：GEO_URL 从 config.py 导入；params=geo_params 会把参数拼到 URL 查询字符串里；requests.get(...) 会发起网络请求，并返回响应对象。
    geo_response = requests.get(GEO_URL, params=geo_params)

    # what：把 API 返回的 JSON 响应解析成 Python 字典。
    # why：HTTP 响应原本是文本/字节，程序要取里面的 results、latitude、longitude，需要先解析成 dict。
    # how：response.json() 会把 JSON 字符串转换成 Python dict。
    geo_data = geo_response.json()

    # what：检查地理编码结果中是否有 results
    # why：避免城市查不到时程序报错
    # how：如果没有 results，直接返回提示文本
    if "results" not in geo_data:
        return f"没有找到城市：{city}"
    
    # what：取地理编码结果中的第一条地点信息
    # why：count=1 时只需要最相关的城市结果
    # how：geo_data["results"][0] 取 results 列表第一个元素
    location = geo_data["results"][0]
    # what：取城市纬度和经度
    # why：天气 API 需要经纬度才能查询天气
    # how：从 location 字典中读取 latitude 和 longitude
    latitude = location["latitude"]
    longitude = location["longitude"]
    # what：取 API 返回的标准城市名
    # why：返回天气结果时使用标准名称更清楚
    # how：从 location["name"] 读取
    location_name = location["name"]

    # what：构建请求天气 API 的参数字典。
    # why：天气 API 不能只靠城市名查询，需要经纬度，并且要指定想获取哪些当前天气字段。
    # how：latitude/longitude 来自地理编码结果；
        # current 指定要返回 temperature_2m、weather_code、wind_speed_10m；
        # timezone 指定使用 Asia/Shanghai 时区。
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "timezone": "Asia/Shanghai",
    }

    # what：向Open-Meteo 天气接口地址发送 GET 请求。
    # why：拿到经纬度后，需要请求天气接口获取真实当前天气数据。
    # how：WEATHER_URL 从 config.py 导入；params=weather_params 会把参数拼到 URL 查询字符串里；requests.get(...) 会发起网络请求，并返回响应对象。
    weather_response = requests.get(WEATHER_URL,params=weather_params)
    # what：把 API 返回的 JSON 响应解析成 Python 字典。
    # why：HTTP 响应原本是文本/字节，需要先解析成 dict。
    # how：response.json() 会把 JSON 字符串转换成 Python dict。
    weather_data = weather_response.json()
    # what：取出当前天气数据对象。
    # why：temperature_2m、weather_code、wind_speed_10m 都在 current 字段里。
    # how：从 weather_data 字典中通过 "current" key 读取。
    current = weather_data["current"]

    # what：取当前温度
    # why：天气回答需要告诉用户温度
    # how：从 current["temperature_2m"] 读取
    temperature = current["temperature_2m"]
    # what：取天气代码
    # why：API 用数字表示天气状况
    # how：从 current["weather_code"] 读取
    weather_code = current["weather_code"]
    # what：取当前风速
    # why：天气回答需要告诉用户风速
    # how：从 current["wind_speed_10m"] 读取
    wind_speed = current["wind_speed_10m"]
    # what：把天气代码转成中文描述
    # why：用户看中文天气描述比数字代码更直观
    # how：调用 weather_code_to_text(weather_code)
    weather_text = weather_code_to_text(weather_code)

    # what：返回最终天气查询结果
    # why：Agent 需要把 Tool 的返回值交给模型，用来组织最终回答
    # how：用 f-string 拼接城市名、天气描述、温度和风速
    return f"{location_name}当前天气：{weather_text}，温度 {temperature}°C，风速 {wind_speed} km/h。"




