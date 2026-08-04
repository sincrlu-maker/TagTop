"""
初始化数据库并写入演示用的视频与用户数据。
运行方式： python init_db.py
"""
from werkzeug.security import generate_password_hash

from db import get_connection, init_db

# 公开可用的免版权测试视频（常用于demo/教学，非受版权保护的商业内容）
SAMPLE_VIDEOS = [
    ("清晨的花朵延时摄影", "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4", "旅行"),
    ("经典动画短片片段", "https://www.w3schools.com/html/mov_bbb.mp4", "电影"),
    ("城市延时风光", "https://media.w3.org/2010/05/sintel/trailer.mp4", "旅行"),
    ("搞笑瞬间合集", "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4", "搞笑"),
    ("厨房美食制作", "https://www.w3schools.com/html/mov_bbb.mp4", "美食"),
    ("街头健身达人", "https://media.w3.org/2010/05/bunny/trailer.mp4", "运动"),
    ("萌宠日常", "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4", "萌宠"),
    ("独立音乐现场", "https://www.w3schools.com/html/mov_bbb.mp4", "音乐"),
    ("科技新品评测", "https://media.w3.org/2010/05/sintel/trailer.mp4", "科技"),
    ("影视混剪片段", "https://media.w3.org/2010/05/bunny/trailer.mp4", "电影"),
]

DEMO_USERS = [
    ("alice", "123456", "Alice", "热爱旅行和摄影", "female"),
    ("bob", "123456", "Bob", "健身爱好者，周末喜欢打球", "male"),
    ("carol", "123456", "Carol", "美食博主，探店达人", "female"),
    ("dave", "123456", "Dave", "科技宅，关注新硬件", "male"),
    ("eva", "123456", "Eva", "音乐是生活的解药", "female"),
]


def main():
    init_db(drop_existing=True)
    conn = get_connection()

    for title, url, category in SAMPLE_VIDEOS:
        conn.execute(
            "INSERT INTO videos (title, url, category) VALUES (?, ?, ?)",
            (title, url, category),
        )

    for username, pwd, nickname, bio, gender in DEMO_USERS:
        conn.execute(
            "INSERT INTO users (username, password_hash, nickname, bio, gender) VALUES (?, ?, ?, ?, ?)",
            (username, generate_password_hash(pwd), nickname, bio, gender),
        )

    conn.commit()
    conn.close()

    print("数据库初始化完成！")
    print("演示账号（密码均为 123456）：alice / bob / carol / dave / eva")
    print("你也可以在 /register 页面自行注册新账号。")


if __name__ == "__main__":
    main()
