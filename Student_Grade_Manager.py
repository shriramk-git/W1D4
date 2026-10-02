import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 0.4rem;
}

/* ---------------- HEADER ---------------- */

.main-header {
    background: linear-gradient(135deg, #173B8F, #2563EB);
    padding: 18px 28px;
    border-radius: 16px;
    color: white;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.18);
}

.main-header h1 {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
}

.main-header p {
    margin: 4px 0 0 0;
    font-size: 14px;
    opacity: 0.9;
}

/* ---------------- SECTION TITLE ---------------- */

.section-title {
    font-size: 17px;
    font-weight: 700;
    color: #1E293B;
    margin-top: 10px;
    margin-bottom: 6px;
}

/* ---------------- SUBJECT CARDS ---------------- */

.subject-card {
    background: white;
    border-radius: 10px;
    padding: 8px;
    border: 1px solid #E2E8F0;
    text-align: center;
    margin-bottom: 4px;
}

.subject-name {
    font-size: 15px;
    font-weight: 700;
    color: #1E3A8A;
}

/* ---------------- METRIC CARDS ---------------- */

.metric-card {
    background: white;
    padding: 10px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

.metric-title {
    color: #64748B;
    font-size: 11px;
    font-weight: 700;
}

.metric-value {
    color: #1E293B;
    font-size: 23px;
    font-weight: 700;
    margin-top: 2px;
}

/* ---------------- FEEDBACK ---------------- */

.feedback {
    padding: 12px 14px;
    border-radius: 12px;
    font-size: 13px;
    line-height: 1.5;
    margin-top: 4px;
}

.excellent {
    background-color: #ECFDF5;
    border-left: 5px solid #10B981;
    color: #065F46;
}

.good {
    background-color: #EFF6FF;
    border-left: 5px solid #3B82F6;
    color: #1E40AF;
}

.average {
    background-color: #FFF7ED;
    border-left: 5px solid #F59E0B;
    color: #92400E;
}

.low {
    background-color: #FEF2F2;
    border-left: 5px solid #EF4444;
    color: #991B1B;
}

/* ---------------- BUTTONS ---------------- */

div.stButton > button {
    border-radius: 9px;
    font-weight: 700;
    min-height: 40px;
    border: 1px solid #CBD5E1;
}

/* Calculate button */
.calculate-button button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
}

/* New student button */
.new-student-button button {
    background-color: white !important;
    color: #DC2626 !important;
    border: 1px solid #FCA5A5 !important;
}

/* ---------------- INPUT ---------------- */

div[data-testid="stNumberInput"] input {
    text-align: center;
    font-weight: 700;
}

/* ---------------- FOOTER ---------------- */

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 11px;
    margin-top: 5px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SUBJECTS
# =========================================================

SUBJECTS = [
    "Maths",
    "Science",
    "Tamil",
    "Sports",
    "Arts"
]


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "calculated" not in st.session_state:
    st.session_state.calculated = False

for subject in SUBJECTS:

    key = f"marks_{subject}"

    if key not in st.session_state:
        st.session_state[key] = 0


# =========================================================
# CLEAR STUDENT
# =========================================================

def clear_student():

    st.session_state.student_name = ""

    for subject in SUBJECTS:
        st.session_state[f"marks_{subject}"] = 0

    st.session_state.calculated = False


# =========================================================
# CALCULATE
# =========================================================

def calculate_grade():

    st.session_state.calculated = True


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">
    <h1>🎓 Student Grade Manager</h1>
    <p>Enter student marks and calculate academic performance instantly.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# STUDENT NAME + NEW STUDENT
# =========================================================

name_col, button_col = st.columns([4, 1])

with name_col:

    st.text_input(
        "👨‍🎓 Student Name",
        key="student_name",
        placeholder="Enter student's name"
    )


