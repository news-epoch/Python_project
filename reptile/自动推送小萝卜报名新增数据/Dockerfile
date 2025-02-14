# 使用官方Python基础镜像
FROM python:3.9-slim
# 设置工作目录
WORKDIR /app
# 将项目的依赖文件和文件复制到工作目录
COPY . /app
# 安装依赖
RUN pip install --no-index --find-links=/app/packet -r  /app/requirements.txt
# 暴露应用的端口
#EXPOSE 5000
# 映射文件
VOLUME ["./conf", "/app/conf"]
# 运行Python应用
CMD ["python", "/app/app.py"]