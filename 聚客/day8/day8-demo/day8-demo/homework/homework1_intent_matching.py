# what：导入 HuggingFace 的 embedding 封装器。
# why：这道作业需要先把文本转换成向量，后面才能做相似度匹配。
# how：通过 LangChain 提供的 HuggingFaceEmbeddings 调用本地 embedding 模型。
from langchain_huggingface import HuggingFaceEmbeddings

# what：导入点积计算函数。
# why：余弦相似度公式里需要先计算两个向量的点积。
# how：使用 numpy.dot 计算两个向量按维度相乘后的求和结果。
from numpy import dot

# what：导入向量范数计算函数。
# why：余弦相似度公式的分母需要用到向量长度。
# how：使用 numpy.linalg.norm 计算向量的模长。
from numpy.linalg import norm

# what：准备意图样本库。
# why：如果只用“订餐、天气、音乐”这种短标签，语义信息太少，匹配容易不准。
# how：给每个意图准备几条更像用户真实表达的 sample，后面用 sample 做向量匹配。
intent_knowledge = [
    {"intent": "订餐", "sample": "我想点外卖"},
    {"intent": "订餐", "sample": "帮我订一份晚饭"},
    {"intent": "查询天气", "sample": "今天天气怎么样"},
    {"intent": "查询天气", "sample": "明天会下雨吗"},
    {"intent": "播放音乐", "sample": "我想听歌"},
    {"intent": "播放音乐", "sample": "放一首音乐"},
    {"intent": "设置闹钟", "sample": "明早七点叫我起床"},
    {"intent": "设置闹钟", "sample": "帮我设一个八点闹钟"},
    {"intent": "讲笑话", "sample": "说个笑话吧"},
    {"intent": "讲笑话", "sample": "讲个搞笑段子"},
]

# what：实例化 embedding 模型。
# why：后面 query 和 sample 都要用同一个模型编码，才能保证维度一致、可比较。
# how：使用 all-MiniLM-L6-v2 这个本地模型，输出 384 维向量。
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# what：定义“文本转向量”的通用函数。
# why：query 和 sample 都需要向量化，封装成函数后可复用。
# how：把传入的单条文本交给 embeddings.embed_query 生成向量。
def get_embedding(text):
    return embeddings.embed_query(text)


# what：定义余弦相似度函数。
# why：意图匹配的核心就是比较两个向量在语义空间里有多接近。
# how：按照 余弦相似度 = 点积 / (两个向量长度乘积) 计算。
def cosine_similarity(vec1, vec2):
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


# what：定义意图匹配主函数。
# why：这一步把“query 向量化、样本向量化、相似度比较、返回意图结果”串成完整流程。
# how：输入 query 和意图样本库，输出最匹配的 intent 和分数。
def match_intent(query, intent_knowledge):
    # what：把用户问题转换成向量。
    # why：后面只有把 query 放到向量空间里，才能和样本做数学比较。
    # how：调用前面封装好的 get_embedding。
    query_embedding = get_embedding(query)

    # what：把每条 sample 转成向量。
    # why：意图匹配不是拿 intent 标签做比较，而是拿更有语义信息的 sample 做比较。
    # how：遍历字典列表，取出 item["sample"] 后逐条向量化。
    intent_knowledge_embeddings = [get_embedding(item["sample"]) for item in intent_knowledge]

    # what：计算 query 和每条样本向量之间的相似度。
    # why：只有把所有候选意图都算一遍，才能知道谁最像用户当前这句话。
    # how：遍历样本向量列表，逐条调用 cosine_similarity。
    similarities = [
        cosine_similarity(query_embedding, intent_knowledge_embedding)
        for intent_knowledge_embedding in intent_knowledge_embeddings
    ]

    # what：找到最高相似度对应的位置。
    # why：最高分所在的下标，就是最匹配样本在知识库中的位置。
    # how：先取最大值，再用 index 找它在列表里的位置。
    most_similar_index = similarities.index(max(similarities))

    # what：返回匹配到的意图标签和最高分。
    # why：业务上我们关心的不是样本下标，而是最终意图和这次匹配的可信度。
    # how：用下标回到原始知识库里取 intent，同时返回最高分。
    return intent_knowledge[most_similar_index]["intent"], max(similarities)


# what：程序入口。
# why：只在直接运行这个脚本时做测试，避免被别的文件导入时自动执行。
# how：使用 __name__ == "__main__" 作为 Python 的标准入口判断。
if __name__ == "__main__":
    # what：准备几条测试 query。
    # why：用不同表述验证意图匹配是否真的能工作。
    # how：把测试问题放进列表，后面循环调用 match_intent。
    queries = ["我想听歌", "今天天气如何", "明早七点叫我起床"]

    # what：遍历测试 query。
    # why：一次性验证多种用户表达，而不是只测一条。
    # how：for 循环逐条取出 query。
    for query in queries:
        # what：执行一次意图匹配。
        # why：得到当前 query 的最匹配意图和分数。
        # how：把 query 和意图样本库传给 match_intent。
        matched_intent, score = match_intent(query, intent_knowledge)

        # what：打印当前 query。
        # why：输出多条测试结果时，需要先知道当前在看哪条问题。
        # how：使用 f-string 把 query 插入输出文本。
        print(f"query: {query}")

        # what：打印匹配到的意图。
        # why：这是这次意图识别的核心业务结果。
        # how：输出 matched_intent 变量。
        print(f"匹配意图: {matched_intent}")

        # what：打印相似度分数。
        # why：可以用来观察这次匹配是否足够可靠。
        # how：输出 score 变量。
        print(f"相似度分数: {score}")

        # what：打印分隔线。
        # why：让多条测试结果在终端中更容易区分。
        # how：输出 30 个连字符。
        print("-" * 30)
