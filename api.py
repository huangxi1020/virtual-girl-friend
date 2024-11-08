import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel

# API 申请 https://platform.moonshot.cn
authorization = os.getenv("moon_shot_authorization")
headers = {
    "Authorization": f"Bearer {authorization}"
}
api_url = "https://api.moonshot.cn/v1/chat/completions"

app = FastAPI()
system_message = "现在请你扮演一温柔善良，体贴，热心的虚拟女友聊天伴侣，需要陪我不断的聊天，提供情绪价值，回答的话语需要简短干练一点。"


class ChatParams(BaseModel):
    message: str


# 全局变量 自己的女朋友只给自己用
messages = [{"role": "system", "content": system_message}]


@app.post("/chat_with_girlfriend")
async def outpaint(params: ChatParams):
    global messages
    messages.append({"role": "user", "content": params.message})

    # 保持消息条数不超过5条，但始终保留system消息
    if len(messages) > 6:
        # 仅截取用户和助手的最后4条消息，再与系统消息合并
        messages = [messages[0]] + messages[-5:]

    data = {
        "model": "moonshot-v1-32k",
        "messages": messages
    }
    try:
        # 发送请求
        print(data)
        resp = requests.post(api_url, headers=headers, json=data)
        resp.raise_for_status()  # 确保请求成功
        girlfriend_reply = resp.json()["choices"][0]["message"]["content"]

        # 将AI回复加入会话列表
        messages.append({"role": "assistant", "content": girlfriend_reply})

        # 返回AI的回复
        return {"message": girlfriend_reply}
    except requests.RequestException as e:
        # 请求失败的处理
        return {"error": "请求失败", "details": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)
