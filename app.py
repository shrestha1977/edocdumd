import streamlit as st
import time

from math_test import run_math_test
from stroop_test import run_stroop_test
from mental_rotation_test import run_mental_rotation_test

st.set_page_config(page_title="Cognitive Assessment Tool", layout="centered")


# =====================================================
# CLOUD SAFE SESSION INITIALIZATION
# =====================================================

if "current_stage" not in st.session_state:
    st.session_state.current_stage = "consent"

if "stage_lock" not in st.session_state:
    st.session_state.stage_lock = True

if "heartbeat" not in st.session_state:
    st.session_state.heartbeat = time.time()


# =====================================================
# CONSENT PAGE
# =====================================================

if st.session_state.current_stage == "consent":

    st.title("Cognitive Assessment Study")

    st.markdown("""
    ### Digital Consent

    - This assessment is conducted solely for academic research purposes.
    - The data collected will be used only for analysis and study related to cognitive performance.
    - No personally identifiable information will be shared with third parties.
    - Your responses will remain confidential and anonymous.
    - Participation in this assessment is voluntary.
    - You may choose to exit the test at any time without any consequences.
    """)

    st.subheader("Eligibility Confirmation")

    c1 = st.checkbox("I confirm that I have passed 12th standard.")
    c2 = st.checkbox("I confirm that I am computer literate and can operate a computer independently.")
    consent = st.checkbox(
        "I agree to participate and allow my data to be used for academic research purposes."
    )

    if c1 and c2 and consent:
        if st.button("Start Test", key="start_test_btn"):
            st.session_state.current_stage = "demographics"
            st.rerun()
    else:
        st.warning("Please confirm all the above statements to continue.")


# =====================================================
# DEMOGRAPHICS PAGE
# =====================================================

if st.session_state.current_stage == "demographics":

    st.markdown("### Baseline & Demographic Information")

    name = st.text_input("Name", key="name")
    age = st.selectbox(
        "Age Category",
        ["18-25", "26-35", "36-45", "46-55", "56+"],
        key="age",
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        key="gender",
    )

    hometown = st.text_input("Home Town", key="hometown")
    current_city = st.text_input("Current City", key="current_city")

    mother_language = st.selectbox(
        "Mother Language",
        [
            "Hindi",
            "English",
            "Bengali",
            "Tamil",
            "Telugu",
            "Marathi",
            "Gujarati",
            "Kannada",
            "Malayalam",
            "Other",
        ],
        key="mother_language",
    )

    academic = st.selectbox(
        "Academic Qualification",
        [
            "Pursuing UG",
            "Pursuing PG",
            "Completed UG",
            "Completed PG",
        ],
        key="academic",
    )

    service = st.selectbox(
        "Service Status",
        [
            "Employed",
            "Not Employed",
            "Retired",
        ],
        key="service",
    )

    handedness = st.selectbox(
        "Handedness",
        [
            "Right",
            "Left",
            "Ambidextrous",
        ],
        key="handedness",
    )

    device = st.selectbox(
        "Device Used",
        [
            "Laptop",
            "Desktop",
            "Mobile",
            "Tablet",
        ],
        key="device",
    )

    vision = st.selectbox(
        "Vision Status",
        [
            "Normal",
            "Corrected to Normal",
        ],
        key="vision",
    )

    prior_exposure = st.selectbox(
        "Prior exposure to any cognitive test recently?",
        [
            "Yes",
            "No",
        ],
        key="prior_exposure",
    )

    if st.button("Continue", key="demo_continue_btn"):

        if name.strip() == "":
            st.warning("Please enter your name.")
            st.stop()

        st.session_state.demographics = {
            "name": name,
            "age": age,
            "gender": gender,
            "hometown": hometown,
            "current_city": current_city,
            "mother_language": mother_language,
            "academic": academic,
            "service": service,
            "handedness": handedness,
            "device": device,
            "vision": vision,
            "prior_exposure": prior_exposure,
        }

        st.session_state.current_stage = "instructions"
        st.rerun()


# =====================================================
# INSTRUCTION SCREEN
# =====================================================

elif st.session_state.current_stage == "instructions":

    st.title("Instructions")

    st.markdown("""
    You will complete **three cognitive tasks** as part of this assessment:

    ### 🧠 Tasks Included
    1. **Numerical Ability Test**
    2. **Stroop Test**
    3. **Mental Rotation Task**

    ---

    ### ⏱️ Guidelines
    - Respond **as quickly and accurately as possible**.
    - Each task is **time-sensitive**, so avoid delays.
    - Read each question carefully before answering.
    - Do not use any external aids (calculators, pen, paper, etc.) during the test.

    ---

    ### ⚠️ Important Notes
    - Ensure you are in a **quiet and distraction-free environment**.
    - Do not refresh or close the browser during the test.
    - Once started, the test should be completed in one session.

    ---

    Click the button below when you are ready to begin.
    """)

    if st.button("Continue to Test"):

        st.session_state.stage_lock = False
        st.session_state.current_stage = "math"

        st.rerun()


# =====================================================
# TEST ROUTER
# =====================================================

elif st.session_state.current_stage == "math":
    run_math_test()

elif st.session_state.current_stage == "stroop":
    run_stroop_test()

elif st.session_state.current_stage == "mental":
    run_mental_rotation_test()


# =====================================================
# FINAL SCREEN
# =====================================================

elif st.session_state.current_stage == "final":

    st.title("Thank You for Participating!")

    st.markdown("""
    Your participation is greatly appreciated.

    This data will be used strictly for academic purposes.
    """)

    st.success("You may now close this window.")
