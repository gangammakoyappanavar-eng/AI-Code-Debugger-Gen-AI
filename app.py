import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

# Application state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""
if "saved_code" not in st.session_state:
    st.session_state.saved_code = ""

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Change this if list_models.py shows another model
MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeMate AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
        radial-gradient(
            circle at top left,
            rgba(99, 102, 241, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at top right,
            rgba(236, 72, 153, 0.15),
            transparent 30%
        ),
        #0f172a;
    color: white;
}

/* Hide Streamlit default menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Header */
.hero {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed,
        #db2777
    );

    padding: 35px;
    border-radius: 25px;

    text-align: center;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.35);

    margin-bottom: 25px;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 5px;
    color: white;
}

.hero p {
    font-size: 18px;
    color: #f1f5f9;
}


/* Cards */

.card {
    background: rgba(30, 41, 59, 0.85);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 20px;

    padding: 22px;

    margin: 10px 0;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.25);
}

.card h3 {
    color: #c4b5fd;
}


/* Chat bubbles */

.user-message {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    padding: 16px 20px;

    border-radius: 20px 20px 5px 20px;

    margin: 12px 0 12px auto;

    max-width: 85%;
}

.ai-message {
    background: #1e293b;

    border: 1px solid #334155;

    padding: 18px 20px;

    border-radius: 20px 20px 20px 5px;

    margin: 12px 0;

    max-width: 90%;
}


/* Buttons */

.stButton > button {

    background: linear-gradient(
        135deg,
        #6366f1,
        #a855f7
    );

    color: white;

    border: none;

    border-radius: 12px;

    padding: 12px 25px;

    font-weight: bold;

    transition: 0.3s;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(139,92,246,0.4);
}


/* Sidebar */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #111827,
            #1e1b4b
        );
}


/* Input boxes */

textarea,
input {

    border-radius: 12px !important;

}


/* Feature cards */

.feature {

    background: linear-gradient(
        135deg,
        rgba(79,70,229,0.2),
        rgba(168,85,247,0.15)
    );

    border: 1px solid rgba(167,139,250,0.25);

    border-radius: 18px;

    padding: 20px;

    text-align: center;

    min-height: 130px;
}

.feature-icon {
    font-size: 32px;
}

.feature-title {
    font-weight: bold;
    color: #ddd6fe;
}

.feature-text {
    color: #cbd5e1;
    font-size: 14px;
}


/* Status badges */
.status-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 8px 0 18px;
}
.badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(99,102,241,0.16);
    border: 1px solid rgba(167,139,250,0.25);
    color: #ddd6fe;
    font-size: 13px;
}

/* Code preview */
.code-preview {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 14px;
    overflow-x: auto;
}

