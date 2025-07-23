# 使用官方Python基础镜像
FROM docker.1ms.run/library/python:3.9-slim
# 设置工作目录
WORKDIR /app
# 将项目的依赖文件和文件复制到工作目录
COPY . /app
# 安装依赖
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip config set global.progress_bar off   # 防止线程不够用的情况
RUN pip install --upgrade pip setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r  /app/requirements.txt
# 暴露应用的端口
#EXPOSE 5000
# 映射文件
VOLUME ["./conf", "/app/conf"]
# 运行Python应用
CMD ["python", "/app/app.py"]