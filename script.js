// Ultimate Schooling Universal Script v7.1

const config = {
    folderName: 'articles',
    itemsPerPage: 15,
    authorName: 'Marcus J. Holloway',
    defaultAuthorImg: 'images/marcus-holloway.jpg'
};

const pageKey = window.location.pathname.split('/').pop() || 'index.html';
let allArticles = [];
// Per-container pagination state (fixes next-page layout bug)
const containerState = {};

const isArticlePage = window.location.pathname.includes('/' + config.folderName + '/');
const basePath = isArticlePage ? '' : config.folderName + '/';
const linkPrefix = isArticlePage ? '' : config.folderName + '/';
const rootPrefix = isArticlePage ? '../' : '';

const style = document.createElement('style');
style.innerHTML = `
    .sidebar-text-link { padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .sidebar-text-link:last-child { border-bottom: none; }
    .sidebar-text-link a { color: #4da6ff; font-size: 0.95rem; font-weight: 500; text-decoration: none; display: flex; align-items: flex-start; gap: 8px; transition: all 0.3s ease; line-height: 1.5; }
    .sidebar-text-link a i { margin-top: 4px; font-size: 0.8rem; color: #ffcc00; flex-shrink: 0; }
    .sidebar-text-link a:hover { color: #fff; transform: translateX(5px); text-decoration: underline; }
    .mini-avatar { width: 24px; height: 24px; border-radius: 50%; object-fit: cover; vertical-align: middle; margin-right: 6px; }
    .author-link { font-weight: 600; cursor: pointer; }
    .verified-tick { color: #1da1f2; margin-left: 4px; font-size: 0.8em; }
    .card-author-img { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; margin-right: 8px; border: 1px solid #ddd; }
    .pagination-controls { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; flex-wrap: wrap; }
    .page-btn { padding: 6px 12px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; font-weight: 600; font-size: 0.9rem; min-width: 38px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }
    .page-btn.active { background: #0066cc; color: white; border-color: #0066cc; }
    @media (max-width: 600px) { .page-btn { padding: 5px 8px; font-size: 0.8rem; min-width: 32px; height: 32px; } }
    #search-full-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 20000; display: none; justify-content: center; padding-top: 80px; }
    .search-modal { width: 90%; max-width: 650px; background: #fff; border-radius: 15px; overflow: hidden; height: fit-content; }
    .search-header { display: flex; align-items: center; padding: 15px 20px; border-bottom: 2px solid #f0f0f0; }
    .search-header input { flex: 1; border: none; outline: none; font-size: 1.2rem; padding: 10px; }
    .search-result-item { display: flex; gap: 15px; padding: 12px; border-bottom: 1px solid #f9f9f9; cursor: pointer; }
    .search-result-item:hover { background: #f5faff; }
    .search-result-item img { width: 60px; height: 45px; object-fit: cover; border-radius: 4px; }
    .related-section { margin-top: 50px; padding-top: 30px; border-top: 2px solid #eee; }
    .related-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 20px; }
    .related-card { background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: 0.3s; cursor: pointer; border: 1px solid #f0f0f0; }
    .related-card:hover { transform: translateY(-5px); }
    .related-card img { width: 100%; height: 140px; object-fit: cover; }
    .related-card-content { padding: 15px; }
    .related-card-title { font-size: 0.95rem; font-weight: 600; margin: 0 0 8px; line-height: 1.4; transition: color 0.3s ease; }
    .related-card:hover .related-card-title { color: #0066cc; }
    [data-theme="dark"] .related-card { background: #1e1e1e; border-color: #333; color: #fff; }
    [data-theme="dark"] .related-card:hover .related-card-title { color: #4da6ff !important; }
`;
document.head.appendChild(style);

