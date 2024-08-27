from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('patients_data.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

def login_required(f):
    def wrapper(*args, **kwargs):
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')

            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Admins WHERE username=? AND password=?", (username, password))
            admin = cursor.fetchone()

            if admin:
                return f(*args, **kwargs)
            else:
                return "Authentication failed. Please check your credentials and try again.", 403
        else:
            return render_template_string('''
                <h2>Admin Authentication</h2>
                <form method="POST">
                    Username: <input type="text" name="username"><br>
                    Password: <input type="password" name="password"><br>
                    <input type="submit" value="Authenticate">
                </form>
            ''')
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
def index():
    return '''
        <h1>Welcome to the Patient Data API!</h1>
        
        <p>This API provides the following CRUD methods:</p>
        <ul>
            <li><strong>GET /GET:</strong> Retrieve all patient data.</li>
            <li><strong>GET /GET/&lt;id&gt;:</strong> Retrieve data for a specific patient by their ID.</li>
            <li><strong>POST /POST:</strong> Add new patient data.</li>
            <li><strong>PUT /PUT/&lt;id&gt;:</strong> Update the data of an existing patient by their ID.</li>
            <li><strong>DELETE /DELETE/&lt;id&gt;:</strong> Delete a patient's data by their ID.</li>
        </ul>

        <p>To access the <strong>GET</strong> method, you must be registered as an admin.
        Please <a href="/register">register as an admin</a> if you haven't already.</p>
    '''


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = db_connection()
        cursor = conn.cursor()
        username = request.form['username']
        password = request.form['password']

        cursor.execute("INSERT INTO Admins (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return "Admin registered successfully!"
    else:
        return render_template_string('''
            <h2>Register as Admin</h2>
            <form method="POST">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Register">
            </form>
        ''')

# GET all patients
@app.route("/GET", methods=["GET", "POST"])
@login_required
def get():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PatientsData')
    patients_data = [
        dict(id=row[0], name=row[1], disease=row[2])
        for row in cursor.fetchall()
    ]
    return jsonify(patients_data)

# GET single patient by id
@app.route("/GET/<int:id>")
def single_get(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PatientsData WHERE id=?", (id,))
    row = cursor.fetchone()
    if row:
        return jsonify(dict(id=row[0], name=row[1], disease=row[2])), 200
    else:
        return "Patient not found", 404

# POST new patient data
@app.route("/POST", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        conn = db_connection()
        cursor = conn.cursor()
        new_name = request.form['name']
        new_dis = request.form['disease']
        sql = """INSERT INTO PatientsData (name, disease) VALUES (?, ?)"""
        cursor.execute(sql, (new_name, new_dis))
        conn.commit()
        return f"Patient with id {cursor.lastrowid} created successfully"
    else:
        return render_template_string('''
            <h2>Add New Patient</h2>
            <form method="POST">
                Name: <input type="text" name="name"><br>
                Disease: <input type="text" name="disease"><br>
                <input type="submit" value="Submit">
            </form>
        ''')

# PUT update patient data
@app.route("/PUT/<int:id>", methods=["GET", "POST"])
def put(id):
    if request.method == "POST":
        conn = db_connection()
        cursor = conn.cursor()
        name = request.form['name']
        disease = request.form['disease']
        sql = """UPDATE PatientsData SET name=?, disease=? WHERE id=?"""
        cursor.execute(sql, (name, disease, id))
        conn.commit()
        return jsonify({'id': id, 'name': name, 'disease': disease})
    else:
        return render_template_string(f'''
            <h2>Update Patient Data (ID: {id})</h2>
            <form method="POST">
                Name: <input type="text" name="name"><br>
                Disease: <input type="text" name="disease"><br>
                <input type="submit" value="Update">
            </form>
        ''')

# DELETE patient data
@app.route("/DELETE/<int:id>")
def delete(id):
    conn = db_connection()
    cursor = conn.cursor()
    sql = """DELETE FROM PatientsData WHERE id=?"""
    cursor.execute(sql, (id,))
    conn.commit()
    return f"The patient data with id {id} has been deleted.", 200

if __name__ == '__main__':
    app.run(debug=True)