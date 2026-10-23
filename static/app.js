document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. SETTINGS DROPDOWN & DARK MODE (GLOBAL)
    // ==========================================
    const themeCheckbox = document.getElementById('theme-checkbox');
    
    // Fungsi buka/tutup menu (dipanggil dari onclick di HTML)
    window.toggleSettingsMenu = function(e) {
        if (e) { e.preventDefault(); e.stopPropagation(); }
        const menu = document.getElementById('settings-menu');
        if (menu) menu.classList.toggle('show');
    };

    // Tutup menu kalau klik di luar area
    document.addEventListener('click', function(e) {
        const menu = document.getElementById('settings-menu');
        const btn = document.getElementById('settings-btn');
        if (menu && menu.classList.contains('show')) {
            if (!menu.contains(e.target) && (!btn || !btn.contains(e.target))) {
                menu.classList.remove('show');
            }
        }
    });

    // Logic Dark Mode (Cek apakah elemen ada sebelum jalan)
    if (themeCheckbox) {
        // Sinkronisasi status checkbox sama localStorage
        if (localStorage.getItem('saji_theme') === 'dark') {
            themeCheckbox.checked = true;
        }

        // Event listener pas digeser
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

    // --- LIKE ---
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
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_favorit);
                    if (btn.classList.contains('btn-icon')) {
                        btn.innerHTML = data.is_favorit ? '★' : '☆';
                    } else {
                        btn.innerHTML = data.is_favorit ? '⭐ Favorit' : '☆ Favorit';
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
            const followerCountSpan = document.getElementById('follower-count');
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    btn.classList.toggle('aktif', data.is_follow);
                    btn.innerHTML = data.is_follow ? 'Berhenti Mengikuti' : 'Ikuti';
                    if (followerCountSpan) followerCountSpan.textContent = data.follower_count;
                }
            } catch (err) { console.error("Gagal Follow:", err); }
        });
    });

    // --- KOMENTAR ---
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
});