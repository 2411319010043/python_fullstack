# what：导入 HuggingFace 的 embedding 封装器。
# why：问答助手和意图匹配一样，都先要做文本向量化。
# how：使用 LangChain 的 HuggingFaceEmbeddings 调用本地 embedding 模型。
from langchain_huggingface import HuggingFaceEmbeddings

# what：导入点积函数。
# why：余弦相似度公式需要先算向量点积。
# how：使用 numpy.dot 做向量逐维相乘再求和。
from numpy import dot

# what：导入范数函数。
# why：余弦相似度的分母需要向量长度。
# how：使用 numpy.linalg.norm 计算向量模长。
from numpy.linalg import norm

# what：准备问答知识库。
# why：这道题不是让 LLM 生成答案，而是从已有标准问答对里匹配最相似问题并返回答案。
# how：每条数据保存 question 和 answer 两个字段。
qa_knowledge = [
    {"question": "今天天气怎么样", "answer": "你可以打开天气应用查询今天的天气。"},
    {"question": "我想听歌", "answer": "好的，我可以帮你播放音乐。"},
    {"question": "明早七点叫我起床", "answer": "好的，我可以帮你设置一个明早七点的闹钟。"},
    {"question": "我想订外卖", "answer": "你可以打开外卖软件。"},
]

# what：实例化 embedding 模型。
# why：后面 query 和知识库中的 question 都要用同一个模型编码。
# how：仍然使用 all-MiniLM-L6-v2。
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# what：定义单条文本向量化函数。
# why：query 和 question 的编码逻辑完全一样，封装后便于复用。
# how：把传入的 text 交给 embeddings.embed_query 生成向量。
def get_embedding(text):
    return embeddings.embed_query(text)


# what：定义余弦相似度函数。
# why：问答助手的核心是判断“用户问题”和“知识库问题”语义是否接近。
# how：按照标准余弦相似度公式计算。
def cosine_similarity(vec1, vec2):
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


# what：定义问答助手核心函数。
# why：这一步把“匹配问题”和“返回对应答案”连成完整流程。
# how：输入 query 和问答知识库，输出最匹配 answer 和分数。
def answer_question(query, qa_knowledge):
    # what：把用户问题转换成向量。
    # why：只有把 query 放进向量空间里，才能和知识库里的问题做比较。
    # how：调用 get_embedding 获取 query 向量。
    query_embedding = get_embedding(query)

    # what：把知识库中的每个 question 转成向量。
    # why：问答匹配比较的是 question，不是 answer。
    # how：遍历字典列表，取出 item["question"] 逐条向量化。
    question_embeddings = [get_embedding(item["question"]) for item in qa_knowledge]

    # what：计算 query 和每个 question 之间的相似度。
    # why：只有算出所有候选问题的分数，才能知道最像哪一条。
    # how：遍历问题向量，逐个调用 cosine_similarity。
    similarities = [
        cosine_similarity(query_embedding, question_embedding)
        for question_embedding in question_embeddings
    ]

    # what：找到最相似 question 的位置。
    # why：这个下标可以帮助我们回到原始知识库里拿到对应 answer。
    # how：先取最大分数，再找它在 similarities 中的位置。
    most_similar_index = similarities.index(max(similarities))

    # what：返回匹配到的 answer 和分数。
    # why：问答助手最终业务上要给用户的是答案，而不是知识库里那条 question。
    # how：用 most_similar_index 回到 qa_knowledge 中取出 answer。
    return qa_knowledge[most_similar_index]["answer"], max(similarities)


# what：程序入口。
# why：只有直接运行当前脚本时才执行测试逻辑。
# how：用 Python 的 __main__ 判断。
if __name__ == "__main__":
    # what：准备测试问题列表。
    # why：通过多条 query 验证问答匹配效果。
    # how：把测试问题放进列表中，后面逐条调用 answer_question。
    queries = ["我想听歌", "今天天气如何", "明早七点叫我起床"]

    # what：遍历测试问题。
    # why：一次性看到多条 query 的返回结果。
    # how：for 循环逐个取出 query。
    for query in queries:
        # what：调用问答助手核心函数。
        # why：得到最匹配的 answer 和相似度分数。
        # how：把当前 query 和知识库传给 answer_question。
        matched_answer, score = answer_question(query, qa_knowledge)

        # what：打印当前 query。
        # why：方便知道当前展示的是哪次提问。
        # how：用 f-string 输出 query。
        print(f"query: {query}")

        # what：打印匹配到的 answer。
        # why：这是问答助手要返回给用户的最终结果。
        # how：输出 matched_answer 变量。
        print(f"匹配答案: {matched_answer}")

        # what：打印相似度分数。
        # why：用于观察这次问答匹配的可信度。
        # how：输出 score。
        print(f"相似度分数: {score}")

        # what：打印分隔线。
        # why：让多条测试输出更清晰。
        # how：输出 30 个连字符。
        print("-" * 30)
