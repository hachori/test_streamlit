import streamlit as st
from datetime import date, timedelta

# 앱 제목 설정
st.title("🗓️ 날짜별 예약 시스템")

# 예약 기간 설정
start_date = date(2025, 5, 26)
# 사용자가 "23일"이라고 언급한 부분을 우선 5일로 가정 (월~금)
# 만약 26일부터 23일간을 의미했다면 end_date = start_date + timedelta(days=22) 로 변경
num_days_to_show = 5
date_range = [start_date + timedelta(days=i) for i in range(num_days_to_show)]

# 세션 상태 초기화 (예약 데이터 저장)
if 'reservations' not in st.session_state:
    st.session_state.reservations = {day.isoformat(): 0 for day in date_range}
if 'user_reservations' not in st.session_state:
    st.session_state.user_reservations = {} # 사용자별 예약 정보를 저장 (선택적 확장 기능)

st.header("📅 예약 가능 날짜")
st.write(f"{start_date.strftime('%Y년 %m월 %d일')}부터 {date_range[-1].strftime('%Y년 %m월 %d일')}까지 예약 가능합니다.")
st.write("각 날짜별 최대 예약 인원은 3명입니다.")

# 예약 섹션
for day in date_range:
    day_str = day.isoformat()
    current_reservations = st.session_state.reservations.get(day_str, 0)

    col1, col2, col3 = st.columns([2,1,2])

    with col1:
        st.subheader(f"{day.strftime('%Y년 %m월 %d일 (%a)')}") # 요일도 함께 표시

    with col2:
        st.write(f"예약 현황: {current_reservations} / 3 명")

    with col3:
        if current_reservations < 3:
            if st.button(f"{day.strftime('%m월 %d일')} 예약하기", key=f"book_{day_str}"):
                st.session_state.reservations[day_str] += 1
                # 간단한 예약자 정보 입력 (선택 사항)
                # user_name = st.text_input(f"{day_str} 예약자 이름", key=f"user_{day_str}_name_temp") # 실제 사용 시에는 다른 방식으로 처리 필요
                st.success(f"{day.strftime('%Y년 %m월 %d일')}에 예약되었습니다! 현재 예약: {st.session_state.reservations[day_str]}명")
                st.rerun() # 예약 후 화면을 새로고침하여 상태를 즉시 반영
        else:
            st.error("예약 마감")

st.divider() # 구분선

# 현재 예약 현황 확인
st.header("📊 전체 예약 현황")
if any(st.session_state.reservations.values()): # 하나라도 예약이 있다면
    data = []
    for day_iso, count in st.session_state.reservations.items():
        day_obj = date.fromisoformat(day_iso)
        data.append({"날짜": day_obj.strftime('%Y년 %m월 %d일 (%a)'), "예약 인원": f"{count} 명"})
    
    st.table(data)
else:
    st.info("현재 예약된 내역이 없습니다.")

# 초기화 버튼 (테스트용)
if st.sidebar.button("모든 예약 초기화 (테스트용)"):
    st.session_state.reservations = {day.isoformat(): 0 for day in date_range}
    st.session_state.user_reservations = {}
    st.rerun()
