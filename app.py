import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_connection, init_db
from tagging import compute_user_tags
from matching import get_candidates, get_matches, check_mutual_match

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return view_func(*args, **kwargs)
    return wrapped


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    conn.close()
    return dict(row) if row else None


@app.context_processor
def inject_user():
    return {"current_user": current_user()}


# ---------- 认证 ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        nickname = request.form.get("nickname", "").strip() or username

        if not username or not password:
            flash("用户名和密码不能为空")
            return redirect(url_for("register"))

        conn = get_connection()
        existing = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            conn.close()
            flash("用户名已存在")
            return redirect(url_for("register"))

        cursor = conn.execute(
            "INSERT INTO users (username, password_hash, nickname) VALUES (?, ?, ?)",
            (username, generate_password_hash(password), nickname),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        session["user_id"] = user_id
        return redirect(url_for("feed"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            next_url = request.args.get("next") or url_for("feed")
            return redirect(next_url)

        flash("用户名或密码错误")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- 视频流（首页） ----------

@app.route("/")
@login_required
def feed():
    conn = get_connection()
    videos = [dict(row) for row in conn.execute("SELECT * FROM videos ORDER BY id ASC").fetchall()]
    conn.close()
    return render_template("index.html", videos=videos)


@app.route("/api/interact", methods=["POST"])
@login_required
def api_interact():
    data = request.get_json(force=True)
    video_id = data.get("video_id")
    action = data.get("action")  # like / watch / skip
    watch_seconds = float(data.get("watch_seconds", 0))

    if action not in ("like", "watch", "skip"):
        return jsonify({"error": "invalid action"}), 400

    conn = get_connection()
    conn.execute(
        "INSERT INTO interactions (user_id, video_id, action, watch_seconds) VALUES (?, ?, ?, ?)",
        (session["user_id"], video_id, action, watch_seconds),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ---------- 个人标签页 ----------

@app.route("/profile")
@login_required
def profile():
    tags = compute_user_tags(session["user_id"])
    return render_template("profile.html", tags=tags, user=current_user())


@app.route("/api/my_tags")
@login_required
def api_my_tags():
    return jsonify(compute_user_tags(session["user_id"]))


# ---------- 交友模式 ----------

@app.route("/match")
@login_required
def match_page():
    return render_template("match.html")


@app.route("/api/match/candidates")
@login_required
def api_match_candidates():
    candidates = get_candidates(session["user_id"])
    result = [
        {
            "id": c["user"]["id"],
            "nickname": c["user"]["nickname"],
            "bio": c["user"]["bio"],
            "score": c["score"],
            "shared_categories": c["shared_categories"],
            "personality_tags": c["personality_tags"],
        }
        for c in candidates
    ]
    return jsonify(result)


@app.route("/api/match/swipe", methods=["POST"])
@login_required
def api_match_swipe():
    data = request.get_json(force=True)
    to_user_id = data.get("to_user_id")
    liked = bool(data.get("liked"))

    if to_user_id == session["user_id"]:
        return jsonify({"error": "cannot swipe yourself"}), 400

    conn = get_connection()
    conn.execute(
        "INSERT INTO swipes (from_user_id, to_user_id, liked) VALUES (?, ?, ?)",
        (session["user_id"], to_user_id, int(liked)),
    )
    conn.commit()
    conn.close()

    matched = liked and check_mutual_match(session["user_id"], to_user_id)
    return jsonify({"ok": True, "matched": matched})


@app.route("/matches")
@login_required
def matches_page():
    matched_users = get_matches(session["user_id"])
    return render_template("matches.html", matched_users=matched_users)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
