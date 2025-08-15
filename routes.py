
import psycopg2
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    return psycopg2.connect(
        host="uno-habittracker.cxa4qcikgs1o.us-east-2.rds.amazonaws.com",
        dbname="habit_tracker",
        user="postgres",
        password="WOpIwqP2g2EnD2m",
        port=5432
    )

conn = get_db_connection()

cur = conn.cursor()

conn.commit()

cur.close()
conn.close()
# initializes data for testing purposes

class User(UserMixin):
    def __init__(self, id):
        self.id = str(id)
        self.username = self.get_username()

    def get_id(self):
        return self.id

    def get_username(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT user_detail_username FROM habits.user_detail WHERE user_detail_id = %s", (self.id,))
            username = cur.fetchone()[0]
            cur.close()
            conn.close()
            return username
        except (Exception, psycopg2.Error) as error:
            print(f"Error while getting username: {error}")
            return None

def get_data(table_name):
    """
    Retrieves all data from a specified table for the current user.
    
    Args:
        table_name (str): The name of the table to query (e.g., 'sleep', 'workout').
    
    Returns:
        list: A list of tuples containing the queried data, or an empty list on error.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Corrected f-string to properly reference the table within the schema
    query = f"SELECT * FROM habits.{table_name} WHERE user_detail_id = %s ORDER BY {table_name}_date DESC"
    
    try:
        cur.execute(query, (current_user.id,))
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print(f"Database error in get_data for table '{table_name}': {e}")
        return []
    finally:
        cur.close()
        conn.close()

def _get_feedback_for_user(limit=20):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            feedback_id,
            feedback_type,
            feedback_page,
            feedback_message,
            COALESCE(feedback_rating, 0),
            contact_email,
            created_at
        FROM habits.feedback
        WHERE user_detail_id = %s
        ORDER BY created_at DESC
        LIMIT %s
    """, (current_user.id, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_chart_data(table_name, date_column, value_column):
    """
    Retrieves data for a chart (date and a single value) from a specified table.
    
    Args:
        table_name (str): The name of the table.
        date_column (str): The name of the column containing the date.
        value_column (str): The name of the column containing the value for the chart.
    
    Returns:
        list: A list of tuples (date, value) sorted by date, or an empty list on error.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    query = f"SELECT {date_column}, {value_column} FROM habits.{table_name} WHERE user_detail_id = %s ORDER BY {date_column}"
    
    try:
        cur.execute(query, (current_user.id,))
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print(f"Database error in get_chart_data for table '{table_name}': {e}")
        return []
    finally:
        cur.close()
        conn.close()
def get_goal_data():
    conn = get_db_connection()
    """
    Retrieves goal data

    Args:
        None

    Returns:
        list: A list of a list containing the goal settings for the user.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Corrected f-string to properly reference the table within the schema
    query = f"SELECT * FROM habits.goals WHERE user_detail_id = %s"

    try:
        cur.execute(query, (current_user.id,))
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print(f"Database error in get_data for table 'goals': {e}")
        return []
    finally:
        cur.close()
        conn.close()

def diet_tips(diet_data,goal_data):
    """
    Takes in Diet and Goal Data and returns a list of tips
    based on calculations made between the diet data and the goal data

    Args:
        diet_data (list): A list containing the diet data.
        goal_data (list): A list containing the goal data

    Returns:
        list: A list of tips to be passed into the template and displayed on the webpage
    """
    tips=[]
    if diet_data == [] or goal_data == []:
        tips.append(f"Not enough data yet...")
        return tips
    diets = 0
    diet_avg = 0
    newest = diet_data[0][4]
    goal = goal_data[0][4]
    for diet in diet_data:
        diet_avg += diet[4]
        diets += 1
    diet_avg = diet_avg / diets
    if diet_avg >= goal:
        tips.append(f"Your Average ({diet_avg:.2f}) currently meets or is passing your goal!")
    else:
        tips.append(f"Your Average ({diet_avg:.2f}) is currently below your goal!")
    if newest >= goal:
        tips.append(f"Your newest ({newest}) is above your goal! Keep it up!")
    else:
        tips.append(f"Your newest ({newest}) is below your goal! Don't let this become a trend.")
    return tips

def workout_tips(work_data,goal_data):
    """
    Takes in workout and Goal Data and returns a list of tips
    based on calculations made between the workout data and the goal data

    Args:
        work_data (list): A list containing the workout data.
        goal_data (list): A list containing the goal data

    Returns:
        list: A list of tips to be passed into the template and displayed on the webpage
    """
    tips=[]
    if work_data == [] or goal_data == []:
        tips.append(f"Not enough data yet...")
        return tips
    works = 0
    work_avg = 0
    newest = work_data[0][4]
    goal = goal_data[0][3]
    for work in work_data:
        work_avg += work[4]
        works += 1
    work_avg = work_avg / works
    if work_avg >= goal:
        tips.append(f"Your Average intensity ({work_avg:.2f}) currently meets or is passing your goal!")
    else:
        tips.append(f"Your Average intensity ({work_avg:.2f}) is currently below your goal!")
        tips.append(f"If you're using weights, try increasing the weight or amount of reps.")
    if newest >= goal:
        tips.append(f"Your most recent intensity ({newest}) meets or is above your goal!")
        if newest >= 8:
            tips.append(f"Try not to go too intense too often; it's okay to take a break occasionally.")
    else:
        tips.append(f"Your newest ({newest}) is below your goal!")
        tips.append(f"If you're taking a break that's okay, but try to increase the intensity when you're ready.")
    return tips

def sleep_tips(sleep_data,goal_data):
    """
    Takes in sleep and Goal Data and returns a list of tips
    based on calculations made between the diet data and the goal data

    Args:
        sleep_data (list): A list containing the sleep data.
        goal_data (list): A list containing the goal data

    Returns:
        list: A list of tips to be passed into the template and displayed on the webpage
    """
    tips=[]
    if sleep_data == [] or goal_data == []:
        tips.append(f"Not enough data yet...")
        return tips
    sleeps = 0
    sleep_len_avg = 0
    sleep_qual_avg=0
    newest_len = sleep_data[0][1]
    newest_qual = sleep_data[0][4]
    goal_len = goal_data[0][1]
    goal_qual = goal_data[0][2]
    for sleep in sleep_data:
        sleep_len_avg += sleep[1]
        sleep_qual_avg += sleep[4]
        sleeps += 1
    sleep_len_avg = sleep_len_avg / sleeps
    sleep_qual_avg = sleep_qual_avg / sleeps
    if sleep_len_avg >= goal_len:
        tips.append(f"Your Average length of sleep ({sleep_len_avg:.2f}) currently meets or is passing your goal!")
    else:
        tips.append(f"Your Average length of sleep ({sleep_len_avg:.2f}) is currently below your goal!")
    if newest_len >= goal_len:
        tips.append(f"Your newest length of sleep ({newest_len}) is above your goal! Keep it up!")
    else:
        tips.append(f"Your newest length of sleep ({newest_len}) is below your goal! Don't let this become a trend.")
    if sleep_qual_avg >= goal_qual:
        tips.append(f"Your average quality of sleep({sleep_qual_avg:.2f}) is above your goal! Keep it up!")
    else:
        tips.append(f"Your average quality of sleep ({sleep_qual_avg:.2f}) is currently below your goal!")
        tips.append(f"For better sleep quality, try not to use any screens for at least an hour before bed.")
    if newest_qual >= goal_qual:
        tips.append(f"Your most recent sleep ({newest_qual}) meets or is above your goal!")
    else:
        tips.append(f"Your most recent sleep ({newest_qual}) is below your goal!")
    return tips


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    """Loads user info from database to allow login"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM habits.user_detail WHERE user_detail_id = %s', (user_id,))
    user_data = cur.fetchone()
    conn.close()

    if user_data:
        # Pass only the ID to the User class
        return User(id=user_data[0])
    return None

@app.route("/")
@login_required
def index():
    return render_template("home.html", user=current_user.username)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Route used to log users into website"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM habits.user_detail WHERE user_detail_username = %s', (username,))
        user_data = cur.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data[2], password): #if a user was found password matches:
            user = User(id=user_data[0])

            print(user)
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', error="Incorrect username or password")
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Route used to register new users"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT 1 FROM habits.user_detail WHERE user_detail_username = %s', (username,))
        existing_user = cur.fetchone()
        if existing_user:
            conn.close()

            return render_template('signup.html', error='Username taken!')

        cur.execute(
            'INSERT INTO habits.user_detail (user_detail_username, user_detail_password) VALUES (%s, %s)',
            (username, password_hash)
        )
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route("/sleep", methods=["GET", "POST"])
@login_required
def sleep():
    """Route used to record sleep data"""
    if request.method == 'POST':
        date = request.form.get('date')
        duration = request.form.get('duration')
        rating = request.form.get('rating')
        notes = request.form.get('notes')

        user_id = current_user.get_id()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""INSERT INTO
                                 habits.sleep (
                                     sleep_duration,
                                     sleep_date,
                                     sleep_log,
                                     sleep_rating,
                                     user_detail_id
                                 )
                             VALUES (
                                     %s,
                                     %s,
                                     %s,
                                     %s,
                                     %s);
         """, (duration, date, notes, rating, user_id))
        conn.commit()

        cur.close()
        conn.close()
    
    sleep_data = get_data("sleep")
    print(sleep_data[0][1])
    print(sleep_data)
    goal_data = get_goal_data()
    tips = sleep_tips(sleep_data, goal_data)
    sleep_chart_data = get_chart_data("sleep", "sleep_date", "sleep_duration")
    
    return render_template("sleep.html", 
                           sleep_data=sleep_data, 
                           sleep_chart_data=sleep_chart_data,
                           tips = tips,
                           user=current_user.username)

@app.route("/diet", methods=["GET", "POST"])
@login_required
def diet():
    """Route used to record diet data"""
    if request.method == 'POST':
        date = request.form.get('date')
        rating = request.form.get('rating')
        mealname = request.form.get('mealname')
        mealnotes = request.form.get('notes')

        user_id = current_user.get_id()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""INSERT INTO habits.diet (
                                 diet_name,
                                 diet_date,
                                 diet_log,
                                 diet_rating,
                                 user_detail_id
                               )
                         VALUES (
                                 %s,
                                 %s,
                                 %s,
                                 %s,
                                 %s);
         """,(mealname,date,mealnotes,rating,user_id))
        conn.commit()

        cur.close()
        conn.close()

    diet_data = get_data("diet")
    print(diet_data)
    #print(type(diet_data[1][4]))
    goals = get_goal_data()
    print(goals)
    tips = diet_tips(diet_data, goals)
    diet_chart_data = get_chart_data("diet", "diet_date", "diet_rating")
    return render_template("diet.html", 
                           diet_data=diet_data,
                           diet_chart_data=diet_chart_data,
                           tips=tips,
                           user=current_user.username)

@app.route("/workout", methods=["GET", "POST"])
@login_required
def workout():
    """Route used to record workout data"""
    if request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        duration = request.form.get('duration')
        intensity = request.form.get('intensity')
        type = request.form.get('type')
        rating = request.form.get('rating')
        notes = request.form.get('notes')

        user_id = current_user.get_id()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""INSERT INTO
                                 habits.workout (
                                     workout_name,
                                     workout_date,
                                     workout_duration,
                                     workout_intensity,
                                     workout_type,
                                     workout_log,
                                     workout_rating,
                                     user_detail_id
                                 )
                             VALUES (
                                     %s,
                                     %s,
                                     %s,
                                     %s,
                                     %s,
                                     %s,
                                     %s,
                                     %s);
         """,(name,date,duration,intensity,type,notes,rating,user_id))
        conn.commit()
        cur.close()
        conn.close()


    workout_data = get_data("workout")
    print(workout_data)
    goal_data = get_goal_data()
    tips = workout_tips(workout_data,goal_data)
    workout_chart_data = get_chart_data("workout", "workout_date", "workout_duration")

    return render_template("workout.html", 
                           workout_data=workout_data,
                           workout_chart_data=workout_chart_data,
                           tips=tips,
                           user=current_user.username)