function getTodayDate() {
    const d = new Date();
    return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

document.addEventListener('DOMContentLoaded', async function () {
    highlightActiveMenu();
    await loadArticlesFast();
    injectRelatedArticles();

    const homeContainer = document.getElementById('articles-container');
    if (homeContainer) { renderArticles(homeContainer, 'all'); }
    const techContainer = document.getElementById('tech-page-container');
    if (techContainer) { renderArticles(techContainer, 'Tech'); }
    const latestContainer = document.getElementById('latest-page-container') || document.getElementById('latest-news-container');
    if (latestContainer) { renderArticles(latestContainer, 'Latest News'); }

    const sidebar = document.getElementById('sidebar-articles');
    if (sidebar) updateSidebar(sidebar);

    injectMultipleAlsoRead();
    injectHeaderAuthorPic();
    initCommentSystem();
    injectNotificationBell();
    setupCopyLinkButtons();
    initLiveSearchSystem();
    initTopBarFeatures();

    if (isArticlePage) {
        const goBackBtn = document.querySelector('.breadcrumb a[onclick*="history.back"]');
        if (goBackBtn) {
            goBackBtn.removeAttribute('onclick');
            goBackBtn.addEventListener('click', function (e) {
                e.preventDefault();
                if (document.referrer.includes(window.location.hostname)) window.history.back();
                else window.location.href = rootPrefix || '/';
            });
        }
    }

    setTimeout(() => {
        const savedScroll = sessionStorage.getItem('scroll_' + pageKey);
        if (savedScroll && !isArticlePage) window.scrollTo({ top: parseInt(savedScroll), behavior: 'instant' });
    }, 50);

    setTimeout(initNotificationPopup, 3000);
});

async function loadArticlesFast() {
    try {
        const cachedData = sessionStorage.getItem('cached_ultimateschooling_data');
        if (cachedData) allArticles = JSON.parse(cachedData);

        const response = await fetch(basePath + 'data.json?v=' + new Date().getTime());
        if (response.ok) {
            const freshArticles = await response.json();
            // DATE FIX: Do NOT override dates from data.json
            // Articles keep their real publish date
            freshArticles.sort((a, b) => b.id - a.id);
            allArticles = freshArticles;
            sessionStorage.setItem('cached_ultimateschooling_data', JSON.stringify(allArticles));
        }
    } catch (e) { console.error('Data load error:', e); }
}

function renderArticles(container, filter) {
    const containerId = container.id || 'default';
    if (!containerState[containerId]) {
        const savedPage = parseInt(sessionStorage.getItem('page_' + containerId + '_' + pageKey)) || 1;
        containerState[containerId] = { page: savedPage, filter: filter };
    }
    containerState[containerId].filter = filter;
    let currentPage = containerState[containerId].page;

    let displayList = filter !== 'all'
        ? allArticles.filter(art => art.category === filter || (art.category && art.category.includes(filter)))
        : allArticles;
    const totalPages = Math.ceil(displayList.length / config.itemsPerPage);
    if (currentPage > totalPages) { currentPage = 1; containerState[containerId].page = 1; }
    const paginatedItems = displayList.slice((currentPage - 1) * config.itemsPerPage, currentPage * config.itemsPerPage);

    const cardsHTML = paginatedItems.map((art, index) => {
        const priorityAttr = index < 2 ? 'fetchpriority="high"' : 'loading="lazy"';
        const imgSrc = art.image && art.image.startsWith('http') ? art.image : linkPrefix + (art.image || '');
        return `<article class="news-card" onclick="sessionStorage.setItem('scroll_${pageKey}', window.scrollY); window.location.href='${linkPrefix}${art.filename}'">
            <div class="article-image">
                <div class="trending-badge"><i class="fas fa-fire"></i> Trending</div>
                <img src="${imgSrc}" alt="${art.title}" width="1200" height="675" ${priorityAttr}>
            </div>
            <div class="news-content">
                <h3 class="news-title">${art.title}</h3>
                <p class="news-excerpt">${art.excerpt || 'Read the full story...'}</p>
                <div class="news-meta">
                    <img src="${art.authorImg || config.defaultAuthorImg}" class="card-author-img" alt="${art.author || config.authorName}">
                    <span>${art.author || config.authorName} <i class="fas fa-check-circle verified-tick"></i></span>
                    <span class="separator">|</span>
                    <span class="date">${art.date || ''}</span>
                </div>
            </div>
        </article>`;
    }).join('');

    // Set grid cards directly as innerHTML of the container
    container.innerHTML = cardsHTML;

    // Pagination goes into a SIBLING div OUTSIDE the grid container
    const paginId = 'pagination-' + containerId;
    let paginWrapper = document.getElementById(paginId);
    if (!paginWrapper) {
        paginWrapper = document.createElement('div');
        paginWrapper.id = paginId;
        container.parentNode.insertBefore(paginWrapper, container.nextSibling);
    }
    paginWrapper.innerHTML = '';
    if (totalPages > 1) renderPaginationControls(paginWrapper, totalPages, currentPage, containerId, container);
}

function renderPaginationControls(wrapper, totalPages, currentPage, containerId, gridContainer) {
    const paginationDiv = document.createElement('div');
    paginationDiv.className = 'pagination-controls';
    if (currentPage > 1) paginationDiv.appendChild(createPageBtn('«', () => changePage(currentPage - 1, containerId, gridContainer)));
    let pages = [];
    if (totalPages <= 5) pages = Array.from({ length: totalPages }, (_, i) => i + 1);
    else if (currentPage <= 2) pages = [1, 2, 3, '...', totalPages];
    else if (currentPage >= totalPages - 1) pages = [1, '...', totalPages - 2, totalPages - 1, totalPages];
    else pages = [1, '...', currentPage, '...', totalPages];
    pages.forEach(p => {
        if (p === '...') { const d = document.createElement('span'); d.innerText = '...'; d.style.padding = '5px'; paginationDiv.appendChild(d); }
        else { const btn = createPageBtn(p, () => changePage(p, containerId, gridContainer)); if (p === currentPage) btn.classList.add('active'); paginationDiv.appendChild(btn); }
    });
    if (currentPage < totalPages) paginationDiv.appendChild(createPageBtn('»', () => changePage(currentPage + 1, containerId, gridContainer)));
    wrapper.appendChild(paginationDiv);
}

function createPageBtn(text, onClick) {
    const btn = document.createElement('button');
    btn.className = 'page-btn'; btn.innerText = text; btn.onclick = onClick; return btn;
}

function changePage(newPage, containerId, gridContainer) {
    if (!containerState[containerId]) containerState[containerId] = { page: 1, filter: 'all' };
    containerState[containerId].page = newPage;
    sessionStorage.setItem('page_' + containerId + '_' + pageKey, newPage);
    renderArticles(gridContainer, containerState[containerId].filter);
    window.scrollTo({ top: gridContainer.getBoundingClientRect().top + window.pageYOffset - 100, behavior: 'smooth' });
}

function updateSidebar(sidebar) {
    const recent = allArticles.filter(a => a.filename !== window.location.pathname.split('/').pop()).slice(0, 26);
    sidebar.innerHTML = recent.map(art => `
        <div class="sidebar-text-link">
            <a href="${linkPrefix}${art.filename}"><i class="fas fa-chevron-right"></i> ${art.title}</a>
        </div>`).join('');
}

function injectMultipleAlsoRead() {
    if (!isArticlePage) return;
    const articleBody = document.querySelector('.article-body');
    if (!articleBody) return;
    document.querySelectorAll('.also-read').forEach(el => el.remove());
    const currentFile = window.location.pathname.split('/').pop();
    const others = allArticles.filter(a => a.filename !== currentFile);
    if (others.length === 0) return;
    const shuffled = others.sort(() => 0.5 - Math.random());
    const headings = Array.from(articleBody.querySelectorAll('h2, h3'));
    let boxCount = 0;
    const maxBoxes = 5;
    headings.forEach((heading, index) => {
        if (boxCount >= maxBoxes || index % 2 !== 0) return;
        if (shuffled[boxCount]) {
            const art = shuffled[boxCount];
            heading.insertAdjacentHTML('afterend', `<div class="also-read"><h3><i class="fas fa-book-reader"></i> Also Read</h3><a href="${linkPrefix}${art.filename}">${art.title}</a></div>`);
            boxCount++;
        }
    });
    if (boxCount < maxBoxes) {
        const paragraphs = Array.from(articleBody.querySelectorAll('p'));
        paragraphs.forEach((p, index) => {
            if (boxCount >= maxBoxes || index < 2 || index % 3 !== 0) return;
            if (shuffled[boxCount]) {
                const art = shuffled[boxCount];
                p.insertAdjacentHTML('afterend', `<div class="also-read"><h3><i class="fas fa-book-reader"></i> Also Read</h3><a href="${linkPrefix}${art.filename}">${art.title}</a></div>`);
                boxCount++;
            }
        });
    }
}

function injectRelatedArticles() {
    if (!isArticlePage) return;
    const commentsSection = document.querySelector('.comments-section');
    if (!commentsSection) return;
    const currentFile = window.location.pathname.split('/').pop();
    const selected = allArticles.filter(art => art.filename !== currentFile).sort(() => 0.5 - Math.random()).slice(0, 3);
    if (selected.length === 0) return;
    const relatedDiv = document.createElement('div');
    relatedDiv.className = 'related-section';
    relatedDiv.innerHTML = `<h2><i class="fas fa-layer-group" style="color:#0066cc;"></i> You May Also Like</h2><div class="related-grid">` +
        selected.map(art => {
            const img = art.image && art.image.startsWith('http') ? art.image : linkPrefix + art.image;
            return `<div class="related-card" onclick="window.location.href='${linkPrefix}${art.filename}'"><img src="${img}" alt="${art.title}" loading="lazy"><div class="related-card-content"><h4 class="related-card-title">${art.title}</h4><span style="font-size:0.75rem;color:#888;"><i class="far fa-clock"></i> ${art.date || ''}</span></div></div>`;
        }).join('') + `</div>`;
    commentsSection.parentNode.insertBefore(relatedDiv, commentsSection.nextSibling);
}

function injectHeaderAuthorPic() {
    if (!isArticlePage) return;
    const img = document.getElementById('header-author-img');
    const name = document.getElementById('header-author-name');
    if (img) img.src = config.defaultAuthorImg;
    if (name) name.innerHTML = config.authorName + ' <i class="fas fa-check-circle verified-tick"></i>';
}

function initCommentSystem() {
    const form = document.getElementById('comment-form'); if (!form) return;
    loadComments();
    form.onsubmit = (e) => {
        e.preventDefault();
        const comm = { name: document.getElementById('comment-name').value, date: getTodayDate(), text: document.getElementById('comment-msg').value };
        const key = 'comments_' + window.location.pathname.split('/').pop();
        let saved = JSON.parse(localStorage.getItem(key)) || [];
        saved.push(comm);
        localStorage.setItem(key, JSON.stringify(saved));
        renderSingleComment(comm);
        form.reset();
    };
}

function loadComments() {
    const key = 'comments_' + window.location.pathname.split('/').pop();
    (JSON.parse(localStorage.getItem(key)) || []).forEach(c => renderSingleComment(c));
}

function renderSingleComment(c) {
    const area = document.getElementById('comments-display-area'); if (!area) return;
    area.insertAdjacentHTML('beforeend', `<div style="display:flex;gap:15px;margin-bottom:20px;background:#f9f9f9;padding:15px;border-radius:8px;"><div style="width:40px;height:40px;background:#ddd;border-radius:50%;display:flex;align-items:center;justify-content:center;"><i class="fas fa-user"></i></div><div><div style="font-weight:bold;">${c.name} <span style="font-size:0.8rem;color:#888;font-weight:normal;margin-left:10px;">${c.date}</span></div><p style="margin-top:5px;font-size:0.95rem;">${c.text}</p></div></div>`);
}

function highlightActiveMenu() {
    const current = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.main-nav a').forEach(link => {
        const href = (link.getAttribute('href') || '').split('/').pop() || 'index.html';
        if (href === current) link.classList.add('active'); else link.classList.remove('active');
    });
}

