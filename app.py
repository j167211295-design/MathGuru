from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import ast
import operator
from datetime import date

app = Flask(__name__)
app.secret_key = "mathguru-final-secret-key"

DB = "mathguru.db"

USERNAME = "jagan"
PASSWORD = "1234"


# =========================
# DATABASE
# =========================

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            username TEXT PRIMARY KEY,
            points INTEGER DEFAULT 0,
            solved INTEGER DEFAULT 0,
            quiz_score INTEGER DEFAULT 0,
            quiz_total INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 1,
            accuracy INTEGER DEFAULT 0,
            progress INTEGER DEFAULT 0,
            last_date TEXT
        )
    """)

    conn.execute("""
        INSERT OR IGNORE INTO stats
        (username, points, solved, quiz_score, quiz_total,
         streak, accuracy, progress, last_date)
        VALUES (?, 248, 50, 0, 0, 12, 84, 72, ?)
    """, (USERNAME, str(date.today())))

    conn.commit()
    conn.close()


def get_stats():
    conn = db()
    row = conn.execute(
        "SELECT * FROM stats WHERE username=?",
        (USERNAME,)
    ).fetchone()
    conn.close()
    return row


def update_stats(points=0, solved=0,
                 quiz_score=0, quiz_total=0):

    conn = db()

    row = conn.execute(
        "SELECT * FROM stats WHERE username=?",
        (USERNAME,)
    ).fetchone()

    new_points = row["points"] + points
    new_solved = row["solved"] + solved
    new_quiz_score = row["quiz_score"] + quiz_score
    new_quiz_total = row["quiz_total"] + quiz_total

    if new_quiz_total > 0:
        accuracy = int(
            (new_quiz_score / new_quiz_total) * 100
        )
    else:
        accuracy = row["accuracy"]

    progress = min(
        100,
        max(
            row["progress"],
            50 + int(new_solved / 5)
        )
    )

    conn.execute("""
        UPDATE stats
        SET points=?,
            solved=?,
            quiz_score=?,
            quiz_total=?,
            accuracy=?,
            progress=?
        WHERE username=?
    """, (
        new_points,
        new_solved,
        new_quiz_score,
        new_quiz_total,
        accuracy,
        progress,
        USERNAME
    ))

    conn.commit()
    conn.close()


init_db()


# =========================
# SAFE CALCULATOR
# =========================

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def safe_calculate(expression):

    expression = expression.replace("^", "**")

    if len(expression) > 100:
        raise ValueError("Expression too long")

    tree = ast.parse(expression, mode="eval")

    def calculate(node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.UnaryOp):
            if type(node.op) in operators:
                return operators[type(node.op)](
                    calculate(node.operand)
                )

        if isinstance(node, ast.BinOp):
            if type(node.op) in operators:
                left = calculate(node.left)
                right = calculate(node.right)

                if isinstance(node.op, ast.Pow):
                    if abs(right) > 10:
                        raise ValueError("Power too large")

                return operators[type(node.op)](
                    left, right
                )

        raise ValueError("Invalid expression")

    return calculate(tree.body)


# =========================
# GLOBAL HTML
# =========================

BASE_STYLE = """
<style>

*{
    box-sizing:border-box;
    margin:0;
    padding:0;
    font-family:Arial,Helvetica,sans-serif;
}

body{
    background:#f7f6ff;
    color:#202033;
    min-height:100vh;
}

a{
    text-decoration:none;
    color:inherit;
}

.container{
    max-width:720px;
    margin:auto;
    padding:24px 18px 100px;
}

.header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:22px;
}

.good{
    color:#888899;
    font-size:15px;
    margin-bottom:4px;
}

.logo{
    font-size:32px;
    font-weight:800;
}

.avatar-small{
    width:58px;
    height:58px;
    border-radius:20px;
    background:#eee9ff;
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:34px;
}

.card{
    background:white;
    border-radius:28px;
    padding:25px;
    margin-bottom:18px;
    box-shadow:0 10px 35px rgba(80,65,160,.08);
}

