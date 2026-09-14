from flask import Flask, request, render_template_string

app = Flask(__name__)

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
    background:#f7f5ff;
    color:#202060;
}

/* LOGIN */

.login-page{
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:20px;
    background:linear-gradient(135deg,#ffffff,#eee7ff);
}

.login-card{
    width:100%;
    max-width:390px;
    background:white;
    padding:32px 24px;
    border-radius:30px;
    box-shadow:0 20px 60px rgba(91,45,140,.15);
    animation:up .7s ease;
}

@keyframes up{
    from{opacity:0;transform:translateY(35px)}
    to{opacity:1;transform:translateY(0)}
}

.login-logo{
    width:78px;
    height:78px;
    margin:auto;
    border-radius:24px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:40px;
    background:linear-gradient(135deg,#743cff,#a855f7);
    box-shadow:0 12px 30px #8b5cf655;
    animation:pop .8s ease;
}

@keyframes pop{
    0%{transform:scale(.4)}
    70%{transform:scale(1.1)}
    100%{transform:scale(1)}
}

.login-title{
    text-align:center;
    margin-top:18px;
    font-size:29px;
    font-weight:800;
}

.login-sub{
    text-align:center;
    color:#8b86a0;
    margin:8px 0 28px;
}

label{
    font-size:13px;
    font-weight:bold;
    display:block;
    margin:14px 0 7px;
}

.input{
    width:100%;
    height:52px;
    border:1px solid #e4dff0;
    border-radius:15px;
    padding:0 16px;
    outline:none;
    background:#faf9fd;
    font-size:15px;
}

.input:focus{
    border-color:#7c3aed;
    box-shadow:0 0 0 4px #7c3aed15;
}

.login-btn{
    width:100%;
    height:53px;
    margin-top:23px;
    border:0;
    border-radius:16px;
    color:white;
    font-size:16px;
    font-weight:bold;
    background:linear-gradient(135deg,#743cff,#a855f7);
    box-shadow:0 12px 25px #7c3aed35;
    transition:.2s;
}

.login-btn:active{
    transform:scale(.96);
}

.error{
    margin-top:15px;
    padding:11px;
    text-align:center;
    color:#dc2626;
    background:#fff0f2;
    border-radius:12px;
}

/* HOME */

.home{
    display:none;
    min-height:100vh;
    padding-bottom:90px;
    animation:homeIn .7s ease;
}

@keyframes homeIn{
    from{opacity:0}
    to{opacity:1}
}

.topbar{
    padding:25px 22px 18px;
    display:flex;
    align-items:center;
    justify-content:space-between;
}

.brand{
    display:flex;
    align-items:center;
    gap:12px;
}

.brand-logo{
    width:55px;
    height:55px;
    border-radius:17px;
    background:linear-gradient(135deg,#743cff,#a855f7);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:28px;
    box-shadow:0 8px 22px #7c3aed30;
}

.brand h1{
    font-size:25px;
}

.brand p{
    color:#8b86a0;
    font-size:12px;
    margin-top:3px;
}

.icons{
    font-size:27px;
}

/* HERO */

.hero{
    margin:5px 22px 20px;
    min-height:300px;
    border-radius:27px;
    padding:25px;
    position:relative;
    overflow:hidden;
    background:linear-gradient(135deg,#eee9ff,#ffffff);
    border:1px solid #ddd3ff;
    box-shadow:0 15px 40px #5b21b615;
}

.hero h2{
    font-size:27px;
    line-height:1.15;
    margin-top:5px;
}

.hero h2 span{
    color:#713cff;
    font-size:36px;
}

.hero p{
    margin-top:17px;
    color:#6e6880;
    font-size:15px;
}

.student{
    position:absolute;
    right:0;
    bottom:-5px;
    font-size:125px;
    filter:drop-shadow(0 10px 10px #7c3aed20);
}

.streak{
    display:inline-block;
    margin-top:18px;
    padding:10px 17px;
    border-radius:30px;
    background:#e8ddff;
    color:#6730d8;
    font-weight:bold;
}

/* STATS */

.stats{
    margin:0 22px 25px;
    padding:18px 8px;
    background:white;
    border-radius:22px;
    display:grid;
    grid-template-columns:repeat(4,1fr);
    box-shadow:0 10px 30px #4c3b7d12;
}

.stat{
    text-align:center;
    border-right:1px solid #eeeaf5;
}

.stat:last-child{
    border:0;
}

.stat-icon{
    font-size:25px;
}

.stat b{
    display:block;
    margin-top:7px;
    font-size:18px;
    color:#6730d8;
}

.stat small{
    display:block;
    margin-top:4px;
    color:#858095;
    font-size:9px;
}

/* SECTION */

.section-title{
    margin:0 22px 14px;
    font-size:21px;
}

.section-title span{
    float:right;
    color:#7c3aed;
    font-size:12px;
    margin-top:6px;
}

/* CARDS */

.cards{
    margin:0 22px;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
}

.card{
    min-height:190px;
    padding:18px;
    border-radius:22px;
    background:white;
    box-shadow:0 10px 30px #4c3b7d12;
    transition:.25s;
    animation:cardIn .7s ease both;
}

.card:active{
    transform:scale(.96);
}

.card:nth-child(2){animation-delay:.08s}
.card:nth-child(3){animation-delay:.16s}
.card:nth-child(4){animation-delay:.24s}
.card:nth-child(5){animation-delay:.32s}
.card:nth-child(6){animation-delay:.40s}

@keyframes cardIn{
    from{
        opacity:0;
        transform:translateY(20px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

.card-icon{
    width:58px;
    height:58px;
    border-radius:18px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:29px;
    margin-bottom:14px;
}

.purple{background:#eee5ff}
.blue{background:#e2f1ff}
.green{background:#ddfaec}
.pink{background:#ffe5f3}
.yellow{background:#fff2cc}

.card h3{
    font-size:17px;
    margin-bottom:7px;
}

.card p{
    color:#77718b;
    font-size:12px;
    line-height:1.4;
}

.card button{
    border:0;
    color:white;
    font-weight:bold;
    border-radius:20px;
    padding:9px 15px;
    margin-top:13px;
    background:#743cff;
}

/* BOTTOM */

.bottom{
    position:fixed;
    left:0;
    right:0;
    bottom:0;
    height:72px;
    background:rgba(255,255,255,.96);
    backdrop-filter:blur(15px);
    border-top:1px solid #eeeaf5;
    display:flex;
    justify-content:space-around;
    align-items:center;
}

.nav{
    text-align:center;
    color:#88829a;
    font-size:10px;
}

.nav-icon{
    display:block;
    font-size:22px;
    margin-bottom:3px;
}

.nav.active{
    color:#743cff;
    font-weight:bold;
}
</style>
</head>

<body>

<!-- LOGIN -->

<div class="login-page" id="loginPage">

<div class="login-card">

<div class="login-logo">🧠</div>

<div class="login-title">MathGuru</div>

<div class="login-sub">
Learn Smarter. Solve Faster. 🚀
</div>

<form onsubmit="login(event)">

<label>Username</label>
<input class="input" id="username"
placeholder="Enter username" required>

<label>Password</label>
<input class="input" id="password"
type="password"
placeholder="Enter password" required>

<button class="login-btn">
Login →
</button>

<div id="error"></div>

</form>

</div>
</div>


<!-- HOME -->

<div class="home" id="home">

<div class="topbar">

<div class="brand">

<div class="brand-logo">🧠</div>

<div>
<h1>MathGuru</h1>
<p>Learn Smarter. Solve Faster.</p>
</div>

</div>

<div class="icons">🔔 ⚙️</div>

</div>


<div class="hero">

<h2>
Welcome back,<br>
<span>Jagan!</span>
</h2>

<p>Ready for today's challenge? 🚀</p>

<div class="streak">
🔥 Streak: 3 days
</div>

<div class="student">
🧑‍🎓
</div>

</div>


<div class="stats">

<div class="stat">
<div class="stat-icon">🎯</div>
<b>12</b>
<small>Questions</small>
</div>

<div class="stat">
<div class="stat-icon">🏆</div>
<b>80%</b>
<small>Quiz Score</small>
</div>

<div class="stat">
<div class="stat-icon">📅</div>
<b>3</b>
<small>Day Streak</small>
</div>

<div class="stat">
<div class="stat-icon">⭐</div>
<b>2</b>
<small>Achievements</small>
</div>

</div>


<div class="section-title">
Choose What You Want to Do
<span>Small steps. Big results. 🚀</span>
</div>


<div class="cards">

<div class="card">
<div class="card-icon purple">🧮</div>
<h3>Solve Math</h3>
<p>Get instant solutions with step-by-step explanation.</p>
<button>Start Now →</button>
</div>

<div class="card">
<div class="card-icon blue">❓</div>
<h3>Ask Doubt</h3>
<p>Type your question and get simple explanations.</p>
<button style="background:#2196f3">Ask Now →</button>
</div>

<div class="card">
<div class="card-icon green">📋</div>
<h3>Quiz</h3>
<p>Test your knowledge and improve your score.</p>
<button style="background:#16b878">Start Quiz →</button>
</div>

<div class="card">
<div class="card-icon pink">📖</div>
<h3>Learn Topics</h3>
<p>Explore important mathematics chapters.</p>
<button style="background:#ec4899">Explore →</button>
</div>

<div class="card">
<div class="card-icon blue">📈</div>
<h3>Progress</h3>
<p>Track your learning and see your growth.</p>
<button style="background:#2196f3">View Progress →</button>
</div>

<div class="card">
<div class="card-icon yellow">🏆</div>
<h3>Achievements</h3>
<p>Complete goals and unlock rewards.</p>
<button style="background:#f5a900">View Awards →</button>
</div>

</div>


<div class="bottom">

<div class="nav active">
<span class="nav-icon">⌂</span>
Home
</div>

<div class="nav">
<span class="nav-icon">🧮</span>
Solve
</div>

<div class="nav">
<span class="nav-icon">❓</span>
Doubt
</div>

<div class="nav">
<span class="nav-icon">📖</span>
Learn
</div>

<div class="nav">
<span class="nav-icon">📊</span>
Progress
</div>

<div class="nav">
<span class="nav-icon">👤</span>
Profile
</div>

</div>

</div>


<script>

function login(event){

event.preventDefault();

let username =
document.getElementById("username").value;

let password =
document.getElementById("password").value;

let error =
document.getElementById("error");

if(username === "jagan" && password === "1234"){

document.getElementById("loginPage").style.display="none";

document.getElementById("home").style.display="block";

window.scrollTo(0,0);

}else{

error.innerHTML =
'<div class="error">❌ Wrong username or password</div>';

}

}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
