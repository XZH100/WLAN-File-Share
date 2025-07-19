#📂 Django 局域网文件共享工具

这是一个基于 Django 构建的简易局域网文件共享网站，适合在局域网内快速上传、下载文件，自动清理 48 小时前的历史文件，节省存储空间。

##✨ 功能特点

✅ 用户免注册登录（只需输入用户名）

📄 支持文件上传（仅当前用户可见）

📅 显示已上传的文件名和上传时间

📅 一键下载文件

⏲️ 自动删除 48 小时前的旧文件

##🛠️ 安装与部署指南

1. 克隆仓库

git clone https://github.com/XZH100/WLAN-File-Share.git
cd WLAN-File-Share

2. 创建虚拟环境（可选但推荐）

python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

3. 安装依赖

pip install django

4. 初始化数据库

python manage.py makemigrations
python manage.py migrate

5. 启动开发服务器

python manage.py runserver 0.0.0.0:8000

然后在局域网内的其他设备访问：

http://<服务器IP>:8000/

##🧹 定期清理说明

每次用户访问“文件列表页”时，系统会自动检查是否有超过 48 小时的文件，并在数据库和磁盘中一并清除。

如需更稳定的自动清理（例如每天定时），可使用 Django 命令 + cron 实现。

📷 页面预览

登录界面文件列表上传区下载按钮

👉 建议配合截图展示页面外观

📄 License

MIT License

💡 作者

XZH100（https://github.com/XZH100）

欢迎反馈建议或提交 PR！
