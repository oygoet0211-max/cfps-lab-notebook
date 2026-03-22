"""
CFPS Lab Notebook
Cell-Free Protein Synthesis 실험 기록 및 워크플로우 관리
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
from pathlib import Path

# ── 페이지 설정 ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CFPS Lab Notebook",
    page_icon="🧪",
    layout="wide"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# ── CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
* { font-family: Arial, Helvetica, sans-serif !important; }

/* Header */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.block-container { padding-top: 0 !important; max-width: 1300px; }

.cfps-header {
    background: linear-gradient(135deg, #0d2137 0%, #0a3055 60%, #0d4a6e 100%);
    border-bottom: 2px solid #00a8cc;
    padding: 1.2rem 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.cfps-title { font-size: 1.6rem; font-weight: 700; color: #fff; margin: 0; }
.cfps-sub { font-size: 0.78rem; color: #7ecfda; letter-spacing: .08em;
            text-transform: uppercase; margin-top: 3px; }
.cfps-badge {
    margin-left: auto;
    background: rgba(0,168,204,.15);
    border: 1px solid rgba(0,168,204,.4);
    border-radius: 20px;
    padding: .25rem .9rem;
    font-size: .72rem; color: #00c4cc; font-weight: 700;
    letter-spacing: .05em;
}

/* Cards */
.step-card {
    background: #f8fbfe;
    border: 1px solid #d0e4f0;
    border-left: 4px solid #00a8cc;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.step-card h4 { color: #0d2137; margin: 0 0 .4rem 0; font-size: 0.95rem; }
.step-card p  { color: #4a6a82; margin: 0; font-size: 0.82rem; }

.metric-card {
    background: linear-gradient(135deg, #f0f7ff, #e8f4fd);
    border: 1px solid #c0ddf0;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #0d4a6e; }
.metric-lbl { font-size: 0.75rem; color: #4a6a82; text-transform: uppercase;
              letter-spacing: .06em; }

/* Tabs */
[data-testid="stTabs"] button {
    font-family: Arial, sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

/* Tables */
.dataframe { font-size: 0.82rem !important; }

/* Status badges */
.status-ok   { background:#d4f5e0; color:#1a6e3a; padding:2px 8px;
               border-radius:10px; font-size:.75rem; font-weight:600; }
.status-warn { background:#fff3cd; color:#856404; padding:2px 8px;
               border-radius:10px; font-size:.75rem; font-weight:600; }
.status-fail { background:#fde8e8; color:#9b1c1c; padding:2px 8px;
               border-radius:10px; font-size:.75rem; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cfps-header">
  <div>🧪</div>
  <div>
    <div class="cfps-title">CFPS Lab Notebook</div>
    <div class="cfps-sub">Cell-Free Protein Synthesis Workflow</div>
  </div>
  <div class="cfps-badge">DNA · Extract · Reaction · Results</div>
</div>
""", unsafe_allow_html=True)

