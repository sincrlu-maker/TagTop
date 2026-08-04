# TagTok

一个基于 Flask 的短视频 Web 应用演示项目，包含：

- 📱 **首页信息流**：类似抖音的竖屏视频滑动浏览（点赞 / 划走 / 自动记录观看时长）
- 🏷️ **用户标签**：根据浏览、点赞行为，自动分析"兴趣偏好"与"性格标签"
- 💘 **交友模式**：根据用户兴趣标签的相似度进行推荐配对，支持左滑/右滑、互相喜欢即匹配成功

> ⚠️ 说明：本项目中的"性格标签"是基于行为数据的简化规则打分，用于产品娱乐化演示，**不是专业心理学测评**，不应作为真实性格判断依据。示例视频使用的是公开的免版权测试片段。

---

## 技术栈

- 后端：Python + Flask + Flask-SQLAlchemy
- 数据库：SQLite（本地文件，零配置）
- 前端：原生 HTML / CSS / JavaScript（无需构建工具）

---

## 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/<你的用户名>/tagtok.git
cd tagtok

# 2. 创建虚拟环境（可选，但推荐）
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库 + 写入演示数据
python init_db.py

# 5. 启动服务
python app.py
```

启动后访问 http://127.0.0.1:5000

演示账号（密码均为 `123456`）：`alice` / `bob` / `carol` / `dave` / `eva`
也可以在登录页点击"立即注册"创建自己的账号。

---

## 项目结构

```
tagtok/
├── app.py              # Flask 主应用与路由
├── models.py            # 数据库模型（用户/视频/互动/滑动记录）
├── tagging.py            # 用户标签分析逻辑
├── matching.py            # 交友配对推荐逻辑
├── init_db.py            # 数据库初始化 + 演示数据
├── requirements.txt
├── templates/            # Jinja2 页面模板
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── index.html          # 视频信息流
│   ├── profile.html          # 我的标签
│   ├── match.html           # 交友滑卡
│   └── matches.html         # 我的配对列表
└── static/
    ├── css/style.css
    └── js/
        ├── feed.js          # 视频流交互（自动播放/点赞/划走）
        └── match.js          # 交友滑卡交互
```

---

## 如何上传到 GitHub

```bash
git init
git add .
git commit -m "Initial commit: TagTok demo"
git branch -M main
git remote add origin https://github.com/<你的用户名>/tagtok.git
git push -u origin main
```

建议在仓库根目录添加 `.gitignore`（已包含在本项目中），避免把 `venv/`、`__pycache__/`、`tagtok.db` 等文件提交到仓库。

---

## 部署到云端（可选）

GitHub 本身只能托管代码，不能运行 Flask 服务。如果想让别人直接访问网页版，可以将本仓库部署到支持 Python 的平台，例如：

- [Render](https://render.com)（免费额度，支持 Flask）
- [Railway](https://railway.app)
- [PythonAnywhere](https://www.pythonanywhere.com)

部署时的启动命令通常为：

```bash
pip install -r requirements.txt && python init_db.py && python app.py
```

生产环境建议使用 `gunicorn` 等 WSGI 服务器运行，并将 `SECRET_KEY` 通过环境变量设置为随机字符串。

---

## 后续可扩展方向

- 真实的视频上传与存储（本地/对象存储）
- 更精细的推荐算法（协同过滤、embedding 相似度等）
- 配对成功后的即时聊天功能（可接入 WebSocket）
- 用户头像上传、更丰富的个人主页
