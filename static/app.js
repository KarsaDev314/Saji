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
});    // 6. CUSTOM DROPDOWN KATEGORI
    const dropdown = document.getElementById('category-dropdown');
    const dropdownBtn = document.getElementById('category-btn');
    const dropdownMenu = document.getElementById('category-menu');
    const categoryValue = document.getElementById('category-value');
    const categoryLabel = document.getElementById('category-label');

    if (dropdownBtn) {
        // Toggle buka/tutup
        dropdownBtn.addEventListener('click', () => {
            dropdown.classList.toggle('open');
            document.getElementById('search-history').style.display = 'none'; // Tutup history kalau dropdown buka
        });

        // Pilih item
        dropdownMenu.querySelectorAll('li').forEach(item => {
            item.addEventListener('click', () => {
                const val = item.getAttribute('data-value');
                const text = item.innerText;
                
                categoryValue.value = val;
                categoryLabel.innerText = text;
                
                // Update class active
                dropdownMenu.querySelectorAll('li').forEach(li => li.classList.remove('active'));
                item.classList.add('active');
                
                dropdown.classList.remove('open');
            });
        });

        // Tutup kalau klik di luar
        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('open');
            }
        });
    }

    // 7. FITUR HISTORY SEARCH (LOCALSTORAGE)
    const searchInput = document.getElementById('search-input');
    const historyBox = document.getElementById('search-history');
    const historyList = document.getElementById('history-list');
    const clearHistoryBtn = document.getElementById('clear-history');

    if (searchInput) {
        // Ambil history dari localStorage
        let searchHistory = JSON.parse(localStorage.getItem('saji_search_history')) || [];

        // Tampilkan history
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

        // Event saat input di-fokus
        searchInput.addEventListener('focus', () => {
            renderHistory();
            if (dropdown) dropdown.classList.remove('open'); // Tutup dropdown kalau input fokus
        });

        // Event saat ngetik (tutup history biar gak nutupin)
        searchInput.addEventListener('input', () => {
            historyBox.style.display = 'none';
        });

        // Simpan history saat form disubmit
        document.getElementById('search-form').addEventListener('submit', () => {
            const val = searchInput.value.trim();
            if (val && !searchHistory.includes(val)) {
                searchHistory.unshift(val); // Taruh paling atas
                searchHistory = searchHistory.slice(0, 5); // Maksimal 5
                localStorage.setItem('saji_search_history', JSON.stringify(searchHistory));
            }
        });

        // Hapus history
        clearHistoryBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            searchHistory = [];
            localStorage.removeItem('saji_search_history');
            renderHistory();
        });

        // Tutup history kalau klik di luar
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !historyBox.contains(e.target)) {
                historyBox.style.display = 'none';
            }
        });
    }        // Tambahan: Biar bisa diakses pakai keyboard (Enter / Spasi)
        dropdownMenu.querySelectorAll('li').forEach((item, index) => {
            item.setAttribute('tabindex', '0'); // Biar bisa di-focus
            
            item.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    item.click(); // Panggil fungsi klik
                }
            });
        });