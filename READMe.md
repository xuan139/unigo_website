项目创建完成！

- 进入项目目录：`cd $PROJECT_NAME`
- 激活虚拟环境：`source venv/bin/activate`
- 运行服务器：`python3 app.py`
- 生成静态文件：`python3 app.py freeze`
- 测试静态文件：`cd build && python3 -m http.server 8000`
- 测试下载：访问 `http://localhost:5000/static/appcast.xml` 
- 或 `http://localhost:8000/static/appcast.xml`