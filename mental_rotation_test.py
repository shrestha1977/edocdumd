import streamlit as st
import random
import time

# ---------------------------
# CONFIGURATION
# ---------------------------

image_sets = [
    ("images/target1.png", "images/correct1.png", "images/wrong1.png", 45),
    ("images/target2.png", "images/correct2.png", "images/wrong2.png", 90),
    ("images/target3.png", "images/correct3.png", "images/wrong3.png", 45),
    ("images/target4.png", "images/correct4.png", "images/wrong4.png", 90),
    ("images/target5.png", "images/correct5.png", "images/wrong5.png", 90),
    ("images/target6.png", "images/correct6.png", "images/wrong6.png", 90),
    ("images/target7.png", "images/correct7.png", "images/wrong7.png", 90),
    ("images/target8.png", "images/correct8.png", "images/wrong8.png", 0),
    ("images/target9.png", "images/correct9.png", "images/wrong9.png", 45),
    ("images/target10.png", "images/correct10.png", "images/wrong10.png", 90),
    ("images/target11.png", "images/correct11.png", "images/wrong11.png", 135),
    ("images/target12.png", "images/correct12.png", "images/wrong12.png", 45),
    ("images/target13.png", "images/correct13.png", "images/wrong13.png", 0),
    ("images/target14.png", "images/correct14.png", "images/wrong14.png", 45),
    ("images/target15.png", "images/correct15.png", "images/wrong15.png", 90),
]

TOTAL_QUESTIONS = 15
QUESTION_TIME_LIMIT = 15


# ---------------------------
# ANSWER HANDLER
# ---------------------------

def handle_answer(option):
    rt = time.time() - st.session_state.mrt_question_start

    st.session_state.mrt_results.append({
        "correct": option["correct"],
        "time": rt,
        "angle": st.session_state.current_angle,
        "timed_out": False
    })

    st.session_state.mrt_question += 1
    st.session_state.mrt_question_start = None
    st.session_state.mrt_options = None
    st.rerun()


# ---------------------------
# MAIN ENGINE
# ---------------------------

def run_mental_rotation_test():

    st.title("🧠 Mental Rotation Task")

    # ---------- SESSION INIT ----------

    if "mrt_started" not in st.session_state:
        st.session_state.mrt_started = False

    # ---------- INSTRUCTION SCREEN ----------

    if not st.session_state.mrt_started:

        st.subheader("📋 Instructions")

        st.markdown("""
You will see a **reference image** and two options (A and B).

- Select the option that is the **correct rotated version** of the reference image.
- There are **15 questions** in total.
- Each question has a **15 second** time limit.
- Try to respond **as quickly and accurately as possible**.

### 🧪 Sample Question Format
""")

        sample_target = "images/s1.png"
        sample_option_a = "images/s2.png"
        sample_option_b = "images/s3.png"

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image(sample_target, caption="Reference Image", width=150)

        colA, colB = st.columns(2)

        with colA:
            st.image(sample_option_a, caption="Option A", width=130)

        with colB:
            st.image(sample_option_b, caption="Option B", width=130)

        st.markdown("""
👉 Choose the option that matches the reference image after rotation.

### ⚖️ Guidance

- Focus on **shape**, not orientation.
- Only **one option** is correct.
- Respond quickly and accurately.

### 🧩 Cognitive Domains Assessed

- Spatial Ability
- Mental Rotation Skills
- Visual-Spatial Processing
- Working Memory
""")

        st.markdown("---")

        if st.button("Start Mental Rotation Test", key="start_mrt"):
            st.session_state.mrt_started = True
            st.rerun()

        return

    # ---------- INITIALIZE TEST ----------

    if "mrt_initialized" not in st.session_state:

        st.session_state.mrt_initialized = True
        st.session_state.mrt_question = 0
        st.session_state.mrt_results = []

        st.session_state.mrt_randomized = random.sample(
            range(len(image_sets)),
            TOTAL_QUESTIONS
        )

        st.session_state.mrt_question_start = None
        st.session_state.mrt_options = None
        st.session_state.current_angle = 0

    # ---------- COMPLETION ----------

    if st.session_state.mrt_question >= TOTAL_QUESTIONS:

        correct = sum(r["correct"] for r in st.session_state.mrt_results)

        accuracy = (correct / TOTAL_QUESTIONS) * 100

        avg_time = (
            sum(r["time"] for r in st.session_state.mrt_results)
            / TOTAL_QUESTIONS
        )

        timed_out = sum(
            r["timed_out"] for r in st.session_state.mrt_results
        )

        st.markdown("## 🧠 Task Completed")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        col1.metric("Accuracy", f"{accuracy:.1f}%")
        col2.metric("Avg Reaction Time", f"{avg_time:.2f}s")
        col3.metric("Timed Out", f"{timed_out}/{TOTAL_QUESTIONS}")

        if st.button(
            "Continue",
            type="primary",
            use_container_width=True
        ):

            for key in list(st.session_state.keys()):
                if key.startswith("mrt_"):
                    del st.session_state[key]

            st.session_state.current_stage = "final"
            st.rerun()

        return

    # ---------- QUESTION TIMER ----------

    if st.session_state.mrt_question_start is None:
        st.session_state.mrt_question_start = time.time()

    elapsed = time.time() - st.session_state.mrt_question_start

    remaining = max(
        0.0,
        QUESTION_TIME_LIMIT - elapsed
    )

    if remaining <= 0:

        st.session_state.mrt_results.append({
            "correct": False,
            "time": QUESTION_TIME_LIMIT,
            "angle": st.session_state.current_angle,
            "timed_out": True
        })

        st.session_state.mrt_question += 1
        st.session_state.mrt_question_start = None
        st.session_state.mrt_options = None

        st.rerun()

        return

      # ---------- QUESTION UI ----------

    st.markdown(
        f"**Question {st.session_state.mrt_question + 1} of {TOTAL_QUESTIONS}**"
    )

    # Timer display
    timer_color = "🔴" if remaining < 5 else "🟡" if remaining < 10 else "🟢"

    st.markdown(f"### {timer_color} Time Remaining: {remaining:.1f}s")

    st.progress(
        remaining / QUESTION_TIME_LIMIT,
        text=f"⏳ {remaining:.1f}s left"
    )

    # Current trial
    trial_idx = st.session_state.mrt_randomized[
        st.session_state.mrt_question
    ]

    target_img, correct_img, wrong_img, angle = image_sets[trial_idx]
    st.session_state.current_angle = angle

    # Randomize option positions once per question
    if st.session_state.mrt_options is None:

        options = [
            {"img": correct_img, "correct": True},
            {"img": wrong_img, "correct": False},
        ]

        random.shuffle(options)
        st.session_state.mrt_options = options

    else:
        options = st.session_state.mrt_options

    st.markdown("---")

    # Reference image (centered)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(target_img, width=180)

    st.markdown("---")
    st.markdown("### 👆 Click on the correct rotated version:")

    # Option images
    colA, colB = st.columns(2)

    with colA:
        st.image(options[0]["img"], width=150)

        if st.button(
            "Option A",
            key=f"mrt_a_{st.session_state.mrt_question}"
        ):
            handle_answer(options[0])

    with colB:
        st.image(options[1]["img"], width=150)

        if st.button(
            "Option B",
            key=f"mrt_b_{st.session_state.mrt_question}"
        ):
            handle_answer(options[1])

    # ---------- AUTO REFRESH ----------

    if st.session_state.mrt_question < TOTAL_QUESTIONS:
        time.sleep(0.1)
        st.rerun()
