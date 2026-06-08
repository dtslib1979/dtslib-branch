# 박찬대 되기 프로젝트 — 작업 로그 & TODO

> 본문: `박찬대-되기-프로젝트.html` (Section 01~08+)
> 철학 연결맵: `OrbitPrompt/boards/chan-dae-project.md`

---

## 현재 상태 (2026-06-08)

- **완료**: Section 01~08 (AI시대 정치인-시민 관계 모델까지)
- **마지막 커밋**: `7ec61ca` — Section 08 추가
- **다음 섹션**: Section 09 이후 미작성

---

## TODO

- [ ] Section 09+ 작업 재개 (컨텍스트 터짐으로 중단)
- [ ] **Φ12 → 정치 시뮬레이션 MCP 포팅** — `football-model/mcp/` 구조를 박찬대 정치 분석에 적용
- [ ] SD카드 로컬 서버에 박찬대 MCP 인스턴스 추가
- [ ] Election MCP 연동 (`OrbitPrompt/prompts/election/`)

---

## 세션 로그

### 2026-06-08 — phone_aider(DeepSeek) + Claude(Sonnet) 병렬 세션

**박씨 확정 방향**
- MCP = 엔드 프로덕트 (출판 아님 — GitHub 공개 레포 배포)
- SD카드(E:/mcp/) 로컬 서버 운영 → YouTube 반응 좋은 것만 Railway 백업
- GitHub 공개 레포 = 구독자 각자 로컬 설치

**이 세션에서 완료한 것**
1. Section 08 "AI 시대 정치인-시민 관계" 완성 및 커밋 (`7ec61ca`)
   - 핵심 명제: "AI 시대에 시민은 하나의 개인 연구소가 되고, 정치인은 그 연구 결과를 도시와 제도 위에 꽂아볼 수 있는 아바타이자 파트너가 된다."
2. WC2026 축구 예측 MCP 완성 (Φ-I-C-K-P-7AXIS 12차원 모델)
   - 동일한 7드라이버 구조 → 정치 시뮬레이션 MCP 포팅 가능
3. OrbitPrompt 구조 정리 (레포 분리: 철학=OrbitPrompt / 사례=dtslib-branch)

**Φ12 → 정치 MCP 포팅 근거**
- 축구: 48팀 × 7드라이버 × 10,000 MC = WC2026 예측
- 정치: N명 정치인 × 7드라이버 × 시뮬레이션 = 여론/정책 분석
- 구조 동일, 데이터 소스만 교체 (경기결과 → 발언/법안/지지율)
