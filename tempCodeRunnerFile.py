def index():
    if request.method=='POST':
        
        task_content = request.form['content']
        
        new_employee = Employee(content= str(task_content))
      
        
        db.session.add(new_employee)
        db.session.commit()
        return redirect('/')
            
       

    else:
        Employees=Employee.query.order_by(Employee.id).all()
        return render_template('index.html',Employees=Employees)