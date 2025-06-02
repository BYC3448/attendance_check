import streamlit as st
import datetime
import json
import os

# 파일 저장 경로 설정
DATA_PATH = "attendance_data.json"
STUDENT_PATH = "students.json"

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_students():
    if os.path.exists(STUDENT_PATH):
        with open(STUDENT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_students(students):
    with open(STUDENT_PATH, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

# 데이터 불러오기
attendance_data = load_data()
students = load_students()

# 오늘 날짜 문자열
current_date = datetime.date.today().isoformat()

# 앱 제목 표시
st.title("간단 출석체크")
st.subheader(datetime.date.today().strftime("%Y년 %m월 %d일 (%A)"))

# 날짜 선택
saved_dates = sorted(attendance_data.keys(), reverse=True)
selected_date = st.selectbox("저장된 날짜 선택", ["오늘 날짜"] + saved_dates)

if selected_date == "오늘 날짜":
    view_date = current_date
else:
    view_date = selected_date

# 저장, 초기화 버튼
col1, col2 = st.columns(2)
if col1.button("💾 저장"):
    save_data(attendance_data)
    st.success("출석 정보가 저장되었습니다.")

if col2.button("🧹 깨끗이"):
    if view_date in attendance_data:
        for sid in attendance_data[view_date]:
            attendance_data[view_date][sid] = {"morning": False, "afternoon": False}
    st.experimental_rerun()

# 학생 목록 표시
st.markdown("---")
st.write("### 학생 목록")

for idx, student in enumerate(students):
    sid = student['id']
    name = student['name']
    if view_date not in attendance_data:
        attendance_data[view_date] = {}
    if sid not in attendance_data[view_date]:
        attendance_data[view_date][sid] = {"morning": False, "afternoon": False}

    cols = st.columns([0.1, 0.4, 0.2, 0.2, 0.1])
    cols[0].write(f"{idx+1}.")
    cols[1].write(name)
    attendance_data[view_date][sid]["morning"] = cols[2].checkbox("조회", value=attendance_data[view_date][sid]["morning"], key=f"m_{sid}")
    attendance_data[view_date][sid]["afternoon"] = cols[3].checkbox("종례", value=attendance_data[view_date][sid]["afternoon"], key=f"a_{sid}")
    if cols[4].button("삭제", key=f"del_{sid}"):
        students = [s for s in students if s['id'] != sid]
        save_students(students)
        st.experimental_rerun()

# 학생 추가
st.markdown("---")
st.write("### 학생 추가")
with st.form("add_student"):
    new_name = st.text_input("학생 이름 입력")
    submitted = st.form_submit_button("추가")
    if submitted and new_name.strip():
        new_student = {"id": str(datetime.datetime.now().timestamp()), "name": new_name.strip()}
        students.append(new_student)
        save_students(students)
        st.success(f"학생 '{new_name}' 이(가) 추가되었습니다.")
        st.experimental_rerun()