with button_col:

    st.write("")

    st.markdown(
        '<div class="new-student-button">',
        unsafe_allow_html=True
    )

    st.button(
        "🔄 New Student",
        use_container_width=True,
        on_click=clear_student
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# ENTER MARKS
# =========================================================

st.markdown(
    '<div class="section-title">📝 Enter Marks — Out of 100</div>',
    unsafe_allow_html=True
)

subject_columns = st.columns(5)

for index, subject in enumerate(SUBJECTS):

    with subject_columns[index]:

        st.markdown(
            f"""
            <div class="subject-card">
                <div class="subject-name">{subject}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.number_input(
            f"{subject} marks",
            min_value=0,
            max_value=100,
            step=1,
            key=f"marks_{subject}",
            label_visibility="collapsed"
        )


# =========================================================
# CALCULATE BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

calculate_col, spacer_col = st.columns([1, 4])

with calculate_col:

    st.markdown(
        '<div class="calculate-button">',
        unsafe_allow_html=True
    )

    st.button(
        "🎯 Calculate Grade",
        use_container_width=True,
        on_click=calculate_grade
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# ONLY SHOW RESULTS AFTER CALCULATE
# =========================================================

if st.session_state.calculated:

    # =====================================================
    # VALIDATE STUDENT NAME
    # =====================================================

    if not st.session_state.student_name.strip():

        st.warning(
            "Please enter the student's name before calculating the grade."
        )

    else:

        # =================================================
        # CREATE DATAFRAME
        # =================================================

        df = pd.DataFrame({
            "Subject": SUBJECTS,
            "Marks": [
                st.session_state[f"marks_{subject}"]
                for subject in SUBJECTS
            ]
        })

        # =================================================
        # PASS / FAIL
        # =================================================

        # Below 40 = FAIL
        # 40 or above = PASS

        df["Result"] = df["Marks"].apply(
            lambda mark: "FAIL" if mark < 40 else "PASS"
        )

        # =================================================
        # PERFORMANCE
        # =================================================

        df["Performance"] = df["Marks"].apply(
            lambda mark:
                "Excellent" if mark >= 80
                else "Good" if mark >= 60
                else "Needs Improvement" if mark >= 40
                else "Needs Attention"
        )

        # =================================================
        # CALCULATIONS
        # =================================================

        average = df["Marks"].mean()
        highest = df["Marks"].max()
        lowest = df["Marks"].min()

        pass_count = int(
            (df["Marks"] >= 40).sum()
        )

        fail_count = int(
            (df["Marks"] < 40).sum()
        )

        # =================================================
        # OVERALL PERFORMANCE
        # =================================================

        if average >= 80:

            performance = "Excellent"
            feedback_class = "excellent"
            feedback_title = "🌟 Excellent work!"

            feedback_text = (
                "Outstanding overall performance. Keep up the "
                "excellent work and continue challenging yourself."
            )

        elif average >= 60:

            performance = "Good"
            feedback_class = "good"
            feedback_title = "👍 Good performance!"

            feedback_text = (
                "A good overall result. Regular revision and "
                "practice can help achieve even better marks."
            )

        elif average >= 40:

            performance = "Improve"
            feedback_class = "average"
            feedback_title = "📖 Keep improving!"

            feedback_text = (
                "More revision and consistent practice can improve "
                "the results. Focus particularly on subjects with "
                "lower marks."
            )

        else:

            performance = "Attention"
            feedback_class = "low"
            feedback_title = "💪 More study recommended!"

            feedback_text = (
                "Create a regular study routine, practise frequently "
                "and ask teachers for help with difficult topics."
            )

        # =================================================
        # PERFORMANCE SUMMARY
        # =================================================

        st.markdown(
            '<div class="section-title">📊 Performance Summary</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        metrics = [
            (col1, "AVERAGE", f"{average:.1f}"),
            (col2, "HIGHEST", f"{highest}"),
            (col3, "LOWEST", f"{lowest}"),
            (col4, "PASS / FAIL", f"{pass_count} / {fail_count}")
        ]

        for column, title, value in metrics:

            with column:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-title">{title}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # =================================================
        # CHART + FEEDBACK
        # =================================================

        chart_col, feedback_col = st.columns([1.3, 1])

        # =================================================
        # CHART
        # =================================================

        with chart_col:

            st.markdown(
                '<div class="section-title">📈 Subject Performance</div>',
                unsafe_allow_html=True
            )

            # Red = FAIL
            # Green = PASS

            fig = px.bar(
                df,
                x="Subject",
                y="Marks",
                text="Marks",
                range_y=[0, 115],
                color="Result",
                color_discrete_map={
                    "FAIL": "#EF4444",
                    "PASS": "#10B981"
                },
                category_orders={
                    "Subject": SUBJECTS,
                    "Result": ["FAIL", "PASS"]
                }
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            fig.update_layout(
                height=270,
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=False,
                xaxis_title="",
                yaxis_title="Marks",
                yaxis=dict(
                    range=[0, 115],
                    dtick=20,
                    gridcolor="#E2E8F0"
                ),
                font=dict(
                    color="#334155",
                    size=11
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        # =================================================
        # FEEDBACK
        # =================================================

        with feedback_col:

            st.markdown(
                '<div class="section-title">💬 Student Feedback</div>',
                unsafe_allow_html=True
            )

            display_name = (
                st.session_state.student_name.strip()
            )

            st.markdown(
                f"""
                <div class="feedback {feedback_class}">
                    <strong>{feedback_title}</strong><br>
                    {display_name}: average {average:.1f}/100.<br>
                    {feedback_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            # =============================================
            # SUBJECT RESULTS
            # =============================================

            st.markdown("**📋 Subject Results**")

            for _, row in df.iterrows():

                if row["Marks"] < 40:

                    st.markdown(
                        f"🔴 **{row['Subject']}** — "
                        f"{row['Marks']}/100 · **FAIL**"
                    )

                else:

                    st.markdown(
                        f"🟢 **{row['Subject']}** — "
                        f"{row['Marks']}/100 · **PASS**"
                    )


# =========================================================
# HOW TO USE
# =========================================================

st.markdown("""
<div style="
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 8px 14px;
    margin-top: 8px;
    color: #475569;
    font-size: 11px;
    line-height: 1.7;
">

<b style="color:#173B8F;">📘 How to use</b><br>

1. Enter the student's name and marks for Maths, Science, Tamil, Sports and Arts.<br>

2. Click <b>🎯 Calculate Grade</b> to see the results, chart and feedback.<br>

3. Click <b>🔄 New Student</b> to clear everything and enter the next student.

</div>
""", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    Student Grade Manager • Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)