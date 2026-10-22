// static/app.js
document.addEventListener('DOMContentLoaded', () => {
    console.log("🔥 APP JS BERHASIL DIMUAT!");

    const fetchPost = async (url, formData) => {
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        return response.json();
    };

    // Kita pakai Event Delegation biar gak perlu nge-loop satu-satu
    document.addEventListener('submit', async (e) => {
        
        // 1. Handle LIKE
        if (e.target.matches('form[action*="/like"]')) {
            e.preventDefault();
            const form = e.target;
            const btn = form.querySelector('button');
            const countSpan = document.querySelector('.like-count');
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    countSpan.textContent = `❤️ ${data.likes_count} Suka`;
                    btn.classList.toggle('aktif', data.is_liked);
                    btn.innerHTML = data.is_liked ? '❤️ Batal Suka' : '🤍 Suka';
                }
            } catch (err) { console.error("Gagal Like:", err); }
        }

        // 2. Handle FAVORIT
        else if (e.target.matches('form[action*="/favorit"]')) {
            e.preventDefault();
            const form = e.target;
            const btn = form.querySelector('button');
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_favorit);
                    if (btn.classList.contains('btn-icon')) btn.innerHTML = data.is_favorit ? '★' : '☆';
                    else btn.innerHTML = data.is_favorit ? '⭐ Favorit' : '☆ Favorit';
                }
            } catch (err) { console.error("Gagal Favorit:", err); }
        }

        // 3. Handle FOLLOW
        else if (e.target.matches('form[action^="/follow/"]')) {
            e.preventDefault();
            const form = e.target;
            const btn = form.querySelector('button');
            const followerCountSpan = document.getElementById('follower-count');
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_follow);
                    btn.innerHTML = data.is_follow ? 'Berhenti Mengikuti' : 'Ikuti';
                    if (followerCountSpan) followerCountSpan.textContent = data.follower_count;
                }
            } catch (err) { console.error("Gagal Follow:", err); }
        }

        // 4. Handle KOMENTAR (Kirim & Balas)
        else if (e.target.matches('.ajax-comment-form')) {
            e.preventDefault();
            const form = e.target;
            const btn = form.querySelector('button[type="submit"]');
            const oldText = btn.innerHTML;
            btn.innerHTML = 'Mengirim...';
            btn.disabled = true;

            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = data.html;
                    const newCommentNode = tempDiv.firstElementChild;

                    const parentId = form.querySelector('input[name="parent_id"]')?.value;
                    if (parentId) {
                        const parentComment = document.getElementById(`k-${parentId}`);
                        let repliesContainer = parentComment.querySelector('.comment-replies');
                        if (!repliesContainer) {
                            repliesContainer = document.createElement('div');
                            repliesContainer.className = 'comment-replies';
                            parentComment.appendChild(repliesContainer);
                        }
                        repliesContainer.appendChild(newCommentNode);
                    } else {
                        const list = document.querySelector('.comment-list');
                        list.insertBefore(newCommentNode, list.firstChild);
                    }
                    form.reset();
                }
            } catch (err) { console.error("Gagal kirim komentar:", err); } 
            finally {
                btn.innerHTML = oldText;
                btn.disabled = false;
            }
        }
    });
});