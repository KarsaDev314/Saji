document.addEventListener('DOMContentLoaded', () => {
    const fetchPost = async (url, formData) => {
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        return response.json();
    };

    // 1. LIKE
    document.querySelectorAll('form[action*="/like"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_liked);
                    if (data.is_liked) {
                        btn.innerHTML = `❤️ ${data.likes_count} Suka`;
                    } else {
                        btn.innerHTML = `🤍 ${data.likes_count} Suka`;
                    }
                }
            } catch (err) { console.error("Gagal Like:", err); }
        });
    });

    // 2. FAVORIT
    document.querySelectorAll('form[action*="/favorit"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_favorit);
                    
                    // BENERIN DI SINI: Cek apakah tombolnya ikon (beranda) atau teks (detail)
                    if (btn.classList.contains('btn-icon')) {
                        btn.innerHTML = data.is_favorit ? '★' : '☆';
                    } else {
                        btn.innerHTML = data.is_favorit ? '⭐ Favorit' : '☆ Favorit';
                    }
                }
            } catch (err) { console.error("Gagal Favorit:", err); }
        });
    });

        // 3. FOLLOW
    document.querySelectorAll('form[action^="/follow/"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            
            // Cek kalau ini di halaman profil (ada ID follower-count)
            const followerCountSpan = document.getElementById('follower-count');
            
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_follow);
                    
                    // Kalau di halaman profil, update teks tombolnya
                    if (btn.classList.contains('btn-primary') || btn.classList.contains('btn-outline')) {
                        btn.innerHTML = data.is_follow ? 'Mengikuti' : 'Ikuti';
                        
                        // Ganti style tombolnya
                        if (data.is_follow) {
                            btn.classList.add('btn-outline');
                            btn.classList.remove('btn-primary');
                        } else {
                            btn.classList.add('btn-primary');
                            btn.classList.remove('btn-outline');
                        }
                    }
                    
                    if (followerCountSpan) {
                        followerCountSpan.textContent = data.follower_count;
                    }
                }
            } catch (err) { console.error("Gagal Follow:", err); }
        });
    });

    // 4. KOMENTAR (Kirim & Balas)
    document.addEventListener('submit', async (e) => {
        if (e.target.matches('.ajax-comment-form')) {
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

    // 5. RATING (Auto-save saat bintang diklik)
    document.querySelectorAll('.ajax-rating-form input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', async (e) => {
            const form = e.target.closest('form');
            form.style.opacity = '0.5'; 

            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    form.style.opacity = '1';
                }
            } catch (err) {
                console.error("Gagal simpan rating:", err);
                form.style.opacity = '1'; 
            }
        });
    });
});