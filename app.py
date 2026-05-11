from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

# ✅ CREATE APP FIRST
app = Flask(__name__)
app.secret_key = "secret123"

# ✅ CONFIG AFTER APP
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ SINGLE DB FUNCTION ONLY
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- DB ----------
def create_tables():
    conn = get_db_connection()

    conn.execute('DROP TABLE IF EXISTS users')

    conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            email TEXT,
            phone TEXT,
            password TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            qualification TEXT,
            branch TEXT,
            cgpa TEXT,
            job TEXT,
            resume TEXT
        )
    ''')

    conn.commit()
    conn.close()
# ---------- JOBS ----------
jobs = [
{"title":"Software Engineer","company":"Google","location":"Bangalore","description":"Develop scalable applications","image":"https://cdn-icons-png.flaticon.com/512/2721/2721297.png"},
{"title":"Data Analyst","company":"Amazon","location":"Hyderabad","description":"Analyze business data","image":"https://cdn-icons-png.flaticon.com/512/4149/4149679.png"},
{"title":"Web Developer","company":"Infosys","location":"Chennai","description":"Build responsive websites","image":"https://cdn-icons-png.flaticon.com/512/2721/2721275.png"},
{"title":"AI Engineer","company":"Microsoft","location":"Hyderabad","description":"Work on AI models","image":"https://cdn-icons-png.flaticon.com/512/4712/4712109.png"},
{"title":"Python Developer","company":"TCS","location":"Pune","description":"Backend API development","image":"https://cdn-icons-png.flaticon.com/512/5968/5968350.png"},
{"title":"Frontend Developer","company":"Wipro","location":"Bangalore","description":"UI development","image":"https://cdn-icons-png.flaticon.com/512/1055/1055687.png"},
{"title":"Backend Developer","company":"Accenture","location":"Mumbai","description":"Server-side logic","image":"https://cdn-icons-png.flaticon.com/512/919/919825.png"},
{"title":"DevOps Engineer","company":"IBM","location":"Delhi","description":"CI/CD pipelines","image":"https://cdn-icons-png.flaticon.com/512/919/919853.png"},
{"title":"Cloud Engineer","company":"Oracle","location":"Hyderabad","description":"Cloud infrastructure","image":"https://cdn-icons-png.flaticon.com/512/4144/4144788.png"},
{"title":"Full Stack Developer","company":"Capgemini","location":"Pune","description":"Frontend + Backend","image":"https://cdn-icons-png.flaticon.com/512/2721/2721297.png"},
{"title":"UI Designer","company":"Zoho","location":"Chennai","description":"Design user interfaces","image":"https://cdn-icons-png.flaticon.com/512/1821/1821065.png"},
{"title":"UX Designer","company":"Adobe","location":"Bangalore","description":"Improve user experience","image":"https://cdn-icons-png.flaticon.com/512/1821/1821065.png"},
{"title":"QA Engineer","company":"Cognizant","location":"Hyderabad","description":"Testing software","image":"https://cdn-icons-png.flaticon.com/512/906/906175.png"},
{"title":"ML Engineer","company":"Tesla","location":"Bangalore","description":"Machine learning models","image":"https://cdn-icons-png.flaticon.com/512/4712/4712109.png"},
{"title":"Data Scientist","company":"Meta","location":"Hyderabad","description":"Data prediction models","image":"https://cdn-icons-png.flaticon.com/512/4149/4149679.png"},
{"title":"System Engineer","company":"HCL","location":"Noida","description":"System management","image":"https://cdn-icons-png.flaticon.com/512/4248/4248443.png"},
{"title":"Network Engineer","company":"Cisco","location":"Mumbai","description":"Network setup","image":"https://cdn-icons-png.flaticon.com/512/483/483361.png"},
{"title":"Security Analyst","company":"Deloitte","location":"Delhi","description":"Cyber security","image":"https://cdn-icons-png.flaticon.com/512/3064/3064197.png"},
{"title":"Android Developer","company":"Samsung","location":"Bangalore","description":"Mobile apps","image":"https://cdn-icons-png.flaticon.com/512/888/888857.png"},
{"title":"iOS Developer","company":"Apple","location":"Hyderabad","description":"iOS apps","image":"https://cdn-icons-png.flaticon.com/512/888/888857.png"},
{"title":"Game Developer","company":"Ubisoft","location":"Pune","description":"Game development","image":"https://cdn-icons-png.flaticon.com/512/686/686589.png"},
{"title":"Blockchain Developer","company":"Coinbase","location":"Remote","description":"Blockchain apps","image":"https://cdn-icons-png.flaticon.com/512/919/919852.png"},
{"title":"Embedded Engineer","company":"Intel","location":"Bangalore","description":"Embedded systems","image":"https://cdn-icons-png.flaticon.com/512/4248/4248443.png"},
{"title":"AR/VR Developer","company":"Meta","location":"Hyderabad","description":"AR/VR apps","image":"https://cdn-icons-png.flaticon.com/512/4149/4149679.png"},
{"title":"Technical Writer","company":"SAP","location":"Delhi","description":"Documentation","image":"https://cdn-icons-png.flaticon.com/512/1828/1828919.png"},
{"title":"Support Engineer","company":"Freshworks","location":"Chennai","description":"Customer support","image":"https://cdn-icons-png.flaticon.com/512/597/597177.png"},
{"title":"Database Admin","company":"Oracle","location":"Bangalore","description":"Manage DB","image":"https://cdn-icons-png.flaticon.com/512/4248/4248443.png"},
{"title":"ETL Developer","company":"Infosys","location":"Hyderabad","description":"Data pipelines","image":"https://cdn-icons-png.flaticon.com/512/4149/4149679.png"},
{"title":"SAP Consultant","company":"Accenture","location":"Mumbai","description":"SAP systems","image":"https://cdn-icons-png.flaticon.com/512/4248/4248443.png"},
{"title":"HR Executive","company":"TCS","location":"Pune","description":"HR management","image":"https://cdn-icons-png.flaticon.com/512/1077/1077114.png"},
{"title":"Business Analyst","company":"Amazon","location":"Hyderabad","description":"Business insights","image":"https://cdn-icons-png.flaticon.com/512/4149/4149679.png"},
{"title":"Digital Marketer","company":"Google","location":"Bangalore","description":"Online marketing","image":"https://cdn-icons-png.flaticon.com/512/1828/1828919.png"},
{"title":"Content Writer","company":"Flipkart","location":"Bangalore","description":"Content creation","image":"https://cdn-icons-png.flaticon.com/512/1828/1828919.png"},
{"title":"SEO Analyst","company":"Zoho","location":"Chennai","description":"SEO optimization","image":"https://cdn-icons-png.flaticon.com/512/1828/1828919.png"},
{"title":"Sales Executive","company":"Reliance","location":"Mumbai","description":"Sales operations","image":"https://cdn-icons-png.flaticon.com/512/1077/1077114.png"},
{"title":"Product Manager","company":"Microsoft","location":"Hyderabad","description":"Product lifecycle","image":"https://cdn-icons-png.flaticon.com/512/1828/1828919.png"},
{"title":"Project Manager","company":"Wipro","location":"Bangalore","description":"Manage projects","image":"https://cdn-icons-png.flaticon.com/512/1828/1828919.png"},
{"title":"Intern Developer","company":"Startup","location":"Remote","description":"Learn & develop","image":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png"},
{"title":"Research Analyst","company":"EY","location":"Delhi","description":"Research work","image":"https://cdn-icons-png.flaticon.com/512/4149/4149679.png"},
{"title":"Operations Manager","company":"Flipkart","location":"Bangalore","description":"Operations handling","image":"https://cdn-icons-png.flaticon.com/512/1828/1828919.png"}
]

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template("index.html")

# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)",
            (name, email, phone, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')
    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE name=? AND password=?",
            (name, password)
        ).fetchone()
        conn.close()

        if user:
            session['user'] = name
            return redirect('/jobs')
        else:
            return "Invalid Login"

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# ---------- FORGOT ----------
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        name = request.form.get('name')

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE name=?",
            (name,)
        ).fetchone()
        conn.close()

        if user:
            return f"Password: {user['password']}"
        else:
            return "User not found"

    return render_template("forgot.html")

# ---------- JOBS ----------
@app.route('/jobs')
def job_list():
    if 'user' not in session:
        return redirect('/login')

    return render_template("jobs.html", jobs=jobs, user=session['user'])

# ---------- APPLY ----------
@app.route('/apply/<job>', methods=['GET', 'POST'])
def apply(job):
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        qualification = request.form.get('qualification')
        branch = request.form.get('branch')
        cgpa = request.form.get('cgpa')

        file = request.files.get('resume')

        filename = ""
        if file and file.filename != "":
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO applications 
            (name, phone, qualification, branch, cgpa, job, resume)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (name, phone, qualification, branch, cgpa, job, filename)
        )
        conn.commit()
        conn.close()

        return f"✅ {name}, applied successfully for {job}!"

    return render_template("apply.html", job=job)


# ---------- PROFILE ----------
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE name=?",
        (session['user'],)
    ).fetchone()

    applications = conn.execute(
        "SELECT * FROM applications WHERE name=?",
        (session['user'],)
    ).fetchall()

    conn.close()

    return render_template("profile.html", user=user, applications=applications)


# ---------- DASHBOARD ----------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE name=?",
        (session['user'],)
    ).fetchone()

    applications = conn.execute(
        "SELECT * FROM applications WHERE name=?",
        (session['user'],)
    ).fetchall()

    conn.close()

    total = len(applications)

    return render_template(
        "dashboard.html",
        user=user,
        applications=applications,
        total=total
    )
# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)