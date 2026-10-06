import streamlit as st

from backend import (
    initialize_database,
    get_scheme_recommendation
)

# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

initialize_database()

# -----------------------------------
# CUSTOM PAGE STYLING
# -----------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef4ff, #f7f0ff);
}

h1 {
    color: #4f46e5;
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}

h2, h3 {
    color: #3730a3;
}

p, label {
    color: #26324a;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
    border: 1px solid #c7d2fe;
    background-color: #ffffff;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: none;
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    font-weight: 600;
    padding: 10px 20px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #4338ca, #6d28d9);
    transform: scale(1.02);
}

.stSuccess {
    border-radius: 10px;
}

.stInfo {
    border-radius: 10px;
}

.stProgress > div > div {
    background-color: #6366f1;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_state" not in st.session_state:
    st.session_state.user_state = "Telangana"

# NEW: CATEGORY
if "user_category" not in st.session_state:
    st.session_state.user_category = "SC"

if "user_age" not in st.session_state:
    st.session_state.user_age = 20

if "user_occupation" not in st.session_state:
    st.session_state.user_occupation = "Student"

if "user_education" not in st.session_state:
    st.session_state.user_education = "Not Applicable"

if "user_income" not in st.session_state:
    st.session_state.user_income = 100000

if "user_requirement" not in st.session_state:
    st.session_state.user_requirement = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "schemes" not in st.session_state:
    st.session_state.schemes = []

# -----------------------------------
# WELCOME MESSAGE
# -----------------------------------

# -----------------------------------
# WELCOME MESSAGE
# -----------------------------------

if st.session_state.step == 1:

    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #7c3aed);
                padding: 30px;
                border-radius: 20px;
                text-align: center;
                margin-bottom: 25px;">

    <h1 style="color: white; font-size: 42px; margin-bottom: 10px;">
    🌟 Welcome to SCHEME AI
    </h1>

    <p style="color: white; font-size: 18px; margin: 5px;">
    Your Intelligent Government Scheme Assistant
    </p>

    <p style="color: #ede9fe; font-size: 15px; margin-top: 12px;">
    Find suitable Telangana Government Schemes based on your needs and profile.
    </p>

    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# USER INFORMATION
# -----------------------------------

# -----------------------------------
# USER INFORMATION
# -----------------------------------

if st.session_state.step != 9:
    st.header("👤 Tell Us About You")

# ===================================
# STEP 1 - NAME
# ===================================

if st.session_state.step == 1:

    st.subheader("What is your name?")

    st.text_input(
        "Name",
        key="user_name"
    )

    if st.button("Next →", key="next_name"):

        if st.session_state.user_name.strip() == "":
            st.warning("Please enter your name.")
        else:
            st.session_state.step = 2
            st.rerun()

# ===================================
# STEP 2 - STATE
# ===================================

elif st.session_state.step == 2:

    st.subheader("Which state are you from?")

    st.selectbox(
        "Select your State",
        [
            "Telangana",
            "Andhra Pradesh",
            "Karnataka",
            "Tamil Nadu",
            "Maharashtra",
            "Other"
        ],
        key="user_state"
    )

    if st.session_state.user_state != "Telangana":
        st.warning(
            "⚠️ This application is currently available only "
            "for residents of Telangana."
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", key="back_state"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next →", key="next_state"):

            if st.session_state.user_state != "Telangana":
                st.error(
                    "❌ Sorry! SCHEME AI is currently available "
                    "only for Telangana residents."
                )
            else:
                st.session_state.step = 3
                st.rerun()

# ===================================
# STEP 3 - CATEGORY
# ===================================

elif st.session_state.step == 3:

    st.subheader("What is your category / community?")

    st.selectbox(
        "Select your Category",
        [
            "SC",
            "ST",
            "BC-A",
            "BC-B",
            "BC-C",
            "BC-D",
            "BC-E",
            "Minority",
            "OC / General"
        ],
        key="user_category"
    )

    st.info(
        "Please select the category mentioned in your official "
        "community/caste certificate, if applicable."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", key="back_category"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Next →", key="next_category"):
            st.session_state.step = 4
            st.rerun()

# ===================================
# STEP 4 - AGE
# ===================================

elif st.session_state.step == 4:

    st.subheader("What is your age?")

    st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        key="user_age"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", key="back_age"):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("Next →", key="next_age"):
            st.session_state.step = 5
            st.rerun()

# ===================================
# STEP 5 - OCCUPATION
# ===================================

elif st.session_state.step == 5:

    st.subheader("What is your occupation?")

    st.selectbox(
        "Occupation",
        [
            "Student",
            "Farmer",
            "Employee",
            "Business",
            "Unemployed",
            "Other"
        ],
        key="user_occupation"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", key="back_occupation"):
            st.session_state.step = 4
            st.rerun()

    with col2:
        if st.button("Next →", key="next_occupation"):
            st.session_state.step = 6
            st.rerun()

# ===================================
# STEP 6 - EDUCATION
# ===================================

elif st.session_state.step == 6:

    if st.session_state.user_occupation == "Student":

        st.subheader("What is your education level?")

        st.selectbox(
            "Education",
            [
                "School",
                "Intermediate",
                "Diploma",
                "Undergraduate",
                "Postgraduate",
                "Other"
            ],
            key="user_education"
        )

    else:

        st.session_state.user_education = "Not Applicable"

        st.info(
            "Education level is not required for your selected occupation."
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", key="back_education"):
            st.session_state.step = 5
            st.rerun()

    with col2:
        if st.button("Next →", key="next_education"):
            st.session_state.step = 7
            st.rerun()

# ===================================
# STEP 7 - INCOME
# ===================================

elif st.session_state.step == 7:

    st.subheader("What is your annual income?")

    st.number_input(
        "Annual Income (₹)",
        min_value=0,
        step=10000,
        key="user_income"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", key="back_income"):
            st.session_state.step = 6
            st.rerun()

    with col2:
        if st.button("Next →", key="next_income"):
            st.session_state.step = 8
            st.rerun()

# ===================================
# STEP 8 - REQUIREMENT
# ===================================

elif st.session_state.step == 8:

    st.subheader("What kind of help are you looking for?")

    st.text_area(
        "Your Requirement",
        placeholder=(
            "Example: I need financial assistance "
            "for my college education."
        ),
        height=120,
        key="user_requirement"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", key="back_requirement"):
            st.session_state.step = 7
            st.rerun()

    with col2:

        if st.button(
            "🔍 Find Suitable Schemes",
            key="find_schemes"
        ):

            if st.session_state.user_requirement.strip() == "":
                st.warning(
                    "Please enter your requirement."
                )

            else:

                # USER INFORMATION SENT TO RAG
                user_query = f"""
Name: {st.session_state.user_name}

State: {st.session_state.user_state}

Category / Community: {st.session_state.user_category}

Age: {st.session_state.user_age}

Occupation:
{st.session_state.user_occupation}

Education:
{st.session_state.user_education}

Annual Income:
₹{st.session_state.user_income}

Requirement:
{st.session_state.user_requirement}
"""

                with st.spinner(
                    "SCHEME AI is finding suitable schemes..."
                ):

                    answer, schemes = get_scheme_recommendation(
                        user_query
                    )

                st.session_state.answer = answer
                st.session_state.schemes = schemes
                st.session_state.step = 9

                st.rerun()

# ===================================
# STEP 9 - RESULTS
# ===================================

elif st.session_state.step == 9:

    st.success("🎯 Suitable Government Scheme")

    st.markdown(
        st.session_state.answer
    )

    st.divider()

    if st.button(
        "🔄 Start Again",
        key="restart"
    ):

        st.session_state.step = 1
        st.session_state.user_name = ""
        st.session_state.user_state = "Telangana"
        st.session_state.user_category = "SC"
        st.session_state.user_age = 20
        st.session_state.user_occupation = "Student"
        st.session_state.user_education = "Not Applicable"
        st.session_state.user_income = 100000
        st.session_state.user_requirement = ""
        st.session_state.answer = ""
        st.session_state.schemes = []

        st.rerun()