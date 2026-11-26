import streamlit as st
from database.db import init_db
from services.auth_service import register_user, login_user
from services.profile_service import get_profile, save_profile
from services.discovery_service import get_all_students, get_branches
from services.connection_service import (
    send_connection_request,
    get_incoming_requests,
    get_connections,
    accept_connection_request,
    reject_connection_request,
    remove_connection,
    get_connection_status,
)
from services.recommendation_service import get_connection_recommendations
from services.post_service import (
    create_post,
    get_feed_posts,
    toggle_like,
    add_comment,
    get_post_comments,
    delete_post,
    edit_post,
)
from services.notification_service import (
    get_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    delete_notification,
    get_unread_notification_count
)
from services.community_service import (
    create_community,
    get_communities,
    join_community,
    leave_community,
    create_community_post,
    get_community_posts
)

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="UniSphere | Student Network",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Initialize SQLite database
init_db()

# ----------------------------------
# CUSTOM CSS
# ----------------------------------

st.markdown(
    """
<style>

.stApp {
    background-color: #F5F8FC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.brand {
    font-size: 30px;
    font-weight: 800;
    color: #173B67;
}

.hero {
    background: linear-gradient(120deg, #102E50, #2463A5);
    padding: 65px 45px;
    border-radius: 22px;
    color: white;
    margin-top: 25px;
}

.hero h1 {
    color: white;
    font-size: 48px;
    font-weight: 800;
}

.hero p {
    color: #E6EFFA;
    font-size: 18px;
    line-height: 1.7;
}

.section-title {
    color: #173B67;
    font-size: 27px;
    font-weight: 750;
    text-align: center;
    margin-top: 45px;
}

.feature-card {
    background: white;
    border: 1px solid #E1E9F2;
    border-radius: 15px;
    padding: 25px;
    min-height: 180px;
}

.feature-card h3 {
    color: #173B67;
    font-size: 20px;
}

.feature-card p {
    color: #607086;
    font-size: 15px;
    line-height: 1.6;
}

.footer-text {
    color: #718096;
    text-align: center;
    font-size: 13px;
    margin-top: 55px;
}
/* LOGIN FORM TEXT VISIBILITY */

.stApp label {
    color: #173B67 !important;
    font-weight: 600 !important;
}

.stApp input {
    color: #173B67 !important;
    background-color: #FFFFFF !important;
}

.stApp input::placeholder {
    color: #718096 !important;
    opacity: 1 !important;
}

.stApp h1, .stApp h2, .stApp h3 {
    color: #173B67 !important;
}

.stApp p {
    color: #40536B;
}
/* LOGIN SECTION BACKGROUND */

.stTextInput,
.stCheckbox {
    color: #173B67 !important;
}

.stTextInput > div > div > input {
    background-color: #FFFFFF !important;
    color: #173B67 !important;
    border: 1px solid #CBD8E6 !important;
    border-radius: 8px !important;
}

.stButton > button {
    background-color: #173B67 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;

}
/* SIGN UP FORM BUTTON */

.stFormSubmitButton > button {
    background-color: #173B67 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.stFormSubmitButton > button p {
    color: #FFFFFF !important;
}

.stFormSubmitButton > button:hover {
    background-color: #2463A5 !important;
    color: #FFFFFF !important;
}
/* SIGN UP INPUT TEXT */

.stTextInput input {
    background-color: #FFFFFF !important;
    color: #173B67 !important;
    border: 1px solid #CBD8E6 !important;
}

.stTextInput input::placeholder {
    color: #718096 !important;
}
.stButton > button p {
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background-color: #2463A5 !important;
    color: #FFFFFF !important;
}
/* SUCCESS MESSAGE */
.stAlert [data-testid="stAlertContentSuccess"] p {
    color: #FFFFFF !important;
}

/* ERROR MESSAGE */
.stAlert [data-testid="stAlertContentError"] p {
    color: #FFFFFF !important;
}

/* WARNING MESSAGE */
.stAlert [data-testid="stAlertContentWarning"] p {
    color: #FFFFFF !important;
}

/* INFO MESSAGE */
.stAlert [data-testid="stAlertContentInfo"] p {
    color: #FFFFFF !important;
}

/* ALL ALERT BOXES */
.stAlert {
    background-color: #173B67 !important;
    border-radius: 10px !important;
}

/* UNISPHERE SIDEBAR */

[data-testid="stSidebar"] {
    background-color: #102E50 !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background-color: transparent;
    border-radius: 9px;
    padding: 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #2463A5;
}

[data-testid="stSidebar"] button {
    background-color: #2463A5 !important;
    color: #FFFFFF !important;
    border: 1px solid #547BA5 !important;
    border-radius: 9px !important;
}


</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------
# UNISPHERE STUDENT DASHBOARD
# ----------------------------------

if st.session_state.get("logged_in_user"):

    user = st.session_state["logged_in_user"]

    # ----------------------------------
    # PROFESSIONAL SIDEBAR
    # ----------------------------------

    st.sidebar.markdown(
        """
        <div style="padding: 12px 0 20px 0;">
            <h1 style="color:white; font-size:27px;">
                🎓 UniSphere
            </h1>
            <p style="color:#C7D8EA; font-size:13px;">
                Your University. Your Network.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.divider()

    st.sidebar.markdown("### STUDENT MENU")

    selected_page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔍 Discover Students",
            "👥 My Network",
            "📰 Student Feed",
            "🔔 Notifications",
            "🌐 Communities",
            "👤 My Profile",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.divider()

    st.sidebar.markdown(f"**Logged in as**  \n{user['full_name']}")

    if st.sidebar.button("↪ Logout", use_container_width=True):
        del st.session_state["logged_in_user"]
        st.session_state["auth_view"] = "login"
        st.rerun()

    # Main dashboard
    st.title(f"Welcome back, {user['full_name']}! 👋")

    st.write("Stay connected, discover students and explore your university community.")

    st.divider()

    if selected_page == "🏠 Dashboard":

        # UNIVERSITY OVERVIEW
        st.subheader("Your University Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.metric("👥 Connections", "0")
                st.caption("Students in your network")

        with col2:
            with st.container(border=True):
                st.metric("📰 Posts", "0")
                st.caption("Posts shared by you")

        with col3:
            with st.container(border=True):
                st.metric("🌐 Communities", "0")
                st.caption("Communities you joined")

        st.divider()

        # GETTING STARTED
        st.subheader("Getting Started")
        st.write("Make the most of your UniSphere experience.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            <div class="feature-card">
                <h3>👤 Complete Your Profile</h3>
                <p>Add your skills, interests and academic
                information to introduce yourself.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
            <br>
            <div class="feature-card">
                <h3>🔍 Discover Students</h3>
                <p>Find fellow students and build meaningful
                university connections.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div class="feature-card">
                <h3>📰 Explore Student Feed</h3>
                <p>Share updates, exchange ideas and see
                what's happening in your network.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
            <br>
            <div class="feature-card">
                <h3>🌐 Join Communities</h3>
                <p>Connect with students who share your
                interests and hobbies.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.divider()

        # WELCOME MESSAGE
        st.subheader("Your University Journey Starts Here")

        st.info(
            "Welcome to UniSphere! Complete your profile, "
            "connect with students and become part of your "
            "university community."
        )

    elif selected_page == "👤 My Profile":

        st.subheader("My Student Profile")
        st.write("Introduce yourself to the UniSphere community.")

        profile = get_profile(user["id"])

        with st.form("profile_form"):

            st.text_input("Full Name", value=user["full_name"], disabled=True)

            st.text_input("Username", value=user["username"], disabled=True)

            programme_options = ["BTech", "MTech", "Other"]

            programme = st.selectbox(
                "Programme",
                programme_options,
                index=(
                    programme_options.index(profile["programme"])
                    if profile["programme"] in programme_options
                    else 0
                ),
            )

            branch = st.text_input("Branch", value=profile["branch"])

            year_options = ["1st Year", "2nd Year", "3rd Year", "4th Year"]

            academic_year = st.selectbox(
                "Academic Year",
                year_options,
                index=(
                    year_options.index(profile["academic_year"])
                    if profile["academic_year"] in year_options
                    else 1
                ),
            )

            bio = st.text_area(
                "About Me",
                value=profile["bio"],
                placeholder="Tell other students about yourself...",
            )

            skills = st.text_input(
                "Skills",
                value=profile["skills"],
                placeholder="Python, Machine Learning, Web Development",
            )

            interests = st.text_input(
                "Interests",
                value=profile["interests"],
                placeholder="AI, Technology, Sports",
            )

            submitted = st.form_submit_button("Save Profile", use_container_width=True)

        if submitted:

            success, message = save_profile(
                user["id"], programme, branch, academic_year, bio, skills, interests
            )

            if success:
                st.success(message)
            else:
                st.error(f"Could not save profile: {message}")

    elif selected_page == "🔍 Discover Students":

        st.subheader("Discover Students")
        st.write("Find and connect with students across your university.")

        # PEOPLE YOU MAY KNOW
        st.markdown("### ✨ People You May Know")

        recommendations = get_connection_recommendations(user["id"])

        if recommendations:

            for student in recommendations:

                with st.container(border=True):

                    st.markdown(f"**👤 {student['full_name']}**")
                    st.caption(f"@{student['username']}")

                    st.write(f"🤝 {student['mutual_count']} mutual connections")

                    status = get_connection_status(user["id"], student["id"])

                    if status == "connected":
                        st.success("✓ Connected")

                    elif status == "pending":
                        st.info("Request Pending")

                    elif status == "not_connected":

                        if st.button(
                            "Connect",
                            key=f"recommend_connect_{student['id']}",
                            use_container_width=True,
                        ):

                            success, message = send_connection_request(
                                user["id"], student["id"]
                            )

                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.warning(message)

        else:
            st.caption(
                "No recommendations yet. Connect with more students to discover people!"
            )

        st.divider()

        # SEARCH AND FILTERS
        search_col, branch_col, year_col = st.columns([2, 1, 1])

        with search_col:
            search = st.text_input(
                "Search students", placeholder="Search by name or username..."
            )

        with branch_col:
            branches = ["All"] + get_branches()
            selected_branch = st.selectbox("Branch", branches)

        with year_col:
            years = ["All", "1st Year", "2nd Year", "3rd Year", "4th Year"]
            selected_year = st.selectbox("Academic Year", years)

        students = get_all_students(user["id"], search, selected_branch, selected_year)

        st.divider()
        st.write(f"**{len(students)} students found**")

        # STUDENT CARDS
        if students:

            card_columns = st.columns(2)

            for index, student in enumerate(students):

                with card_columns[index % 2]:

                    with st.container(border=True):

                        st.markdown(f"### 👤 {student['full_name']}")
                        st.caption(f"@{student['username']}")

                        st.write(
                            f"**{student['programme']} | " f"{student['branch']}**"
                        )

                        st.write(f"🎓 {student['academic_year']}")

                        if student["bio"]:
                            st.write(student["bio"])
                        else:
                            st.caption("No bio added yet.")

                        if student["skills"]:
                            st.write(f"**Skills:** {student['skills']}")

                        if student["interests"]:
                            st.write(f"**Interests:** {student['interests']}")

                        status = get_connection_status(user["id"], student["id"])

                        if status == "connected":
                            st.success("✓ Connected")

                        elif status == "pending":
                            st.info("Request Pending")

                        elif status == "not_connected":

                            if st.button(
                                "Connect",
                                key=f"connect_{student['id']}",
                                use_container_width=True,
                            ):

                                success, message = send_connection_request(
                                    user["id"], student["id"]
                                )

                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.warning(message)

        else:
            st.info("No students found. Try changing your search or filters.")

    elif selected_page == "👥 My Network":

        st.subheader("My Network")
        st.write("Manage your student connections.")

        # ----------------------------------
        # INCOMING CONNECTION REQUESTS
        # ----------------------------------

        st.markdown("### 📩 Incoming Requests")

        incoming_requests = get_incoming_requests(user["id"])

        if incoming_requests:

            for request in incoming_requests:

                with st.container(border=True):

                    st.markdown(f"**👤 {request['full_name']}**")
                    st.caption(f"@{request['username']}")

                    st.write(f"{request['branch']} | " f"{request['academic_year']}")

                    if request["bio"]:
                        st.write(request["bio"])

                    accept_col, reject_col = st.columns(2)

                    with accept_col:
                        if st.button(
                            "Accept",
                            key=f"accept_{request['request_id']}",
                            use_container_width=True,
                        ):

                            success, message = accept_connection_request(
                                request["request_id"], user["id"]
                            )

                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

                    with reject_col:
                        if st.button(
                            "Reject",
                            key=f"reject_{request['request_id']}",
                            use_container_width=True,
                        ):

                            success, message = reject_connection_request(
                                request["request_id"], user["id"]
                            )

                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

        else:
            st.info("You don't have any pending connection requests.")

        st.divider()

        # MY CONNECTIONS
        st.markdown("### 👥 My Connections")

        connections = get_connections(user["id"])

        st.write(f"**{len(connections)} connections**")

        if connections:

            for connection in connections:

                with st.container(border=True):

                    st.markdown(f"### 👤 {connection['full_name']}")
                    st.caption(f"@{connection['username']}")

                    st.write(
                        f"{connection['branch']} | "
                        f"{connection['academic_year']}"
                    )

                    if connection["bio"]:
                        st.write(connection["bio"])

                    confirm_remove = st.checkbox(
                        "Confirm connection removal",
                        key=f"confirm_remove_{connection['user_id']}"
                    )

                    if st.button(
                        "Remove Connection",
                        key=f"remove_{connection['user_id']}",
                        disabled=not confirm_remove,
                        use_container_width=True
                    ):

                        success, message = remove_connection(
                            user["id"],
                            connection["user_id"]
                        )

                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

        else:
            st.info("You haven't connected with any students yet.")


    elif selected_page == "📰 Student Feed":

        st.subheader("📰 Student Feed")
        st.write("Share updates and see what's happening in your university network.")

        # CREATE A POST
        st.markdown("### ✍️ Create a Post")

        with st.form("create_post_form"):
            post_content = st.text_area(
                "What's on your mind?",
                placeholder="Share something with your university community...",
                height=120,
            )

            publish_post = st.form_submit_button(
                "Publish Post", use_container_width=True
            )

            if publish_post:
                success, message = create_post(user["id"], post_content)

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.warning(message)

        st.divider()

        # DISPLAY FEED
        st.markdown("### 🌐 Recent Posts")

        posts = get_feed_posts(user["id"])

        if not posts:
            st.info("No posts yet. Be the first to share something!")

        else:
            for post in posts:

                with st.container(border=True):

                    st.markdown(f"**👤 {post['full_name']}**")

                    st.caption(f"@{post['username']} · {post['created_at']}")

                    st.write(post["content"])

                    st.caption(
                        f"❤️ {post['like_count']} likes  ·  "
                        f"💬 {post['comment_count']} comments"
                    )

                    # LIKE BUTTON
                    like_label = "Unlike ❤️" if post["liked_by_user"] else "Like 🤍"

                    if st.button(like_label, key=f"like_{post['post_id']}"):
                        success, message = toggle_like(user["id"], post["post_id"])

                        if success:
                            st.rerun()
                        else:
                            st.error(message)

                    # COMMENTS
                    with st.expander("💬 View Comments / Add Comment"):

                        comments = get_post_comments(post["post_id"])

                        if comments:
                            for comment in comments:
                                st.markdown(
                                    f"**{comment['full_name']}**: "
                                    f"{comment['comment']}"
                                )
                                st.caption(comment["created_at"])
                        else:
                            st.caption("No comments yet.")

                        with st.form(f"comment_form_{post['post_id']}"):
                            comment_text = st.text_input(
                                "Write a comment...",
                                key=f"comment_input_{post['post_id']}",
                            )

                            submit_comment = st.form_submit_button("Add Comment")

                            if submit_comment:
                                success, message = add_comment(
                                    user["id"], post["post_id"], comment_text
                                )

                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.warning(message)

                    # EDIT AND DELETE OWN POSTS
                    if post["user_id"] == user["id"]:

                        with st.expander("⚙️ Manage Your Post"):

                            with st.form(f"edit_form_{post['post_id']}"):
                                edited_content = st.text_area(
                                    "Edit your post",
                                    value=post["content"],
                                    key=f"edit_text_{post['post_id']}",
                                )

                                update_post = st.form_submit_button("Save Changes")

                                if update_post:
                                    success, message = edit_post(
                                        user["id"], post["post_id"], edited_content
                                    )

                                    if success:
                                        st.success(message)
                                        st.rerun()
                                    else:
                                        st.error(message)

                            confirm_delete = st.checkbox(
                                "I confirm that I want to delete this post.",
                                key=f"confirm_delete_{post['post_id']}",
                            )

                            if st.button(
                                "🗑️ Delete Post",
                                key=f"delete_{post['post_id']}",
                                disabled=not confirm_delete,
                            ):
                                success, message = delete_post(
                                    user["id"], post["post_id"]
                                )

                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)

    elif selected_page == "🔔 Notifications":

        st.subheader("🔔 Notifications")
        st.write("Stay updated with your UniSphere activity.")

        unread_count = get_unread_notification_count(user["id"])

        col1, col2 = st.columns([3, 1])

        with col1:
            st.metric("Unread Notifications", unread_count)

        with col2:
            if unread_count > 0:
                if st.button("Mark All as Read", use_container_width=True):
                    mark_all_notifications_read(user["id"])
                    st.rerun()

        st.divider()

        status_filter = st.selectbox(
            "Filter Notifications",
            ["All", "Unread", "Read"]
        )

        notifications = get_notifications(user["id"], status_filter)

        if notifications:

            for notification in notifications:

                with st.container(border=True):

                    read_status = (
                        "✓ Read"
                        if notification["is_read"]
                        else "🔵 Unread"
                    )

                    st.caption(
                        f"{read_status} · {notification['created_at']}"
                    )

                    st.markdown(
                        f"**{notification['actor_name']}** "
                        f"{notification['message']}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if not notification["is_read"]:
                            if st.button(
                                "Mark as Read",
                                key=f"read_{notification['id']}"
                            ):
                                mark_notification_read(
                                    notification["id"], user["id"]
                                )
                                st.rerun()

                    with col2:
                        confirm_delete = st.checkbox(
                            "Confirm deletion",
                            key=f"confirm_notification_{notification['id']}"
                        )

                        if st.button(
                            "Delete",
                            key=f"delete_notification_{notification['id']}"
                        ):
                            if confirm_delete:
                                delete_notification(
                                    notification["id"], user["id"]
                                )
                                st.rerun()
                            else:
                                st.warning("Please confirm before deleting.")

        else:
            st.info("You don't have any notifications here yet.")

    elif selected_page == "🌐 Communities":

        st.subheader("🌐 Student Communities")
        st.write("Discover communities, meet students and share ideas.")

        # CREATE COMMUNITY
        st.markdown("### ✨ Create a Community")

        with st.form("create_community_form"):

            community_name = st.text_input(
                "Community Name",
                placeholder="Example: AI Enthusiasts"
            )

            community_description = st.text_area(
                "Description",
                placeholder="What is this community about?"
            )

            create_button = st.form_submit_button(
                "Create Community",
                use_container_width=True
            )

            if create_button:

                success, message = create_community(
                    user["id"],
                    community_name,
                    community_description
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        st.divider()

        # DISPLAY COMMUNITIES
        st.markdown("### 🔍 Explore Communities")

        communities = get_communities(user["id"])

        if not communities:

            st.info(
                "No communities available yet. Create the first community!"
            )

        else:

            for community in communities:

                with st.container(border=True):

                    st.markdown(f"### 🌐 {community['name']}")

                    st.write(community["description"])

                    st.caption(
                        f"Created by {community['creator_name']} · "
                        f"👥 {community['member_count']} members"
                    )

                    if community["is_member"]:

                        st.success("✓ You are a member")

                        if community["created_by"] != user["id"]:

                            if st.button(
                                "Leave Community",
                                key=f"leave_{community['id']}"
                            ):

                                success, message = leave_community(
                                    user["id"],
                                    community["id"]
                                )

                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.warning(message)

                        # COMMUNITY DISCUSSIONS
                        st.markdown("#### 💬 Community Discussions")

                        with st.form(
                            f"community_post_form_{community['id']}"
                        ):

                            discussion = st.text_area(
                                "Share something with this community...",
                                key=f"discussion_{community['id']}"
                            )

                            post_button = st.form_submit_button(
                                "Post Discussion"
                            )

                            if post_button:

                                success, message = create_community_post(
                                    user["id"],
                                    community["id"],
                                    discussion
                                )

                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.warning(message)

                        community_posts = get_community_posts(
                            community["id"]
                        )

                        if community_posts:

                            for post in community_posts:

                                st.markdown(
                                    f"**👤 {post['full_name']}**"
                                )

                                st.write(post["content"])

                                st.caption(post["created_at"])

                                st.divider()

                        else:
                            st.caption("No discussions yet.")

                    else:

                        if st.button(
                            "Join Community",
                            key=f"join_{community['id']}",
                            use_container_width=True
                        ):

                            success, message = join_community(
                                user["id"],
                                community["id"]
                            )

                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.warning(message)



    st.stop()


# ----------------------------------
# NAVIGATION / BRANDING
# ----------------------------------
if st.session_state.get("auth_view") not in ["login", "signup"]:

    nav1, nav2, nav3 = st.columns([6, 1, 1])

    with nav1:
        st.markdown('<div class="brand">🎓 UniSphere</div>', unsafe_allow_html=True)
        st.caption("Your University. Your Network. Your Community.")

    with nav2:
        if st.button("Login", use_container_width=True):
            st.session_state["auth_view"] = "login"
            st.rerun()

    with nav3:
        if st.button("Sign Up", use_container_width=True):
            st.session_state["auth_view"] = "signup"
            st.rerun()
# ----------------------------------
# HERO BUTTONS
# ----------------------------------

hero1, hero2, hero3 = st.columns([1, 1, 4])

with hero1:
    if st.button("Login", key="hero_login", use_container_width=True):
        st.session_state["auth_view"] = "login"

with hero2:
    if st.button("Sign Up", key="hero_signup", use_container_width=True):
        st.session_state["auth_view"] = "signup"


# ----------------------------------
# LOGIN SECTION
# ----------------------------------

if st.session_state.get("auth_view") == "login":

    login_col1, login_col2, login_col3 = st.columns([1, 2, 1])

    with login_col2:

        st.title("Welcome Back!")
        st.write("Login to your UniSphere account.")

        username = st.text_input("Username", placeholder="Enter your username")

        show_password = st.checkbox("Show password")

        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            placeholder="Enter your password",
        )

        remember = st.checkbox("Remember me")

        if st.button("Login to UniSphere", use_container_width=True):

            if username and password:

                success, message, user_data = login_user(username, password)

                if success:
                    st.session_state["logged_in_user"] = user_data
                    st.rerun()

                else:
                    st.error(message)

            else:
                st.warning("Please enter your username and password.")

    if st.button("Create a new account"):
        st.session_state["auth_view"] = "signup"
        st.rerun()

elif st.session_state.get("auth_view") == "signup":

    signup_col1, signup_col2, signup_col3 = st.columns([1, 2, 1])

    with signup_col2:

        st.title("Create Your Account")
        st.write("Join the UniSphere student community.")

        with st.form("signup_form"):

            full_name = st.text_input("Full Name", placeholder="Enter your full name")

            username = st.text_input("Username", placeholder="Choose a username")

            email = st.text_input(
                "University Email", placeholder="Enter your email address"
            )

            password = st.text_input(
                "Password", type="password", placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
            )

            terms = st.checkbox("I agree to the Terms and Conditions")

            submitted = st.form_submit_button(
                "Create Account", use_container_width=True
            )

            if submitted:

                if not all([full_name, username, email, password, confirm_password]):
                    st.warning("Please fill in all required fields.")

                elif password != confirm_password:
                    st.error("Passwords do not match.")

                elif len(password) < 8:
                    st.error("Password must contain at least 8 characters.")

                elif not terms:
                    st.warning("Please accept the Terms and Conditions.")

                else:
                    success, message = register_user(
                        full_name, username, email, password
                    )

                    if success:
                        st.success(message)
                        st.balloons()
                    else:
                        st.error(message)

        if st.button("Already have an account? Login"):
            st.session_state["auth_view"] = "login"
            st.rerun()

# ----------------------------------
# PLATFORM FEATURES
# ----------------------------------

st.markdown(
    '<div class="section-title">Explore UniSphere</div>', unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    <div class="feature-card">
        <h3>👥 Student Network</h3>
        <p>
            Discover students, explore their skills
            and build meaningful connections.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
    <div class="feature-card">
        <h3>📰 Student Feed</h3>
        <p>
            Share updates, exchange ideas and
            stay connected with your network.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
    <div class="feature-card">
        <h3>🌐 Communities</h3>
        <p>
            Join communities, discuss interests
            and learn together.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ----------------------------------
# FOOTER
# ----------------------------------

st.markdown(
    """
<div class="footer-text">
    UniSphere | Chanakya University
    <br>
    Connecting Students. Building Communities.
</div>
""",
    unsafe_allow_html=True,
)
