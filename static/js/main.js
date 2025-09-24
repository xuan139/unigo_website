
// ======================
// i18n 多语言
// ======================
  
async function loadTranslations(lang) {
    try {
      const res = await fetch(`/static/i18n/${lang}.json?v=${Date.now()}`);
      if (!res.ok) throw new Error('Failed to load translations');
      return await res.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  }
  
  function applyTranslations(translations) {
    if (!translations) return;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (translations[key]) {
        const tag = el.tagName.toLowerCase();
        const value = translations[key];
        if (tag === 'title') {
          document.title = value;
        } else if (tag === 'input' || tag === 'textarea') {
          el.placeholder = value;
        } else if (tag === 'button') {
          el.textContent = value;
        } else {
          el.innerHTML = String(value).replace(/\n/g, '<br>');
        }
      }
    });
  }
  
  async function updateTexts(lang) {
    const translations = await loadTranslations(lang);
    applyTranslations(translations);
  }
  
  function setLangUI(lang) {
    const btn = document.getElementById('langDropdown');
    if (!btn) return;
    const map = {
      en: { flag: '🇺🇸', label: 'English' },
      zh: { flag: '🇨🇳', label: '简体中文' },
      zh_tw: { flag: '🇭🇰', label: '繁體中文' },
      ja: { flag: '🇯🇵', label: '日本語' },
      ko: { flag: '🇰🇷', label: '한국어' },
      th: { flag: '🇹🇭', label: 'ไทย' }
    };
    const info = map[lang] || map.en;
    btn.querySelector('.flag').textContent = info.flag;
    btn.querySelector('.label').textContent = info.label;
  }
  
  // 绑定语言切换事件
  document.querySelectorAll('.lang-item').forEach(item => {
    item.addEventListener('click', async (e) => {
      e.preventDefault();
      const lang = item.getAttribute('data-lang');
      await updateTexts(lang);
      localStorage.setItem('lang', lang);
      document.documentElement.setAttribute('lang', lang);
      setLangUI(lang);
    });
  });
  
  // ======================
  // FAQ 搜索
  // ======================
  (function() {
    const searchEl = document.getElementById('faqSearch');
    if (!searchEl) return;
    searchEl.addEventListener('input', function(e) {
      const searchTerm = e.target.value.toLowerCase();
      document.querySelectorAll('.professional-accordion-item').forEach(item => {
        const q = (item.querySelector('.question-title')?.textContent || '').toLowerCase();
        const a = (item.querySelector('.answer-text')?.textContent || '').toLowerCase();
        item.style.display = (q.includes(searchTerm) || a.includes(searchTerm)) ? 'block' : 'none';
      });
    });
  })();
  
  // ======================
  // 页面加载初始化
  // ======================


  document.addEventListener("DOMContentLoaded", function () {
    // 1. 点击语言选项后关闭 dropdown
    const langItems = document.querySelectorAll(".lang-item");
    langItems.forEach(item => {
      item.addEventListener("click", function () {
        // 切换语言逻辑（你原本的语言切换代码放这里）
  
        // 自动关闭 dropdown
        const dropdownToggle = document.getElementById("langDropdown");
        const dropdownInstance = bootstrap.Dropdown.getInstance(dropdownToggle);
        if (dropdownInstance) {
          dropdownInstance.hide();
        }
  
        // 如果是手机端，顺便关闭整个 navbar collapse
        const navbarCollapse = document.getElementById("navbarNav");
        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
        if (bsCollapse) {
          bsCollapse.hide();
        }
      });
    });
  
    // 2. 点击普通导航链接时（核心功能、优势等），也自动关闭手机菜单
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    navLinks.forEach(link => {
      link.addEventListener("click", function () {
        const navbarCollapse = document.getElementById("navbarNav");
        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
        if (bsCollapse) {
          bsCollapse.hide();
        }
      });
    });
  });

  
  window.addEventListener('DOMContentLoaded', async () => {
    // i18n 初始化
    let savedLang = localStorage.getItem('lang');
    if (!savedLang) {
      const nav = (navigator.language || 'en').toLowerCase();
      if (nav.startsWith('zh-tw') || nav.startsWith('zh-hk') || nav.startsWith('zh-hant')) savedLang = 'zh_tw';
      else if (nav.startsWith('zh')) savedLang = 'zh';
      else if (nav.startsWith('ja')) savedLang = 'ja';
      else if (nav.startsWith('ko')) savedLang = 'ko';
      else if (nav.startsWith('th')) savedLang = 'th';
      else savedLang = 'en';
    }
    document.documentElement.setAttribute('lang', savedLang);
    await updateTexts(savedLang);
    setLangUI(savedLang);
  });
  
  // ======================
  // Header 滚动交互
  // ======================
  const navbar = document.querySelector('.navbar');
  const progress = document.getElementById('scroll-progress');
  let lastY = 0;
  
  const links = document.querySelectorAll('.navbar .nav-link[href^="#"]');
  const sections = Array.from(links).map(a => ({
    a, id: a.getAttribute('href'),
    el: document.querySelector(a.getAttribute('href'))
  })).filter(x => x.id && x.el);
  
  function updateActiveLink(y) {
    const offset = 120;
    let current = null;
    for (const s of sections) {
      const top = s.el.getBoundingClientRect().top + window.scrollY;
      if (y + offset >= top) current = s;
    }
    links.forEach(l => l.classList.remove('active'));
    if (current) current.a.classList.add('active');
  }
  
  function onScroll() {
    const y = window.scrollY || document.documentElement.scrollTop;
    if (navbar) {
      if (y > 10) navbar.classList.add('navbar-scrolled');
      else navbar.classList.remove('navbar-scrolled');
      if (y > lastY && y > 80) navbar.classList.add('navbar-hidden');
      else navbar.classList.remove('navbar-hidden');
    }
    if (progress) {
      const doc = document.documentElement;
      const pct = (doc.scrollHeight - doc.clientHeight) > 0 ? (y / (doc.scrollHeight - doc.clientHeight)) * 100 : 0;
      progress.style.width = pct + '%';
    }
    updateActiveLink(y);
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  
  // ======================
  // 导航点击后自动收起
  // ======================
  const collapseEl = document.getElementById('navbarNav');
  if (collapseEl) {
    const navLinks = document.querySelectorAll('.navbar .nav-link[href^="#"]');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (collapseEl.classList.contains('show')) {
          bootstrap.Collapse.getOrCreateInstance(collapseEl).hide();
        }
      });
    });
  }
  
  // ======================
  // FAQ 鼠标悬停展开
  // ======================
  document.querySelectorAll('.professional-accordion-button').forEach(button => {
    const targetId = button.getAttribute('data-bs-target');
    const collapseEl = document.querySelector(targetId);
    if (!collapseEl) return;
    button.addEventListener('mouseenter', () => new bootstrap.Collapse(collapseEl, { toggle: false }).show());
    button.addEventListener('mouseleave', () => new bootstrap.Collapse(collapseEl, { toggle: false }).hide());
  });
  
  // ======================
  // 强制刷新回顶部
  // ======================
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }
  window.addEventListener('load', () => window.scrollTo(0, 0));
  
  // ======================
  // Serial 表单
  // ======================
  const serialForm = document.getElementById("serialForm");
  if (serialForm) {
    serialForm.addEventListener("submit", function(e) {
      e.preventDefault();
      const searchValue = document.getElementById("search").value;
      fetch(`/serials_ajax?search=${encodeURIComponent(searchValue)}`)
        .then(res => res.json())
        .then(data => alert(`${data.result}`))
        .catch(err => { alert("Error fetching data"); console.error(err); });
    });
  }
  
  // ======================
  // Chatbot
  // ======================
  const toggleBtn = document.getElementById("chatbot-toggle");
  const chatBox = document.getElementById("chatbot-box");
  const closeBtn = document.getElementById("chatbot-close");
  const chatLog = document.getElementById("chat-log");
  
  if (toggleBtn && chatBox && closeBtn) {
    toggleBtn.onclick = () => {
      chatBox.style.display = (chatBox.style.display === "flex") ? "none" : "flex";
      chatBox.scrollTop = chatBox.scrollHeight;
    };
    closeBtn.onclick = () => { chatBox.style.display = "none"; };
    document.addEventListener('keydown', e => {
      if (e.key === "Escape") chatBox.style.display = "none";
    });
  }
  
  function sendMessage() {
    const input = document.getElementById("chat-message");
    const msg = input.value.trim();
    if (!msg) return;
    chatLog.innerHTML += `<div><strong>You:</strong> ${msg}</div>`;
    input.value = "";
    setTimeout(() => {
      const reply = getBotReply(msg);
      chatLog.innerHTML += `<div><strong>Bot:</strong> ${reply}</div>`;
      chatLog.scrollTop = chatLog.scrollHeight;
    }, 500);
  }
  
  function getBotReply(msg) {
    msg = msg.toLowerCase();
    if (msg.includes("download")) return "You can download it from the Downloads page.";
    if (msg.includes("vmware")) return "Yes, a VMware image is included in your SSD package.";
    if (msg.includes("steam")) return "Steam is ready with pre-installed games.";
    return "I'm here to assist you! You can ask about setup, features, or downloads.";
  }
  