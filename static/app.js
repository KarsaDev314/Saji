document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. SETTINGS DROPDOWN & DARK MODE (GLOBAL)
    // ==========================================
    const themeCheckbox = document.getElementById('theme-checkbox');
    
    window.toggleSettingsMenu = function(e) {
        if (e) { e.preventDefault(); e.stopPropagation(); }
        const menu = document.getElementById('settings-menu');
        const btn = document.getElementById('settings-btn');
        if (menu) {
            menu.classList.toggle('show');
            if (btn) btn.classList.toggle('active');
        }
    };

    document.addEventListener('click', function(e) {
        const menu = document.getElementById('settings-menu');
        const btn = document.getElementById('settings-btn');
        if (menu && menu.classList.contains('show')) {
            if (!menu.contains(e.target) && (!btn || !btn.contains(e.target))) {
                menu.classList.remove('show');
                if (btn) btn.classList.remove('active');
            }
        }
    });

    if (themeCheckbox) {
        if (localStorage.getItem('saji_theme') === 'dark') {
            themeCheckbox.checked = true;
        }
        themeCheckbox.addEventListener('change', function() {
            if (this.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('saji_theme', 'dark');
            } else {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('saji_theme', 'light');
            }
        });
    }

    // ==========================================
    // 2. AJAX & FITUR INTERAKTIF (PAGE SPECIFIC)
    // ==========================================
    const fetchPost = async (url, formData) => {
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        return response.json();
    };

    // --- LIKE (RESEP) ---
    document.querySelectorAll('form[action*="/like"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_liked);
                    btn.innerHTML = data.is_liked 
                        ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg> ${data.likes_count} Suka`
                        : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg> ${data.likes_count} Suka`;
                }
            } catch (err) { console.error("Gagal Like:", err); }
        });
    });

            // --- FAVORIT ---
    document.querySelectorAll('form[action*="/favorit"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            const svg = btn.querySelector('svg'); // Ambil elemen SVG-nya aja
            
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_favorit);
                    
                    // Cuma ganti warna fill SVG, gak ngeganti teks/tombol
                    if (svg) {
                        svg.setAttribute('fill', data.is_favorit ? 'currentColor' : 'none');
                    }
                }
            } catch (err) { console.error("Gagal Favorit:", err); }
        });
    });

    // --- FOLLOW ---
    document.querySelectorAll('form[action^="/follow/"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            const card = btn.closest('.user-card');
            const followerCountSpan = card ? card.querySelector('.follower-count-text') : null;
            
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.innerHTML = data.is_follow ? 'Mengikuti' : 'Ikuti';
                    
                    if (data.is_follow) {
                        btn.classList.remove('btn-primary');
                        btn.classList.add('btn-outline');
                    } else {
                        btn.classList.remove('btn-outline');
                        btn.classList.add('btn-primary');
                    }
                    
                    if (followerCountSpan) {
                        followerCountSpan.textContent = data.follower_count;
                    }
                }
            } catch (err) { console.error("Gagal Follow:", err); }
        });
    });

    // --- KOMENTAR (KIRIM & BALAS) ---
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
                        form.parentElement.style.display = 'none'; 
                    } else {
                        const list = document.querySelector('.comment-list');
                        list.insertBefore(newCommentNode, list.firstChild);
                    }
                    form.reset();
                }
            } catch (err) { 
                console.error("Gagal kirim komentar:", err); 
            } finally {
                btn.innerHTML = oldText;
                btn.disabled = false;
            }
        }
    });

        // --- TOGGLE EDIT & CANCEL EDIT ---
    window.toggleEdit = function(id) {
        document.getElementById(`text-${id}`).style.display = 'none';
        document.getElementById(`edit-form-${id}`).style.display = 'block';
    };

    window.cancelEdit = function(id) {
        document.getElementById(`text-${id}`).style.display = 'block';
        document.getElementById(`edit-form-${id}`).style.display = 'none';
    };

    // --- SUBMIT EDIT KOMENTAR (AJAX) ---
    document.addEventListener('submit', async (e) => {
        if (e.target.matches('.ajax-edit-form')) {
            e.preventDefault();
            const form = e.target;
            const commentId = form.id.replace('edit-form-', ''); // Ambil ID dari ID form
            
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    // 1. Ganti teks lama dengan teks baru
                    document.getElementById(`text-${commentId}`).innerText = data.teks;
                    // 2. Sembunyikan form, munculin teks lagi
                    cancelEdit(commentId);
                }
            } catch (err) { console.error("Gagal edit komentar:", err); }
        }
    });

    // --- HAPUS KOMENTAR (AJAX) ---
    document.addEventListener('submit', async (e) => {
        if (e.target.matches('.ajax-delete-comment')) {
            e.preventDefault();
            const form = e.target;
            const commentId = form.action.split('/').filter(Boolean).slice(-2)[0]; 
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    const el = document.getElementById(`k-${commentId}`);
                    if (el) el.remove();
                }
            } catch (err) { console.error("Gagal hapus komentar:", err); }
        }
    });

    // --- RATING ---
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

    // ==========================================
    // 3. CUSTOM SEARCH & DROPDOWN (INDEX ONLY)
    // ==========================================
    const dropdown = document.getElementById('category-dropdown');
    if (dropdown) {
        const dropdownBtn = document.getElementById('category-btn');
        const dropdownMenu = document.getElementById('category-menu');
        const categoryValue = document.getElementById('category-value');
        const categoryLabel = document.getElementById('category-label');

        dropdownBtn.addEventListener('click', () => {
            dropdown.classList.toggle('open');
            document.getElementById('search-history').style.display = 'none';
        });

        dropdownMenu.querySelectorAll('li').forEach(item => {
            item.addEventListener('click', () => {
                const val = item.getAttribute('data-value');
                const text = item.innerText;
                categoryValue.value = val;
                categoryLabel.innerText = text;
                dropdownMenu.querySelectorAll('li').forEach(li => li.classList.remove('active'));
                item.classList.add('active');
                dropdown.classList.remove('open');
            });
        });

        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
        });
    }

    // Search History
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        const historyBox = document.getElementById('search-history');
        const historyList = document.getElementById('history-list');
        const clearHistoryBtn = document.getElementById('clear-history');
        let searchHistory = JSON.parse(localStorage.getItem('saji_search_history')) || [];

        const renderHistory = () => {
            if (searchHistory.length === 0) {
                historyBox.style.display = 'none';
                return;
            }
            historyList.innerHTML = '';
            searchHistory.forEach(term => {
                const li = document.createElement('li');
                li.innerText = term;
                li.addEventListener('click', () => {
                    searchInput.value = term;
                    document.getElementById('search-form').submit();
                });
                historyList.appendChild(li);
            });
            historyBox.style.display = 'block';
        };

        searchInput.addEventListener('focus', () => {
            renderHistory();
            if (dropdown) dropdown.classList.remove('open');
        });

        searchInput.addEventListener('input', () => {
            historyBox.style.display = 'none';
        });

        document.getElementById('search-form').addEventListener('submit', () => {
            const val = searchInput.value.trim();
            if (val && !searchHistory.includes(val)) {
                searchHistory.unshift(val);
                searchHistory = searchHistory.slice(0, 5);
                localStorage.setItem('saji_search_history', JSON.stringify(searchHistory));
            }
        });

        clearHistoryBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            searchHistory = [];
            localStorage.removeItem('saji_search_history');
            renderHistory();
        });

        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !historyBox.contains(e.target)) {
                historyBox.style.display = 'none';
            }
        });
    }

    // --- LAPOR BUG ---
    window.bukaLaporBug = function(e) {
        if (e) { e.preventDefault(); e.stopPropagation(); }
        const modal = document.getElementById('bug-modal');
        if (modal) modal.style.display = 'flex';
        
        const menu = document.getElementById('settings-menu');
        const btn = document.getElementById('settings-btn');
        if (menu) menu.classList.remove('show');
        if (btn) btn.classList.remove('active');
    };

    window.tutupLaporBug = function() {
        const modal = document.getElementById('bug-modal');
        if (modal) modal.style.display = 'none';
    };

    window.kirimLaporBug = async function(e) {
        e.preventDefault();
        const form = e.target;
        const btn = form.querySelector('button[type="submit"]');
        const oldText = btn.innerHTML;
        btn.innerHTML = 'Mengirim...';
        btn.disabled = true;

        try {
            // Kita tembak langsung ke endpoint API
            const response = await fetch('/api/lapor-bug', {
                method: 'POST',
                body: new FormData(form),
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await response.json();
            
            if (data.status === 'ok') {
                alert(data.message);
                tutupLaporBug();
                form.reset();
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error("Gagal kirim bug:", err);
            alert("Terjadi kesalahan sistem.");
        } finally {
            btn.innerHTML = oldText;
            btn.disabled = false;
        }
    };

    window.addEventListener('click', function(e) {
        const modal = document.getElementById('bug-modal');
        if (e.target === modal) {
            tutupLaporBug();
        }
    });
});