/**
 * DTSLIB HQ Bridge SDK v3.0.0
 * Franchise OS — Catalog + Subscription Runtime
 *
 * Features:
 *  - Branch detection (all 5 branches + HQ)
 *  - Catalog loading (pub/sub feed system)
 *  - Subscription resolution (branch.json → catalog.json)
 *  - Feed loader (fetch subscribed content)
 *  - Notice system
 *  - Heartbeat + Analytics
 *  - Feature flags
 *  - HQ branding
 *
 * @author DTSLIB HQ
 * @version 3.0.0
 */

(function(global) {
    'use strict';

    const VERSION = '3.0.0';
    const HQ_BASE = 'https://dtslib1979.github.io/dtslib-branch';
    const GITHUB_BASE = 'https://dtslib1979.github.io';
    const HQ_API = HQ_BASE + '/hq/api';
    const HQ_NOTICES = HQ_BASE + '/hq/notices';
    const HQ_CATALOG = HQ_BASE + '/hq/catalog.json';

    const KNOWN_BRANCHES = ['koosy', 'gohsy', 'artrew', 'papafly', 'lotus', 'tango-magenta'];

    // ═══════════════════════════════════════════════════════════
    // CORE: Bridge Engine
    // ═══════════════════════════════════════════════════════════

    class DTSLibBridge {
        constructor() {
            this.version = VERSION;
            this.branch = null;
            this.branchConfig = null;
            this.catalog = null;
            this.feeds = new Map();
            this.config = null;
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

            console.log(`%c[DTSLIB Bridge] v${VERSION} initializing...`, 'color: #D4AF37; font-weight: bold;');

            // Detect current branch
            this.branch = options.branch || this._detectBranch();

            // Load branch.json (local to this repo)
            this.branchConfig = await this._loadBranchJson();

            // Load HQ catalog
            this.catalog = await this._fetchJSON(HQ_CATALOG);

            // Load subscribed feeds
            if (this.branchConfig?.subscriptions) {
                await this._loadSubscriptions();
            }

            // Initialize subsystems
            await this._initSubsystems(options);

            this.initialized = true;
            this._emit('ready', {
                branch: this.branch,
                config: this.branchConfig,
                catalog: this.catalog,
                feeds: Object.fromEntries(this.feeds)
            });

            console.log(`%c[DTSLIB Bridge] Connected: ${this.branch.toUpperCase()} | ${this.feeds.size} feeds loaded`, 'color: #10B981; font-weight: bold;');

            return this;
        }

        async _initSubsystems(options) {
            // Notice System
            if (options.notices !== false) {
                await this.notices.load();
            }

            // Heartbeat
            if (options.heartbeat !== false) {
                this._startHeartbeat();
            }

            // Feature Flags
            this.features = new FeatureFlags(this.config?.features || {});

            // Analytics
            if (options.analytics !== false) {
                this.analytics.init();
            }

            // HQ Branding
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
            for (const b of KNOWN_BRANCHES) {
                if (hostname.includes(b)) return b;
            }
            if (hostname.includes('dtslib')) return 'hq';

            // GitHub Pages pattern: username.github.io/reponame/
            const match = pathname.match(/\/([^\/]+)/);
            if (match) {
                const repo = match[1].toLowerCase();
                if (KNOWN_BRANCHES.includes(repo)) return repo;
                if (repo === 'dtslib-branch') return 'hq';
            }

            return 'unknown';
        }

        // ─────────────────────────────────────────────────────────
        // Branch.json Loader
        // ─────────────────────────────────────────────────────────

        async _loadBranchJson() {
            // Try loading branch.json from current repo root
            const paths = [
                './branch.json',
                '../branch.json',
                '/branch.json'
            ];

            for (const path of paths) {
                try {
                    const resp = await fetch(path + '?t=' + Date.now());
                    if (resp.ok) {
                        const data = await resp.json();
                        console.log(`%c[DTSLIB Bridge] branch.json loaded: ${data.name}`, 'color: #6366F1;');
                        return data;
                    }
                } catch (e) { /* try next */ }
            }

            // If on GitHub Pages, try absolute path
            if (this.branch !== 'unknown' && this.branch !== 'hq') {
                try {
                    const url = `${GITHUB_BASE}/${this.branch}/branch.json`;
                    const resp = await fetch(url + '?t=' + Date.now());
                    if (resp.ok) return await resp.json();
                } catch (e) { /* fallback */ }
            }

            console.warn('[DTSLIB Bridge] branch.json not found');
            return null;
        }

        // ─────────────────────────────────────────────────────────
        // Subscription & Feed System
        // ─────────────────────────────────────────────────────────

        async _loadSubscriptions() {
            const subs = this.branchConfig.subscriptions;
            if (!subs || !this.catalog) return;

            const loadPromises = subs.map(sub => this._loadFeed(sub));
            await Promise.allSettled(loadPromises);
        }

        async _loadFeed(subscription) {
            const { feedId, publisher } = subscription;

            // Find feed in catalog
            const pub = this.catalog.publishers?.find(p => p.id === publisher);
            if (!pub) {
                console.warn(`[DTSLIB Bridge] Publisher not found: ${publisher}`);
                return;
            }

            const feed = pub.feeds?.find(f => f.id === feedId);
            if (!feed) {
                console.warn(`[DTSLIB Bridge] Feed not found: ${feedId}`);
                return;
            }

            // Resolve feed URL
            const url = GITHUB_BASE + feed.path;

            try {
                const data = await this._fetchJSON(url);
                if (data) {
                    this.feeds.set(feedId, {
                        ...feed,
                        publisher: pub.id,
                        publisherName: pub.name,
                        data: data
                    });
                }
            } catch (e) {
                console.warn(`[DTSLIB Bridge] Feed load failed: ${feedId}`);
            }
        }

        // Public: Get feed data
        getFeed(feedId) {
            return this.feeds.get(feedId) || null;
        }

        // Public: Get all loaded feeds
        getAllFeeds() {
            return Object.fromEntries(this.feeds);
        }

        // Public: Check if subscribed to a feed
        isSubscribed(feedId) {
            return this.feeds.has(feedId);
        }

        // ─────────────────────────────────────────────────────────
        // Notice System
        // ─────────────────────────────────────────────────────────

        notices = {
            _bridge: null,
            data: [],
            dismissed: [],

            async load() {
                try {
                    const response = await fetch(HQ_NOTICES + '/notices.json?t=' + Date.now());
                    if (!response.ok) return;
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
                this._adjustPadding();
            },

            _render() {
                const branch = global.DTSLIB?.branch || 'unknown';
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
                    info: { bg: 'linear-gradient(135deg, #3B82F6, #1D4ED8)', icon: 'i' },
                    warning: { bg: 'linear-gradient(135deg, #F59E0B, #D97706)', icon: '!' },
                    success: { bg: 'linear-gradient(135deg, #10B981, #059669)', icon: '+' },
                    urgent: { bg: 'linear-gradient(135deg, #EF4444, #DC2626)', icon: '!!' }
                };
                const style = styles[notice.type] || styles.info;

                const banner = document.createElement('div');
                banner.id = 'dtslib-notice-' + notice.id;
                banner.className = 'dtslib-notice';
                banner.style.cssText = `
                    position: fixed;
                    top: ${index * 52}px;
                    left: 0; right: 0;
                    background: ${style.bg};
                    color: white;
                    padding: 14px 20px;
                    z-index: 10000;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    font-size: 14px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                    animation: dtslibSlideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                `;

                banner.innerHTML = `
                    <div style="display:flex;align-items:center;gap:12px;flex:1;">
                        <span style="font-size:16px;font-weight:bold;background:rgba(255,255,255,0.2);width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;">${style.icon}</span>
                        <div>
                            <strong style="margin-right:10px;">${notice.title}</strong>
                            <span style="opacity:0.9;">${notice.content}</span>
                        </div>
                    </div>
                    <button onclick="DTSLIB.notices.dismiss('${notice.id}')" style="
                        background: rgba(255,255,255,0.2);
                        border: none; color: white;
                        width: 28px; height: 28px;
                        border-radius: 50%; cursor: pointer;
                        font-size: 14px;
                    ">x</button>
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
        // Heartbeat
        // ─────────────────────────────────────────────────────────

        _startHeartbeat() {
            const report = () => {
                const status = {
                    branch: this.branch,
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    online: navigator.onLine,
                    feeds: this.feeds.size,
                    subscriptions: this.branchConfig?.subscriptions?.length || 0
                };
                localStorage.setItem('dtslib_heartbeat', JSON.stringify(status));
                this._emit('heartbeat', status);
            };

            report();
            this.heartbeatInterval = setInterval(report, 30000);
        }

        // ─────────────────────────────────────────────────────────
        // Analytics
        // ─────────────────────────────────────────────────────────

        analytics = {
            _bridge: null,
            sessionId: null,
            events: [],

            init() {
                this.sessionId = 'sess_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
                this.track('page_view', {
                    path: window.location.pathname,
                    referrer: document.referrer,
                    title: document.title
                });
            },

            track(event, data = {}) {
                const entry = {
                    event, data,
                    timestamp: new Date().toISOString(),
                    sessionId: this.sessionId,
                    branch: global.DTSLIB?.branch
                };
                this.events.push(entry);
                this._persist();
            },

            _persist() {
                const key = `dtslib_analytics_${global.DTSLIB?.branch || 'unknown'}`;
                const existing = JSON.parse(localStorage.getItem(key) || '[]');
                existing.push(...this.events.splice(0));
                localStorage.setItem(key, JSON.stringify(existing.slice(-100)));
            },

            getEvents() {
                const key = `dtslib_analytics_${global.DTSLIB?.branch || 'unknown'}`;
                return JSON.parse(localStorage.getItem(key) || '[]');
            }
        };

        // ─────────────────────────────────────────────────────────
        // HQ Branding
        // ─────────────────────────────────────────────────────────

        _injectBranding() {
            const badge = document.createElement('div');
            badge.id = 'dtslib-hq-badge';
            badge.innerHTML = `
                <a href="${HQ_BASE}" target="_blank" style="
                    position: fixed;
                    bottom: 16px; right: 16px;
                    background: rgba(15,15,25,0.9);
                    border: 1px solid rgba(212,175,55,0.3);
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-family: -apple-system, sans-serif;
                    font-size: 11px;
                    color: #D4AF37;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    z-index: 9999;
                    opacity: 0.6;
                    transition: opacity 0.3s;
                " onmouseover="this.style.opacity='1'"
                   onmouseout="this.style.opacity='0.6'">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
                if (cached && Date.now() - cached.time < 300000) {
                    return cached.data;
                }
                const response = await fetch(url + (url.includes('?') ? '&' : '?') + 't=' + Date.now());
                if (!response.ok) return null;
                const data = await response.json();
                this.cache.set(url, { data, time: Date.now() });
                return data;
            } catch (e) {
                return null;
            }
        }

        // ─────────────────────────────────────────────────────────
        // Public API
        // ─────────────────────────────────────────────────────────

        getBranchInfo() { return this.branchConfig; }
        getCatalog() { return this.catalog; }
        getVersion() { return VERSION; }

        isFeatureEnabled(feature) {
            return this.features?.isEnabled(feature) || false;
        }

        async sendToHQ(type, data) {
            const messages = JSON.parse(localStorage.getItem('dtslib_messages') || '[]');
            messages.push({
                type, data,
                branch: this.branch,
                timestamp: new Date().toISOString()
            });
            localStorage.setItem('dtslib_messages', JSON.stringify(messages.slice(-50)));
            this._emit('message_sent', { type, data });
        }

        destroy() {
            if (this.heartbeatInterval) clearInterval(this.heartbeatInterval);
            const badge = document.getElementById('dtslib-hq-badge');
            if (badge) badge.remove();
            document.querySelectorAll('.dtslib-notice').forEach(el => el.remove());
            this.initialized = false;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // Feature Flags
    // ═══════════════════════════════════════════════════════════

    class FeatureFlags {
        constructor(flags = {}) { this.flags = flags; }

        isEnabled(feature) {
            const flag = this.flags[feature];
            if (!flag) return false;
            if (typeof flag === 'boolean') return flag;
            if (flag.enabled === false) return false;
            if (flag.branches && !flag.branches.includes(global.DTSLIB?.branch)) return false;
            if (flag.percentage) return Math.random() * 100 < flag.percentage;
            return true;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // Auto-Initialize
    // ═══════════════════════════════════════════════════════════

    const bridge = new DTSLibBridge();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => bridge.init());
    } else {
        bridge.init();
    }

    global.DTSLIB = bridge;

})(typeof window !== 'undefined' ? window : this);
