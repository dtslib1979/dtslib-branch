# Digital Business Card Implementation Guide

> buddies.kr/card/ 명함 로직을 기반으로 한 구현 가이드

## Overview

프리미엄 디지털 명함 페이지 구현을 위한 완전한 가이드입니다.

**특징**:
- Dark + Gold 프리미엄 테마
- vCard 연락처 저장 기능
- QR 코드 토글
- 클립보드 복사 + 햅틱 피드백
- 반응형 디자인
- CSS 애니메이션 효과

---

## 1. 디렉토리 구조

```
/card/
  └── index.html      # 메인 명함 페이지
/assets/
  └── icons/
      └── logo.png    # 로고 이미지 (72x72 이상)
  └── og/
      └── card-preview.png  # OG 이미지 (1200x630)
```

---

## 2. CSS 변수 시스템

```css
:root {
  /* 배경 */
  --bg: #0A0A0A;
  --card-bg: linear-gradient(145deg, #1a1a1a 0%, #0d0d0d 100%);
  
  /* 골드 컬러 팔레트 */
  --gold: #D4AF37;
  --gold-light: #E8C547;
  --gold-dark: #B8962E;
  --gold-shine: linear-gradient(135deg, #D4AF37 0%, #F4E4A6 25%, #D4AF37 50%, #B8962E 75%, #D4AF37 100%);
  
  /* 텍스트 */
  --text: #F5F5F0;
  --text-muted: rgba(245,245,240,.5);
  
  /* 보더 */
  --border-gold: rgba(212,175,55,.4);
}
```

### 커스터마이징 예시

| 테마 | --bg | --gold | 용도 |
|------|------|--------|------|
| Gold (기본) | #0A0A0A | #D4AF37 | 프리미엄/럭셔리 |
| Silver | #0A0A0A | #C0C0C0 | 테크/모던 |
| Rose Gold | #0A0A0A | #B76E79 | 패션/뷰티 |
| Emerald | #0A0A0A | #50C878 | 친환경/헬스 |

---

## 3. 핵심 애니메이션

### 3.1 카드 진입 애니메이션
```css
@keyframes cardEntry {
  0% { opacity: 0; transform: translateY(30px) scale(0.95); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

.card-wrapper {
  animation: cardEntry 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
```

### 3.2 골드 시머 효과
```css
@keyframes shimmer {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: -200% 0; }
}

.brand-name {
  background: var(--gold-shine);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 3s ease-in-out infinite;
}
```

### 3.3 로고 펄스 효과
```css
@keyframes logoPulse {
  0%, 100% { box-shadow: 0 4px 20px rgba(212,175,55,.25); }
  50% { box-shadow: 0 4px 30px rgba(212,175,55,.45), 0 0 40px rgba(212,175,55,.2); }
}

.logo {
  animation: logoPulse 3s ease-in-out infinite;
}
```

---

## 4. HTML 구조

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0A0A0A">

  <!-- SEO & OG Tags -->
  <title>YOUR BRAND</title>
  <meta name="description" content="Your tagline here">
  <meta property="og:title" content="YOUR BRAND">
  <meta property="og:description" content="Your tagline">
  <meta property="og:image" content="https://yourdomain.com/assets/og/card-preview.png">
  <meta property="og:url" content="https://yourdomain.com/card/">
  
  <link rel="icon" href="../assets/icons/logo.png">
</head>
<body>
  <div class="card-wrapper">
    <article class="business-card" id="card">
      
      <!-- 로고 섹션 -->
      <section class="logo-section">
        <div class="logo">
          <img src="../assets/icons/logo.png" alt="BRAND" loading="eager">
        </div>
        <h1 class="brand-name">Your Brand Name</h1>
        <p class="tagline">Your Tagline</p>
      </section>

      <div class="divider"></div>

      <!-- 인용구/슬로건 -->
      <section class="quote-section">
        <p class="quote">"Your <span>powerful</span> message here."</p>
      </section>

      <div class="divider"></div>

      <!-- 연락처 -->
      <section class="contact-section">
        <p class="contact-item">
          <a href="https://yourdomain.com"><span class="contact-icon">🌐</span>yourdomain.com</a>
        </p>
        <p class="contact-item">
          <a href="mailto:hello@yourdomain.com"><span class="contact-icon">✉️</span>hello@yourdomain.com</a>
        </p>
      </section>

      <!-- 액션 버튼 -->
      <section class="action-section">
        <button class="action-btn" onclick="saveContact()">
          <span class="action-icon">📇</span>Save Contact
        </button>
        <a href="mailto:hello@yourdomain.com?subject=Inquiry" class="action-btn primary">
          <span class="action-icon">✉️</span>Contact
        </a>
      </section>

      <!-- QR 코드 -->
      <section class="qr-section">
        <button class="qr-toggle" onclick="toggleQR()">Show QR Code</button>
        <div class="qr-container" id="qrContainer">
          <div class="qr-code">
            <!-- QR SVG or Image -->
          </div>
          <p class="qr-hint">Scan to open this card</p>
        </div>
      </section>
      
    </article>
    <p class="footer-note">Tap card to copy link</p>
  </div>

  <div class="toast" id="toast">Link copied</div>
