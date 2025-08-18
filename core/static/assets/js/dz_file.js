(function () {
    const input = document.getElementById('id_images');   // file input
    const drop = document.getElementById('dropArea');
    const grid = document.getElementById('previewGrid');

    // Manage a mutable FileList
    const dt = new DataTransfer();

    function renderPreviews() {
        grid.innerHTML = '';
        for (let i = 0; i < dt.files.length; i++) {
            const file = dt.files[i];
            const url = URL.createObjectURL(file);
            const card = document.createElement('div');
            card.className = 'dz-thumb';
            card.innerHTML = `
        <img src="${url}" alt="">
        <button type="button" class="dz-remove" title="Remove" data-index="${i}">✕</button>
      `;
            grid.appendChild(card);
        }
    }

    function addFiles(fileList) {
        const allowed = ['image/jpeg', 'image/png', 'image/svg+xml', 'image/jpg'];
        Array.from(fileList).forEach(f => {
            if (allowed.includes(f.type) || /\.(jpg|jpeg|png|svg)$/i.test(f.name)) {
                dt.items.add(f);
            }
        });
        input.files = dt.files;
        renderPreviews();
    }

    function removeAt(index) {
        const tmp = new DataTransfer();
        for (let i = 0; i < dt.files.length; i++) {
            if (i !== index) tmp.items.add(dt.files[i]);
        }
        dt.items.clear();
        for (let i = 0; i < tmp.files.length; i++) dt.items.add(tmp.files[i]);
        input.files = dt.files;
        renderPreviews();
    }

    // Click drop area to open chooser
    drop.addEventListener('click', () => input.click());
    drop.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            input.click();
        }
    });

    // From chooser
    input.addEventListener('change', (e) => addFiles(e.target.files));

    // Drag & drop
    ['dragenter', 'dragover'].forEach(evt => {
        drop.addEventListener(evt, e => {
            e.preventDefault();
            e.stopPropagation();
            drop.classList.add('dragover');
        }, false);
    });
    ['dragleave', 'drop'].forEach(evt => {
        drop.addEventListener(evt, e => {
            e.preventDefault();
            e.stopPropagation();
            drop.classList.remove('dragover');
        }, false);
    });
    drop.addEventListener('drop', (e) => addFiles(e.dataTransfer.files));

    // Remove preview
    grid.addEventListener('click', (e) => {
        const btn = e.target.closest('.dz-remove');
        if (!btn) return;
        removeAt(parseInt(btn.dataset.index, 10));
    });
})();