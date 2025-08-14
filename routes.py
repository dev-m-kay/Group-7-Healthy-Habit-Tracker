
import psycopg2
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)

cur = conn.cursor()

cur.execute(open("static/db/delete.sql", "r").read())
cur.execute(open("static/db/create.sql", "r").read())

conn.commit()

cur.close()
conn.close()
#initializes data for testing purposes, will be removed before final release

class User(UserMixin):
    def __init__(self, id):
        self.id = str(id)
        self.username = self.get_username()

    def get_id(self):
        return self.id

    def get_username(self):
        try:
            conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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
    conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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
    conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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

app = Flask(__name__)
app.secret_key = 'your_secret_key'
#initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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
    return render_template("home.html",user= current_user.username)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the username already exists
        conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
        cur = conn.cursor()
        cur.execute('SELECT * FROM habits.user_detail WHERE user_detail_username = %s', (username,))
        existing_user = cur.fetchone() #check is user already exists
        if existing_user:
            conn.close()
            return render_template('signup.html', error='Username taken!')

        # Insert the new user into the database
        cur.execute('INSERT INTO habits.user_detail (user_detail_username, user_detail_password) VALUES (%s, %s)', (username, password_hash))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

@app.route("/sleep", methods=["GET","POST"])
@login_required
def sleep():
    if request.method == 'POST':
        date = request.form.get('date')
        duration = request.form.get('duration')
        rating = request.form.get('rating')
        notes = request.form.get('notes')

        user_id = current_user.get_id()

        conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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
    sleep_chart_data = get_chart_data("sleep", "sleep_date", "sleep_duration")
    
    return render_template("sleep.html", 
                           sleep_data=sleep_data, 
                           sleep_chart_data=sleep_chart_data,
                           user=current_user.username)

@app.route("/diet", methods=["GET", "POST"])
@login_required
def diet():
    if request.method == 'POST':
        date = request.form.get('date')
        rating = request.form.get('rating')
        mealname = request.form.get('mealname')
        mealnotes = request.form.get('notes')

        user_id = current_user.get_id()

        conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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
    diet_chart_data = get_chart_data("diet", "diet_date", "diet_rating")
    return render_template("diet.html", 
                           diet_data=diet_data,
                           diet_chart_data=diet_chart_data,
                           user=current_user.username)

@app.route("/workout", methods=["GET","POST"])
@login_required
def workout():
    if request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        duration = request.form.get('duration')
        intensity = request.form.get('intensity')
        type = request.form.get('type')
        rating = request.form.get('rating')
        notes = request.form.get('notes')
        
        user_id = current_user.get_id()

        conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password", port=5432)
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
    workout_chart_data = get_chart_data("workout", "workout_date", "workout_duration")

    return render_template("workout.html", 
                           workout_data=workout_data,
                           workout_chart_data=workout_chart_data,
                           user=current_user.username)

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        moresleep = request.form.get('duration')
        print("moresleep: "+moresleep)
        bettersleep = request.form.get('quality')
        print("bettersleep: "+bettersleep)
        user_id = current_user.get_id()
        conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password",
                                 port=5432)
        cur = conn.cursor()
        cur.execute("""INSERT INTO habits.goals(sleep_len_goal, better_sleep, user_detail_id)
                         VALUES (%s, %s, %s)
                         ON CONFLICT (user_detail_id) 
                         DO UPDATE SET 
                             sleep_len_goal = EXCLUDED.sleep_len_goal, 
                             better_sleep = EXCLUDED.better_sleep""",(moresleep, bettersleep,user_id))
        conn.commit()
        cur.close()
        conn.close()
                                            
    goal_data = get_data("goals")
    print(goal_data)
    return render_template("goals.html", user= current_user.username)

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        moresleep = request.form.get('duration')
        print("moresleep: "+moresleep)
        bettersleep = request.form.get('quality')
        print("bettersleep: "+bettersleep)
        intensity = request.form.get('intense')
        diet = request.form.get('diet')
        user_id = current_user.get_id()
        conn = psycopg2.connect(host="localhost", dbname="habit_tracker", user="postgres", password="password",
                                port=5432)
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
                                    
    goal_data=get_data("habits.goals")
    print(goal_data)
    return render_template("goals.html", user= current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11596, debug=True)

