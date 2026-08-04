(function () {
    const cardStack = document.getElementById("card-stack");
    const likeBtn = document.getElementById("like-btn");
    const passBtn = document.getElementById("pass-btn");
    const matchToast = document.getElementById("match-toast");

    let candidates = [];
    let currentIndex = 0;

    function renderCard() {
        cardStack.innerHTML = "";

        if (currentIndex >= candidates.length) {
            cardStack.innerHTML = '<p class="empty-state">暂时没有更多推荐了，晚点再来看看吧～</p>';
            likeBtn.style.display = "none";
            passBtn.style.display = "none";
            return;
        }

        const c = candidates[currentIndex];
        const card = document.createElement("div");
        card.className = "match-card";
        card.innerHTML = `
            <div class="avatar-placeholder">${c.nickname ? c.nickname[0] : "?"}</div>
            <div class="match-score">匹配度 ${c.score}%</div>
            <h3>${c.nickname}</h3>
            <p class="bio">${c.bio || "这个人很神秘，还没有写简介"}</p>
            <div class="tag-chips">
                ${c.personality_tags.map((t) => `<span class="chip chip-personality">${t}</span>`).join("")}
            </div>
        `;
        cardStack.appendChild(card);
    }

    async function loadCandidates() {
        const res = await fetch("/api/match/candidates");
        candidates = await res.json();
        currentIndex = 0;
        renderCard();
    }

    async function swipe(liked) {
        if (currentIndex >= candidates.length) return;
        const target = candidates[currentIndex];

        const res = await fetch("/api/match/swipe", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ to_user_id: target.id, liked: liked }),
        });
        const data = await res.json();

        currentIndex += 1;
        renderCard();

        if (data.matched) {
            matchToast.classList.remove("hidden");
        }
    }

    likeBtn.addEventListener("click", () => swipe(true));
    passBtn.addEventListener("click", () => swipe(false));

    loadCandidates();
})();
