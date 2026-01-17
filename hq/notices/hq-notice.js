/**
 * HQ Notice Display Component
 * 본사(dtslib-branch)에서 배포된 공지를 표시하는 컴포넌트
 */
(function() {
    'use strict';

    const HQ_NOTICE_URL = 'https://dtslib1979.github.io/dtslib-branch/hq/notices/notices.json';
    const STORAGE_KEY = 'hq_dismissed_notices';

    // 현재 브랜치 자동 감지
    function detectBranch() {
        const hostname = window.location.hostname;
        const pathname = window.location.pathname;

        if (hostname.includes('koosy') || pathname.includes('koosy')) return 'koosy';
        if (hostname.includes('gohsy') || pathname.includes('gohsy')) return 'gohsy';
        if (hostname.includes('papafly') || pathname.includes('papafly')) return 'papafly';

        // GitHub Pages 패턴: dtslib1979.github.io/reponame/
        const match = pathname.match(/\/([^\/]+)\//);
        if (match) return match[1];

        return 'unknown';
    }

    // 닫힌 공지 목록 가져오기
    function getDismissedNotices() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
        } catch {
            return [];
        }
    }

    // 공지 닫기 저장
    function dismissNotice(id) {
        const dismissed = getDismissedNotices();
        if (!dismissed.includes(id)) {
            dismissed.push(id);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(dismissed));
        }
    }

    // 공지 타입별 스타일
    function getNoticeStyle(type) {
        const styles = {
            info: { bg: '#3B82F6', icon: 'ℹ️' },
            warning: { bg: '#F59E0B', icon: '⚠️' },
            success: { bg: '#10B981', icon: '✅' },
            urgent: { bg: '#EF4444', icon: '🚨' }
        };
        return styles[type] || styles.info;
    }

    // 공지 배너 생성
    function createNoticeBanner(notice) {
        const style = getNoticeStyle(notice.type);

        const banner = document.createElement('div');
        banner.id = 'hq-notice-' + notice.id;
        banner.className = 'hq-notice-banner';
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: ${style.bg};
            color: white;
            padding: 12px 20px;
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            animation: slideDown 0.3s ease-out;
        `;

        const content = document.createElement('div');
        content.style.cssText = 'display: flex; align-items: center; gap: 10px; flex: 1;';
        content.innerHTML = `
            <span style="font-size: 18px;">${style.icon}</span>
            <div>
                <strong style="margin-right: 8px;">${notice.title}</strong>
                <span style="opacity: 0.9;">${notice.content}</span>
            </div>
        `;

        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '✕';
        closeBtn.style.cssText = `
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        `;
        closeBtn.onmouseover = () => closeBtn.style.background = 'rgba(255,255,255,0.3)';
        closeBtn.onmouseout = () => closeBtn.style.background = 'rgba(255,255,255,0.2)';
        closeBtn.onclick = () => {
            dismissNotice(notice.id);
            banner.style.animation = 'slideUp 0.3s ease-out forwards';
            setTimeout(() => banner.remove(), 300);
            adjustBodyPadding();
        };

        banner.appendChild(content);
        banner.appendChild(closeBtn);

        return banner;
    }

    // body 패딩 조정 (배너 높이만큼)
    function adjustBodyPadding() {
        const banners = document.querySelectorAll('.hq-notice-banner');
        let totalHeight = 0;
        banners.forEach(b => totalHeight += b.offsetHeight);
        document.body.style.paddingTop = totalHeight + 'px';
    }

    // 스타일 주입
    function injectStyles() {
        if (document.getElementById('hq-notice-styles')) return;

        const style = document.createElement('style');
        style.id = 'hq-notice-styles';
        style.textContent = `
            @keyframes slideDown {
                from { transform: translateY(-100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes slideUp {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(-100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }

    // 공지 로드 및 표시
    async function loadAndDisplayNotices() {
        const branch = detectBranch();
        const dismissed = getDismissedNotices();

        try {
            const response = await fetch(HQ_NOTICE_URL + '?t=' + Date.now());
            if (!response.ok) return;

            const data = await response.json();
            const notices = data.notices || [];

            // 현재 브랜치에 해당하고, 닫지 않은 공지만 필터
            const activeNotices = notices.filter(n =>
                n.branches.includes(branch) &&
                !dismissed.includes(n.id) &&
                new Date(n.expiresAt) > new Date()
            );

            if (activeNotices.length === 0) return;

            injectStyles();

            // 최신 공지 1개만 표시 (여러 개면 스택)
            activeNotices.slice(0, 3).forEach((notice, index) => {
                const banner = createNoticeBanner(notice);
                banner.style.top = (index * 50) + 'px';
                document.body.insertBefore(banner, document.body.firstChild);
            });

            adjustBodyPadding();

        } catch (err) {
            console.log('[HQ Notice] Failed to load notices:', err.message);
        }
    }

    // 페이지 로드 시 실행
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadAndDisplayNotices);
    } else {
        loadAndDisplayNotices();
    }

    // 전역 API 노출 (옵션)
    window.HQNotice = {
        refresh: loadAndDisplayNotices,
        dismiss: dismissNotice,
        clearDismissed: () => localStorage.removeItem(STORAGE_KEY)
    };
})();