/* Better metrics */
.metric-card {
    background: rgba(30,41,59,0.75);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<h1>🤖 CodeMate AI</h1>

<p>
Your intelligent coding assistant for debugging,
code explanation and optimization.
</p>

</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="status-row">
        <span class="badge">🟢 AI Assistant Ready</span>
        <span class="badge">🔐 API Key Protected</span>
        <span class="badge">🚀 Multi-Mode Analysis</span>
        <span class="badge">📥 File Upload & Export</span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h1 style="text-align:center;">
        🤖 CodeMate
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("⚙️ Code Settings")

    language = st.selectbox(
        "Programming Language",
        [
            "Python",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "HTML",
            "CSS",
            "SQL"
        ]
    )

    analysis_mode = st.selectbox(
        "AI Mode",
        [
            "🐛 Debug",
            "💡 Explain",
            "⚡ Optimize",
            "🔍 Code Review",
            "🧪 Generate Tests",
            "📝 Generate Documentation"
        ]
    )

    temperature_hint = st.select_slider(
        "Response Detail",
        options=["Concise", "Balanced", "Detailed"],
        value="Balanced"
    )

    st.markdown("---")
    st.subheader("🧰 Quick Tools")

    uploaded = st.file_uploader(
        "Upload a code file",
        type=["py", "java", "c", "cpp", "js", "html", "css", "sql", "txt"]
    )

    if uploaded is not None:
        try:
            uploaded_code = uploaded.read().decode("utf-8")
            st.session_state.saved_code = uploaded_code
            st.success(f"Loaded: {uploaded.name}")
        except Exception:
            st.error("Could not read this file.")

    st.markdown("---")

    st.markdown(
        """
        ### ✨ Features

        🐛 Bug Detection

        🔧 Code Fixing

        💡 Code Explanation

        ⚡ Optimization

        📊 Complexity Analysis

        🎯 Best Practices
        """
    )

    st.markdown("---")

    st.caption(
        "Powered by Google Gemini"
    )


# ============================================================
# FEATURES
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""
    <div class="feature">

    <div class="feature-icon">🐛</div>

    <div class="feature-title">
    Bug Detection
    </div>

    <div class="feature-text">
    Find syntax and logic errors
    </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="feature">

    <div class="feature-icon">🔧</div>

    <div class="feature-title">
    Auto Fix
    </div>

    <div class="feature-text">
    Generate corrected code
    </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="feature">

    <div class="feature-icon">⚡</div>

    <div class="feature-title">
    Optimization
    </div>

    <div class="feature-text">
    Improve performance
    </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown("""
    <div class="feature">

    <div class="feature-icon">💡</div>

    <div class="feature-title">
    Explanation
    </div>

    <div class="feature-text">
    Understand your code
    </div>

    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# CODE INPUT
# ============================================================

st.markdown(
    '<div class="card"><h3>💻 Your Code</h3></div>',
    unsafe_allow_html=True
)

code = st.text_area(
    "Paste your code here",
    value=st.session_state.saved_code,
    height=300,
    placeholder="""Example:

def add(a, b)
    return a + b

print(add(10, 20))
""",
    label_visibility="collapsed"
)


# ============================================================
# DEBUG FUNCTION
# ============================================================

def analyze_code(code, language, mode, detail):
    """Analyze code using a selected CodeMate AI mode."""
    mode_instructions = {
        "🐛 Debug": """
Find syntax, runtime, and logical errors. Explain each issue and provide corrected code.
""",
        "💡 Explain": """
Explain the code step by step for a student. Explain important functions, variables,
control flow, and concepts in simple language.
""",
        "⚡ Optimize": """
Suggest performance, readability, and maintainability improvements. Provide an optimized
version and explain the important changes.
""",
        "🔍 Code Review": """
Perform a professional code review. Check correctness, readability, security, error
handling, maintainability, and best practices. Give actionable suggestions.
""",
        "🧪 Generate Tests": """
Create useful test cases for the code, including normal cases, edge cases, and invalid
inputs where appropriate. Provide executable test code when possible.
""",
        "📝 Generate Documentation": """
Create clear documentation for the code, including purpose, inputs, outputs, important
functions, usage examples, and notes for future developers.
"""
    }

    prompt = f"""
You are CodeMate AI, an expert programming tutor and coding assistant.

Programming language: {language}
Selected mode: {mode}
Requested response detail: {detail}

{mode_instructions.get(mode, "Analyze the code carefully.")}

Always:
- Be accurate and do not invent problems.
- Clearly distinguish confirmed issues from suggestions.
- Use Markdown headings.
- Put code inside fenced code blocks.
- When appropriate, include Time Complexity and Space Complexity.
- Keep explanations beginner-friendly but technically correct.

Code:
```{language.lower()}
{code}
```
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            return """### ⚠️ API Quota Exceeded

Your Gemini API quota has been reached.

Please wait for the quota to reset or use a Gemini project with available quota.
"""
        return f"### ❌ API Error\n\n{str(e)}"


# ============================================================
# DEBUG BUTTON
# ============================================================

if st.button(
    "🚀 Debug My Code",
    use_container_width=True
):

    if not code.strip():

        st.warning(
            "⚠️ Please paste some code first."
        )

    else:

        with st.spinner(
            "🤖 CodeMate is thinking..."
        ):

            result = analyze_code(
                code,
                language,
                analysis_mode,
                temperature_hint
            )
            st.session_state.analysis_result = result

        st.markdown(
            """
            <div class="card">

            <h3>🤖 CodeMate Analysis</h3>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(result)

        download_text = f"""CodeMate AI Analysis
Language: {language}
Mode: {analysis_mode}

{result}
"""
        st.download_button(
            "📥 Download Analysis",
            data=download_text,
            file_name="codemate_analysis.md",
            mime="text/markdown",
            use_container_width=True
        )

        if code.strip():
            st.download_button(
                "💾 Download Current Code",
                data=code,
                file_name=f"codemate_{language.lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )


# ============================================================
# QUICK ACTIONS
# ============================================================

st.markdown("### ⚡ Quick Actions")
qa1, qa2, qa3, qa4 = st.columns(4)

quick_prompts = {
    "Explain": "Explain this code line by line and teach me the important concepts.",
    "Find Bugs": "Find all likely bugs and explain how to fix them.",
    "Optimize": "Optimize this code for performance and readability.",
    "Tests": "Generate test cases, including edge cases, for this code."
}

with qa1:
    explain_clicked = st.button("💡 Explain", use_container_width=True)
with qa2:
    bugs_clicked = st.button("🐛 Find Bugs", use_container_width=True)
with qa3:
    optimize_clicked = st.button("⚡ Optimize", use_container_width=True)
with qa4:
    tests_clicked = st.button("🧪 Tests", use_container_width=True)

selected_quick = None
if explain_clicked:
    selected_quick = quick_prompts["Explain"]
elif bugs_clicked:
    selected_quick = quick_prompts["Find Bugs"]
elif optimize_clicked:
    selected_quick = quick_prompts["Optimize"]
elif tests_clicked:
    selected_quick = quick_prompts["Tests"]

if selected_quick:
    if not code.strip():
        st.warning("⚠️ Paste or upload code first.")
    else:
        with st.spinner("🤖 CodeMate is working..."):
            quick_prompt = f"""
You are CodeMate AI, an expert programming tutor.

Language: {language}
Task: {selected_quick}

Analyze this code and answer with clear Markdown and fenced code blocks where useful.

Code:
```{language.lower()}
{code}
```
"""
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=quick_prompt
                )
                st.session_state.analysis_result = response.text
                st.markdown(
                    '<div class="card"><h3>⚡ Quick Action Result</h3></div>',
                    unsafe_allow_html=True
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")


# ============================================================
# CHATBOT
# ============================================================

st.divider()

st.markdown(
    """
    <div class="card">

    <h2>💬 Chat with CodeMate</h2>

    <p>
    Ask questions about programming, errors,
    algorithms or your code.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# Display chat history

for message in st.session_state.chat_history:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">

            👤 <b>You</b>

            <br><br>

            {message["content"]}

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-message">

            🤖 <b>CodeMate AI</b>

            <br><br>

            {message["content"]}

            </div>
            """,
            unsafe_allow_html=True
        )


# Chat input

question = st.chat_input(
    "Ask CodeMate anything about coding..."
)


if question:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    prompt = f"""
You are CodeMate AI, a friendly expert programming assistant.

Answer the user's programming question clearly and accurately.

Programming language:
{language}

Question:
{question}

Give examples when useful. If code is requested, provide complete code.
"""
    with st.spinner("🤖 CodeMate is thinking..."):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            answer = response.text
        except Exception as e:
            answer = f"### ❌ API Error\\n\\n{str(e)}"

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# ============================================================
# CHAT EXPORT
# ============================================================

if st.session_state.chat_history:
    chat_export = "\n\n".join(
        f"{'USER' if m['role'] == 'user' else 'CODEMATE AI'}:\n{m['content']}"
        for m in st.session_state.chat_history
    )
    st.download_button(
        "📥 Export Chat",
        data=chat_export,
        file_name="codemate_chat.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# CLEAR CHAT
# ============================================================

if st.session_state.chat_history:

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>

    <div style="
        text-align:center;
        color:#94a3b8;
        padding:20px;
    ">

    🤖 <b>CodeMate AI</b>

    <br>

    Smart coding assistance powered by Generative AI

    <br><br>

    💻 Debug • 🔧 Fix • 💡 Learn • ⚡ Optimize

    </div>
    """,
    unsafe_allow_html=True
)