function setupCopyLinkButtons() {
    document.body.addEventListener('click', (e) => {
        if (e.target.closest('.btn-copy')) { e.preventDefault(); navigator.clipboard.writeText(window.location.href); alert('Link Copied!'); }
    });
}

function injectNotificationBell() {
    const bell = document.createElement('div');
    bell.className = 'notification-bell';
    bell.style.cssText = 'position:fixed;bottom:20px;left:20px;width:50px;height:50px;background:#2c3e9c;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:1000;font-size:1.2rem;';
    bell.innerHTML = '<i class="fas fa-bell"></i>';
    document.body.appendChild(bell);
    bell.onclick = () => alert('📚 Stay tuned for the latest tech and learning guides from Ultimate Schooling! 💻');
}

function initNotificationPopup() {
    if (localStorage.getItem('notify_status_ultimateschooling')) return;
    const pop = document.createElement('div');
    pop.className = 'notify-popup-overlay';
    pop.innerHTML = `<div class="notify-popup" style="background:#fff;padding:30px;border-radius:12px;text-align:center;max-width:350px;"><div style="font-size:2rem;color:#0066cc;margin-bottom:15px;"><i class="fas fa-graduation-cap"></i></div><h3>Never Miss a Lesson!</h3><p>Get daily tech tutorials, AI guides, and coding tips from Ultimate Schooling.</p><div style="display:flex;gap:10px;justify-content:center;margin-top:20px;"><button class="btn-deny" style="padding:8px 20px;cursor:pointer;border:1px solid #ddd;border-radius:5px;">Not Now</button><button class="btn-allow" style="padding:8px 20px;background:#0066cc;color:#fff;border:none;border-radius:5px;cursor:pointer;">Allow</button></div></div>`;
    document.body.appendChild(pop);
    pop.querySelector('.btn-deny').onclick = () => { localStorage.setItem('notify_status_ultimateschooling', 'denied'); pop.remove(); };
    pop.querySelector('.btn-allow').onclick = () => { localStorage.setItem('notify_status_ultimateschooling', 'allowed'); pop.remove(); };
}

