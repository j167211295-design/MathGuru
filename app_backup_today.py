from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "mathguru-secret-key"

USERNAME = "jagan"
PASSWORD = "1234"


HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MathGuru</title>

<style>
*{
    box-sizing:border-box;
    margin:0;
    padding:0;
    font-family:Arial,sans-serif;
}

body{
    background:#f6f7ff;
    color:#20213a;
}

.app{
    max-width:480px;
    margin:auto;
    min-height:100vh;
    padding-bottom:85px;
}

button{
    border:0;
    cursor:pointer;
}

/* LOGIN */

.login-page{
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:25px;
    background:linear-gradient(145deg,#eeeeff,#ffffff);
}

.login-box{
    width:100%;
    background:white;
    border-radius:30px;
    padding:30px 24px;
    box-shadow:0 20px 50px #5d55a322;
}

.logo{
    width:75px;
    height:75px;
    margin:auto;
    border-radius:23px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:40px;
    background:linear-gradient(135deg,#665bea,#987dff);
}

.login-title{
    text-align:center;
    font-size:29px;
    font-weight:800;
    margin-top:18px;
}

.login-sub{
    text-align:center;
    color:#85869a;
    margin:8px 0 28px;
}

.input{
    width:100%;
    padding:16px;
    margin-bottom:14px;
    border:1px solid #e1e2ed;
    border-radius:15px;
    outline:none;
    font-size:15px;
    background:#fafaff;
}

.login-btn{
    width:100%;
    padding:16px;
    border-radius:16px;
    background:linear-gradient(135deg,#655bea,#947aff);
    color:white;
    font-size:16px;
    font-weight:bold;
}

.demo{
    text-align:center;
    margin-top:18px;
    color:#999aaa;
    font-size:12px;
}

/* HEADER */

.header{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:22px 18px 12px;
}

.small{
    color:#85869b;
    font-size:13px;
}

.header h2{
    font-size:24px;
    margin-top:4px;
}

.avatar{
    width:48px;
    height:48px;
    border-radius:16px;
    background:#e9e7ff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:25px;
}

/* HERO */

.student-area{
    margin:5px 18px 18px;
    border-radius:28px;
    background:linear-gradient(135deg,#e6e3ff,#f7f5ff);
    height:210px;
    position:relative;
    overflow:hidden;
}

.hero-text{
    position:absolute;
    left:20px;
    top:28px;
    z-index:3;
}

.hero-text h2{
    font-size:23px;
    line-height:1.25;
}

.hero-text p{
    color:#70718a;
    margin-top:9px;
    font-size:13px;
    line-height:1.5;
}

.student{
    position:absolute;
    right:25px;
    bottom:0;
    z-index:3;
    animation:float 3s infinite ease-in-out;
}

.head{
    width:62px;
    height:62px;
    border-radius:50%;
    background:#f1b58e;
    margin:auto;
    position:relative;
}

.hair{
    position:absolute;
    width:64px;
    height:32px;
    top:-3px;
    left:-1px;
    background:#3c3040;
    border-radius:40px 40px 10px 10px;
}

.body{
    width:108px;
    height:94px;
    background:#7064eb;
    border-radius:55px 55px 10px 10px;
    margin-top:8px;
}

.book{
    position:absolute;
    width:67px;
    height:49px;
    background:white;
    border-radius:7px;
    left:-58px;
    bottom:25px;
    transform:rotate(-10deg);
    box-shadow:0 5px 12px #aaa5;
}

/* WELCOME */

.welcome{
    margin:0 18px 18px;
    padding:20px;
    border-radius:23px;
    background:white;
    box-shadow:0 10px 25px #322d640d;
}

.welcome h3{
    font-size:20px;
}

.welcome p{
    color:#7d7e91;
    font-size:13px;
    margin-top:7px;
    line-height:1.5;
}

/* STATS */

.stats{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:10px;
    margin:0 18px 20px;
}

.stat{
    background:white;
    padding:16px 8px;
    text-align:center;
    border-radius:18px;
    box-shadow:0 8px 20px #322d640b;
}

.stat strong{
    display:block;
    font-size:19px;
}

.stat span{
    color:#88899c;
    font-size:11px;
    margin-top:5px;
    display:block;
}

/* SECTIONS */

.section{
    padding:0 18px;
    margin-bottom:20px;
}

.section-title{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:13px;
}

.section-title h3{
    font-size:18px;
}

.section-title span{
    color:#7469ec;
    font-size:12px;
}

/* CARDS */

.features{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:13px;
}

.card{
    background:white;
    border-radius:22px;
    padding:18px;
    min-height:135px;
    box-shadow:0 9px 22px #322d640f;
    transition:.2s;
}

.card:active{
    transform:scale(.96);
}

.icon{
    width:45px;
    height:45px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:23px;
    background:#efedff;
}

.card h4{
    margin-top:13px;
    font-size:15px;
}

.card p{
    color:#8a8b9c;
    font-size:11px;
    margin-top:5px;
}

/* PAGES */

.page{
    padding:5px 18px;
}

.page-box{
    background:white;
    padding:20px;
    border-radius:23px;
    margin-bottom:15px;
    box-shadow:0 8px 20px #322d640d;
}

.page-box h3{
    margin-bottom:8px;
}

.page-box p{
    color:#77788b;
    font-size:13px;
    line-height:1.5;
}

.math-input{
    width:100%;
    padding:16px;
    border:1px solid #ddddeb;
    border-radius:15px;
    margin:12px 0;
    font-size:17px;
}

.action{
    padding:13px 18px;
    border-radius:14px;
    background:#7166ec;
    color:white;
    font-weight:bold;
}

.answer{
    margin-top:15px;
    padding:15px;
    border-radius:15px;
    background:#f0efff;
    color:#5147c4;
}

/* NAV */

.bottom{
    position:fixed;
    bottom:0;
    left:50%;
    transform:translateX(-50%);
    width:min(480px,100%);
    background:#ffffffee;
    backdrop-filter:blur(12px);
    border-top:1px solid #eeeeF5;
    display:flex;
    justify-content:space-around;
    padding:11px 5px 10px;
    z-index:20;
}

.nav{
    text-align:center;
    color:#9798a8;
    font-size:10px;
    text-decoration:none;
}

.nav-icon{
    font-size:21px;
    display:block;
    margin-bottom:3px;
}

.active{
    color:#665ce7;
    font-weight:bold;
}

/* PROFILE */

.profile-head{
    text-align:center;
    padding:28px 20px;
    background:linear-gradient(145deg,#eeeaff,#ffffff);
}

.profile-avatar{
    width:95px;
    height:95px;
    margin:auto;
    border-radius:32px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:52px;
    background:linear-gradient(135deg,#7166ec,#9a82ff);
    box-shadow:0 12px 25px #7166ec44;
    animation:float 3s infinite ease-in-out;
}

.achievement{
    display:flex;
    align-items:center;
    gap:12px;
    margin-top:10px;
    padding:13px;
    background:#f7f6ff;
    border-radius:15px;
}

.achievement-icon{
    font-size:28px;
}

.achievement p{
    font-size:11px;
    margin-top:3px;
}

/* ANIMATION */

@keyframes float{
    0%,100%{transform:translateY(0)}
    50%{transform:translateY(-8px)}
}

@media(min-width:700px){
    body{
        background:#e9e9f3;
    }

    .app{
        background:#f6f7ff;
        box-shadow:0 0 50px #0001;
    }
}
</style>
</head>

<body>

{% if page == "login" %}

<div class="login-page">

    <div class="login-box">

        <div class="logo">📐</div>

        <div class="login-title">
            MathGuru
        </div>

        <div class="login-sub">
            Learn Maths. Solve Faster. Grow Smarter.
        </div>

        {% if error %}
        <div style="
            background:#fff0f0;
            color:#d95353;
            padding:12px;
            border-radius:12px;
            text-align:center;
            margin-bottom:15px;
            font-size:13px;">
            {{ error }}
        </div>
        {% endif %}

        <form method="POST" action="/login">

            <input
                class="input"
                name="username"
                placeholder="Username"
                required
            >

            <input
                class="input"
                type="password"
                name="password"
                placeholder="Password"
                required
            >

            <button class="login-btn" type="submit">
                Login 🚀
            </button>

        </form>

        <div class="demo">
            Demo: jagan / 1234
        </div>

    </div>
</div>

{% else %}

<div class="app">

<div class="header">

    <div>
        <div class="small">Good Morning 👋</div>
        <h2>MathGuru</h2>
    </div>

    <a href="/profile" style="text-decoration:none;">
        <div class="avatar">🧑‍🎓</div>
    </a>

</div>


{% if page == "home" %}

<div class="student-area">

    <div class="hero-text">
        <h2>Learn Maths<br>with confidence!</h2>

        <p>
            Practice daily and<br>
            become a Math Master.
        </p>
    </div>

    <div class="student">

        <div class="book"></div>

        <div class="head">
            <div class="hair"></div>
        </div>

        <div class="body"></div>

    </div>

</div>


<div class="welcome">

    <h3>
        Welcome, Jagan! 🎉
    </h3>

    <p>
        Ready to continue your maths journey?
        Let's solve something amazing today.
    </p>

</div>


<div class="stats">

    <div class="stat">
        <strong>12 🔥</strong>
        <span>Day Streak</span>
    </div>

    <div class="stat">
        <strong>84%</strong>
        <span>Accuracy</span>
    </div>

    <div class="stat">
        <strong>248</strong>
        <span>Points</span>
    </div>

</div>


<div class="section">

    <div class="section-title">
        <h3>What do you want to do?</h3>
        <span>Explore →</span>
    </div>

    <div class="features">

        <a href="/solve" style="text-decoration:none;color:inherit;">
            <div class="card">
                <div class="icon">🧮</div>
                <h4>Solve Math</h4>
                <p>Calculate and solve problems</p>
            </div>
        </a>

        <a href="/doubt" style="text-decoration:none;color:inherit;">
            <div class="card">
                <div class="icon">💡</div>
                <h4>Ask Doubt</h4>
                <p>Understand difficult concepts</p>
            </div>
        </a>

        <a href="/quiz" style="text-decoration:none;color:inherit;">
            <div class="card">
                <div class="icon">📝</div>
                <h4>Quiz</h4>
                <p>Test your knowledge</p>
            </div>
        </a>

        <a href="/learn" style="text-decoration:none;color:inherit;">
            <div class="card">
                <div class="icon">📚</div>
                <h4>Learn Topics</h4>
                <p>Explore maths concepts</p>
            </div>
        </a>

    </div>

</div>


<div class="section">

    <div class="section-title">
        <h3>Daily Challenge 🔥</h3>
    </div>

    <div class="page-box"
         style="background:linear-gradient(135deg,#7166ec,#9585ff);color:white;">

        <h3>
            Can you solve this?
        </h3>

        <p style="color:#eee;">
            If 5x + 10 = 35, what is x?
        </p>

        <a href="/quiz">
            <button class="action"
                    style="background:white;color:#655bea;margin-top:14px;">
                Try Challenge →
            </button>
        </a>

    </div>

</div>


{% elif page == "solve" %}

<div class="page">

    <div class="section-title">
        <h3>🧮 Solve Math</h3>
    </div>

    <div class="page-box">

        <h3>Quick Calculator</h3>

        <p>
            Enter a mathematical expression.
        </p>

        <form method="POST">

            <input
                class="math-input"
                name="expression"
                placeholder="Example: 25 + 15 * 2"
                value="{{ expression }}"
                required
            >

            <button class="action">
                Calculate
            </button>

        </form>

        {% if answer %}
        <div class="answer">
            <b>Answer:</b><br><br>
            {{ answer }}
        </div>
        {% endif %}

    </div>

</div>


{% elif page == "doubt" %}

<div class="page">

    <div class="section-title">
        <h3>💡 Ask Doubt</h3>
    </div>

    <div class="page-box">

        <h3>Math Doubt Helper</h3>

        <p>
            Type your maths doubt below.
        </p>

        <form method="POST">

            <input
                class="math-input"
                name="question"
                placeholder="Example: What is a derivative?"
                required
            >

            <button class="action">
                Explain
            </button>

        </form>

        {% if explanation %}
        <div class="answer">
            <b>MathGuru 💡</b><br><br>
            {{ explanation }}
        </div>
        {% endif %}

    </div>

</div>


{% elif page == "quiz" %}

<div class="page">

    <div class="section-title">
        <h3>📝 Math Quiz</h3>
    </div>

    <div class="page-box">

        <p>Question 1 of 5</p>

        <h3 style="margin-top:15px;">
            What is 12 × 8?
        </h3>

        <form method="POST">

            <button class="option" name="answer" value="86">
                A. 86
            </button>

            <button class="option" name="answer" value="96">
                B. 96
            </button>

            <button class="option" name="answer" value="108">
                C. 108
            </button>

            <button class="option" name="answer" value="88">
                D. 88
            </button>

        </form>

        {% if quiz_result %}
        <div class="answer">
            {{ quiz_result }}
        </div>
        {% endif %}

    </div>

</div>


{% elif page == "learn" %}

<div class="page">

    <div class="section-title">
        <h3>📚 Learn Topics</h3>
    </div>

    <div class="features">

        <div class="card">
            <div class="icon">➕</div>
            <h4>Arithmetic</h4>
            <p>Numbers and calculations</p>
        </div>

        <div class="card">
            <div class="icon">📐</div>
            <h4>Geometry</h4>
            <p>Shapes and angles</p>
        </div>

        <div class="card">
            <div class="icon">✖️</div>
            <h4>Algebra</h4>
            <p>Equations and variables</p>
        </div>

        <div class="card">
            <div class="icon">📊</div>
            <h4>Statistics</h4>
            <p>Data and graphs</p>
        </div>

        <div class="card">
            <div class="icon">∫</div>
            <h4>Calculus</h4>
            <p>Limits and derivatives</p>
        </div>

        <div class="card">
            <div class="icon">🎯</div>
            <h4>Trigonometry</h4>
            <p>Angles and triangles</p>
        </div>

    </div>

</div>


{% elif page == "progress" %}

<div class="page">

    <div class="section-title">
        <h3>📈 My Progress</h3>
    </div>

    <div class="page-box">

        <div style="
            display:flex;
            justify-content:space-between;
        ">
            <h3>Overall Progress</h3>
            <b style="color:#7166ec;">72%</b>
        </div>

        <div style="
            margin-top:16px;
            background:#ececf5;
            height:12px;
            border-radius:20px;
        ">

            <div style="
                width:72%;
                height:100%;
                background:#7166ec;
                border-radius:20px;
            "></div>

        </div>

        <p style="margin-top:10px;">
            Keep going! You're doing great 💪
        </p>

    </div>

    <div class="page-box">

        <h3>🏆 Achievements</h3>

        <p style="margin-top:12px;">
            🔥 12 day streak
        </p>

        <p style="margin-top:10px;">
            🧠 50 problems solved
        </p>

        <p style="margin-top:10px;">
            ⭐ 248 points earned
        </p>

    </div>

</div>


{% elif page == "profile" %}

<div class="page">

    <div class="section-title">
        <h3>👤 My Profile</h3>
    </div>


    <!-- PROFILE -->

    <div class="page-box profile-head">

        <div class="profile-avatar">
            🧑‍🎓
        </div>

        <h2 style="margin-top:16px;">
            Jagan
        </h2>

        <p style="
            margin-top:6px;
            color:#7166ec;
            font-weight:bold;
        ">
            MathGuru Student 🎓
        </p>

        <p style="
            margin-top:6px;
            color:#88899c;
            font-size:12px;
        ">
            Keep learning. Keep growing. 🚀
        </p>

    </div>


    <!-- STATS -->

    <div class="stats">

        <div class="stat">
            <strong>248</strong>
            <span>Points ⭐</span>
        </div>

        <div class="stat">
            <strong>12 🔥</strong>
            <span>Streak</span>
        </div>

        <div class="stat">
            <strong>50</strong>
            <span>Solved</span>
        </div>

    </div>


    <!-- PROGRESS -->

    <div class="page-box">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

            <h3>📊 Learning Progress</h3>

            <b style="color:#7166ec;">
                72%
            </b>

        </div>

        <div style="
            margin-top:15px;
            background:#ececf5;
            height:12px;
            border-radius:20px;
            overflow:hidden;
        ">

            <div style="
                width:72%;
                height:100%;
                background:linear-gradient(90deg,#7166ec,#9a82ff);
                border-radius:20px;
            "></div>

        </div>

        <p style="margin-top:10px;">
            You're doing great! 💪
        </p>

    </div>


    <!-- ACHIEVEMENTS -->

    <div class="page-box">

        <h3>🏆 Achievements</h3>

        <div class="achievement">

            <div class="achievement-icon">🔥</div>

            <div>
                <b>12 Day Streak</b>
                <p>Learning every day</p>
            </div>

        </div>


        <div class="achievement">

            <div class="achievement-icon">🧠</div>

            <div>
                <b>Problem Solver</b>
                <p>50 problems solved</p>
            </div>

        </div>


        <div class="achievement">

            <div class="achievement-icon">⭐</div>

            <div>
                <b>Math Explorer</b>
                <p>248 points earned</p>
            </div>

        </div>

    </div>


    <!-- SETTINGS -->

    <div class="page-box">

        <h3>⚙️ Settings</h3>

        <div style="
            padding:15px 0;
            border-bottom:1px solid #eeeeF5;
            display:flex;
            justify-content:space-between;
        ">
            <span>🔔 Notifications</span>
            <span style="color:#7166ec;">ON</span>
        </div>

        <div style="
            padding:15px 0;
            display:flex;
            justify-content:space-between;
        ">
            <span>🌙 Theme</span>
            <span style="color:#88899c;">Light</span>
        </div>

    </div>


    <!-- LOGOUT -->

    <a href="/logout" style="text-decoration:none;">

        <button class="action"
                style="
                width:100%;
                background:#fff0f0;
                color:#e05252;
                margin-bottom:20px;
                ">

            🚪 Logout

        </button>

    </a>

</div>

{% endif %}


<!-- BOTTOM NAV -->

<div class="bottom">

    <a class="nav {% if page=='home' %}active{% endif %}"
       href="/">
        <span class="nav-icon">🏠</span>
        Home
    </a>

    <a class="nav {% if page=='learn' %}active{% endif %}"
       href="/learn">
        <span class="nav-icon">📚</span>
        Learn
    </a>

    <a class="nav {% if page=='quiz' %}active{% endif %}"
       href="/quiz">
        <span class="nav-icon">📝</span>
        Quiz
    </a>

    <a class="nav {% if page=='progress' %}active{% endif %}"
       href="/progress">
        <span class="nav-icon">📈</span>
        Progress
    </a>

    <a class="nav {% if page=='profile' %}active{% endif %}"
       href="/profile">
        <span class="nav-icon">👤</span>
        Profile
    </a>

</div>

</div>

{% endif %}

</body>
</html>
"""


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True
            return redirect("/")

        return render_template_string(
            HTML,
            page="login",
            error="Wrong username or password"
        )

    return render_template_string(
        HTML,
        page="login",
        error=None
    )


def logged_in():

    return session.get("logged_in", False)


@app.route("/")
def home():

    if not logged_in():
        return redirect("/login")

    return render_template_string(
        HTML,
        page="home"
    )


@app.route("/solve", methods=["GET", "POST"])
def solve():

    if not logged_in():
        return redirect("/login")

    answer = None
    expression = ""

    if request.method == "POST":

        expression = request.form.get("expression", "")

        try:

            allowed = "0123456789+-*/(). "

            if all(c in allowed for c in expression):

                answer = eval(
                    expression,
                    {"__builtins__": None},
                    {}
                )

            else:

                answer = "Use numbers and + - * / only."

        except:

            answer = "Invalid expression."

    return render_template_string(
        HTML,
        page="solve",
        answer=answer,
        expression=expression
    )


@app.route("/doubt", methods=["GET", "POST"])
def doubt():

    if not logged_in():
        return redirect("/login")

    explanation = None

    if request.method == "POST":

        q = request.form.get(
            "question",
            ""
        ).lower()

        if "derivative" in q:

            explanation = (
                "A derivative tells how quickly "
                "a quantity changes. "
                "For example, derivative of x² is 2x."
            )

        elif "percentage" in q:

            explanation = (
                "Percentage means a value out of 100. "
                "For example, 25% means 25 out of 100."
            )

        elif "fraction" in q:

            explanation = (
                "A fraction represents a part of a whole. "
                "Example: 1/2 means one part out of two."
            )

        elif "algebra" in q:

            explanation = (
                "Algebra uses letters and numbers "
                "to represent unknown values."
            )

        else:

            explanation = (
                "Please ask a specific maths question. "
                "Example: What is a derivative?"
            )

    return render_template_string(
        HTML,
        page="doubt",
        explanation=explanation
    )


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if not logged_in():
        return redirect("/login")

    result = None

    if request.method == "POST":

        answer = request.form.get("answer")

        if answer == "96":
            result = "🎉 Correct! 12 × 8 = 96."
        else:
            result = "❌ Wrong answer. Try again!"

    return render_template_string(
        HTML,
        page="quiz",
        quiz_result=result
    )


@app.route("/learn")
def learn():

    if not logged_in():
        return redirect("/login")

    return render_template_string(
        HTML,
        page="learn"
    )


@app.route("/progress")
def progress():

    if not logged_in():
        return redirect("/login")

    return render_template_string(
        HTML,
        page="progress"
    )


@app.route("/profile")
def profile():

    if not logged_in():
        return redirect("/login")

    return render_template_string(
        HTML,
        page="profile"
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