.hero{
    min-height:255px;
    background:linear-gradient(135deg,#eee9ff,#faf9ff);
    display:flex;
    align-items:center;
    justify-content:space-between;
    overflow:hidden;
}

.hero-text{
    width:58%;
}

.hero h1{
    font-size:30px;
    line-height:1.15;
    margin-bottom:15px;
}

.hero p{
    color:#858397;
    font-size:16px;
    line-height:1.5;
}

.student{
    width:145px;
    height:190px;
    position:relative;
}

.student .head{
    width:78px;
    height:78px;
    background:#f4b47e;
    border-radius:50%;
    position:absolute;
    top:15px;
    left:35px;
    z-index:2;
}

.student .hair{
    width:82px;
    height:40px;
    background:#34263d;
    border-radius:45px 45px 12px 12px;
    position:absolute;
    top:10px;
    left:33px;
    z-index:3;
}

.student .body{
    width:130px;
    height:110px;
    background:#7160e9;
    border-radius:70px 70px 15px 15px;
    position:absolute;
    bottom:0;
    left:8px;
}

.student .book{
    width:75px;
    height:50px;
    background:white;
    border-radius:10px;
    position:absolute;
    left:-5px;
    bottom:35px;
    transform:rotate(-8deg);
    box-shadow:0 6px 15px #ccc;
    z-index:5;
}

.welcome h2{
    font-size:23px;
    margin-bottom:8px;
}

.muted{
    color:#8d8b99;
    line-height:1.5;
}

.stats{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
}

.stat{
    background:white;
    border-radius:23px;
    padding:20px 8px;
    text-align:center;
    box-shadow:0 8px 25px rgba(80,65,160,.06);
}

.stat strong{
    font-size:25px;
    display:block;
}

.stat span{
    color:#9997a5;
    font-size:14px;
    margin-top:5px;
    display:block;
}

.section-title{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin:28px 0 15px;
}

.section-title h2{
    font-size:22px;
}

.explore{
    color:#7562dc;
}

.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
}

.feature{
    background:white;
    border-radius:25px;
    padding:22px;
    min-height:170px;
    box-shadow:0 8px 28px rgba(80,65,160,.07);
    transition:.2s;
}

.feature:active{
    transform:scale(.97);
}

.feature-icon{
    width:55px;
    height:55px;
    border-radius:18px;
    background:#f0edff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
    margin-bottom:20px;
}

.feature h3{
    font-size:18px;
    margin-bottom:7px;
}

.feature p{
    color:#9997a5;
    font-size:14px;
    line-height:1.4;
}

.progress-box{
    background:white;
    border-radius:27px;
    padding:25px;
    box-shadow:0 8px 28px rgba(80,65,160,.06);
}

.progress-head{
    display:flex;
    justify-content:space-between;
    margin-bottom:16px;
}

.progress-head strong{
    color:#7562dc;
    font-size:21px;
}

.progress-bar{
    height:13px;
    background:#ecebf2;
    border-radius:20px;
    overflow:hidden;
}

