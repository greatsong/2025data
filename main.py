# streamlit_app.py
# ─────────────────────────────────────────────────────────────────────────────
# 🎓 MBTI 학습 코치 — 16개 MBTI별 학습 장단점 & 공부법 추천
# Streamlit Cloud에서 추가 설치 없이 실행 가능 (streamlit만 필요)
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from datetime import date, timedelta
import random

# 기본 페이지 설정
st.set_page_config(
    page_title="MBTI 학습 코치",
    page_icon="🎓",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────────────────────
# 데이터 준비
# ─────────────────────────────────────────────────────────────────────────────

MBTI_TYPES = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# 16유형 한줄 별명(가볍게/재미용)
NICK = {
    "ISTJ":"📘 현실적 관리자", "ISFJ":"🫶 성실한 보호자", "INFJ":"🔮 통찰형 상담가", "INTJ":"🧠 전략 설계자",
    "ISTP":"🧰 실전 해결가", "ISFP":"🎨 따뜻한 예술가", "INFP":"🌱 이상주의 탐구자", "INTP":"🧩 사색형 분석가",
    "ESTP":"⚡ 현장형 실행가", "ESFP":"🎉 에너지 메이커", "ENFP":"✨ 아이디어 뱅크", "ENTP":"🗣️ 토론형 발명가",
    "ESTJ":"🏗️ 체계적 리더", "ESFJ":"🤝 분위기 메이커", "ENFJ":"🏅 격려형 코치", "ENTJ":"🚀 목표 지향 리더"
}

# 글자별(차원별) 장점/약점/전략 템플릿
DIM = {
    "I":{
        "strengths":["혼자 집중 잘함 🧘","깊이 있는 몰입/정독에 강함 📖","자기주도 복습 습관화에 유리 🔁"],
        "pitfalls":["질문/피드백 요청이 적어 정보 누락 위험 🙊","과도한 완벽주의로 진도 지연 ⏳"],
        "strategies":[
            "❗ 매 수업 후 5분 '요점 3줄' 기록",
            "🤝 주 1회 질문 리스트 만들어 선생님/친구에게 확인",
            "⏱️ 25분 몰입 + 5분 휴식(Pomodoro)로 과몰입 방지"
        ]
    },
    "E":{
        "strengths":["토론/스터디에서 이해가 빨라짐 🗣️","학습 동기 유지가 쉬움 🔥","발표·설명으로 기억 강화 🧠➡️🧠"],
        "pitfalls":["말하다 산만해질 위험 😅","계획 없이 즉흥 학습으로 누락 발생 ⚠️"],
        "strategies":[
            "👥 스터디에서 '설명 담당' 맡아 가르치며 학습",
            "📋 학습 전 3개 체크포인트 정하고 시작(탈선 방지)",
            "🔕 공부 시간엔 알림 OFF, 토론은 블록 타임에만"
        ]
    },
    "S":{
        "strengths":["사례/문제풀이에 강함 🧮","매뉴얼/교과서 기반 학습 최적화 📘","세부 암기력 좋음 🧩"],
        "pitfalls":["큰 그림/추상 개념 연결이 약할 수 있음 🧱","암기에 치중해 응용력이 떨어질 수 있음"],
        "strategies":[
            "🔗 '개념-예시-반례' 3단 노트",
            "🧱 유사문제 3종(쉬움/보통/응용)로 난이도 사다리",
            "🗺️ 단원 시작마다 '한 장 개념 지도' 작성"
        ]
    },
    "N":{
        "strengths":["빅픽처/패턴 파악 탁월 🌐","아이디어 전환·추론에 강함 💡","교과 간 연결 넘버원 🔗"],
        "pitfalls":["세부실수/단계 누락 ⚙️","아이디어만 많고 실행 약해질 수 있음 🌀"],
        "strategies":[
            "🧭 '개념→근거→예시' 순서 체크리스트로 단계 고정",
            "📌 문제 풀이 후 '놓친 디테일 1개' 반드시 점검",
            "🗂️ 프로젝트는 마감 2개(소프트/하드)로 실행력 확보"
        ]
    },
    "T":{
        "strengths":["분석적 사고/비교/검증에 강함 🧪","오답 원인추적·패턴화 잘함 🔍"],
        "pitfalls":["스스로/타인에 비판적이라 동기 저하 가능 🥲","감정·동기 관리 소홀 위험"],
        "strategies":[
            "📊 오답 사유(개념/계산/부주의) 태깅 후 비율 관리",
            "🎯 목표를 수치화(예: 주당 오답률 15%→8%)",
            "💬 스스로에게 '칭찬 로그' 추가(성취 1줄 기록)"
        ]
    },
    "F":{
        "strengths":["공동학습/피어피드백 효과 큼 🤝","이야기/서사로 기억 잘됨 📚"],
        "pitfalls":["관계 스트레스가 성과에 영향 😥","비판이 두려워 질문 회피 가능"],
        "strategies":[
            "💗 스터디서 '칭찬 1, 제안 1' 규칙 만들기",
            "📜 서사형 노트(개념이 생긴 이유→적용 사례)로 기억 강화",
            "🌿 감정 체크(😄/😐/😣)와 학습량 상관관계 관찰"
        ]
    },
    "J":{
        "strengths":["계획/마감 준수 🗓️","체크리스트로 성취 ↑ ☑️"],
        "pitfalls":["계획 변경에 스트레스 🫨","유연한 탐색/실험이 부족할 수 있음"],
        "strategies":[
            "📆 타임블록(과목별 45~60분) + 버퍼(15분) 확보",
            "🧺 '오늘 할 일 3개' 초점제한(Too much 계획 방지)",
            "🔄 매주 일요일 15분 리플랜(계획-현실 차이 조정)"
        ]
    },
    "P":{
        "strengths":["유연/창의/문제 전환 능력 👍","압박 속 번뜩임 ⚡"],
        "pitfalls":["미루기/마감 직전 몰아치기 🏃‍♂️","누락·정리 부족"],
        "strategies":[
            "⏳ 10분 착수 규칙(시작 장벽 낮추기)",
            "🍅 25-5 뽀모도로 3세트 후 '정리 10분' 고정",
            "🧷 소프트 데드라인(실제 2일 전) + 하드 데드라인"
        ]
    }
}

# 유형별 '분위기' 설명(가벼운 요약)
ONE_LINER = {
    "ISTJ":"체계와 근거로 차근차근 쌓는 타입.",
    "ISFJ":"성실·배려형, 루틴이 학습력으로 연결돼요.",
    "INFJ":"의미/맥락을 찾아 깊게 연결하는 탐구가.",
    "INTJ":"목표-전략-실행 루틴이 잘 맞아요.",
    "ISTP":"원리 이해 후 바로 적용/튜닝하는 현장형.",
    "ISFP":"감각·정서 친화적, 편안한 몰입 환경이 중요.",
    "INFP":"가치/의미가 생기면 폭발적으로 몰입!",
    "INTP":"논리 구조화, 오답 원인 추적의 달인.",
    "ESTP":"행동-피드백-개선 사이클이 빠른 실전형.",
    "ESFP":"재밌어야 오래 가는 타입! 보상·경험 설계 👍",
    "ENFP":"아이디어 풍부! 실행·정리 장치만 더하면 금상첨화.",
    "ENTP":"토론·반박으로 개념을 단단히 만듭니다.",
    "ESTJ":"규칙/목표 중심, 성과 관리에 강함.",
    "ESFJ":"사람과 함께할 때 학습 동력이 커져요.",
    "ENFJ":"목표·격려·리더십으로 팀도 나도 성장!",
    "ENTJ":"큰 목표를 쪼개고 드라이브하는 추진가."
}

# 재미용 성향 점수(대략치, 과학적 지표 아님)
def trait_scores(mbti: str):
    base = 50
    # Focus
    focus = base + (15 if "I" in mbti else 0) + (15 if "J" in mbti else -10) + (10 if "S" in mbti else -5)
    # Planning
    planning = base + (25 if "J" in mbti else -15) + (5 if "S" in mbti else -5) + (5 if "I" in mbti else 0)
    # Idea
    idea = base + (25 if "N" in mbti else -10) + (5 if "P" in mbti else 0)
    # Social
    social = base + (25 if "E" in mbti else -10) + (10 if "F" in mbti else -5)
    clamp = lambda x: max(5, min(95, x))
    return clamp(focus), clamp(planning), clamp(idea), clamp(social)

def dedup(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            out.append(x); seen.add(x)
    return out

def build_profile(mbti: str):
    letters = list(mbti)
    strengths = []
    pitfalls = []
    strategies = []
    for ch in letters:
        strengths += DIM[ch]["strengths"]
        pitfalls  += DIM[ch]["pitfalls"]
        strategies += DIM[ch]["strategies"]
    # 정리
    strengths = dedup(strengths)[:6]
    pitfalls  = dedup(pitfalls)[:6]
    strategies = dedup(strategies)[:10]
    return strengths, pitfalls, strategies

# 랜덤 미션(짧고 실천 가능한 것들)
MICRO_MISSIONS = [
    "📝 오늘 배운 개념을 '10문장 요약→3문장 요약'으로 줄이기",
    "🔁 오답 3개를 같은 유형 문제로 재도전",
    "⌛ 25분 뽀모도로 2세트 + 5분 스트레칭",
    "📣 개념 1개를 가족/친구에게 1분 설명하기",
    "🗂️ 노트에 '개념-예시-반례' 한 세트 만들기",
    "📆 이번 주 학습 일정 15분 리플랜",
    "🔕 40분 집중 타임 동안 휴대폰 비행기 모드",
    "🌿 2분 호흡 명상 후 학습 시작",
    "📌 다음 시험에 나올 만한 서술형 문제 1개 스스로 만들기",
    "🧠 오늘 배운 것 중 '한 가지 왜?'를 3번 연속 질문"
]

# ─────────────────────────────────────────────────────────────────────────────
# 사이드바 UI
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎓 MBTI 학습 코치")
    st.caption("※ MBTI는 참고용입니다. 개인차가 훨씬 커요!")
    mbti = st.selectbox("MBTI를 선택하세요", MBTI_TYPES, index=10)  # ENFP를 기본 선택(흥미 유도)
    show_confetti = st.toggle("재미 효과 켜기(🎈/❄️)", value=True)
    st.divider()
    st.subheader("루틴 생성 (선택)")
    subj = st.text_input("목표 과목/단원", value="수학 함수")
    exam_day = st.date_input("시험/평가일", value=date.today() + timedelta(days=30))
    daily_min = st.slider("하루 공부 가능 시간(분)", 30, 240, 90, step=15)
    make_plan = st.button("📅 루틴 만들기")

# ─────────────────────────────────────────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────────────────────────────────────────
colA, colB = st.columns([0.8, 0.2])
with colA:
    st.markdown(f"## {NICK[mbti]} — **{mbti}**")
    st.caption(ONE_LINER[mbti])
with colB:
    st.metric("오늘의 기분", "🔥 파이팅!", help="스스로를 격려해요! 작은 성취가 큰 동력이 됩니다.")
    if show_confetti:
        st.balloons()

# 성향 지표(재미용)
foc, plan, idea, soci = trait_scores(mbti)
st.markdown("### 🧭 학습 성향(가벼운 참고용)")
c1, c2, c3, c4 = st.columns(4)
for (c, label, val, tip) in [
    (c1, "집중력", foc, "방해 차단 + 짧은 몰입 세트"),
    (c2, "계획성", plan, "타임블록 + 주간 리플랜"),
    (c3, "아이디어", idea, "개념 지도/연결 노트"),
    (c4, "사회적 학습", soci, "스터디/설명 학습")
]:
    with c:
        st.progress(val/100, text=f"{label} {val}/100")
        st.caption(f"Tip: {tip}")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# 본문 탭
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🧠 핵심 요약", "📚 추천 공부법", "🏆 오늘의 미션"])

with tab1:
    strengths, pitfalls, strategies = build_profile(mbti)
    st.subheader("장점(Strengths)")
    st.write("\n".join([f"- {s}" for s in strengths]))
    st.subheader("주의할 점(Pitfalls)")
    st.write("\n".join([f"- {p}" for p in pitfalls]))

    with st.expander("🔎 왜 이런 경향이 나타날까요? (참고용)"):
        st.markdown(
            "- MBTI는 **성향 경향**을 가볍게 보는 도구예요. 개인차가 큽니다.\n"
            "- 장점을 살리고, 단점은 **작은 습관**으로 보완해요.\n"
            "- 아래 추천 공부법은 '한 번에 전부'가 아니라 **가장 쉬운 것 1~2개**부터!"
        )

with tab2:
    st.subheader("이 유형에게 특히 잘 맞는 공부법")
    st.write("\n".join([f"✅ {tip}" for tip in strategies]))

    st.markdown("#### 📒 노트 & 복습 루틴 예시")
    if "S" in mbti:
        st.markdown("- **개념-예시-반례** 3단 노트로 정확도 강화")
    else:
        st.markmarkdown = st.markdown  # 안전장치
        st.markdown("- **개념 지도/연결 화살표**로 큰 그림 유지")

    if "J" in mbti:
        st.markdown("- 매일 **할 일 3개** + 주 1회 **리플랜 15분**")
    else:
        st.markdown("- **10분 착수 규칙**으로 먼저 시작 → 흐름 타기")

    if "T" in mbti:
        st.markdown("- 오답을 **원인 태깅**(개념/계산/부주의)하여 재발 방지")
    else:
        st.markdown("- **서사형 요약**(왜 배웠는지→어디에 쓰는지)로 기억 강화")

    st.markdown("#### 🧪 시험 대비")
    st.markdown("- '실수 리스트'를 만들어 **시험 하루 전 10분**에만 훑기")
    st.markdown("- 서술형: **근거 문장**(정의/법칙/조건)을 맨 앞에 쓰는 연습")

with tab3:
    st.subheader("오늘의 3분 미션")
    # 세션별 고정 미션
    if "missions" not in st.session_state:
        st.session_state.missions = random.sample(MICRO_MISSIONS, k=3)
        st.session_state.done = [False, False, False]

    for idx, m in enumerate(st.session_state.missions):
        st.session_state.done[idx] = st.checkbox(m, value=st.session_state.done[idx], key=f"m{idx}")

    if all(st.session_state.done):
        st.success("완료! 대단해요 🎉 작아도 '완료 경험'이 동기부여의 핵심!")
        if show_confetti:
            st.snow()

# ─────────────────────────────────────────────────────────────────────────────
# 루틴 생성기 (사이드바에서 입력 시)
# ─────────────────────────────────────────────────────────────────────────────
if make_plan:
    days = (exam_day - date.today()).days
    days = max(7, days)  # 최소 1주
    weekly_goal = int(daily_min * 7 / 60)  # 시간 단위
    st.markdown("## 📅 맞춤 루틴 제안")
    st.caption("※ 개인 사정에 따라 유연하게 조정하세요!")

    # 유형별 한 줄 코칭
    coach_line = {
        "J":"계획은 충분! '버퍼 15분'을 꼭 넣어 유연성을 확보해요.",
        "P":"'10분 착수'로 시작 장벽을 낮추고, 끝나면 10분 정리까지.",
        "S":"예제-유형-응용 순서로 난이도를 조금씩 올려요.",
        "N":"개념 연결 지도를 유지하면서 세부 체크리스트로 누락 방지!",
        "T":"오답 태깅으로 효율 상승! 수치 목표를 작게 잡아도 좋아요.",
        "F":"파트너와 '칭찬1+제안1' 피드백 규칙으로 즐겁게 지속!"
    }
    tip = " / ".join([coach_line[ch] for ch in mbti])
    st.info(f"코치 한마디: {tip}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("D-Day", f"{days}일 남음")
    with col2:
        st.metric("하루 학습(분)", f"{daily_min}분")
    with col3:
        st.metric("주간 목표(시간)", f"{weekly_goal}시간")

    # 주당 템플릿(간단 예시)
    st.markdown("### 주간 템플릿 (예시)")
    st.markdown(f"""
- **월/수/금**: {subj} 개념 정리(각 {daily_min//3}~{daily_min//2}분)
- **화/목**: {subj} 문제풀이 + 오답 태깅(각 {daily_min//2}분)
- **토**: 서술형/프로젝트형 정리(요약 노트, 예상문제 만들기)
- **일**: 15분 리플랜(이번 주 성과 체크 → 다음 주 수정)
""")
    if show_confetti:
        st.balloons()

# ─────────────────────────────────────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption("ⓘ MBTI는 절대적인 진리가 아니라 '참고용 프레임'이에요. 결국 중요한 건 당신의 실제 데이터(시간·오답·습관)!")
