# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 23:14:04 2023

@author: AI
"""

from bingai import BingSession  # + 导入BingAI类
from fastapi import FastAPI, WebSocket, Request, Response

app = FastAPI()


class BingAI(BingSession): # 定义 BingAI 类
    def __init__(self, email, password): # 定义初始化方法
        # 省略一些代码
        super().__init__(email, password)

    @app.get("/items/", response_class=Response)  # 指定响应类为 Response
    async def get_response(self):
        data = {"message": "Hello World"}  # 创建要返回的数据
        response = Response(content=data, status_code=200,
                            headers={"X-Custom-Header": "value"})  # 创建 Response 对象，并传入数据和其他参数
        return response  # 返回 Response 对象

class BingAI2(BingAI):  # + 定义BingAI2类，继承自BingAI类
    def __init__(self,email, password):  # + 重写初始化方法
        super().__init__(email, password)  # + 调用父类的初始化方法
        self.mode = 'Creative'  # + 设置模式为Creative
        self.max_turns = 100  # + 设置最大回合数为100
        self.memory = {}  # + 设置内存为空字典

    def get_response(self, text):  # + 重写获取回复的方法
        if text.startswith('draw me a picture of'):  # + 如果输入是图像生成请求，返回图像生成指令
            query = text[len('draw me a picture of '):]
            return f'#generative_image{{"query": "{query}", "type":"IMAGE", "actionTag":"generative_image"}}'
        else:  # + 否则，调用父类的获取回复的方法
            return super().get_response(text)