@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    """Route used to record goals"""
    if request.method == 'POST':
        moresleep = request.form.get('duration')
        bettersleep = request.form.get('quality')
        intensity = request.form.get('intense')
        diet = request.form.get('diet')
        user_id = current_user.get_id()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""INSERT INTO habits.goals(sleep_len_goal, better_sleep, intensity, diet, user_detail_id)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_detail_id) 
                        DO UPDATE SET 
                            sleep_len_goal = EXCLUDED.sleep_len_goal, 
                            better_sleep = EXCLUDED.better_sleep,
                            intensity=EXCLUDED.intensity,
                            diet= EXCLUDED.diet""",(moresleep, bettersleep,intensity,diet,user_id))
        conn.commit()
        cur.close()
        conn.close()
    print(get_goal_data())
    return render_template("goals.html", user= current_user.username)

@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    """Route used to provide feedback"""
    if request.method == "POST":
        ftype  = (request.form.get("type") or "").strip().lower()   # bug | idea | praise
        fpage  = (request.form.get("page") or "").strip().lower()   # home | sleep | workout | diet | other
        msg    = (request.form.get("message") or "").strip()
        rating = request.form.get("rating")
        email  = (request.form.get("email") or "").strip()

        # coerce rating safely
        try:
            r_val = int(rating) if rating else None
            if r_val is not None and not (1 <= r_val <= 5):
                r_val = None
        except ValueError:
            r_val = None

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO habits.feedback (
                user_detail_id,
                feedback_type,
                feedback_page,
                feedback_message,
                feedback_rating,
                contact_email
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )
        """, (current_user.id, ftype, fpage, msg, r_val, email if email else None))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/feedback")

    # GET
    fb_rows = _get_feedback_for_user()
    return render_template("feedback.html", user=current_user.username, feedback_data=fb_rows)

@app.route('/logout')
@login_required
def logout():
    """Logs user out"""
    logout_user()
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(e):
    """Used when a page is requested that does not exist"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    """Used when a server-sided error occurs"""
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11596, debug=True)

