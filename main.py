import streamlit as st
from datetime import date, timedelta

# --- 페이지 설정 ---
# 'centered' 레이아웃이 모바일 환경에 더 적합할 수 있습니다. (기본값이기도 함)
# st.set_page_config(layout="centered") # 명시적으로 설정하거나 기본값을 사용

# --- 앱 제목 ---
st.title("🗓️ 녹색어머니 활동 날짜별 예약 시스템")

# --- 예약 기간 설정 ---
start_date = date(2025, 5, 26)
num_days_to_show = 5 # 5월 26일 ~ 5월 30일
date_range = [start_date + timedelta(days=i) for i in range(num_days_to_show)]

# --- 세션 상태 초기화 ---
if 'reservations' not in st.session_state:
    st.session_state.reservations = {day.isoformat(): 0 for day in date_range}

# --- 예약 가능 날짜 및 예약 인터페이스 ---
st.header("📅 예약 가능 날짜")
st.write(f"{start_date.strftime('%Y년 %m월 %d일')}부터 {date_range[-1].strftime('%Y년 %m월 %d일')}까지 예약 가능합니다.")
st.write("각 날짜별 최대 예약 인원은 3명입니다.")
st.markdown("---") # 구분선

# "표" 형태로 각 날짜별 예약 정보 표시
# 각 날짜가 표의 한 행(row)처럼 표시됩니다.
for day in date_range:
    day_str = day.isoformat()
    current_reservations = st.session_state.reservations.get(day_str, 0)

    # 모바일에서는 이 컬럼들이 세로로 쌓입니다.
    # 비율을 조정하여 모바일에서의 가독성을 고려할 수 있습니다.
    col1, col2, col3 = st.columns([2, 1.5, 1.5]) # 날짜, 현황, 버튼/상태

    with col1:
        st.markdown(f"**{day.strftime('%Y-%m-%d (%a)')}**") # 날짜 및 요일 (굵게)

    with col2:
        st.write(f"예약: {current_reservations} / 3 명")

    with col3:
        if current_reservations < 3:
            if st.button(f"예약하기", key=f"book_{day_str}", use_container_width=True): # 버튼 너비 조정
                st.session_state.reservations[day_str] += 1
                st.success(f"{day.strftime('%Y-%m-%d')} 예약 완료! (현재: {st.session_state.reservations[day_str]}명)")
                # st.experimental_rerun() # Streamlit 1.18.0 이전 버전
                st.rerun() # 변경사항 즉시 반영
        else:
            st.error("예약 마감")
    st.markdown("---") # 각 날짜 항목 사이에 구분선 추가

# --- 전체 예약 현황 확인 ---
st.header("📊 전체 예약 현황")
if any(st.session_state.reservations.values()):
    data = []
    for day_iso, count in sorted(st.session_state.reservations.items()): # 날짜순 정렬
        day_obj = date.fromisoformat(day_iso)
        status = "예약 가능" if count < 3 else "예약 마감"
        data.append({
            "날짜": day_obj.strftime('%Y-%m-%d (%a)'),
            "예약 인원": f"{count} 명",
            "상태": status
        })
    
    st.table(data) # 이 부분은 실제 표로 깔끔하게 현황을 보여줍니다.
else:
    st.info("현재 예약된 내역이 없습니다.")

# --- 예약 초기화 버튼 (테스트용) ---
if st.sidebar.button("모든 예약 초기화 (테스트용)"):
    st.session_state.reservations = {day.isoformat(): 0 for day in date_range}
    st.rerun()
