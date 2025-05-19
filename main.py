import streamlit as st
from datetime import date, timedelta

# --- 페이지 설정 ---
st.set_page_config(layout="centered", page_title="녹색어미니 활동 예약 시스템") # 페이지 제목 추가

# --- 앱 제목 ---
st.title("🗓️ 날짜별 예약 시스템")

# --- 예약 기간 설정 ---
start_date = date(2025, 5, 26)
num_days_to_show = 5 # 5월 26일 ~ 5월 30일
date_range = [start_date + timedelta(days=i) for i in range(num_days_to_show)]

# --- 세션 상태 초기화 ---
# reservations는 이제 각 날짜에 대한 예약 목록을 저장합니다.
# booking_day_selected는 현재 어떤 날짜에 대해 예약 폼을 보여줄지 추적합니다.
if 'reservations' not in st.session_state:
    # {날짜(isoformat): [예약1 정보, 예약2 정보, ...]} 형태
    st.session_state.reservations = {day.isoformat(): [] for day in date_range}
if 'booking_day_selected' not in st.session_state:
    st.session_state.booking_day_selected = None # 예약 폼 표시를 위한 상태 변수

MAX_RESERVATIONS_PER_DAY = 3

# --- 예약 가능 날짜 및 예약 인터페이스 (열 형태로 표시) ---
st.header("📅 예약 가능 날짜")
st.write(f"{start_date.strftime('%Y년 %m월 %d일')}부터 {date_range[-1].strftime('%Y년 %m월 %d일')}까지 예약 가능합니다.")
st.write(f"각 날짜별 최대 예약 인원은 {MAX_RESERVATIONS_PER_DAY}명입니다.")
st.markdown("---") # 구분선

# 각 날짜를 세로 "열"로 표시합니다.
columns = st.columns(len(date_range))

for i, day in enumerate(date_range):
    day_str = day.isoformat()
    current_reservations = st.session_state.reservations.get(day_str, []) # 해당 날짜의 예약 목록 가져오기
    current_reservation_count = len(current_reservations) # 현재 예약 인원 수

    with columns[i]:
        st.markdown(f"<h5 style='text-align: center;'>{day.strftime('%Y-%m-%d')}</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'><strong>({day.strftime('%a')})</strong></p>", unsafe_allow_html=True)
        st.markdown("---") # 각 열 내부의 날짜와 내용 구분

        st.write(f"예약: {current_reservation_count} / {MAX_RESERVATIONS_PER_DAY} 명")

        if current_reservation_count < MAX_RESERVATIONS_PER_DAY:
            # 현재 날짜에 대해 예약 폼이 활성화되지 않았을 때만 버튼 표시
            if st.session_state.booking_day_selected != day_str:
                 if st.button(f"예약하기", key=f"book_btn_{day_str}", use_container_width=True):
                    # 버튼 클릭 시 해당 날짜의 예약 폼 활성화 상태로 변경
                    st.session_state.booking_day_selected = day_str
                    st.rerun() # 상태 변경을 반영하기 위해 새로고침
            else:
                 # 해당 날짜에 대해 예약 폼이 활성화 되었음을 표시
                 st.info("정보 입력 대기 중...")

        else:
            st.error("예약 마감")

st.markdown("---") # 전체 열 그룹 다음의 구분선

# --- 예약 정보 입력 폼 ---
# booking_day_selected 값이 있을 때만 폼을 표시합니다.
if st.session_state.booking_day_selected:
    selected_day_iso = st.session_state.booking_day_selected
    selected_day_obj = date.fromisoformat(selected_day_iso)

    st.subheader(f"{selected_day_obj.strftime('%Y년 %m월 %d일')} 예약 정보 입력")

    # st.form을 사용하여 입력 위젯들을 그룹화
    with st.form(key=f"booking_form_{selected_day_iso}"):
        user_name = st.text_input("이름", key=f"name_{selected_day_iso}")
        user_contact = st.text_input("연락처", help="예: 010-1234-5678", key=f"contact_{selected_day_iso}")

        # 폼 제출 버튼
        submit_button = st.form_submit_button("예약 확인")

        # 폼 제출 버튼 클릭 시 처리
        if submit_button:
            # 입력값 유효성 검사 (간단하게 비어있는지 확인)
            if not user_name or not user_contact:
                st.warning("이름과 연락처를 모두 입력해주세요.")
            else:
                # 예약 추가 로직
                # 다시 한번 해당 날짜의 현재 예약 인원을 확인합니다 (폼 열린 후 다른 사람이 예약했을 경우 대비)
                current_reservations_count = len(st.session_state.reservations.get(selected_day_iso, []))
                if current_reservations_count < MAX_RESERVATIONS_PER_DAY:
                    st.session_state.reservations[selected_day_iso].append({
                        "name": user_name,
                        "contact": user_contact
                    })
                    st.success(f"{selected_day_obj.strftime('%Y년 %m월 %d일')} 예약이 완료되었습니다! ({user_name} 님)")

                    # 폼 비활성화 및 상태 초기화
                    st.session_state.booking_day_selected = None
                    st.rerun() # 변경사항 반영 및 폼 숨김

                else:
                    st.error(f"{selected_day_obj.strftime('%Y년 %m월 %d일')}은 이미 예약 마감되었습니다.")
                    st.session_state.booking_day_selected = None # 폼 비활성화
                    st.rerun() # 변경사항 반영


# --- 전체 예약 현황 확인 (상세 정보 포함) ---
st.header("📊 전체 예약 현황")

all_reservations_list = []
# 날짜 순서대로 정렬하여 표시
for day_iso in sorted(st.session_state.reservations.keys()):
    day_obj = date.fromisoformat(day_iso)
    reservations_for_day = st.session_state.reservations[day_iso]
    day_status = "예약 가능" if len(reservations_for_day) < MAX_RESERVATIONS_PER_DAY else "예약 마감"

    if reservations_for_day:
        for i, res in enumerate(reservations_for_day):
             all_reservations_list.append({
                "날짜": day_obj.strftime('%Y-%m-%d (%a)'),
                # "예약 번호 (당일)": i + 1, # 필요하다면 예약 순서 추가
                "이름": res["name"],
                "연락처": res["contact"],
                "날짜 상태": day_status # 해당 날짜의 현재 상태
            })
    else:
         # 예약이 하나도 없는 날짜도 목록에 추가 (선택 사항)
         all_reservations_list.append({
            "날짜": day_obj.strftime('%Y-%m-%d (%a)'),
            # "예약 번호 (당일)": "-",
            "이름": "예약 없음",
            "연락처": "-",
            "날짜 상태": day_status
         })

if all_reservations_list:
     # pandas DataFrame을 사용하여 더 보기 좋게 표시
     import pandas as pd
     df = pd.DataFrame(all_reservations_list)
     st.dataframe(df, use_container_width=True)
else:
    st.info("현재 예약된 내역이 없습니다.")


# --- 예약 초기화 버튼 (테스트용) ---
if st.sidebar.button("모든 예약 초기화 (테스트용)"):
    st.session_state.reservations = {day.isoformat(): [] for day in date_range} # 예약 목록을 빈 리스트로 초기화
    st.session_state.booking_day_selected = None # 폼 활성화 상태도 초기화
    st.rerun()
