from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)



class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    assigned_tasks = db.relationship('Task', backref='employee', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'assigned_tasks': [task.to_dict() for task in self.assigned_tasks]
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description
        }




with app.app_context():
    db.create_all()
CORS(app)




@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        task_content = request.form['content']

        new_employee = Employee(name=str(task_content))

        db.session.add(new_employee)
        db.session.commit()
        return redirect('/')

    else:
        Employees = Employee.query.order_by(Employee.id).all()
        return render_template('index.html', Employees=Employees)


@app.route('/api')
def get_employees():
    Employees = Employee.query.order_by(Employee.id).all()
    Employees_list=[Employee.to_dict(employee) for employee  in Employees]
    return jsonify(Employees_list)

@app.route('/delete_employee/<int:entry_id>', methods=['POST'])
def delete_entry_by_id(entry_id):
    entry = Employee.query.get(entry_id)
    if entry:

        db.session.delete(entry)
        db.session.commit()
        return redirect('/')
    else:
        return False
@app.route('/delete_task/<int:entry_id>', methods=['POST'])
def delete_task(entry_id):
    entry = Task.query.get(entry_id)
    if entry:

        db.session.delete(entry)
        db.session.commit()
        return redirect('/')
    else:
        return jsonify("Task doesn't exist")
    pass
    
@app.route('/add_task/<int:employee_id>', methods=['POST'])
def add_task(employee_id):
    entry = Employee.query.get(employee_id)
    if entry:
        task_content = request.form['content']
        new_task = Task(employee_id=employee_id, description=str(task_content))
        db.session.add(new_task)
        db.session.commit()

        # Instead of redirecting, return the updated data as JSON
        
        return redirect('/')
    else:
        return "Employee not found"



if __name__ == '__main__':
    app.run(debug=True)
