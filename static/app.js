document.addEventListener('DOMContentLoaded', () => {
    // Fungsi bantu buat nembak data ke server tanpa reload
    const fetchPost = async (url, formData) => {
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        return response.json();
    };

    // 1. Handle AJAX untuk LIKE
    const likeForms = document.querySelectorAll('form[action*="/like"]');
    likeForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            const countSpan = document.querySelector('.like-count');
            
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    countSpan.textContent = `❤️ ${data.likes_count} Suka`;
                    if (data.is_liked) {
                        btn.classList.add('aktif');
                        btn.innerHTML = '❤️ Batal Suka';
                    } else {
                        btn.classList.remove('aktif');
                        btn.innerHTML = '🤍 Suka';
                    }
                }
            } catch (err) {
                console.error("Gagal Like:", err);
            }
        });
    });

    // 2. Handle AJAX untuk FAVORIT (Beranda & Detail)
    const favForms = document.querySelectorAll('form[action*="/favorit"]');
    favForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            
            try {
                const data = await fetchPost(form.action, new FormData(form));
                if (data.status === 'ok') {
                    if (data.is_favorit) {
                        btn.classList.add('aktif');
                        if (btn.classList.contains('btn-icon')) btn.innerHTML = '★';
                        else btn.innerHTML = '⭐ Favorit';
                    } else {
                        btn.classList.remove('aktif');
                        if (btn.classList.contains('btn-icon')) btn.innerHTML = '☆';
                        else btn.innerHTML = '☆ Favorit';
                    }
                }
            } catch (err) {
                console.error("Gagal Favorit:", err);
            }
        });
    });
});