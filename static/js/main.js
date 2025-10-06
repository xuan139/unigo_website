/**
 * Main JavaScript file for handling internationalization (i18n), navigation, FAQ search,
 * serial form submission, chatbot functionality, and UI interactions.
 * Organized into modular objects for better maintainability and readability.
 */

// ======================
// Utility Functions
// ======================
const Utils = {
  /**
   * Determines the user's preferred language based on browser settings.
   * Maps browser language codes to supported languages, defaulting to 'en' if unsupported.
   * @returns {string} The selected language code (e.g., 'en', 'zh', 'zh_tw').
   */
  getLanguageFromNavigator() {
    // const navLang = navigator.language || navigator.userLanguage; // Get browser language (e.g., 'en-US', 'zh-CN')
    // if (navLang.startsWith('zh-HK') || navLang.startsWith('zh-TW') || navLang.startsWith('zh-hant')) {
    //   return 'zh_tw'; // Traditional Chinese for Hong Kong or Taiwan
    // }
    // if (navLang.startsWith('zh')) return 'zh'; // Simplified Chinese
    // if (navLang.startsWith('ja')) return 'ja'; // Japanese
    // if (navLang.startsWith('ko')) return 'ko'; // Korean
    // if (navLang.startsWith('th')) return 'th'; // Thai
    return 'zh_tw'; // Default to English
  }
};

// ======================
// Internationalization (i18n)
// ======================
const I18n = {
  /**
   * Loads translation JSON file for the specified language.
   * Includes cache-busting via timestamp to ensure fresh data.
   * @param {string} lang - Language code (e.g., 'en', 'zh').
   * @returns {Promise<object|null>} Translation data or null if loading fails.
   */
  async loadTranslations(lang) {
    try {
      const res = await fetch(`/static/i18n/${lang}.json?v=${Date.now()}`); // Fetch translation file
      if (!res.ok) throw new Error('Failed to load translations'); // Check for HTTP errors
      return await res.json(); // Parse JSON response
    } catch (e) {
      console.error('Translation load error:', e); // Log error for debugging
      return null; // Return null on failure
    }
  },

  /**
   * Applies translations to elements with 'data-i18n' attributes.
   * Updates text content based on element type (title, input, button, etc.).
   * @param {object} translations - Translation key-value pairs.
   */
  applyTranslations(translations) {
    if (!translations) return; // Exit if no translations provided
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n'); // Get translation key
      if (translations[key]) {
        const tag = el.tagName.toLowerCase(); // Get element tag name
        const value = translations[key]; // Get translated text
        if (tag === 'title') {
          document.title = value; // Update page title
        } else if (tag === 'input' || tag === 'textarea') {
          el.placeholder = value; // Update placeholder for input/textarea
        } else if (tag === 'button') {
          el.textContent = value; // Update button text
        } else {
          el.innerHTML = String(value).replace(/\n/g, '<br>'); // Update other elements, converting newlines to <br>
        }
      }
    });
  },

  /**
   * Updates all translatable elements on the page with the specified language.
   * @param {string} lang - Language code to apply.
   */
  async updateTexts(lang) {
    const translations = await this.loadTranslations(lang); // Load translations
    this.applyTranslations(translations); // Apply them to the DOM
  },

  /**
   * Updates the language dropdown UI to reflect the current language.
   * Sets flag and label based on the selected language.
   * @param {string} lang - Language code to display.
   */
  setLangUI(lang) {
    const btn = document.getElementById('langDropdown'); // Get language dropdown button
    if (!btn) return; // Exit if button not found
    const map = {
      en: { flag: '🇺🇸', label: 'English' },
      zh: { flag: '🇨🇳', label: '简体中文' },
      zh_tw: { flag: '🇭🇰', label: '繁體中文' },
      ja: { flag: '🇯🇵', label: '日本語' },
      ko: { flag: '🇰🇷', label: '한국어' },
      th: { flag: '🇹🇭', label: 'ไทย' }
    };
    const info = map[lang] || map.en; // Get language info, default to English
    btn.querySelector('.flag').textContent = info.flag; // Update flag emoji
    btn.querySelector('.label').textContent = info.label; // Update language label
  },

  /**
   * Initializes the page language based on saved preference or browser settings.
   * Sets the HTML lang attribute and updates UI.
   */
  // async initLanguage() {
  //   let lang = localStorage.getItem('lang') || Utils.getLanguageFromNavigator(); // Get saved or browser language
  //   document.documentElement.setAttribute('lang', lang); // Set HTML lang attribute
  //   await this.updateTexts(lang); // Load and apply translations
  //   this.setLangUI(lang); // Update dropdown UI
  // },

  async initLanguage() {
    let lang =  Utils.getLanguageFromNavigator(); // Get saved or browser language
    document.documentElement.setAttribute('lang', lang); // Set HTML lang attribute
    await this.updateTexts(lang); // Load and apply translations
    this.setLangUI(lang); // Update dropdown UI
  },

  /**
   * Binds click events to language switcher items.
   * Updates language, saves preference, and closes dropdown/nav on mobile.
   */
  bindLanguageSwitch() {
    document.querySelectorAll('.lang-item').forEach(item => {
      item.addEventListener('click', async (e) => {
        e.preventDefault(); // Prevent default link behavior
        const lang = item.getAttribute('data-lang'); // Get selected language
        await this.updateTexts(lang); // Update page text
        localStorage.setItem('lang', lang); // Save language preference
        document.documentElement.setAttribute('lang', lang); // Update HTML lang
        this.setLangUI(lang); // Update dropdown UI
        // Close dropdown
        const dropdownToggle = document.getElementById('langDropdown');
        const dropdownInstance = bootstrap.Dropdown.getInstance(dropdownToggle);
        if (dropdownInstance) dropdownInstance.hide();
        // Close navbar on mobile
        const navbarCollapse = document.getElementById('navbarNav');
        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
        if (bsCollapse) bsCollapse.hide();
      });
    });
  }
};