function initTopBarFeatures() {
    const dateDisplay = document.getElementById('current-date-display');
    if (dateDisplay) dateDisplay.innerHTML = '<i class="far fa-calendar-alt"></i> ' + new Date().toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });

    const ticker = document.getElementById('hot-news-ticker');
    if (ticker && allArticles.length > 0) ticker.innerHTML = allArticles.slice(0, 5).map(art => `<a href="${linkPrefix}${art.filename}"><i class="fas fa-code" style="color:#ffcc00;margin-right:5px;"></i>${art.title}</a>`).join('');

    const randomBtn = document.getElementById('random-article-btn');
    if (randomBtn) randomBtn.onclick = () => { if (allArticles.length) window.location.href = linkPrefix + allArticles[Math.floor(Math.random() * allArticles.length)].filename; };

    const darkBtn = document.getElementById('dark-mode-toggle');
    if (darkBtn) {
        darkBtn.onclick = () => {
            const isDark = document.documentElement.hasAttribute('data-theme');
            if (isDark) { document.documentElement.removeAttribute('data-theme'); localStorage.setItem('theme', 'light'); darkBtn.innerHTML = '<i class="fas fa-moon"></i>'; }
            else { document.documentElement.setAttribute('data-theme', 'dark'); localStorage.setItem('theme', 'dark'); darkBtn.innerHTML = '<i class="fas fa-sun" style="color:#ffcc00;"></i>'; }
        };
    }
}

