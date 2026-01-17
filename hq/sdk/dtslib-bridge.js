/**
 * DTSLIB HQ Bridge SDK v1.0.0
 * 본사-계열사 통합 연동 시스템
 *
 * @author DTSLIB HQ
 * @license MIT
 */

(function(global) {
    'use strict';

    const VERSION = '1.0.0';
    const HQ_BASE = 'https://dtslib1979.github.io/dtslib-branch';
    const HQ_API = HQ_BASE + '/hq/api';
    const HQ_NOTICES = HQ_BASE + '/hq/notices';

    // ═══════════════════════════════════════════════════════════
    // CORE: Bridge Engine
    // ═══════════════════════════════════════════════════════════

    class DTSLibBridge {
        constructor() {
            this.version = VERSION;
            this.branch = null;
            this.config = null;
            this.manifest = null;
            this.initialized = false;
            this.listeners = {};
            this.cache = new Map();
            this.heartbeatInterval = null;
        }

        // ─────────────────────────────────────────────────────────
        // Initialization
        // ─────────────────────────────────────────────────────────

        async init(options = {}) {
            if (this.initialized) return this;

            console.log(`%c[DTSLIB Bridge] v${VERSION} Initializing...`, 'color: #D4AF37; font-weight: bold;');

            // Detect current branch
            this.branch = options.branch || this._detectBranch();

            // Load configurations in parallel
            const [config, manifest] = await Promise.all([
                this._fetchJSON(HQ_API + '/config.json'),
                this._fetchJSON(HQ_API + '/manifest.json')
            ]);

            this.config = config;
            this.manifest = manifest;

            // Get branch-specific config
            this.branchConfig = this._getBranchConfig();

            // Initialize subsystems
            await this._initSubsystems(options);

            this.initialized = true;
            this._emit('ready', { branch: this.branch, config: this.branchConfig });

            console.log(`%c[DTSLIB Bridge] Connected as: ${this.branch.toUpperCase()}`, 'color: #10B981; font-weight: bold;');

            return this;
        }

        async _initSubsystems(options) {
            // Notice System
            if (options.notices !== false) {
                await this.notices.load();
            }

            // Heartbeat System
            if (options.heartbeat !== false) {
                this._startHeartbeat();
            }

            // Feature Flags
            this.features = new FeatureFlags(this.config?.features || {});

            // Analytics
            if (options.analytics !== false) {
                this.analytics.init();
            }

            // Inject HQ Branding (optional)
            if (options.branding !== false) {
                this._injectBranding();
            }
        }

        // ─────────────────────────────────────────────────────────
        // Branch Detection
        // ─────────────────────────────────────────────────────────

        _detectBranch() {
            const hostname = window.location.hostname;
            const pathname = window.location.pathname;

            // Direct domain check
            if (hostname.includes('koosy')) return 'koosy';
            if (hostname.includes('gohsy')) return 'gohsy';
            if (hostname.includes('papafly')) return 'papafly';
            if (hostname.includes('dtslib')) return 'hq';

            // GitHub Pages pattern: username.github.io/reponame/
            const match = pathname.match(/\/([^\/]+)/);
            if (match) {
                const repo = match[1].toLowerCase();
                if (['koosy', 'gohsy', 'papafly'].includes(repo)) return repo;
                if (repo === 'dtslib-branch') return 'hq';
            }

            return 'unknown';
        }

        _getBranchConfig() {
            if (!this.manifest?.branches) return null;
            return this.manifest.branches.find(b => b.id === this.branch) || null;
        }

        // ─────────────────────────────────────────────────────────
        // Notice System
        // ─────────────────────────────────────────────────────────

        notices = {
            _parent: this,
            data: [],
            dismissed: [],

            async load() {
                try {
                    const response = await fetch(HQ_NOTICES + '/notices.json?t=' + Date.now());
                    const json = await response.json();
                    this.data = json.notices || [];
                    this.dismissed = this._getDismissed();
                    this._render();
                } catch (e) {
                    console.warn('[DTSLIB Bridge] Notice load failed:', e.message);
                }
            },

            _getDismissed() {
                try {
                    return JSON.parse(localStorage.getItem('dtslib_dismissed_notices') || '[]');
                } catch { return []; }
            },

            _saveDismissed() {
                localStorage.setItem('dtslib_dismissed_notices', JSON.stringify(this.dismissed));
            },

            dismiss(id) {
                if (!this.dismissed.includes(id)) {
                    this.dismissed.push(id);
                    this._saveDismissed();
                }
                const el = document.getElementById('dtslib-notice-' + id);
                if (el) {
                    el.style.animation = 'dtslibSlideUp 0.3s ease forwards';
                    setTimeout(() => el.remove(), 300);
                }
            },

            _render() {
                const branch = this._parent.branch;
                const now = new Date();

                const active = this.data.filter(n =>
                    n.branches.includes(branch) &&
                    !this.dismissed.includes(n.id) &&
                    new Date(n.expiresAt) > now
                );

                if (active.length === 0) return;

                this._injectStyles();

                active.slice(0, 3).forEach((notice, i) => {
                    const banner = this._createBanner(notice, i);
                    document.body.insertBefore(banner, document.body.firstChild);
                });

                this._adjustPadding();
            },

            _createBanner(notice, index) {
                const styles = {
                    info: { bg: 'linear-gradient(135deg, #3B82F6, #1D4ED8)', icon: 'ℹ️' },
                    warning: { bg: 'linear-gradient(135deg, #F59E0B, #D97706)', icon: '⚠️' },
                    success: { bg: 'linear-gradient(135deg, #10B981, #059669)', icon: '✅' },
                    urgent: { bg: 'linear-gradient(135deg, #EF4444, #DC2626)', icon: '🚨' }
                };
                const style = styles[notice.type] || styles.info;

                const banner = document.createElement('div');
                banner.id = 'dtslib-notice-' + notice.id;
                banner.className = 'dtslib-notice';
                banner.style.cssText = `
                    position: fixed;
                    top: ${index * 52}px;
                    left: 0;
                    right: 0;
                    background: ${style.bg};
                    color: white;
                    padding: 14px 20px;
                    z-index: 10000;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    font-size: 14px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                    animation: dtslibSlideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                `;

                banner.innerHTML = `
                    <div style="display:flex;align-items:center;gap:12px;flex:1;">
                        <span style="font-size:20px;">${style.icon}</span>
                        <div>
                            <strong style="margin-right:10px;">${notice.title}</strong>
                            <span style="opacity:0.9;">${notice.content}</span>
                        </div>
                    </div>
                    <button onclick="DTSLIB.notices.dismiss('${notice.id}')" style="
                        background: rgba(255,255,255,0.2);
                        border: none;
                        color: white;
                        width: 30px;
                        height: 30px;
                        border-radius: 50%;
                        cursor: pointer;
                        font-size: 16px;
                        transition: all 0.2s;
                    " onmouseover="this.style.background='rgba(255,255,255,0.3)';this.style.transform='scale(1.1)'"
                       onmouseout="this.style.background='rgba(255,255,255,0.2)';this.style.transform='scale(1)'">✕</button>
                `;

                return banner;
            },

            _injectStyles() {
                if (document.getElementById('dtslib-notice-styles')) return;
                const style = document.createElement('style');
                style.id = 'dtslib-notice-styles';
                style.textContent = `
                    @keyframes dtslibSlideDown {
                        from { transform: translateY(-100%); opacity: 0; }
                        to { transform: translateY(0); opacity: 1; }
                    }
                    @keyframes dtslibSlideUp {
                        from { transform: translateY(0); opacity: 1; }
                        to { transform: translateY(-100%); opacity: 0; }
                    }
                `;
                document.head.appendChild(style);
            },

            _adjustPadding() {
                const notices = document.querySelectorAll('.dtslib-notice');
                document.body.style.paddingTop = (notices.length * 52) + 'px';
            }
        };

        // ─────────────────────────────────────────────────────────
        // Heartbeat System (Status Reporting)
        // ─────────────────────────────────────────────────────────

        _startHeartbeat() {
            const report = () => {
                const status = {
                    branch: this.branch,
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    screen: `${screen.width}x${screen.height}`,
                    online: navigator.onLine,
                    performance: this._getPerformanceMetrics()
                };

                // Store in localStorage for dashboard to read
                localStorage.setItem('dtslib_heartbeat', JSON.stringify(status));
                this._emit('heartbeat', status);
            };

            report();
            this.heartbeatInterval = setInterval(report, 30000); // Every 30s
        }

        _getPerformanceMetrics() {
            if (!performance || !performance.timing) return null;
            const t = performance.timing;
            return {
                loadTime: t.loadEventEnd - t.navigationStart,
                domReady: t.domContentLoadedEventEnd - t.navigationStart,
                firstByte: t.responseStart - t.navigationStart
            };
        }

        // ─────────────────────────────────────────────────────────
        // Analytics System
        // ─────────────────────────────────────────────────────────

        analytics = {
            _parent: this,
            sessionId: null,
            events: [],

            init() {
                this.sessionId = this._generateId();
                this._trackPageView();
                this._setupListeners();
            },

            _generateId() {
                return 'sess_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
            },

            _trackPageView() {
                this.track('page_view', {
                    path: window.location.pathname,
                    referrer: document.referrer,
                    title: document.title
                });
            },

            _setupListeners() {
                // Track clicks on external links
                document.addEventListener('click', (e) => {
                    const link = e.target.closest('a');
                    if (link && link.hostname !== window.location.hostname) {
                        this.track('external_link', { url: link.href });
                    }
                });

                // Track scroll depth
                let maxScroll = 0;
                window.addEventListener('scroll', () => {
                    const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
                    if (scrollPercent > maxScroll) {
                        maxScroll = scrollPercent;
                        if ([25, 50, 75, 100].includes(maxScroll)) {
                            this.track('scroll_depth', { depth: maxScroll });
                        }
                    }
                }, { passive: true });
            },

            track(event, data = {}) {
                const entry = {
                    event,
                    data,
                    timestamp: new Date().toISOString(),
                    sessionId: this.sessionId,
                    branch: this._parent.branch
                };
                this.events.push(entry);
                this._persist();
            },

            _persist() {
                const key = `dtslib_analytics_${this._parent.branch}`;
                const existing = JSON.parse(localStorage.getItem(key) || '[]');
                existing.push(...this.events.splice(0));
                // Keep only last 100 events
                const trimmed = existing.slice(-100);
                localStorage.setItem(key, JSON.stringify(trimmed));
            },

            getEvents() {
                const key = `dtslib_analytics_${this._parent.branch}`;
                return JSON.parse(localStorage.getItem(key) || '[]');
            }
        };

        // ─────────────────────────────────────────────────────────
        // HQ Branding
        // ─────────────────────────────────────────────────────────

        _injectBranding() {
            // Add subtle HQ badge
            const badge = document.createElement('div');
            badge.id = 'dtslib-hq-badge';
            badge.innerHTML = `
                <a href="${HQ_BASE}" target="_blank" style="
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: linear-gradient(135deg, #1a1a2e, #16213e);
                    border: 1px solid rgba(212,175,55,0.3);
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                    font-size: 11px;
                    color: #D4AF37;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    z-index: 9999;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    transition: all 0.3s ease;
                    opacity: 0.7;
                " onmouseover="this.style.opacity='1';this.style.transform='translateY(-2px)'"
                   onmouseout="this.style.opacity='0.7';this.style.transform='translateY(0)'">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                    </svg>
                    DTSLIB HQ
                </a>
            `;
            document.body.appendChild(badge);
        }

        // ─────────────────────────────────────────────────────────
        // Event System
        // ─────────────────────────────────────────────────────────

        on(event, callback) {
            if (!this.listeners[event]) this.listeners[event] = [];
            this.listeners[event].push(callback);
            return this;
        }

        off(event, callback) {
            if (!this.listeners[event]) return;
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
            return this;
        }

        _emit(event, data) {
            if (!this.listeners[event]) return;
            this.listeners[event].forEach(cb => cb(data));
        }

        // ─────────────────────────────────────────────────────────
        // Utilities
        // ─────────────────────────────────────────────────────────

        async _fetchJSON(url) {
            try {
                const cached = this.cache.get(url);
                if (cached && Date.now() - cached.time < 60000) {
                    return cached.data;
                }

                const response = await fetch(url + '?t=' + Date.now());
                if (!response.ok) throw new Error('Fetch failed');
                const data = await response.json();

                this.cache.set(url, { data, time: Date.now() });
                return data;
            } catch (e) {
                console.warn('[DTSLIB Bridge] Fetch failed:', url);
                return null;
            }
        }

        // ─────────────────────────────────────────────────────────
        // Public API
        // ─────────────────────────────────────────────────────────

        getBranchInfo() {
            return this.branchConfig;
        }

        getHQConfig() {
            return this.config;
        }

        isFeatureEnabled(feature) {
            return this.features?.isEnabled(feature) || false;
        }

        async sendToHQ(type, data) {
            // Store message for HQ to retrieve
            const messages = JSON.parse(localStorage.getItem('dtslib_messages') || '[]');
            messages.push({
                type,
                data,
                branch: this.branch,
                timestamp: new Date().toISOString()
            });
            localStorage.setItem('dtslib_messages', JSON.stringify(messages.slice(-50)));
            this._emit('message_sent', { type, data });
        }

        destroy() {
            if (this.heartbeatInterval) {
                clearInterval(this.heartbeatInterval);
            }
            const badge = document.getElementById('dtslib-hq-badge');
            if (badge) badge.remove();
            document.querySelectorAll('.dtslib-notice').forEach(el => el.remove());
            this.initialized = false;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // Feature Flags System
    // ═══════════════════════════════════════════════════════════

    class FeatureFlags {
        constructor(flags = {}) {
            this.flags = flags;
        }

        isEnabled(feature) {
            const flag = this.flags[feature];
            if (!flag) return false;
            if (typeof flag === 'boolean') return flag;
            if (flag.enabled === false) return false;
            if (flag.branches && !flag.branches.includes(window.DTSLIB?.branch)) return false;
            if (flag.percentage) return Math.random() * 100 < flag.percentage;
            return true;
        }

        getAll() {
            return this.flags;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // Auto-Initialize
    // ═══════════════════════════════════════════════════════════

    const bridge = new DTSLibBridge();

    // Auto-init when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => bridge.init());
    } else {
        bridge.init();
    }

    // Expose to global
    global.DTSLIB = bridge;

})(typeof window !== 'undefined' ? window : this);
