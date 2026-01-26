# Chalkboard Pack — {BRANCH_NAME}

## 촬영 루틴 10줄

1. **칠판 열기** — `index.html` 실행
2. **오늘 주제 확인** — Topic 섹션 읽기
3. **카드 훑기** — 3~6개 카드 클릭해서 자료 확인
4. **REC 누르기** — 칠판 상단으로 스크롤
5. **촬영 시작** — 화면 녹화 또는 카메라 ON
6. **칠판 보며 말하기** — 카드 순서대로 설명
7. **촬영 종료** — 녹화 정지
8. **Quick Access → Archive** — 결과물 저장
9. **Quick Access → Engine** — 발행 플랫폼 이동
10. **내일 board.json 업데이트** — HQ Brief 반영

---

## 파일 구성

| 파일 | 용도 |
|------|------|
| `index.html` | 칠판 UI |
| `board.json` | 오늘 카드/주제 데이터 |
| `README.md` | 이 문서 |

---

## 업데이트 방법

HQ에서 새 칠판 팩 배포 시:
```bash
# HQ가 실행
dts release {BRANCH_ID}
```

브랜치에서 수동 pull:
```bash
git pull origin main
```

---

*Chalkboard Pack v1*
*Branch: {BRANCH_NAME}*
