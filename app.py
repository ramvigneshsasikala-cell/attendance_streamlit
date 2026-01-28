import streamlit as st
import pandas as pd
import os
from datetime import date

STUDENTS_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"

if not os.path.exists(STUDENTS_FILE):
    pd.DataFrame(columns=["Student Name"]).to_csv(STUDENTS_FILE, index=False)

if not os.path.exists(ATTENDANCE_FILE):
    pd.DataFrame(columns=["Date", "Student Name", "Status"]).to_csv(ATTENDANCE_FILE, index=False)

students_df = pd.read_csv(STUDENTS_FILE)
attendance_df = pd.read_csv(ATTENDANCE_FILE)

st.set_page_config(page_title="Attendance System", layout="centered")
st.title("📋 Attendance Maintenance System")

menu = st.sidebar.radio("Menu", ["Add Student", "Mark Attendance", "View Attendance"])

if menu == "Add Student":
    st.header("➕ Add Student")

    new_student = st.text_input("Student Name")

    if st.button("Add"):
        if new_student.strip() == "":
            st.warning("Name cannot be empty")
        elif new_student in students_df["Student Name"].values:
            st.warning("Student already exists")
        else:
            students_df.loc[len(students_df)] = [new_student]
            students_df.to_csv(STUDENTS_FILE, index=False)
            st.success(f"{new_student} added successfully")

elif menu == "Mark Attendance":
    st.header("✅ Mark Attendance")

    if students_df.empty:
        st.warning("No students added yet")
    else:
        selected_date = st.date_input("Select Date", date.today())
        attendance_data = []

        for student in students_df["Student Name"]:
            status = st.radio(
                student,
                ["Present", "Absent"],
                horizontal=True,
                key=student
            )
            attendance_data.append([selected_date, student, status])

        if st.button("Submit Attendance"):
            new_entries = pd.DataFrame(
                attendance_data,
                columns=["Date", "Student Name", "Status"]
            )

            attendance_df = pd.concat([attendance_df, new_entries], ignore_index=True)
            attendance_df.to_csv(ATTENDANCE_FILE, index=False)

            st.success("Attendance recorded")

elif menu == "View Attendance":
    st.header("📊 Attendance Records")

    if attendance_df.empty:
        st.info("No attendance records yet")
    else:
        selected_student = st.selectbox(
            "Filter by Student (optional)",
            ["All"] + students_df["Student Name"].tolist()
        )

        if selected_student != "All":
            filtered_df = attendance_df[
                attendance_df["Student Name"] == selected_student
            ]
        else:
            filtered_df = attendance_df

        st.dataframe(filtered_df, use_container_width=True)