# ── 데이터 로드/저장 유틸 ──────────────────────────────────────────────────
def load_data(filename):
    path = DATA_DIR / filename
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── 탭 ───────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📋 대시보드",
    "🧬 DNA 준비 (PCR)",
    "🔬 Cell Extract",
    "⚗️ CFPS 반응",
    "📊 결과 분석",
    "📓 실험 노트"
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1: 대시보드
# ════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.subheader("실험 현황 대시보드")

    pcr_data     = load_data("pcr.json")
    extract_data = load_data("extract.json")
    cfps_data    = load_data("cfps.json")
    note_data    = load_data("notes.json")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{len(pcr_data)}</div>
            <div class="metric-lbl">PCR 실험</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{len(extract_data)}</div>
            <div class="metric-lbl">Cell Extract 배치</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{len(cfps_data)}</div>
            <div class="metric-lbl">CFPS 반응</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{len(note_data)}</div>
            <div class="metric-lbl">노트 기록</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### CFPS 워크플로우")
    cols = st.columns(4)
    steps = [
        ("① DNA 준비", "PCR로 선형 DNA 템플릿 제작\n프라이머 설계 및 증폭 확인"),
        ("② Cell Extract 제조", "세포 파쇄 및 원심분리\n추출물 수율/활성 측정"),
        ("③ CFPS 반응", "Reaction Mixture 준비\n최적 조건에서 단백질 합성"),
        ("④ 결과 분석", "SDS-PAGE / Western Blot\n단백질 수율 정량"),
    ]
    for col, (title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""<div class="step-card">
                <h4>{title}</h4>
                <p>{desc.replace(chr(10), '<br>')}</p>
            </div>""", unsafe_allow_html=True)

    # 최근 실험
    st.markdown("### 최근 기록")
    all_recent = []
    for item in pcr_data[-3:]:
        all_recent.append({"날짜": item.get("date",""), "구분": "PCR",
                           "실험명": item.get("name",""), "결과": item.get("result","")})
    for item in cfps_data[-3:]:
        all_recent.append({"날짜": item.get("date",""), "구분": "CFPS",
                           "실험명": item.get("name",""), "결과": item.get("yield_ug_ml","")})
    if all_recent:
        df = pd.DataFrame(all_recent).sort_values("날짜", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("아직 기록된 실험이 없습니다. 각 탭에서 실험을 추가해주세요.")

# ════════════════════════════════════════════════════════════════════════
# TAB 2: DNA 준비 (PCR)
# ════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.subheader("🧬 DNA 준비 — PCR 실험 기록")

    col_form, col_list = st.columns([1, 1.4])

    with col_form:
        with st.form("pcr_form", clear_on_submit=True):
            st.markdown("**새 PCR 실험 추가**")
            pcr_name    = st.text_input("실험명", placeholder="예) GFP_linear_v1")
            pcr_date    = st.date_input("날짜", value=date.today())
            template    = st.text_input("템플릿 DNA", placeholder="예) pUC19-GFP")
            fwd_primer  = st.text_input("Forward Primer")
            rev_primer  = st.text_input("Reverse Primer")
            annealing   = st.number_input("Annealing 온도 (°C)", 50.0, 72.0, 60.0, 0.5)
            cycles      = st.number_input("Cycle 수", 20, 40, 30, 1)
            band_size   = st.text_input("예상 밴드 크기 (bp)", placeholder="예) 750")

            c1, c2 = st.columns(2)
            with c1:
                result = st.selectbox("결과", ["성공", "실패", "재확인 필요"])
            with c2:
                conc = st.text_input("DNA 농도 (ng/μL)", placeholder="예) 125.4")

            memo = st.text_area("메모", height=80)

            if st.form_submit_button("💾 저장", use_container_width=True):
                data = load_data("pcr.json")
                data.append({
                    "id": len(data) + 1,
                    "name": pcr_name,
                    "date": str(pcr_date),
                    "template": template,
                    "fwd_primer": fwd_primer,
                    "rev_primer": rev_primer,
                    "annealing_temp": annealing,
                    "cycles": cycles,
                    "band_size_bp": band_size,
                    "result": result,
                    "conc_ng_ul": conc,
                    "memo": memo
                })
                save_data("pcr.json", data)
                st.success("저장됐습니다!")
                st.rerun()

    with col_list:
        st.markdown("**PCR 실험 목록**")
        pcr_data = load_data("pcr.json")
        if pcr_data:
            df = pd.DataFrame(pcr_data)
            display_cols = ["id","date","name","template","band_size_bp","conc_ng_ul","result"]
            display_cols = [c for c in display_cols if c in df.columns]
            df_show = df[display_cols].rename(columns={
                "id":"#","date":"날짜","name":"실험명","template":"템플릿",
                "band_size_bp":"밴드(bp)","conc_ng_ul":"농도(ng/μL)","result":"결과"
            })
            st.dataframe(df_show, use_container_width=True, hide_index=True)

            # PCR Mixture 계산기
            st.markdown("---")
            st.markdown("**PCR Mixture 계산기**")
            n_rxn = st.number_input("반응 수", 1, 50, 1, key="pcr_rxn")
            vol   = st.number_input("최종 볼륨 (μL)", 10, 100, 50, key="pcr_vol")
            mix = {
                "10x Buffer": vol * 0.1,
                "dNTPs (10mM)": vol * 0.02,
                "Forward Primer (10μM)": vol * 0.04,
                "Reverse Primer (10μM)": vol * 0.04,
                "Template DNA": vol * 0.02,
                "Polymerase": vol * 0.02,
                "ddH₂O": round(vol * 0.78, 1),
            }
            df_mix = pd.DataFrame([
                {"성분": k, "1 rxn (μL)": round(v,1), f"{n_rxn} rxn (μL)": round(v*n_rxn,1)}
                for k, v in mix.items()
            ])
            st.dataframe(df_mix, use_container_width=True, hide_index=True)
        else:
            st.info("PCR 실험 기록이 없습니다.")

# ════════════════════════════════════════════════════════════════════════
# TAB 3: Cell Extract
# ════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.subheader("🔬 Cell Extract 제조 기록")

    col_form, col_list = st.columns([1, 1.4])

    with col_form:
        with st.form("extract_form", clear_on_submit=True):
            st.markdown("**새 Extract 배치 추가**")
            ext_name    = st.text_input("배치명", placeholder="예) BL21_extract_batch01")
            ext_date    = st.date_input("날짜", value=date.today())
            strain      = st.text_input("균주", placeholder="예) E. coli BL21(DE3)")
            od_harvest  = st.number_input("수확 OD₆₀₀", 0.1, 20.0, 3.0, 0.1)
            vol_culture = st.number_input("배양 볼륨 (mL)", 10, 5000, 500, 50)
            lysis_method= st.selectbox("Lysis 방법", ["Sonication","French Press","Bead Beating","Freeze-Thaw"])
            spin_speed  = st.text_input("원심분리 조건", placeholder="예) 12,000 × g, 10 min, 4°C")
            protein_conc= st.text_input("단백질 농도 (mg/mL)", placeholder="예) 12.5")
            activity    = st.selectbox("활성 테스트", ["Pass", "Fail", "미실시"])
            storage     = st.text_input("보관 조건", placeholder="예) -80°C, 10μL aliquot")
            memo        = st.text_area("메모", height=80)

            if st.form_submit_button("💾 저장", use_container_width=True):
                data = load_data("extract.json")
                data.append({
                    "id": len(data)+1,
                    "name": ext_name, "date": str(ext_date),
                    "strain": strain, "od_harvest": od_harvest,
                    "vol_culture_ml": vol_culture, "lysis_method": lysis_method,
                    "spin_condition": spin_speed, "protein_conc_mg_ml": protein_conc,
                    "activity_test": activity, "storage": storage, "memo": memo
                })
                save_data("extract.json", data)
                st.success("저장됐습니다!")
                st.rerun()

    with col_list:
        st.markdown("**Cell Extract 목록**")
        extract_data = load_data("extract.json")
        if extract_data:
            df = pd.DataFrame(extract_data)
            cols = ["id","date","name","strain","od_harvest","protein_conc_mg_ml","activity_test"]
            cols = [c for c in cols if c in df.columns]
            st.dataframe(df[cols].rename(columns={
                "id":"#","date":"날짜","name":"배치명","strain":"균주",
                "od_harvest":"수확 OD","protein_conc_mg_ml":"단백질(mg/mL)","activity_test":"활성"
            }), use_container_width=True, hide_index=True)
        else:
            st.info("Cell Extract 기록이 없습니다.")

        # Extract 제조 프로토콜 요약
        st.markdown("---")
        st.markdown("**표준 제조 프로토콜 요약**")
        protocol = [
            ("1. 배양", "LB 또는 2xYTPG 배지, 37°C, 200 rpm"),
            ("2. 수확", "OD₆₀₀ = 2.0~4.0에서 원심분리 (5,000 × g, 10 min, 4°C)"),
            ("3. 세척", "S30 버퍼로 3회 세척"),
            ("4. Lysis", "Sonication (on ice, 3×30 sec, 50% amplitude)"),
            ("5. 원심분리", "12,000 × g, 10 min, 4°C → 상등액 수집"),
            ("6. Run-off", "30°C, 80 rpm, 80 min (리보솜 성숙)"),
            ("7. 보관", "-80°C 분주 보관"),
        ]
        for step, desc in protocol:
            st.markdown(f"**{step}**: {desc}")

# ════════════════════════════════════════════════════════════════════════
# TAB 4: CFPS 반응
# ════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.subheader("⚗️ CFPS 반응 기록")

    col_form, col_mix = st.columns([1, 1])

    with col_form:
        with st.form("cfps_form", clear_on_submit=True):
            st.markdown("**새 CFPS 반응 추가**")
            cfps_name   = st.text_input("실험명", placeholder="예) GFP_CFPS_v1")
            cfps_date   = st.date_input("날짜", value=date.today())
            target_prot = st.text_input("목적 단백질", placeholder="예) sfGFP")
            dna_template= st.text_input("DNA 템플릿", placeholder="예) GFP_linear_v1")
            extract_used= st.text_input("사용 Extract", placeholder="예) BL21_extract_batch01")
            rxn_vol     = st.number_input("반응 볼륨 (μL)", 5, 1000, 15, 5)
            temp        = st.number_input("반응 온도 (°C)", 25.0, 42.0, 30.0, 0.5)
            time_h      = st.number_input("반응 시간 (h)", 0.5, 24.0, 4.0, 0.5)
            extract_pct = st.slider("Extract 비율 (%)", 10, 50, 33)

            st.markdown("**반응 결과**")
            c1, c2 = st.columns(2)
            with c1:
                yield_val = st.text_input("단백질 수율 (μg/mL)", placeholder="예) 450")
            with c2:
                result_cfps = st.selectbox("결과", ["성공","실패","부분 성공","진행 중"])
            memo = st.text_area("메모", height=80)

            if st.form_submit_button("💾 저장", use_container_width=True):
                data = load_data("cfps.json")
                data.append({
                    "id": len(data)+1,
                    "name": cfps_name, "date": str(cfps_date),
                    "target_protein": target_prot, "dna_template": dna_template,
                    "extract_used": extract_used, "rxn_vol_ul": rxn_vol,
                    "temp_c": temp, "time_h": time_h,
                    "extract_pct": extract_pct,
                    "yield_ug_ml": yield_val, "result": result_cfps, "memo": memo
                })
                save_data("cfps.json", data)
                st.success("저장됐습니다!")
                st.rerun()

    with col_mix:
        st.markdown("**CFPS Reaction Mixture 계산기**")
        st.caption("표준 Cytomim 조성 기반")

        rxn_vol_calc  = st.number_input("반응 볼륨 (μL)", 5, 500, 15, 5, key="mix_vol")
        n_rxn_calc    = st.number_input("반응 수", 1, 50, 1, key="mix_rxn")
        extract_ratio = st.slider("Extract 비율 (%)", 10, 50, 33, key="mix_ext")

        ext_vol = rxn_vol_calc * extract_ratio / 100
        remain  = rxn_vol_calc - ext_vol

        components = [
            ("Cell Extract",            ext_vol),
            ("Amino Acids (4mM each)",   remain * 0.10),
            ("ATP (50mM)",               remain * 0.06),
            ("GTP/CTP/UTP (20mM ea)",    remain * 0.06),
            ("Creatine Phosphate (500mM)",remain * 0.06),
            ("Creatine Kinase (10mg/mL)",remain * 0.02),
            ("Mg-glutamate (1M)",         remain * 0.02),
            ("K-glutamate (3M)",          remain * 0.04),
            ("HEPES pH7.2 (1M)",          remain * 0.02),
            ("spermidine (1mM)",          remain * 0.01),
            ("DNA template (200ng/μL)",   remain * 0.05),
            ("RNase Inhibitor",           remain * 0.02),
            ("ddH₂O",                     remain * 0.54),
        ]

        rows = [{"성분": c, "1 rxn (μL)": round(v, 2),
                 f"{n_rxn_calc} rxn (μL)": round(v * n_rxn_calc, 2)}
                for c, v in components]
        df_mix = pd.DataFrame(rows)
        st.dataframe(df_mix, use_container_width=True, hide_index=True)
        st.caption(f"총 볼륨: {rxn_vol_calc} μL | Extract: {round(ext_vol,1)} μL ({extract_ratio}%)")

    # CFPS 기록 목록
    st.markdown("---")
    st.markdown("**CFPS 반응 목록**")
    cfps_data = load_data("cfps.json")
    if cfps_data:
        df = pd.DataFrame(cfps_data)
        cols = ["id","date","name","target_protein","temp_c","time_h","yield_ug_ml","result"]
        cols = [c for c in cols if c in df.columns]
        st.dataframe(df[cols].rename(columns={
            "id":"#","date":"날짜","name":"실험명","target_protein":"단백질",
            "temp_c":"온도(°C)","time_h":"시간(h)","yield_ug_ml":"수율(μg/mL)","result":"결과"
        }), use_container_width=True, hide_index=True)
    else:
        st.info("CFPS 반응 기록이 없습니다.")

# ════════════════════════════════════════════════════════════════════════
# TAB 5: 결과 분석
# ════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.subheader("📊 결과 분석")

    cfps_data = load_data("cfps.json")

    if cfps_data:
        df = pd.DataFrame(cfps_data)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**결과 분포**")
            if "result" in df.columns:
                result_counts = df["result"].value_counts()
                st.bar_chart(result_counts)

        with col2:
            st.markdown("**단백질 수율 추이**")
            if "yield_ug_ml" in df.columns:
                df_yield = df[["date","name","yield_ug_ml"]].copy()
                df_yield["yield_ug_ml"] = pd.to_numeric(df_yield["yield_ug_ml"], errors="coerce")
                df_yield = df_yield.dropna(subset=["yield_ug_ml"])
                if not df_yield.empty:
                    df_yield = df_yield.set_index("date")
                    st.line_chart(df_yield["yield_ug_ml"])

        st.markdown("---")
        st.markdown("**전체 데이터 테이블**")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # CSV 다운로드
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 CSV 다운로드", csv, "cfps_results.csv", "text/csv")
    else:
        st.info("CFPS 반응 데이터가 없습니다. '⚗️ CFPS 반응' 탭에서 실험을 추가해주세요.")

# ════════════════════════════════════════════════════════════════════════
# TAB 6: 실험 노트
# ════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.subheader("📓 자유 실험 노트")

    col_form, col_list = st.columns([1, 1.3])

    with col_form:
        with st.form("note_form", clear_on_submit=True):
            st.markdown("**새 노트 추가**")
            note_date    = st.date_input("날짜", value=date.today())
            note_title   = st.text_input("제목", placeholder="예) sfGFP 발현 조건 최적화 관찰")
            note_category= st.selectbox("분류", ["일반","실험 계획","트러블슈팅","프로토콜 수정","미팅 내용"])
            note_content = st.text_area("내용", height=200,
                placeholder="실험 내용, 관찰 사항, 아이디어 등을 자유롭게 기록하세요...")
            note_todo    = st.text_area("다음 할 일", height=80,
                placeholder="다음 단계 계획...")

            if st.form_submit_button("💾 저장", use_container_width=True):
                data = load_data("notes.json")
                data.append({
                    "id": len(data)+1,
                    "date": str(note_date),
                    "title": note_title,
                    "category": note_category,
                    "content": note_content,
                    "todo": note_todo,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                save_data("notes.json", data)
                st.success("노트가 저장됐습니다!")
                st.rerun()

    with col_list:
        st.markdown("**노트 목록**")
        note_data = load_data("notes.json")
        if note_data:
            for note in reversed(note_data):
                with st.expander(f"📝 {note.get('date','')} — {note.get('title','')} [{note.get('category','')}]"):
                    st.markdown(note.get("content",""))
                    if note.get("todo"):
                        st.markdown("**다음 할 일:**")
                        st.markdown(note.get("todo",""))
        else:
            st.info("노트가 없습니다.")
