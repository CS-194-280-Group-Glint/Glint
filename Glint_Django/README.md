# Glint Django 项目

这是一个基于Django框架的播客网站项目。它保留了原始Glint前端项目的所有样式和功能，同时移除了登录注册功能，并将偏好设置功能与Django后端连接。

## 功能特点

1. 保留原有前端样式和功能
2. 将Preferences偏好设置连接到Django后端
3. 播客列表展示和详情页面
4. 音频播放器功能

## 项目结构

```
Glint_Django/
├── glint_project/        # Django项目目录
│   ├── glint_app/        # Django应用目录
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static/           # 静态文件目录
│   │   ├── audio/        # 音频文件
│   │   ├── css/          # CSS样式文件
│   │   ├── images/       # 图片文件
│   │   └── js/           # JavaScript文件
│   ├── templates/        # 模板文件目录
│   │   ├── index.html    # 首页模板
│   │   └── podcast.html  # 播客详情页模板
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py             # Django管理脚本
└── README.md             # 项目说明文件
```

## 安装与运行

1. 确保已安装Python 3.8或更高版本
2. 安装Django框架：

```bash
pip install django
```

3. 启动开发服务器：

```bash
cd Glint_Django
python manage.py runserver
```

4. 打开浏览器访问：http://127.0.0.1:8000/

## 注意事项

- 本项目仅用于演示，不包含数据库配置
- 使用了模拟数据（mockData.js）来展示播客内容
- 偏好设置会通过API发送到后端，并在控制台日志中显示
