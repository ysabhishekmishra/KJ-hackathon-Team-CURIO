from flask import Flask,render_template,request,redirect,session,flash
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)
conn=mysql.connector.connect(host="localhost",user="root",database="kjhackathon")
cursor=conn.cursor()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 'user_data' in session:
        flash('You were successfully logged in')
        user_id = session['user_data'][0][0]
        print(user_id)
        cursor.execute("select * from signupdata where id='{}'".format(user_id))
        user_data = cursor.fetchall()
        print(user_data)
        return render_template("dashboard.html",data=user_data)
    else:
        return redirect('/login')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM signupdata Where email Like '{}' and password like '{}'""".format(email,password))
    userdata=cursor.fetchall()
    print(userdata)

    if len(userdata)>0:
        session['user_data']=userdata
        return redirect('/dashboard')
    else:
        return redirect('/login') 

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup_validation',methods=['POST'])  
def signup_validation():
    name=request.form.get('uname')
    email= request.form.get('uemail')
    contactnumber=request.form.get('ucontactnumber')
    password= request.form.get('upassword')
    cursor.execute("""INSERT INTO signupdata values('NULL','{}','{}','{}','{}')""".format(name,email,contactnumber,password))
    conn.commit()

    cursor.execute("""SELECT * FROM signupdata WHERE email LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['userdata']=myuser[0][0]
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user_data')
    return redirect('/')



if __name__=='__main__':
    app.run(debug=True)
