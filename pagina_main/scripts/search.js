
document.addEventListener('DOMContentLoaded', () => {
            const input = document.getElementById('search-input');
            const preview = document.getElementById('search-preview');
            const wrapper = document.querySelector('.search-wrapper');

            input.addEventListener('input', () => {
                const q = input.value.trim();
                if (!q) {
                    preview.classList.remove('show');
                    preview.innerHTML = '';
                    return;
                }
                fetch(`/anime/search/?q=${encodeURIComponent(q)}`)
                    .then(res => res.json())
                    .then(data => {
                        preview.innerHTML = '';
                        if (data.results.length) {
                            data.results.forEach(anime => {
                                const a = document.createElement('a');
                                a.href = `/anime/${anime.slug}/`;
                                a.innerHTML = `
                                <img src="${anime.image}" alt="${anime.title}" />
                                <span>${anime.title}</span>
                              `;
                                preview.appendChild(a);
                            });
                        } else {
                            preview.innerHTML = '<div class="px-2 py-1 text-gray-400 text-sm">Sin resultados</div>';
                        }
                        preview.classList.add('show');
                    })
                    .catch(() => preview.classList.remove('show'));
            });

            document.addEventListener('click', e => {
                if (!wrapper.contains(e.target)) {
                    preview.classList.remove('show');
                }
            });
        });