</body>
</html>
```

---

## 5. JavaScript 기능

### 5.1 vCard 저장 기능

```javascript
function saveContact() {
  const vCard = `BEGIN:VCARD
VERSION:3.0
FN:YOUR NAME
ORG:YOUR ORGANIZATION
TITLE:Your Title
EMAIL;TYPE=WORK:hello@yourdomain.com
URL:https://yourdomain.com
NOTE:Your note here
END:VCARD`;

  const blob = new Blob([vCard], { type: 'text/vcard;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'YOUR_NAME.vcf';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);

  showToast('Contact saved');
  if (navigator.vibrate) navigator.vibrate(50);
}
```

### 5.2 클립보드 복사 + 햅틱

```javascript
const card = document.getElementById('card');

card.addEventListener('click', (e) => {
  // 버튼/링크 클릭 시 무시
  if (e.target.closest('button') || e.target.closest('a')) return;

  navigator.clipboard.writeText('https://yourdomain.com/card/').then(() => {
    showToast('Link copied');
    if (navigator.vibrate) navigator.vibrate(50);
  });
});
```

### 5.3 Toast 알림

```javascript
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2000);
}
```

### 5.4 QR 토글

```javascript
function toggleQR() {
  const container = document.getElementById('qrContainer');
  const toggle = document.querySelector('.qr-toggle');

  container.classList.toggle('show');
  toggle.textContent = container.classList.contains('show') 
    ? 'Hide QR Code' 
    : 'Show QR Code';
}
```

---

## 6. vCard 필드 레퍼런스

```
BEGIN:VCARD
VERSION:3.0
FN:Full Name                          # 필수: 표시 이름
N:Last;First;Middle;Prefix;Suffix     # 이름 구조
ORG:Organization Name                 # 조직명
TITLE:Job Title                       # 직함
TEL;TYPE=WORK:+82-10-1234-5678       # 전화번호
TEL;TYPE=CELL:+82-10-1234-5678       # 휴대폰
EMAIL;TYPE=WORK:email@domain.com     # 이메일
URL:https://domain.com                # 웹사이트
ADR;TYPE=WORK:;;Street;City;State;Zip;Country  # 주소
NOTE:Additional notes                 # 메모
PHOTO;VALUE=URI:https://...          # 프로필 사진 URL
END:VCARD
```

---

## 7. QR 코드 생성

### 옵션 A: 외부 서비스 사용
```html
<img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://yourdomain.com/card/" alt="QR">
```

### 옵션 B: JavaScript 라이브러리
```html
<script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>
<script>
  QRCode.toCanvas(document.getElementById('qr-canvas'), 'https://yourdomain.com/card/', {
    width: 120,
    margin: 1,
    color: { dark: '#000', light: '#fff' }
  });
</script>
```

### 옵션 C: SVG 직접 삽입 (buddies.kr 방식)
- 오프라인 지원
- 로딩 속도 최적화
- SVG QR 생성기 사용: https://www.qrcode-monkey.com/

---

## 8. 체크리스트

### 구현 전
- [ ] 로고 이미지 준비 (72x72px 이상, PNG/SVG)
- [ ] OG 프리뷰 이미지 준비 (1200x630px)
- [ ] 브랜드명, 태그라인, 인용구 확정
- [ ] 연락처 정보 (이메일, 웹사이트, 전화번호)
- [ ] 컬러 테마 결정

### 구현 후
- [ ] 모바일 반응형 테스트
- [ ] vCard 저장 테스트 (iOS/Android)
- [ ] 클립보드 복사 테스트
- [ ] QR 코드 스캔 테스트
- [ ] OG 태그 프리뷰 확인 (카카오톡, 슬랙 등)
- [ ] Lighthouse 성능 테스트

---

## 9. 전체 코드 템플릿

`card/index.html` 전체 코드는 아래 참조:

**Source**: https://github.com/dtslib1979/buddies.kr/blob/main/card/index.html

---

## 10. 배포

```bash
# GitHub Pages 사용 시
git add card/
git commit -m "Add digital business card"
git push origin main
```

**Live URL**: `https://yourdomain.com/card/`

---

## License

MIT License - 자유롭게 수정 및 사용 가능
