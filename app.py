import streamlit as st
import hashlib
from db_config import get_connection

st.set_page_config(page_title="AI Study Companion", layout="wide")

# ---------------- PASSWORD HASH ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ================= AUTH SECTION =================
if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

    # -------- LOGIN --------
    with tab1:
        st.subheader("Login to Your Account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            conn = get_connection()

            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM users WHERE username=%s AND password=%s",
                    (username, hash_password(password))
                )
                user = cursor.fetchone()

                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password ❌")

                cursor.close()
                conn.close()
            else:
                st.error("Database connection failed ❌")

    # -------- SIGNUP --------
    with tab2:
        st.subheader("Create New Account")

        new_user = st.text_input("Username", key="newuser")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password", key="newpass")

        if st.button("Signup"):
            conn = get_connection()

            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                        (new_user, new_email, hash_password(new_pass))
                    )
                    conn.commit()
                    st.success("Account Created Successfully ✅")
                except:
                    st.error("Username or Email already exists ❌")

                cursor.close()
                conn.close()
            else:
                st.error("Database connection failed ❌")

# ================= MAIN APP =================
else:

    st.sidebar.success(f"Welcome {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    menu = st.sidebar.radio(
        "Choose Module",
        ["📘 Notes Generator", "📝 Quiz Generator"]
    )

    # ================= SQL NOTES =================
    if menu == "📘 Notes Generator":

        st.title("📘 SQL Notes")
        topic = st.text_input("Enter Topic (Example:SQL)")
        if st.button("Generate Notes"):
            if topic.strip().lower() == "sql":

                st.header("Definition")
                st.write("• SQL (Structured Query Language) is a language used to create, manage, and manipulate relational databases.")
                st.write("• It is used in database systems like MySQL, Oracle, SQL Server, etc.")

                st.header("Types of SQL Commands")

                st.header("• DDL (Data Definition Language)")
                st.write("     Used to define structure of database.")
                st.write("     Examples: CREATE, ALTER, DROP, TRUNCATE")

                st.header("• DML (Data Manipulation Language)")
                st.write("     Used to modify data.")
                st.write("     Examples: INSERT,UPDATE,DELETE")

                st.header("• DQL (Data Query Language)")
                st.write("     Used to retrieve data.")
                st.write("     Examples: SELECT")

                st.header("• DCL (Data Control Language)")
                st.write("     Used to control access.")
                st.write("     Examples: GRANT,REVOKE")

                st.header("TCL (Transaction Control Language)")
                st.write("     Used to manage transactions.")
                st.write("     Examples: COMMIT,ROLLBACK")
                

                st.header("Key Concepts")
                st.write("     • Primary Key - Uniquely identifies each record")
                st.write("     • Foreign Key - Connects two tables")
                st.write("     • Constraints - NOT NULL,UNIQUE,CHECK")
                

                st.header("Advantages")
                st.write("     • Easy to learn")
                st.write("     • Fast data retrieval")
                st.write("     • Secure")
                st.write("     • Manages large data efficiently")

        
    # ================= SQL QUIZ =================
    elif menu == "📝 Quiz Generator":

        st.title("📝 SQL Quiz")

        conn = get_connection()

        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM quiz_questions WHERE category=%s",
                ("SQL",)
            )
            questions = cursor.fetchall()

            if not questions:
                st.warning("No SQL questions found in database.")
            else:
                st.info("Answer all questions and click Submit.")

                user_answers = {}

                for q in questions:
                    st.markdown(f"### {q['question']}")
                    user_answers[q["id"]] = st.radio(
                        "Choose your answer:",
                        [q["option1"], q["option2"], q["option3"], q["option4"]],
                        key=f"q_{q['id']}"
                    )

                if st.button("Submit Quiz"):

                    score = 0
                    st.subheader("📊 Quiz Results")

                    for q in questions:
                        user_answer = user_answers.get(q["id"])
                        correct_answer = q["answer"]

                        st.markdown(f"### {q['question']}")
                        st.write(f"Your Answer: {user_answer}")

                        if user_answer == correct_answer:
                            st.success("✅ Correct")
                            score += 1
                        else:
                            st.error("❌ Wrong")
                            st.info(f"Correct Answer: {correct_answer}")

                        st.markdown("---")

                    st.success(f"🎯 Final Score: {score} / {len(questions)}")

                    if score == len(questions):
                        st.balloons()

            cursor.close()
            conn.close()
        else:
            st.error("Database connection failed ❌")
