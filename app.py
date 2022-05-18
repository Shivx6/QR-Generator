import uuid
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class UUID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), unique=True)
    status = db.Column(db.String(20), nullable=False)

@app.route("/getToken")
def generate_token():
    uid = uuid.uuid4()
    uuid_db = UUID(uuid=str(uid), status="generated")
    db.session.add(uuid_db)
    db.session.commit()
    print(uid)
    result = {'uuid': uid}
    return result


@app.route('/dashboard')
def dashboard():
    return "Logged In successfully"

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    uuid = request.args.get('code')
    db_uuid = UUID.query.filter_by(uuid=uuid).first()
    if db_uuid != None:
        db_uuid.status = 'scanned'
        db.session.commit()
    else:
        message = 'Your code is not valid'
        return render_template('login.html', message=message)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_db = User.query.filter_by(username=username, password=password).first()
        print(user_db)
        if user_db != None:
            db_uuid.status = 'loggedin'
            db.session.commit()
            return redirect('/dashboard')
        else:
            message = "Username or password is incorrect"
            return render_template('login.html', message=message)


    return render_template('login.html')

@app.route('/')
def qr_page():
    return render_template('qrpage.html')

@app.route('/getStatus')
def qr_status():
    uuid = request.args.get('code')
    db_uuid = UUID.query.filter_by(uuid=uuid).first()
    if db_uuid != None:
        return {'status': db_uuid.status}
    else:
        return {'status': 'Invalid ID'}


def createTempUsers():
    kavin = User(username="kavin", password="kavin@123")
    ananth = User(username="anantharam", password="anantharam@123")
    db.session.add(kavin)
    db.session.add(ananth)
    db.session.commit()

if __name__ == "__main__":
    db.create_all()
    # createTempUsers()
    app.run(debug=True)