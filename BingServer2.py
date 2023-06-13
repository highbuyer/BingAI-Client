# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 23:14:04 2023

@author: AI
"""

import os
import sys
import json
import requests
import speech_recognition as sr # + 新增语音识别库
from PIL import Image # + 新增图像处理库
from transformers import pipeline # + 新增图像生成模块

# - from BingAI import BingAI
# - from BingAI import BingAISettings
# - from BingAI import BingAIContext

from BingAI2 import BingAI2 # + 新增BingAI2类，继承自BingAI类，添加了新的功能

# - bing = BingAI()
bing = BingAI2("cyhighbuyery@gmail.com", "b1$20/Feb,5") # + 使用BingAI2类创建对象

def get_text_from_speech(): # + 新增函数，用于从语音文件中获取文本
    r = sr.Recognizer()
    with sr.AudioFile('speech.wav') as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='zh-CN')
        return text
    except sr.UnknownValueError:
        return '无法识别语音'
    except sr.RequestError as e:
        return '无法连接到Google API服务'

def generate_image_from_text(text): # + 新增函数，用于从文本中生成图像
    image_generator = pipeline('text2image', model='openai/DALL-E')
    image_data = image_generator(text)[0]
    image = Image.open(image_data)
    image.save('image.png')
    return '已生成图像'

def get_response_from_bing(text): # + 修改函数，用于从BingAI2对象中获取回复
    response = bing.get_response(text)
    if response.startswith('#generative_image'): # + 如果回复是图像生成请求，调用图像生成函数
        query = response.split('"')[1]
        response = generate_image_from_text(query)
    return response

def send_response_to_user(response): # + 修改函数，用于向用户发送回复
    print('已收到消息. ' + response)
    if os.path.exists('image.png'): # + 如果存在图像文件，发送给用户
        print('已发送图片. image.png')
        os.remove('image.png')
    if os.path.exists('speech.wav'): # + 如果存在语音文件，删除它
        os.remove('speech.wav')

while True: # + 修改循环，用于接收用户的输入和输出
    if os.path.exists('speech.wav'): # + 如果存在语音文件，调用语音识别函数
        text = get_text_from_speech()
        print('已发送电子邮件. ' + text)
    else: # + 否则，正常接收用户的输入
        text = input('已发送电子邮件. ')
    if text == '退出': # + 如果用户输入退出，结束循环
        break
    response = get_response_from_bing(text) # + 调用BingAI2对象的回复函数
    send_response_to_user(response) # + 调用发送回复函数