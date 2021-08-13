from flask import Flask, render_template, request, redirect, session
from users import User

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def index():
    print("@/")
    users = User.get_all()
    print(users)
    return render_template("read.html", users=users)

@app.route('/create.html')
def create():
    print('@/create.html')
    return render_template('create.html')

@app.route('/process', methods=["POST"])
def process():
    print("@/process")
    data = {
        'fname' : request.form['first_name'],
        'lname' : request.form['last_name'],
        'email' : request.form['email']
    }
    User.save(data)
    users = User.get_all()
    # Find user in User.get_all by name
    user = None
    for this_user in users:
        if this_user.first_name == request.form['first_name']:
            user = this_user
        # else not found!
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:num>')
def display(num):
    print(f'@/users/{num}')
    session['user_id'] = num
    users = User.get_all()
    # Find user in User.get_all by id
    user = None
    for this_user in users:
        if this_user.id == num:
            user = this_user
        # else not found!
    return render_template('read_one.html', user=user, user_id=session['user_id'])

@app.route('/users/<int:num>/edit')
def edit(num):
    print(f'@/users/{num}/edit')
    users = User.get_all()
    for this_user in users:
        if this_user.id == num:
            user = this_user
        # else not found!
    return render_template('update.html', num=num, user=user)

@app.route('/process_edit', methods=["POST"])
def process_edit():
    print(f'@/process_edit')
    data = {
        'id'    : session['user_id'],
        'fname' : request.form['first_name'],
        'lname' : request.form['last_name'],
        'email' : request.form['email']
    }
    User.update(data)
    return redirect(f'/users/{session["user_id"]}')

@app.route('/delete/<int:num>')
def delete(num):
    print(f'@/delete/{num}')
    data = {'id': num}
    User.delete(data)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
