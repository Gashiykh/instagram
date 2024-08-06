(function() {
    async function ServerCall(uri) {
        const response = await fetch(uri);
        const data = await response.json();
        return data;
    };

    async function heartClick(event) {
        let heart = event.target;
        let postId = heart.getAttribute("post-id");

        const data = await ServerCall(`/like/${postId}/`);

        if (data.success) {
            console.log(data);
            const likeCountElement = document.getElementById(`like-count-${postId}`);
            likeCountElement.textContent = data.like_count;

            if (data.liked) {
                heart.classList.remove("unliked");
                heart.classList.add("liked");
            } else {
                heart.classList.remove("liked");
                heart.classList.add("unliked");
            }
        }
    }

    document.querySelectorAll(".heart").forEach(heart => {
        heart.addEventListener("click", heartClick);
    });
})();