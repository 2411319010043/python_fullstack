# what：导入统一结构化输出的 JSON 和 XML 格式化函数
# why：run_output_parsers.py 只负责演示调用，不重复定义 parser 逻辑
# how：从 parsers.output_parsers_demo 导入 format_text_as_json 和 format_text_as_xml
from parsers.output_parsers_demo import format_text_as_json, format_text_as_xml

# what：定义 Output Parser 演示入口函数
# why：把运行逻辑集中到 main 中，便于直接运行和后续扩展
# how：准备原始文本，分别调用 JSON 和 XML 格式化函数，并打印结果
def main():
    weather_text = "北京当前天气：晴，温度 22.8°C，风速 5.1 km/h。"
    image_text = "图片展示了一条木栈道，穿过绿色草地，天空晴朗，整体是自然风景场景。"

    json_result = format_text_as_json("weather", weather_text)
    xml_result = format_text_as_xml("image", image_text)

    print(json_result)
    print(xml_result)

if __name__ == "__main__":
    main()