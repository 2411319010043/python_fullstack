# 演示如何调用 tools/image_tool.py 里的 image_understanding_tool。

from tools.image_tool import image_understanding_tool

def main() -> None:
    result = image_understanding_tool.invoke(
        {
            "image_source":r"D:\yl-workplace\github_code\python_fullstack\聚客\day7\day7-demo\day7-demo\images\scene1.jpg",
            "question":"这张图片里有什么？请用中文描述。",
        }
    )

    print(result)

if __name__ == "__main__":
    main()