from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

# Wait for MySQL Container
for i in range(10):
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root123",
            database="employeedb"
        )
        break
    except:
        time.sleep(5)

cursor = db.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(100)
)
""")

@app.route('/')
def home():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']

    query = "INSERT INTO employees (name, email, department) VALUES (%s, %s, %s)"
    values = (name, email, department)

    cursor.execute(query, values)
    db.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
