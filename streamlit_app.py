import streamlit as st
import datetime
import json

# 페이지 설정
st.set_page_config(
    page_title="간단 출석체크",
    page_icon="📝",
    layout="centered"
)

# CSS 스타일 적용
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 1.5em;
        margin-bottom: 20px;
        color: #495057;
        font-weight: 500;
    }
    
    .student-item {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #eee;
        margin-bottom: 5px;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    
    .student-number {
        min-width: 30px;
        margin-right: 10px;
        color: #666;
        font-weight: bold;
    }
    
    .student-name {
        flex: 1;
        font-size: 1.1em;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        border: none;
        padding: 8px 16px;
        font-size: 0.95em;
        transition: background-color 0.2s;
    }
    
    .save-btn {
        background-color: #40c057 !important;
        color: white !important;
    }
    
    .clear-btn {
        background-color: #ff922b !important;
        color: white !important;
    }
    
    .add-btn {
        background-color: #228be6 !important;
        color: white !important;
    }
    
    .delete-btn {
        background-color: #adb5bd !important;
        color: white !important;
    }
    
    .unsaved-changes {
        color: #ff6b6b;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session state 초기화
if 'students' not in st.session_state:
    st.session_state.students = []

if 'attendance' not in st.session_state:
    st.session_state.attendance = {}

if 'current_view_date' not in st.session_state:
    st.session_state.current_view_date = datetime.date.today()

if 'has_unsaved_changes' not in st.session_state:
    st.session_state.has_unsaved_changes = False

# 현재 날짜 표시
current_date = st.session_state.current_view_date
date_str = current_date.strftime("%Y년 %m월 %d일 %A")

# 한국어 요일 변환
weekdays = {
    'Monday': '월요일',
    'Tuesday': '화요일', 
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}

for eng, kor in weekdays.items():
    date_str = date_str.replace(eng, kor)

st.markdown(f'<div class="main-title">{date_str}</div>', unsafe_allow_html=True)

# 저장된 날짜 선택
col1, col2 = st.columns([3, 1])

with col1:
    saved_dates = list(st.session_state.attendance.keys())
    saved_dates.sort(reverse=True)
    
    if saved_dates:
        date_options = ['오늘 날짜'] + [str(date) for date in saved_dates]
        selected_date_option = st.selectbox(
            "저장된 날짜 선택",
            options=date_options,
            index=0
        )
        
        if selected_date_option != '오늘 날짜':
            selected_date = datetime.datetime.strptime(selected_date_option, '%Y-%m-%d').date()
            if st.session_state.current_view_date != selected_date:
                st.session_state.current_view_date = selected_date
                st.session_state.has_unsaved_changes = False
                st.rerun()

with col2:
    if st.session_state.has_unsaved_changes:
        st.markdown('<div class="unsaved-changes">*저장되지 않은 변경사항</div>', unsafe_allow_html=True)

# 버튼 그룹
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 저장", key="save_btn"):
        date_key = str(st.session_state.current_view_date)
        if date_key not in st.session_state.attendance:
            st.session_state.attendance[date_key] = {}
        st.session_state.has_unsaved_changes = False
        st.success("저장되었습니다!")

with col2:
    if st.button("🧹 깨끗이", key="clear_btn"):
        date_key = str(st.session_state.current_view_date)
        if date_key in st.session_state.attendance:
            for student_id in st.session_state.attendance[date_key]:
                st.session_state.attendance[date_key][student_id] = {
                    'morning': False,
                    'afternoon': False
                }
        st.session_state.has_unsaved_changes = True
        st.rerun()

# 학생 목록 표시
if st.session_state.students:
    st.markdown("### 📋 학생 출석 현황")
    
    date_key = str(st.session_state.current_view_date)
    if date_key not in st.session_state.attendance:
        st.session_state.attendance[date_key] = {}
    
    for i, student in enumerate(st.session_state.students):
        student_id = student['id']
        
        # 학생별 출석 데이터 초기화
        if student_id not in st.session_state.attendance[date_key]:
            st.session_state.attendance[date_key][student_id] = {
                'morning': False,
                'afternoon': False
            }
        
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
        
        with col1:
            st.markdown(f"**{i+1}.**")
        
        with col2:
            st.markdown(f"**{student['name']}**")
        
        with col3:
            sub_col1, sub_col2 = st.columns(2)
            
            with sub_col1:
                morning_key = f"morning_{student_id}_{date_key}"
                morning_checked = st.checkbox(
                    "조회", 
                    value=st.session_state.attendance[date_key][student_id]['morning'],
                    key=morning_key
                )
                
                if morning_checked != st.session_state.attendance[date_key][student_id]['morning']:
                    st.session_state.attendance[date_key][student_id]['morning'] = morning_checked
                    st.session_state.has_unsaved_changes = True
            
            with sub_col2:
                afternoon_key = f"afternoon_{student_id}_{date_key}"
                afternoon_checked = st.checkbox(
                    "종례", 
                    value=st.session_state.attendance[date_key][student_id]['afternoon'],
                    key=afternoon_key
                )
                
                if afternoon_checked != st.session_state.attendance[date_key][student_id]['afternoon']:
                    st.session_state.attendance[date_key][student_id]['afternoon'] = afternoon_checked
                    st.session_state.has_unsaved_changes = True
        
        with col4:
            if st.button("🗑️", key=f"delete_{student_id}", help="학생 삭제"):
                st.session_state.students = [s for s in st.session_state.students if s['id'] != student_id]
                # 출석 데이터에서도 해당 학생 정보 제거
                for date in st.session_state.attendance:
                    if student_id in st.session_state.attendance[date]:
                        del st.session_state.attendance[date][student_id]
                st.rerun()

else:
    st.info("👥 아직 등록된 학생이 없습니다. 아래에서 학생을 추가해주세요!")

# 학생 추가
st.markdown("---")
st.markdown("### ➕ 학생 추가")

col1, col2 = st.columns([3, 1])

with col1:
    new_student_name = st.text_input("학생 이름을 입력하세요", key="student_input")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # 간격 맞추기
    if st.button("추가", key="add_student_btn"):
        if new_student_name.strip():
            new_student = {
                'id': str(datetime.datetime.now().timestamp()),
                'name': new_student_name.strip()
            }
            st.session_state.students.append(new_student)
            st.session_state.student_input = ""  # 입력창 초기화
            st.success(f"'{new_student_name}' 학생이 추가되었습니다!")
            st.rerun()
        else:
            st.error("학생 이름을 입력해주세요!")

# 통계 정보 표시
if st.session_state.students:
    st.markdown("---")
    st.markdown("### 📊 출석 통계")
    
    date_key = str(st.session_state.current_view_date)
    if date_key in st.session_state.attendance:
        total_students = len(st.session_state.students)
        morning_present = sum(1 for student_id in st.session_state.attendance[date_key] 
                            if st.session_state.attendance[date_key][student_id].get('morning', False))
        afternoon_present = sum(1 for student_id in st.session_state.attendance[date_key] 
                              if st.session_state.attendance[date_key][student_id].get('afternoon', False))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("전체 학생 수", total_students)
        
        with col2:
            st.metric("조회 출석", f"{morning_present}/{total_students}")
        
        with col3:
            st.metric("종례 출석", f"{afternoon_present}/{total_students}")

# 하단 정보
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    💡 팁: 체크박스를 클릭한 후 '저장' 버튼을 눌러주세요!
</div>
""", unsafe_allow_html=True)