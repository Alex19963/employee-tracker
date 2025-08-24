from flask import Flask, render_template
from models import db, Employee, Shift
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/admin/dashboard')
def admin_dashboard():
    employees = Employee.query.all()
    status_data = []
    for emp in employees:
        last_shift = Shift.query.filter_by(employee_id=emp.id).order_by(Shift.start_time.desc()).first()
        if last_shift and last_shift.end_time is None:
            status = 'on'
            last_time = last_shift.start_time
        else:
            status = 'off'
            last_time = last_shift.end_time if last_shift else None
        status_data.append({
            'id': emp.id,
            'name': emp.name,
            'status': status,
            'last_time': last_time
        })
    return render_template('admin_dashboard.html', employees=status_data)

if __name__ == '__main__':
    app.run(debug=True)
