"""
交友模式配对逻辑：基于用户兴趣标签的相似度进行匹配排序
"""
from db import get_connection
from tagging import compute_user_tags


def tag_similarity(tags_a, tags_b):
    """
    计算两组兴趣标签的相似度（0~100分），使用简化的余弦相似度思路
    tags_a / tags_b: [[category, score], ...]
    """
    dict_a = dict(tags_a)
    dict_b = dict(tags_b)
    if not dict_a or not dict_b:
        return 0.0

    categories = set(dict_a.keys()) | set(dict_b.keys())
    dot = sum(dict_a.get(c, 0) * dict_b.get(c, 0) for c in categories)
    norm_a = sum(v * v for v in dict_a.values()) ** 0.5
    norm_b = sum(v * v for v in dict_b.values()) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    cosine = dot / (norm_a * norm_b)
    return round(max(0.0, min(cosine, 1.0)) * 100, 1)


def get_candidates(current_user_id, limit=20):
    """
    获取当前用户的推荐候选人列表，按标签相似度降序排列。
    排除：自己、已经滑过的人
    """
    my_tags = compute_user_tags(current_user_id)["interest_tags"]
    my_categories = {c for c, _ in my_tags}

    conn = get_connection()
    swiped_rows = conn.execute(
        "SELECT to_user_id FROM swipes WHERE from_user_id = ?", (current_user_id,)
    ).fetchall()
    excluded_ids = {row["to_user_id"] for row in swiped_rows}
    excluded_ids.add(current_user_id)

    placeholders = ",".join("?" * len(excluded_ids)) if excluded_ids else "NULL"
    query = f"SELECT * FROM users WHERE id NOT IN ({placeholders})"
    candidate_rows = conn.execute(query, tuple(excluded_ids)).fetchall()
    conn.close()

    scored = []
    for row in candidate_rows:
        other_result = compute_user_tags(row["id"])
        other_tags = other_result["interest_tags"]
        score = tag_similarity(my_tags, other_tags)
        scored.append({
            "user": dict(row),
            "score": score,
            "shared_categories": [c for c, _ in other_tags if c in my_categories][:5],
            "personality_tags": other_result["personality_tags"],
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]


def check_mutual_match(from_user_id, to_user_id):
    """判断两人是否互相右滑（喜欢），互相喜欢即为匹配成功"""
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM swipes WHERE from_user_id = ? AND to_user_id = ? AND liked = 1",
        (to_user_id, from_user_id),
    ).fetchone()
    conn.close()
    return row is not None


def get_matches(user_id):
    """获取当前用户已配对成功（互相喜欢）的用户列表"""
    conn = get_connection()
    my_likes = conn.execute(
        "SELECT to_user_id FROM swipes WHERE from_user_id = ? AND liked = 1", (user_id,)
    ).fetchall()

    matched_users = []
    for row in my_likes:
        to_user_id = row["to_user_id"]
        if check_mutual_match(user_id, to_user_id):
            user_row = conn.execute("SELECT * FROM users WHERE id = ?", (to_user_id,)).fetchone()
            if user_row:
                matched_users.append(dict(user_row))
    conn.close()
    return matched_users
