from flask import Flask, render_template, request, redirect 
from models import db
import os
from models import User
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search', '')
    if search != "":
        return render_template('search.html', search=search)
    
    return render_template("/index.html")

    


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        if not userid and not password:
            return render_template('login.html', warning="Enter User ID and Password")
        elif not userid :
            return render_template('login.html', warning="Enter User ID")
        elif not password :
            return render_template('login.html', warning="Enter Password")
        else:
            return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        userid = request.form.get('userid') 
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password)
        if not (userid and username and password and re_password) :
            return render_template('register.html', warning="Enter all")
        elif password != re_password:
            return render_template('register.html', warning="Password confirm isn't correct")
        else: 
            user = User()         
            user.password = password          
            user.userid = userid
            user.username = username      
            db.session.add(user)
            db.session.commit()
            return "/login"

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__)) 
    dbfile = os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

    db.init_app(app)
    db.app = app
    with app.app_context():
        db.create_all()


    app.run(host='127.0.0.1', port=5000, debug=True) 