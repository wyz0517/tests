# 使用官方的Python镜像
FROM python:3.9-slim-buster

# 设置工作目录
WORKDIR /usr/src/app

# 将当前目录的内容复制到容器的工作目录内
COPY . .

# 安装python-telegram-bot库
RUN pip install -r requirements.txt

# 定义环境变量
# 如果有需要可以设置，例如代理等

# 暴露的端口（如果有的话）
# EXPOSE port

# 运行python脚本
CMD [ "python", "./main.py" ]
