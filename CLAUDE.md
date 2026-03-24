# CFPS Lab Notebook

## 프로젝트 개요
Cell-Free Protein Synthesis 실험 기록 및 워크플로우 관리 — Streamlit 기반 랩노트

## 기술 스택
- Python 3.11, Streamlit 1.45
- conda 환경: `multievolve`
- 실행: `conda activate multievolve && streamlit run app.py`

## 주요 구성
- `app.py` — 메인 Streamlit 앱
- `data/` — JSON 형태로 실험 데이터 저장 (git 제외)

## 탭 구성
1. 대시보드 — 실험 현황 요약
2. DNA 준비 (PCR) — PCR 기록 + Mixture 계산기
3. Cell Extract — 추출물 제조 기록 + 프로토콜
4. CFPS 반응 — 반응 기록 + Cytomim Mixture 계산기
5. 결과 분석 — 수율 그래프 + CSV 다운로드
6. 실험 노트 — 자유 기록

## GitHub
- Remote: https://github.com/oygoet0211-max/cfps-lab-notebook
- 푸시: `git push origin main`