.progress-fill{
    height:100%;
    background:linear-gradient(90deg,#6d59df,#a37aff);
    border-radius:20px;
}

.btn{
    display:block;
    width:100%;
    border:0;
    background:linear-gradient(135deg,#6855dc,#9271f4);
    color:white;
    padding:16px;
    border-radius:17px;
    font-size:17px;
    font-weight:bold;
    cursor:pointer;
    margin-top:15px;
}

.btn:active{
    transform:scale(.98);
}

.input{
    width:100%;
    padding:16px;
    border:1px solid #e5e2f0;
    border-radius:16px;
    font-size:16px;
    outline:none;
    margin-top:10px;
}

.input:focus{
    border-color:#7965e5;
}

textarea.input{
    min-height:130px;
    resize:vertical;
}

.answer{
    background:#f3f0ff;
    border-radius:20px;
    padding:20px;
    margin-top:18px;
    line-height:1.7;
}

.option{
    display:block;
    background:#f7f6ff;
    padding:17px;
    border-radius:16px;
    margin:10px 0;
    border:1px solid #eeeafc;
}

.option input{
    margin-right:10px;
}

.topic{
    min-height:165px;
}

.topic-icon{
    font-size:40px;
    margin-bottom:15px;
}

.achievement{
    background:#f7f6ff;
    border-radius:20px;
    padding:17px;
    display:flex;
    align-items:center;
    gap:15px;
    margin-top:12px;
}

.achievement-icon{
    font-size:35px;
}

.achievement h3{
    margin-bottom:4px;
}

.achievement p{
    color:#9997a5;
    font-size:14px;
}

.profile{
    text-align:center;
}

.profile-avatar{
    width:145px;
    height:145px;
    margin:auto;
    background:linear-gradient(135deg,#725ce4,#9878ff);
    border-radius:40px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:75px;
}

.profile h1{
    margin-top:20px;
}

.badge{
    color:#715edf;
    font-weight:bold;
    margin-top:8px;
}

.bottom-nav{
    position:fixed;
    bottom:0;
    left:50%;
    transform:translateX(-50%);
    width:min(720px,100%);
    height:76px;
    background:white;
    display:grid;
    grid-template-columns:repeat(5,1fr);
    box-shadow:0 -5px 25px rgba(40,30,90,.1);
    z-index:20;
}

.nav-item{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    color:#9997a5;
    font-size:12px;
    gap:4px;
}

.nav-item span:first-child{
    font-size:25px;
}

.nav-active{
    color:#715edf;
    font-weight:bold;
}

.login-page{
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:20px;
    background:linear-gradient(135deg,#f5f2ff,#ffffff);
}

.login-card{
    width:100%;
    max-width:420px;
    background:white;
    padding:35px 27px;
    border-radius:32px;
    box-shadow:0 20px 60px rgba(80,65,160,.14);
}

.login-logo{
    text-align:center;
    margin-bottom:28px;
}

.login-logo .icon{
    font-size:65px;
}

.login-logo h1{
    font-size:34px;
    margin-top:8px;
}

.login-logo p{
    color:#9997a5;
    margin-top:7px;
}

.error{
    background:#fff0f0;
    color:#c74747;
    padding:13px;
    border-radius:14px;
    margin-bottom:15px;
    text-align:center;
}

.back{
    display:inline-block;
    margin-bottom:20px;
    color:#715edf;
    font-weight:bold;
}

.result{
    font-size:28px;
    font-weight:bold;
    color:#715edf;
    text-align:center;
    padding:20px;
}

.small-note{
    text-align:center;
    color:#aaa;
    font-size:13px;
    margin-top:15px;
}

@media(max-width:480px){

    .container{
        padding-left:15px;
        padding-right:15px;
    }

    .hero h1{
        font-size:25px;
    }

    .student{
        transform:scale(.85);
        margin-right:-15px;
    }

    .feature{
        min-height:155px;
        padding:18px;
    }
}

</style>
"""


# =========================
# NAVIGATION
# =========================

def nav(active="home"):

    items = [
        ("🏠", "Home", "/"),
        ("📚", "Learn", "/learn"),
        ("📝", "Quiz", "/quiz"),
        ("📈", "Progress", "/progress"),
        ("👤", "Profile", "/profile")
    ]

    html = '<div class="bottom-nav">'

    for icon, name, link in items:

        cls = "nav-item nav-active" if active == name.lower() else "nav-item"

        html += f"""
        <a href="{link}" class="{cls}">
            <span>{icon}</span>
            <span>{name}</span>
        </a>
        """

    html += "</div>"

    return html


def layout(content, active="home"):

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <title>MathGuru</title>
        {BASE_STYLE}
    </head>

    <body>

        <main class="container">

            <div class="header">
                <div>
                    <div class="good">Good Morning 👋</div>
                    <div class="logo">MathGuru</div>
                </div>

                <a href="/profile">
                    <div class="avatar-small">🧑‍🎓</div>
                </a>
            </div>

            {content}

        </main>

        {nav(active)}

    </body>
    </html>
    """


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True
            return redirect("/")

        error = "Incorrect username or password ❌"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <title>MathGuru Login</title>
        {BASE_STYLE}
    </head>

    <body>

    <div class="login-page">

        <div class="login-card">

            <div class="login-logo">
                <div class="icon">🧑‍🎓</div>
                <h1>MathGuru</h1>
                <p>Learn Maths. Build Confidence.</p>
            </div>

            {f'<div class="error">{error}</div>' if error else ''}

            <form method="POST">

                <label>Username</label>
                <input
                    class="input"
                    name="username"
                    placeholder="Enter username"
                    required
                >

                <br>

                <label>Password</label>
                <input
                    class="input"
                    type="password"
                    name="password"
                    placeholder="Enter password"
                    required
                >

                <button class="btn" type="submit">
                    Login 🚀
                </button>

            </form>

            <div class="small-note">
                MathGuru Student Portal
            </div>

        </div>

    </div>

    </body>
    </html>
    """


# =========================
# LOGIN CHECK
# =========================

@app.before_request
def check_login():

    allowed = [
        "/login",
        "/static"
    ]

    if request.path.startswith("/static"):
        return

    if request.path not in allowed:

        if not session.get("logged_in"):

            return redirect("/login")


# =========================
# HOME
# =========================

@app.route("/")
def home():

    s = get_stats()

    content = f"""

    <section class="card hero">

        <div class="hero-text">

            <h1>
                Learn Maths<br>
                with confidence!
            </h1>

            <p>
                Practice daily and
                become a Math Master.
            </p>

        </div>

        <div class="student">

            <div class="head"></div>
            <div class="hair"></div>
            <div class="body"></div>
            <div class="book"></div>

        </div>

    </section>


    <section class="card welcome">

        <h2>
            Welcome, Jagan! 🎉
        </h2>

        <p class="muted">
            Ready to continue your maths journey?
            Let's solve something amazing today.
        </p>

    </section>


    <section class="stats">

        <div class="stat">
            <strong>{s["streak"]} 🔥</strong>
            <span>Day Streak</span>
        </div>

        <div class="stat">
            <strong>{s["accuracy"]}%</strong>
            <span>Accuracy</span>
        </div>

        <div class="stat">
            <strong>{s["points"]}</strong>
            <span>Points</span>
        </div>

    </section>


    <div class="section-title">

        <h2>What do you want to do?</h2>

        <a class="explore" href="/learn">
            Explore →
        </a>

    </div>


    <div class="grid">

        <a href="/solve" class="feature">

            <div class="feature-icon">🧮</div>

            <h3>Solve Math</h3>

            <p>
                Calculate and solve problems
            </p>

        </a>


        <a href="/doubt" class="feature">

            <div class="feature-icon">💡</div>

            <h3>Ask Doubt</h3>

            <p>
                Understand difficult concepts
            </p>

        </a>


        <a href="/quiz" class="feature">

            <div class="feature-icon">📝</div>

            <h3>Quiz</h3>

            <p>
                Test your knowledge
            </p>

        </a>


        <a href="/learn" class="feature">

            <div class="feature-icon">📚</div>

            <h3>Learn Topics</h3>

            <p>
                Explore maths concepts
            </p>

        </a>

    </div>


    <div class="section-title">
        <h2>Learning Progress</h2>
    </div>


    <div class="progress-box">

        <div class="progress-head">

            <span>
                Keep going! 💪
            </span>

            <strong>
                {s["progress"]}%
            </strong>

        </div>

        <div class="progress-bar">
            <div
                class="progress-fill"
                style="width:{s["progress"]}%">
            </div>
        </div>

    </div>

    """

    return layout(content, "home")


# =========================
# SOLVE MATH
# =========================

@app.route("/solve", methods=["GET", "POST"])
def solve():

    result = ""
    error = ""

    if request.method == "POST":

        expression = request.form.get(
            "expression", ""
        ).strip()

        try:

            answer = safe_calculate(expression)

            if isinstance(answer, float):
                answer_text = f"{answer:.8f}".rstrip("0").rstrip(".")
            else:
                answer_text = str(answer)

            result = answer_text

            update_stats(
                points=5,
                solved=1
            )

        except Exception:

            error = """
            Please enter a valid mathematical expression.
            Example: 25 * 4 + 10
            """

    content = f"""

    <a class="back" href="/">← Back Home</a>

    <div class="section-title">
        <h2>🧮 Solve Math</h2>
    </div>

    <div class="card">

        <p class="muted">
            Enter your calculation below.
        </p>

        <form method="POST">

            <input
                class="input"
                name="expression"
                placeholder="Example: 25 * 4 + 10"
                autocomplete="off"
                required
            >

            <button class="btn">
                Calculate ✨
            </button>

        </form>

        {
            f'<div class="answer result">Answer = {result}</div>'
            if result else ''
        }

        {
            f'<div class="error">{error}</div>'
            if error else ''
        }

    </div>


    <div class="card">

        <h3>Examples</h3>

        <p class="muted" style="margin-top:12px">
            25 + 15<br>
            12 * 8<br>
            100 / 4<br>
            (25 + 5) * 2<br>
            2 ^ 5
        </p>

    </div>

    """

    return layout(content)


# =========================
# ASK DOUBT
# =========================

@app.route("/doubt", methods=["GET", "POST"])
def doubt():

    answer = ""

    if request.method == "POST":

        question = request.form.get(
            "question", ""
        ).lower().strip()

        if "derivative" in question or "differentiate" in question:

            answer = """
            <b>Derivative:</b><br><br>

            A derivative tells us how quickly
            one quantity changes with respect
            to another quantity.<br><br>

            Basic rule:<br>
            d/dx (xⁿ) = n xⁿ⁻¹<br><br>

            Example:<br>
            d/dx (x²) = 2x
            """

        elif "percentage" in question or "percent" in question:

            answer = """
            <b>Percentage:</b><br><br>

            Percentage means a value out of 100.<br><br>

            Formula:<br>
            Percentage = (Part / Total) × 100<br><br>

            Example:<br>
            20 out of 50<br>
            = (20/50) × 100<br>
            = 40%
            """

        elif "fraction" in question:

            answer = """
            <b>Fractions:</b><br><br>

            A fraction has a numerator
            and denominator.<br><br>

            Example:<br>
            1/2 + 1/2 = 1
            """

        elif "algebra" in question:

            answer = """
            <b>Algebra:</b><br><br>

            Algebra uses letters to represent
            unknown values.<br><br>

            Example:<br>
            x + 5 = 10<br>
            x = 5
            """

        elif "area" in question:

            answer = """
            <b>Area:</b><br><br>

            Rectangle:<br>
            Area = length × breadth<br><br>

            Square:<br>
            Area = side × side
            """

        elif "triangle" in question:

            answer = """
            <b>Triangle:</b><br><br>

            Sum of the three interior angles
            of a triangle is 180°.<br><br>

            Area = 1/2 × base × height
            """

        else:

            answer = """
            I can help with basic Maths topics
            such as Algebra, Derivatives,
            Percentages, Fractions, Geometry
            and more.<br><br>

            Try asking:<br>
            "What is a derivative?"<br>
            "Explain percentage"
            """

    content = f"""

    <a class="back" href="/">← Back Home</a>

    <div class="section-title">
        <h2>💡 Ask Math Doubt</h2>
    </div>

    <div class="card">

        <p class="muted">
            Ask your maths question in simple words.
        </p>

        <form method="POST">

            <textarea
                class="input"
                name="question"
                placeholder="Example: Explain derivative..."
                required
            ></textarea>

            <button class="btn">
                Explain 🚀
            </button>

        </form>

        {
            f'<div class="answer">{answer}</div>'
            if answer else ''
        }

    </div>

    """

    return layout(content)


# =========================
# QUIZ DATA
# =========================

QUIZ = [

    {
        "q": "What is 12 × 8?",
        "options": ["86", "96", "108", "88"],
        "answer": "96"
    },

    {
        "q": "What is 25% of 200?",
        "options": ["25", "40", "50", "75"],
        "answer": "50"
    },

    {
        "q": "What is 15 + 27?",
        "options": ["40", "42", "45", "48"],
        "answer": "42"
    },

    {
        "q": "What is √64?",
        "options": ["6", "7", "8", "9"],
        "answer": "8"
    },

    {
        "q": "What is 10²?",
        "options": ["20", "50", "100", "110"],
        "answer": "100"
    }

]


# =========================
# QUIZ
# =========================

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    score = None

    if request.method == "POST":

        score = 0

        for i, question in enumerate(QUIZ):

            selected = request.form.get(
                f"q{i}"
            )

            if selected == question["answer"]:
                score += 1

        update_stats(
            points=score * 10,
            quiz_score=score,
            quiz_total=len(QUIZ)
        )

    if score is not None:

        percentage = int(
            (score / len(QUIZ)) * 100
        )

        content = f"""

        <div class="section-title">
            <h2>🎉 Quiz Complete!</h2>
        </div>

        <div class="card" style="text-align:center">

            <div style="font-size:65px">
                🏆
            </div>

            <h1 style="margin-top:10px">
                {score} / {len(QUIZ)}
            </h1>

            <p class="muted" style="margin-top:10px">
                Your Score: {percentage}%
            </p>

            <a href="/quiz" class="btn">
                Try Again 🔄
            </a>

            <a href="/" class="btn"
               style="background:#eeeafd;color:#715edf">
                Back Home
            </a>

        </div>

        """

        return layout(content, "quiz")


    questions_html = ""

    for i, question in enumerate(QUIZ):

        options_html = ""

        for option in question["options"]:

            options_html += f"""
            <label class="option">

                <input
                    type="radio"
                    name="q{i}"
                    value="{option}"
                    required
                >

                {option}

            </label>
            """

        questions_html += f"""

        <div class="card">

            <p class="muted">
                Question {i+1} of {len(QUIZ)}
            </p>

            <h2 style="margin-top:12px">
                {question["q"]}
            </h2>

            <div style="margin-top:18px">
                {options_html}
            </div>

        </div>

        """

    content = f"""

    <div class="section-title">
        <h2>📝 Math Quiz</h2>
    </div>

    <p class="muted" style="margin-bottom:18px">
        Test your maths knowledge and earn points.
    </p>

    <form method="POST">

        {questions_html}

        <button class="btn">
            Submit Quiz 🚀
        </button>

    </form>

    """

    return layout(content, "quiz")


# =========================
# LEARN TOPICS
# =========================

@app.route("/learn")
def learn():

    topics = [

        ("➕", "Arithmetic",
         "Numbers and calculations"),

        ("📐", "Geometry",
         "Shapes and angles"),

        ("✖️", "Algebra",
         "Equations and variables"),

        ("📊", "Statistics",
         "Data and graphs"),

        ("∫", "Calculus",
         "Limits and derivatives"),

        ("🎯", "Trigonometry",
         "Angles and triangles")

    ]

    cards = ""

    for icon, title, description in topics:

        cards += f"""

        <div class="feature topic">

            <div class="topic-icon">
                {icon}
            </div>

            <h3>{title}</h3>

            <p class="muted">
                {description}
            </p>

        </div>

        """

    content = f"""

    <div class="section-title">
        <h2>📚 Learn Topics</h2>
    </div>

    <div class="grid">

        {cards}

    </div>

    """

    return layout(content, "learn")


# =========================
# PROGRESS
# =========================

@app.route("/progress")
def progress():

    s = get_stats()

    content = f"""

    <div class="section-title">
        <h2>📈 My Progress</h2>
    </div>


    <div class="progress-box">

        <div class="progress-head">

            <h2>Learning Progress</h2>

            <strong>
                {s["progress"]}%
            </strong>

        </div>

        <div class="progress-bar">

            <div
                class="progress-fill"
                style="width:{s["progress"]}%">
            </div>

        </div>

        <p class="muted" style="margin-top:15px">
            Keep learning and reach 100%! 💪
        </p>

    </div>


    <div class="section-title">
        <h2>Your Statistics</h2>
    </div>


    <div class="stats">

        <div class="stat">
            <strong>{s["points"]}</strong>
            <span>Points</span>
        </div>

        <div class="stat">
            <strong>{s["solved"]}</strong>
            <span>Solved</span>
        </div>

        <div class="stat">
            <strong>{s["accuracy"]}%</strong>
            <span>Accuracy</span>
        </div>

    </div>


    <div class="section-title">
        <h2>🏆 Achievements</h2>
    </div>


    <div class="card">

        <div class="achievement">

            <div class="achievement-icon">
                🔥
            </div>

            <div>
                <h3>
                    {s["streak"]} Day Streak
                </h3>

                <p>
                    Learning every day
                </p>
            </div>

        </div>


        <div class="achievement">

            <div class="achievement-icon">
                🧠
            </div>

            <div>
                <h3>
                    Problem Solver
                </h3>

                <p>
                    {s["solved"]} problems solved
                </p>
            </div>

        </div>


        <div class="achievement">

            <div class="achievement-icon">
                ⭐
            </div>

            <div>
                <h3>
                    Math Explorer
                </h3>

                <p>
                    {s["points"]} points earned
                </p>
            </div>

        </div>

    </div>

    """

    return layout(content, "progress")


# =========================
# PROFILE
# =========================

@app.route("/profile")
def profile():

    s = get_stats()

    content = f"""

    <div class="section-title">
        <h2>👤 My Profile</h2>
    </div>


    <div class="card profile">

        <div class="profile-avatar">
            🧑‍🎓
        </div>

        <h1>Jagan</h1>

        <div class="badge">
            MathGuru Student 🎓
        </div>

        <p class="muted" style="margin-top:10px">
            Keep learning. Keep growing. 🚀
        </p>

    </div>


    <div class="stats">

        <div class="stat">
            <strong>{s["points"]}</strong>
            <span>Points ⭐</span>
        </div>

        <div class="stat">
            <strong>{s["streak"]}</strong>
            <span>Streak 🔥</span>
        </div>

        <div class="stat">
            <strong>{s["solved"]}</strong>
            <span>Solved</span>
        </div>

    </div>


    <div class="progress-box" style="margin-top:18px">

        <div class="progress-head">

            <h2>📊 Learning Progress</h2>

            <strong>
                {s["progress"]}%
            </strong>

        </div>

        <div class="progress-bar">

            <div
                class="progress-fill"
                style="width:{s["progress"]}%">
            </div>

        </div>

        <p class="muted" style="margin-top:15px">
            You're doing great! 💪
        </p>

    </div>


    <div class="section-title">
        <h2>🏆 Achievements</h2>
    </div>


    <div class="card">

        <div class="achievement">

            <div class="achievement-icon">🔥</div>

            <div>
                <h3>{s["streak"]} Day Streak</h3>
                <p>Learning every day</p>
            </div>

        </div>


        <div class="achievement">

            <div class="achievement-icon">🧠</div>

            <div>
                <h3>Problem Solver</h3>
                <p>{s["solved"]} problems solved</p>
            </div>

        </div>


        <div class="achievement">

            <div class="achievement-icon">⭐</div>

            <div>
                <h3>Math Explorer</h3>
                <p>{s["points"]} points earned</p>
            </div>

        </div>

    </div>


    <a href="/logout"
       class="btn"
       style="background:#fff0ee;color:#c9574f">

        🚪 Logout

    </a>

    """

    return layout(content, "profile")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# RUN
# =========================

if __name__ == "__main__":

    print("")
    print("================================")
    print("        MATHGURU AI")
    print("================================")
    print("Open: http://127.0.0.1:5000")
    print("Username: jagan")
    print("Password: 1234")
    print("================================")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