function initLiveSearchSystem() {
    const overlay = document.createElement('div');
    overlay.id = 'search-full-overlay';
    overlay.innerHTML = `<div class="search-modal"><div class="search-header"><i class="fas fa-search" style="margin-right:10px;color:#888;"></i><input type="text" id="main-search-input" placeholder="Search articles & tutorials..."><i class="fas fa-times close-search-btn" style="cursor:pointer;margin-left:10px;color:#888;"></i></div><div id="search-results-list" style="max-height:400px;overflow-y:auto;"></div></div>`;
    document.body.appendChild(overlay);
    const searchIcon = document.querySelector('.search-icon');
    if (searchIcon) searchIcon.onclick = (e) => { e.preventDefault(); overlay.style.display = 'flex'; document.getElementById('main-search-input').focus(); };
    overlay.querySelector('.close-search-btn').onclick = () => overlay.style.display = 'none';
    overlay.onclick = (e) => { if (e.target === overlay) overlay.style.display = 'none'; };
    document.getElementById('main-search-input').oninput = function () {
        const val = this.value.toLowerCase();
        const list = document.getElementById('search-results-list');
        list.innerHTML = '';
        if (val.length < 1) return;
        const filtered = allArticles.filter(a => a.title.toLowerCase().includes(val)).slice(0, 8);
        list.innerHTML = filtered.length
            ? filtered.map(art => {
                const img = art.image && art.image.startsWith('http') ? art.image : linkPrefix + art.image;
                return `<div class="search-result-item" onclick="window.location.href='${linkPrefix}${art.filename}'"><img src="${img}" alt=""><div><h4 style="margin:0;font-size:0.95rem;">${art.title}</h4><small style="color:#888;">${art.category || ''}</small></div></div>`;
            }).join('')
            : '<p style="padding:20px;color:#888;text-align:center;">No results found.</p>';
    };
}

window.addEventListener('scroll', () => {
    const prog = document.getElementById('reading-progress');
    if (prog) prog.style.width = ((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100) + '%';
    const topBtn = document.getElementById('scroll-to-top');
    if (topBtn) { if (window.scrollY > 300) topBtn.classList.add('show'); else topBtn.classList.remove('show'); }
});

document.head.insertAdjacentHTML('beforeend', '<style>.content-wrapper{display:flex!important;align-items:flex-start!important}.sidebar{display:flex!important;flex-direction:column!important;height:fit-content!important;min-height:auto!important}.sidebar-widget{flex:none!important;height:fit-content!important}.latest-articles{max-height:none!important;overflow-y:visible!important}</style>');