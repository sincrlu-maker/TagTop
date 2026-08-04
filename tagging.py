"""
用户标签分析模块
说明：这里的"性格标签"是基于用户浏览/点赞行为的简化规则打分，
仅作为产品娱乐化功能演示，不是专业的心理学测评，不应作为真实性格判断依据。
"""
from collections import Counter
from db import get_connection

# 行为权重：点赞 > 完整观看 > 短暂观看，划走为负权重
ACTION_WEIGHT = {
    "like": 3.0,
    "watch": 1.0,
    "skip": -0.5,
}

# 类别 -> 性格关键词的简化映射规则（仅用于demo展示，非科学测评）
CATEGORY_PERSONALITY_MAP = {
    "搞笑": "幽默开朗",
    "美食": "热爱生活",
    "旅行": "自由探索",
    "音乐": "感性文艺",
    "运动": "活力自律",
    "萌宠": "温柔治愈",
    "科技": "理性极客",
    "电影": "深度思考",
}


def compute_user_tags(user_id):
    """
    根据用户的历史互动记录，计算兴趣标签（带权重）和性格标签。
    返回:
        {
            "interest_tags": [[category, score], ...],  # 按分数降序
            "personality_tags": [keyword, ...],
            "top_category": category or None
        }
    """
    conn = get_connection()
    interactions = conn.execute(
        "SELECT i.action, i.watch_seconds, v.category "
        "FROM interactions i JOIN videos v ON i.video_id = v.id "
        "WHERE i.user_id = ?",
        (user_id,),
    ).fetchall()
    conn.close()

    if not interactions:
        return {
            "interest_tags": [],
            "personality_tags": ["新用户"],
            "top_category": None,
        }

    scores = Counter()
    for row in interactions:
        weight = ACTION_WEIGHT.get(row["action"], 0)
        bonus = min(row["watch_seconds"] / 30.0, 1.0) if row["action"] == "watch" else 0
        scores[row["category"]] += weight + bonus

    positive_scores = {cat: round(score, 1) for cat, score in scores.items() if score > 0}
    interest_tags = sorted(positive_scores.items(), key=lambda x: x[1], reverse=True)

    personality_tags = []
    for cat, _ in interest_tags[:3]:
        keyword = CATEGORY_PERSONALITY_MAP.get(cat)
        if keyword and keyword not in personality_tags:
            personality_tags.append(keyword)

    if len(positive_scores) >= 5:
        personality_tags.append("兴趣广泛的探索型")

    if not personality_tags:
        personality_tags = ["性格分析中"]

    top_category = interest_tags[0][0] if interest_tags else None

    return {
        "interest_tags": [list(t) for t in interest_tags],
        "personality_tags": personality_tags,
        "top_category": top_category,
    }
