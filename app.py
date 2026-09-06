import streamlit as st

from college_data import (
    faculty,
    rooms,
    assignments,
    contacts,
    timetable,
    attendance,
    notices
)

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="College Copilot",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

if "attendance_data" not in st.session_state:
    st.session_state.attendance_data = attendance.copy()

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ==================================================
       MAIN APP
    ================================================== */

    .stApp {
        background: #FFFDF8;
    }

    .main {
        background: #FFFDF8;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* ==================================================
       HEADINGS
    ================================================== */

    h1 {
        color: #46354D !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #46354D !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #46354D !important;
        font-weight: 700 !important;
    }

    p {
        color: #65556B;
    }

    /* ==================================================
       SIDEBAR
    ================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #E7D8F5 0%,
            #F2E7F7 50%,
            #FFFDF8 100%
        );

        border-right: 1px solid #DCC8EA;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #46354D !important;
    }

    section[data-testid="stSidebar"] p {
        color: #65556B;
    }

    /* ==================================================
       SIDEBAR NAVIGATION
    ================================================== */

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 7px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 13px;
        padding: 8px 12px;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: #F7C6D9;
        transform: translateX(3px);
    }

    /* ==================================================
       CARDS
    ================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #E7D8F5;
        border-radius: 20px;
        box-shadow: 0 5px 18px rgba(70, 53, 77, 0.08);
        padding: 8px;
        transition: all 0.2s ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(70, 53, 77, 0.12);
    }

    /* ==================================================
       BUTTONS
    ================================================== */

    .stButton > button {
        background: #F7C6D9;
        color: #46354D;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        padding: 10px 18px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #EFB0C9;
        color: #46354D;
        transform: translateY(-2px);
    }

    /* ==================================================
       TEXT INPUT
    ================================================== */

    .stTextInput input {
        background: #FFFFFF !important;
        border: 2px solid #E7D8F5 !important;
        border-radius: 14px !important;
        color: #46354D !important;
        padding: 12px !important;
    }

    .stTextInput input:focus {
        border-color: #F7C6D9 !important;
        box-shadow: 0 0 0 2px rgba(247, 198, 217, 0.25) !important;
    }

    /* ==================================================
       PROGRESS BAR
    ================================================== */

    .stProgress > div > div > div > div {
        background: #B9D69A;
    }

    /* ==================================================
       METRICS
    ================================================== */

    [data-testid="stMetricValue"] {
        color: #46354D;
        font-weight: 800;
    }

    [data-testid="stMetricLabel"] {
        color: #8C7894;
    }

    /* ==================================================
       ALERT BOXES
    ================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid #E7D8F5;
    }

    /* ==================================================
       DIVIDERS
    ================================================== */

    hr {
        border-color: #E7D8F5;
    }

    /* ==================================================
       FOOTER
    ================================================== */

    .footer-text {
        text-align: center;
        color: #8C7894;
        font-size: 14px;
        padding: 25px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_overall_attendance():

    total_attended = 0
    total_classes = 0

    for subject, data in st.session_state.attendance_data.items():

        if isinstance(data, dict):

            try:
                total_attended += int(
                    data.get("attended", 0)
                )

                total_classes += int(
                    data.get("total", 0)
                )

            except (ValueError, TypeError):
                pass

    if total_classes == 0:
        return 0.0

    return (
        total_attended /
        total_classes
    ) * 100


def get_next_class():

    if not timetable:
        return None

    if isinstance(timetable, list):

        if len(timetable) > 0:
            return timetable[0]

    if isinstance(timetable, dict):

        for day, classes in timetable.items():

            if isinstance(classes, list):

                if len(classes) > 0:
                    return classes[0]

    return None


def get_value(item, keys, default=""):

    if not isinstance(item, dict):
        return default

    for key in keys:

        if key in item:
            return item[key]

    return default


def display_data(data):

    if isinstance(data, list):

        for item in data:

            if isinstance(item, dict):

                with st.container(border=True):

                    for key, value in item.items():

                        label = str(key).replace(
                            "_",
                            " "
                        ).title()

                        st.write(
                            f"**{label}:** {value}"
                        )

            else:

                st.write(
                    f"• {item}"
                )

    elif isinstance(data, dict):

        for key, value in data.items():

            with st.container(border=True):

                title = str(key).replace(
                    "_",
                    " "
                ).title()

                st.markdown(
                    f"### {title}"
                )

                if isinstance(value, dict):

                    for sub_key, sub_value in value.items():

                        label = str(
                            sub_key
                        ).replace(
                            "_",
                            " "
                        ).title()

                        st.write(
                            f"**{label}:** {sub_value}"
                        )

                elif isinstance(value, list):

                    for item in value:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.write(value)

    else:

        st.write(data)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🎓 College Copilot")

st.sidebar.caption(
    "Your smart campus companion"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "✨ My Day",
        "📅 Timetable",
        "📝 Assignments",
        "📊 Attendance",
        "📢 Notices",
        "👩‍🏫 Faculty",
        "🏫 Campus"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "💗 Tip\n\n"
    "Use College Copilot to quickly find "
    "classes, faculty, rooms, assignments "
    "and attendance."
)

# ==================================================
# DASHBOARD
# ==================================================

if page == "🏠 Dashboard":

    st.title("Good morning 👋")

    st.write(
        "Your college information, schedule and tasks — all in one place."
    )

    st.header("🏠 Dashboard")

    next_class = get_next_class()

    # --------------------------------------------------
    # NEXT CLASS
    # --------------------------------------------------

    if next_class:

        class_subject = get_value(
            next_class,
            ["subject", "name", "course"],
            "No class"
        )

        class_time = get_value(
            next_class,
            ["time", "start_time"],
            ""
        )

        class_room = get_value(
            next_class,
            ["room", "location", "venue"],
            ""
        )

    else:

        class_subject = "No more classes"
        class_time = ""
        class_room = ""

    # --------------------------------------------------
    # NEXT ASSIGNMENT
    # --------------------------------------------------

    next_assignment = None

    if isinstance(assignments, list):

        if len(assignments) > 0:
            next_assignment = assignments[0]

    # --------------------------------------------------
    # ATTENDANCE
    # --------------------------------------------------

    overall_attendance = get_overall_attendance()

    total_attended = 0
    total_classes = 0

    for subject, data in st.session_state.attendance_data.items():

        if isinstance(data, dict):

            try:

                total_attended += int(
                    data.get("attended", 0)
                )

                total_classes += int(
                    data.get("total", 0)
                )

            except (ValueError, TypeError):

                pass

    # --------------------------------------------------
    # TODAY'S CLASSES
    # --------------------------------------------------

    if isinstance(timetable, list):

        today_classes = timetable

    elif isinstance(timetable, dict):

        today_classes = []

        for value in timetable.values():

            if isinstance(value, list):
                today_classes.extend(value)

    else:

        today_classes = []

    # ==================================================
    # DASHBOARD CARD ROW 1
    # ==================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------
    # NEXT CLASS CARD
    # --------------------------------------------------

    with col1:

        with st.container(border=True):

            st.markdown("### 📚 NEXT CLASS")

            st.markdown(
                f"## {class_subject}"
            )

            if class_time:

                st.write(
                    f"🕐 {class_time}"
                )

            if class_room:

                st.write(
                    f"📍 {class_room}"
                )

    # --------------------------------------------------
    # NEXT ASSIGNMENT CARD
    # --------------------------------------------------

    with col2:

        with st.container(border=True):

            st.markdown("### 📝 NEXT ASSIGNMENT")

            if next_assignment:

                assignment_name = get_value(
                    next_assignment,
                    [
                        "title",
                        "name",
                        "assignment"
                    ],
                    "Assignment"
                )

                due_date = get_value(
                    next_assignment,
                    [
                        "due",
                        "deadline",
                        "due_date"
                    ],
                    "Upcoming"
                )

                st.markdown(
                    f"## {due_date}"
                )

                st.write(
                    assignment_name
                )

            else:

                st.markdown(
                    "## No assignments"
                )

                st.write(
                    "You're all caught up! 🎉"
                )

    # ==================================================
    # DASHBOARD CARD ROW 2
    # ==================================================

    col3, col4 = st.columns(2)

    # --------------------------------------------------
    # ATTENDANCE CARD
    # --------------------------------------------------

    with col3:

        with st.container(border=True):

            st.markdown(
                "### 📊 ATTENDANCE"
            )

            st.markdown(
                f"## {overall_attendance:.1f}%"
            )

            st.write(
                f"{total_attended} / "
                f"{total_classes} classes"
            )

            st.progress(
                min(
                    max(
                        overall_attendance / 100,
                        0
                    ),
                    1
                )
            )

    # --------------------------------------------------
    # TODAY CARD
    # --------------------------------------------------

    with col4:

        with st.container(border=True):

            st.markdown(
                "### 📅 TODAY"
            )

            st.markdown(
                f"## {len(today_classes)} Classes"
            )

            st.write(
                "Stay on top of your schedule."
            )

    # ==================================================
    # MY DAY
    # ==================================================

    st.header("✨ My Day")

    st.write(
        "A quick overview of what you need to know today."
    )

    if next_class:

        st.info(
            f"📚 Your first class is "
            f"**{class_subject}** at "
            f"**{class_time}** in "
            f"**{class_room}**."
        )

    if next_assignment:

        assignment_name = get_value(
            next_assignment,
            [
                "title",
                "name",
                "assignment"
            ],
            "Assignment"
        )

        due_date = get_value(
            next_assignment,
            [
                "due",
                "deadline",
                "due_date"
            ],
            "Upcoming"
        )

        st.info(
            f"📝 Remember your assignment: "
            f"**{assignment_name}** — due "
            f"**{due_date}**."
        )

    st.success(
        f"✅ Your attendance is currently "
        f"**{overall_attendance:.1f}%**."
    )

    st.info(
        f"📅 You have **{len(today_classes)} classes** "
        f"on today's timetable."
    )

    # ==================================================
    # QUICK ACCESS
    # ==================================================

    st.header("⚡ Quick access")

    q1, q2 = st.columns(2)

    with q1:

        with st.container(border=True):

            st.markdown("### 🤖 COPILOT")

            st.markdown(
                "## Ask Copilot"
            )

            st.write(
                "Ask about college information."
            )

    with q2:

        with st.container(border=True):

            st.markdown("### 📚 CLASSES")

            st.markdown(
                "## Timetable"
            )

            st.write(
                "Check today's schedule."
            )

    q3, q4 = st.columns(2)

    with q3:

        with st.container(border=True):

            st.markdown("### 📝 WORK")

            st.markdown(
                "## Assignments"
            )

            st.write(
                "Check your academic work."
            )

    with q4:

        with st.container(border=True):

            st.markdown("### 📊 PROGRESS")

            st.markdown(
                "## Attendance"
            )

            st.write(
                "Check your attendance."
            )

    # ==================================================
    # COPILOT
    # ==================================================

    st.divider()

    st.subheader(
        "🤖 College Copilot"
    )

    st.write(
        "Your smart campus assistant. Ask about "
        "classes, faculty, rooms, assignments, "
        "attendance, notices or campus contacts."
    )

    st.caption(
        'Try asking: "Who teaches Physics?", '
        '"Where is Physics?", '
        '"Show my attendance", '
        '"What assignments do I have?"'
    )

    question = st.text_input(
        "Ask a question",
        placeholder="Try: Who teaches Physics?",
        key="dashboard_question"
    )

    if question:

        q = question.lower().strip()

        # ==================================================
        # GREETINGS
        # ==================================================

        if q in [
            "hi",
            "hello",
            "hey",
            "hii",
            "good morning",
            "good afternoon"
        ]:

            st.success(
                "Hello! 👋 I'm your College Copilot. "
                "What would you like to know?"
            )

        # ==================================================
        # HELP
        # ==================================================

        elif "help" in q:

            st.info(
                "I can help you with:\n\n"
                "• Faculty\n"
                "• Rooms\n"
                "• Timetable\n"
                "• Assignments\n"
                "• Attendance\n"
                "• Notices\n"
                "• Campus contacts"
            )

        # ==================================================
        # FACULTY
        # ==================================================

        elif (
            "teacher" in q
            or "faculty" in q
            or "professor" in q
            or "teaches" in q
        ):

            found = False

            for member in faculty:

                if isinstance(member, dict):

                    text = " ".join(
                        str(value).lower()
                        for value in member.values()
                    )

                    words = q.split()

                    if any(
                        word in text
                        for word in words
                        if len(word) > 3
                    ):

                        with st.container(border=True):

                            for key, value in member.items():

                                label = str(
                                    key
                                ).replace(
                                    "_",
                                    " "
                                ).title()

                                st.write(
                                    f"**{label}:** {value}"
                                )

                        found = True

            if not found:

                st.warning(
                    "I couldn't find that faculty member "
                    "or subject."
                )

        # ==================================================
        # ROOMS
        # ==================================================

        elif (
            "room" in q
            or "where is" in q
            or "location" in q
        ):

            found = False

            for room in rooms:

                if isinstance(room, dict):

                    text = " ".join(
                        str(value).lower()
                        for value in room.values()
                    )

                    words = q.split()

                    if any(
                        word in text
                        for word in words
                        if len(word) > 3
                    ):

                        with st.container(border=True):

                            for key, value in room.items():

                                label = str(
                                    key
                                ).replace(
                                    "_",
                                    " "
                                ).title()

                                st.write(
                                    f"**{label}:** {value}"
                                )

                        found = True

            if not found:

                display_data(rooms)

        # ==================================================
        # ASSIGNMENTS
        # ==================================================

        elif (
            "assignment" in q
            or "homework" in q
            or "work" in q
        ):

            st.subheader(
                "📝 Your Assignments"
            )

            display_data(
                assignments
            )

        # ==================================================
        # ATTENDANCE
        # ==================================================

        elif (
            "attendance" in q
            or "present" in q
            or "absent" in q
        ):

            st.subheader(
                "📊 Your Attendance"
            )

            st.metric(
                "Overall Attendance",
                f"{overall_attendance:.1f}%"
            )

            st.progress(
                min(
                    max(
                        overall_attendance / 100,
                        0
                    ),
                    1
                )
            )

            display_data(
                st.session_state.attendance_data
            )

        # ==================================================
        # TIMETABLE
        # ==================================================

        elif (
            "timetable" in q
            or "schedule" in q
            or "class" in q
        ):

            st.subheader(
                "📅 Timetable"
            )

            display_data(
                timetable
            )

        # ==================================================
        # NOTICES
        # ==================================================

        elif (
            "notice" in q
            or "announcement" in q
            or "news" in q
        ):

            st.subheader(
                "📢 Notices"
            )

            display_data(
                notices
            )

        # ==================================================
        # CONTACTS
        # ==================================================

        elif (
            "contact" in q
            or "phone" in q
            or "email" in q
        ):

            st.subheader(
                "📞 Campus Contacts"
            )

            display_data(
                contacts
            )

        # ==================================================
        # MY DAY
        # ==================================================

        elif (
            "my day" in q
            or "today" in q
        ):

            st.subheader(
                "✨ My Day"
            )

            st.write(
                f"📚 Classes today: "
                f"**{len(today_classes)}**"
            )

            st.write(
                f"📊 Attendance: "
                f"**{overall_attendance:.1f}%**"
            )

            if next_assignment:

                assignment_name = get_value(
                    next_assignment,
                    [
                        "title",
                        "name",
                        "assignment"
                    ],
                    "Assignment"
                )

                st.write(
                    f"📝 Assignment: "
                    f"**{assignment_name}**"
                )

        # ==================================================
        # UNKNOWN
        # ==================================================

        else:

            st.warning(
                "I'm not sure what you mean yet. "
                "Try asking about faculty, rooms, "
                "assignments, attendance, timetable "
                "or notices."
            )


# ==================================================
# MY DAY PAGE
# ==================================================

elif page == "✨ My Day":

    st.title("✨ My Day")

    st.write(
        "Everything you need to know about today."
    )

    next_class = get_next_class()

    if next_class:

        subject = get_value(
            next_class,
            ["subject", "name", "course"],
            "Class"
        )

        time = get_value(
            next_class,
            ["time", "start_time"],
            ""
        )

        room = get_value(
            next_class,
            ["room", "location", "venue"],
            ""
        )

        with st.container(border=True):

            st.markdown(
                f"### 📚 {subject}"
            )

            st.write(
                f"🕐 {time}"
            )

            st.write(
                f"📍 {room}"
            )

    st.subheader(
        "📊 Attendance"
    )

    overall_attendance = get_overall_attendance()

    st.metric(
        "Overall attendance",
        f"{overall_attendance:.1f}%"
    )

    st.progress(
        min(
            max(
                overall_attendance / 100,
                0
            ),
            1
        )
    )

    st.subheader(
        "📝 Assignments"
    )

    display_data(
        assignments
    )


# ==================================================
# TIMETABLE PAGE
# ==================================================

elif page == "📅 Timetable":

    st.title(
        "📅 Timetable"
    )

    st.write(
        "Check your classes and schedule."
    )

    display_data(
        timetable
    )


# ==================================================
# ASSIGNMENTS PAGE
# ==================================================

elif page == "📝 Assignments":

    st.title(
        "📝 Assignments"
    )

    st.write(
        "Keep track of your academic work."
    )

    display_data(
        assignments
    )


# ==================================================
# ATTENDANCE PAGE
# ==================================================

elif page == "📊 Attendance":

    st.title(
        "📊 Attendance"
    )

    overall_attendance = get_overall_attendance()

    st.metric(
        "Overall Attendance",
        f"{overall_attendance:.1f}%"
    )

    st.progress(
        min(
            max(
                overall_attendance / 100,
                0
            ),
            1
        )
    )

    st.divider()

    display_data(
        st.session_state.attendance_data
    )


# ==================================================
# NOTICES PAGE
# ==================================================

elif page == "📢 Notices":

    st.title(
        "📢 Notices"
    )

    st.write(
        "Latest college announcements."
    )

    display_data(
        notices
    )


# ==================================================
# FACULTY PAGE
# ==================================================

elif page == "👩‍🏫 Faculty":

    st.title(
        "👩‍🏫 Faculty"
    )

    st.write(
        "Find information about your faculty."
    )

    display_data(
        faculty
    )


# ==================================================
# CAMPUS PAGE
# ==================================================

elif page == "🏫 Campus":

    st.title(
        "🏫 Campus"
    )

    st.subheader(
        "📍 Rooms"
    )

    display_data(
        rooms
    )

    st.divider()

    st.subheader(
        "📞 Contacts"
    )

    display_data(
        contacts
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown(
    '<p class="footer-text">'
    '🎓 College Copilot • '
    'Your AI-powered campus companion • '
    'Version 1.0'
    '</p>',
    unsafe_allow_html=True
)