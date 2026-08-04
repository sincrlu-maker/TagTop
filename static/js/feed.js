(function () {
    const items = document.querySelectorAll(".feed-item");
    let watchStartTime = {};

    function sendInteraction(videoId, action, watchSeconds) {
        fetch("/api/interact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                video_id: Number(videoId),
                action: action,
                watch_seconds: watchSeconds || 0,
            }),
        }).catch(() => {});
    }

    // 视频进入/离开可视区域时自动播放/暂停，并统计观看时长
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                const item = entry.target;
                const video = item.querySelector(".feed-video");
                const videoId = item.dataset.videoId;

                if (entry.isIntersecting) {
                    video.currentTime = 0;
                    video.play().catch(() => {});
                    watchStartTime[videoId] = Date.now();
                } else {
                    video.pause();
                    if (watchStartTime[videoId]) {
                        const seconds = (Date.now() - watchStartTime[videoId]) / 1000;
                        if (seconds > 1) {
                            sendInteraction(videoId, "watch", seconds);
                        }
                        delete watchStartTime[videoId];
                    }
                }
            });
        },
        { threshold: 0.6 }
    );

    items.forEach((item) => {
        observer.observe(item);

        const likeBtn = item.querySelector(".like-btn");
        const skipBtn = item.querySelector(".skip-btn");
        const videoId = item.dataset.videoId;

        likeBtn.addEventListener("click", () => {
            likeBtn.classList.toggle("liked");
            sendInteraction(videoId, "like");
        });

        skipBtn.addEventListener("click", () => {
            sendInteraction(videoId, "skip");
            const next = item.nextElementSibling;
            if (next) {
                next.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // 页面关闭/切走时，记录当前正在观看的视频时长
    window.addEventListener("beforeunload", () => {
        Object.keys(watchStartTime).forEach((videoId) => {
            const seconds = (Date.now() - watchStartTime[videoId]) / 1000;
            if (seconds > 1) {
                navigator.sendBeacon(
                    "/api/interact",
                    new Blob(
                        [JSON.stringify({ video_id: Number(videoId), action: "watch", watch_seconds: seconds })],
                        { type: "application/json" }
                    )
                );
            }
        });
    });
})();