// ======================
// Navigation
// ======================
const Navigation = {
  /**
   * Initializes scroll restoration to ensure page loads at the top.
   */
  initScrollBehavior() {
    if ('scrollRestoration' in history) {
      history.scrollRestoration = 'manual'; // Prevent browser from restoring scroll position
    }
    window.addEventListener('load', () => window.scrollTo(0, 0)); // Scroll to top on load
  },

  /**
   * Handles navbar behavior on scroll, including hiding/showing, progress bar,
   * and active link highlighting.
   */
  initNavbarScroll() {
    const navbar = document.querySelector('.navbar'); // Get navbar element
    const progress = document.getElementById('scroll-progress'); // Get scroll progress bar
    const links = document.querySelectorAll('.navbar .nav-link[href^="#"]'); // Get section links
    const sections = Array.from(links)
      .map(a => ({
        a, // Link element
        id: a.getAttribute('href'), // Section ID
        el: document.querySelector(a.getAttribute('href')) // Target section element
      }))
      .filter(x => x.id && x.el); // Filter valid sections
    let lastY = 0; // Track last scroll position

    /**
     * Updates the active navigation link based on scroll position.
     * @param {number} y - Current scroll position.
     */
    function updateActiveLink(y) {
      const offset = 120; // Offset for active link detection
      let current = null;
      for (const s of sections) {
        const top = s.el.getBoundingClientRect().top + window.scrollY; // Section top position
        if (y + offset >= top) current = s; // Mark as current if within view
      }
      links.forEach(l => l.classList.remove('active')); // Clear active state
      if (current) current.a.classList.add('active'); // Set active link
    }

    /**
     * Handles scroll events to update navbar classes and progress bar.
     */
    function onScroll() {
      const y = window.scrollY || document.documentElement.scrollTop; // Get current scroll position
      if (navbar) {
        navbar.classList.toggle('navbar-scrolled', y > 10); // Add scrolled class after 10px
        navbar.classList.toggle('navbar-hidden', y > lastY && y > 80); // Hide navbar on scroll down
      }
      if (progress) {
        const doc = document.documentElement;
        const pct = (doc.scrollHeight - doc.clientHeight) > 0
          ? (y / (doc.scrollHeight - doc.clientHeight)) * 100
          : 0; // Calculate scroll progress percentage
        progress.style.width = pct + '%'; // Update progress bar
      }
      updateActiveLink(y); // Update active link
      lastY = y; // Update last scroll position
    }

    window.addEventListener('scroll', onScroll, { passive: true }); // Add scroll listener
    onScroll(); // Initialize on load
  },

  /**
   * Binds click events to navigation links to collapse navbar on mobile.
   */
  bindNavLinks() {
    const collapseEl = document.getElementById('navbarNav'); // Get navbar collapse element
    if (collapseEl) {
      document.querySelectorAll('.navbar .nav-link[href^="#"]').forEach(link => {
        link.addEventListener('click', () => {
          if (collapseEl.classList.contains('show')) {
            bootstrap.Collapse.getOrCreateInstance(collapseEl).hide(); // Collapse navbar
          }
        });
      });
    }
  }
};

