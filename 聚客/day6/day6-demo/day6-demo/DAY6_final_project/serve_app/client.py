import requests

# response1 = requests.post(url="http://127.0.0.1:8012/fixed/invoke",
#                          json={"input":{"question":"什么是LangServe?"}}
#                         )

# response2 = requests.post(url="http://127.0.0.1:8012/selector/invoke",
#                          json={"input":{"question":"什么是LangServe?"}}
#                         )
# print(response1.json())
# print("---------------------------------")
# print(response2.json())


# response3 = requests.post(
#     url="http://127.0.0.1:8012/history/invoke",
#     json={"input":{"question":"我叫小王。"},
#           "config":{"configurable":{"session_id":"u1"}}
#         }
# )
# print(response3.json()["output"]["content"])

# response4 = requests.post(
#     url="http://127.0.0.1:8012/history/invoke",
#     json={"input":{"question":"我叫什么？"},
#           "config":{"configurable":{"session_id":"u1"}}
#         }
# )
# print(response4.json()["output"]["content"])

# chat
response5 = requests.post(
    url="http://127.0.0.1:8012/chat/invoke",
    json={"input":{"question":"什么是 LangChain?"},
          "config":{"configurable":{"session_id":"u3"}}
        }
)
print(response5.json())


response6 = requests.post(
    url="http://127.0.0.1:8012/chat/invoke",
    json={"input":{"question":"我刚刚问了什么？"},
          "config":{"configurable":{"session_id":"u3"}}
        }
)
print(response6.json())