// ======================
// FAQ
// ======================
const FAQ = {
  /**
   * Initializes FAQ search functionality.
   * Filters accordion items based on search input.
   * 
   * 
   */

  
  initSearch() {
    const searchEl = document.getElementById('faqSearch'); // Get search input
    if (!searchEl) return; // Exit if not found
    searchEl.addEventListener('input', function(e) {
      const searchTerm = e.target.value.toLowerCase(); // Get search term
      document.querySelectorAll('.professional-accordion-item').forEach(item => {
        const q = (item.querySelector('.question-title')?.textContent || '').toLowerCase(); // Get question text
        const a = (item.querySelector('.answer-text')?.textContent || '').toLowerCase(); // Get answer text
        item.style.display = (q.includes(searchTerm) || a.includes(searchTerm)) ? 'block' : 'none'; // Show/hide item
      });
    });
  },

  /**
   * Initializes hover effects for FAQ accordion buttons.
   * Shows/hides accordion content on mouse enter/leave.
   */
  initAccordionHover() {
    document.querySelectorAll('.professional-accordion-button').forEach(button => {
      const targetId = button.getAttribute('data-bs-target'); // Get target collapse ID
      const collapseEl = document.querySelector(targetId); // Get collapse element
      if (!collapseEl) return; // Exit if not found
      button.addEventListener('mouseenter', () => new bootstrap.Collapse(collapseEl, { toggle: false }).show()); // Show on hover
      button.addEventListener('mouseleave', () => new bootstrap.Collapse(collapseEl, { toggle: false }).hide()); // Hide on leave
    });
  }
};

// ======================
// Serial Form
// ======================
const SerialForm = {
  /**
   * Initializes serial form submission.
   * Submits search value via AJAX and displays result.
   */
  init() {
    const serialForm = document.getElementById('serialForm'); // Get serial form
    if (serialForm) {
      serialForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        const searchValue = document.getElementById('search').value; // Get search input value
        fetch(`/serials_ajax?search=${encodeURIComponent(searchValue)}`) // Send AJAX request
          .then(res => res.json()) // Parse JSON response
          .then(data => alert(`${data.result}`)) // Display result
          .catch(err => {
            alert('Error fetching data'); // Show error message
            console.error(err); // Log error
          });
      });
    }
  }
};

// ======================
// Chatbot
// ======================
const Chatbot = {
  /**
   * Initializes chatbot toggle and close functionality.
   * Handles visibility and escape key press.
   */
  init() {
    const toggleBtn = document.getElementById('chatbot-toggle'); // Get toggle button
    const chatBox = document.getElementById('chatbot-box'); // Get chatbox
    const closeBtn = document.getElementById('chatbot-close'); // Get close button

    if (toggleBtn && chatBox && closeBtn) {
      toggleBtn.onclick = () => {
        chatBox.style.display = chatBox.style.display === 'flex' ? 'none' : 'flex'; // Toggle chatbox visibility
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
      };
      closeBtn.onclick = () => { chatBox.style.display = 'none'; }; // Hide chatbox
      document.addEventListener('keydown', e => {
        if (e.key === 'Escape') chatBox.style.display = 'none'; // Hide on Escape key
      });
    }
  },

  /**
   * Sends a user message to the chatbot and displays the bot's reply.
   */
  sendMessage() {
    const input = document.getElementById('chat-message'); // Get message input
    const chatLog = document.getElementById('chat-log'); // Get chat log
    const msg = input.value.trim(); // Get and trim user message
    if (!msg) return; // Exit if message is empty
    chatLog.innerHTML += `<div><strong>You:</strong> ${msg}</div>`; // Add user message to log
    input.value = ''; // Clear input
    setTimeout(() => {
      const reply = this.getBotReply(msg); // Get bot reply
      chatLog.innerHTML += `<div><strong>Bot:</strong> ${reply}</div>`; // Add bot reply to log
      chatLog.scrollTop = chatLog.scrollHeight; // Scroll to bottom
    }, 500); // Simulate response delay
  },

  /**
   * Generates a bot reply based on the user's message.
   * @param {string} msg - User's message (lowercase).
   * @returns {string} Bot's response.
   */
  getBotReply(msg) {
    msg = msg.toLowerCase(); // Normalize message
    if (msg.includes('download')) return 'You can download it from the Downloads page.';
    if (msg.includes('vmware')) return 'Yes, a VMware image is included in your SSD package.';
    if (msg.includes('steam')) return 'Steam is ready with pre-installed games.';
    return 'I\'m here to assist you! You can ask about setup, features, or downloads.'; // Default response
  }
};

// ======================
// Initialization
// ======================
/**
 * Initializes all features when the DOM is fully loaded.
 */
document.addEventListener('DOMContentLoaded', async () => {
  await I18n.initLanguage(); // Initialize language and translations
  I18n.bindLanguageSwitch(); // Bind language switcher events
  Navigation.initScrollBehavior(); // Set up scroll restoration
  Navigation.initNavbarScroll(); // Initialize navbar scroll behavior
  Navigation.bindNavLinks(); // Bind nav link click events
  FAQ.initSearch(); // Initialize FAQ search
  FAQ.initAccordionHover(); // Initialize FAQ accordion hover
  SerialForm.init(); // Initialize serial form
  Chatbot.init(); // Initialize chatbot
});

// Expose sendMessage for HTML onclick events
window.sendMessage = Chatbot.sendMessage.bind(Chatbot);



document.querySelectorAll('#qaAccordion .accordion-item').forEach(item => {
  const button = item.querySelector('.accordion-button');
  const collapse = item.querySelector('.accordion-collapse');

  item.addEventListener('mouseenter', () => {
    // 展开当前项
    const bsCollapse = new bootstrap.Collapse(collapse, { toggle: false });
    bsCollapse.show();
  });

  item.addEventListener('mouseleave', () => {
    // 收起当前项
    const bsCollapse = new bootstrap.Collapse(collapse, { toggle: false });
    bsCollapse.hide();
  });
});


  // 选中所有折叠菜单里的链接
  const navLinks = document.querySelectorAll('.navbar-collapse .nav-link');
  const navbarCollapse = document.querySelector('.navbar-collapse');

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      // 判断菜单是否展开
      if (navbarCollapse.classList.contains('show')) {
        // 使用 Bootstrap 的 Collapse API 收起菜单
        const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
          toggle: true
        });
        bsCollapse.hide();
      }
    });
  });
  
  window.onload = function() {
    window.scrollTo(0, 0);
  };