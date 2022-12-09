from flask import Flask, request, redirect, session, url_for,flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_session import Session
from datetime import date, time, datetime,timedelta
from time import time, sleep
from werkzeug.security import generate_password_hash, check_password_hash

today = datetime.now()


app = Flask(__name__)
app.debug = True
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key='dinesh'
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
# Settings for migrations
migrate = Migrate(app, db)



class track(db.Model):
	current_date = db.Column(db.Date,primary_key=True)
	Total=db.Column(db.Integer, unique=False, nullable=False)
	def __repr__(self):
		return f"Total : {self.Total}"

# @app.route('/update')
# def update():
# 	start=track.query.all()
# 	for data in start:
# 		start_date=datetime.date(data.current_date)
# 	if(today.date()>start_date):
# 		day=today-start_date
# 		day=day.days
# 		start_date+=timedelta(days=day)
# 		data.current_date=start_date
# 		db.session.commit()
# 		return 'success'
		



# @app.route('/adddate')
# def adddate():
# 	current_date=datetime(2020,9,9)
# 	Total=0
# 	p=track(current_date=current_date,Total=Total)
# 	db.session.add(p)
# 	db.session.commit()
# 	return('added')

class Centre(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Name = db.Column(db.String(50), unique=False, nullable=False)
	dose = db.Column(db.Integer,unique=False, nullable=True)
	Address = db.Column(db.String(50), unique=False, nullable=False)
	pincode = db.Column(db.Integer, unique=False, nullable=False)
	
	# repr method represents how one object of this datatable
	# will look like
	def __repr__(self):
		return f"Name : {self.Name}, Age: {self.Address}"


# Models User Table
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), unique=False, nullable=False)
	last_name = db.Column(db.String(20), unique=False, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	gender = db.Column(db.String(20),unique=False,nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	pas = db.Column(db.String(255), unique=False, nullable=False)
	status = db.Column(db.String(5), unique=False,nullable=False)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	@password.setter
	def password(self, password):
		self.pas = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.pas, password)


#Models Admin Table
class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), unique=False, nullable=False)
	last_name = db.Column(db.String(20), unique=False, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	role=db.Column(db.String(20),nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	pas = db.Column(db.String(20), unique=False, nullable=False)
    

	# repr method represents how one object of this datatable
	# will look like
	def __repr__(self):
		return f"Name : {self.first_name}, Age: {self.age}"

# @app.route('/addadmin')
# def add():
# 	p=Admin(first_name='Dinesh',last_name='kumar',age=21,role='Senior Doctor',email='dineshkumar@gmail.com',pas='meghana')
# 	db.session.add(p)
# 	db.session.commit()
# 	return redirect('/')

# @app.route('/adduser')
# def add():
# 	p=User(first_name='Dinesh',last_name='kumar',age=21,gender='Male',email='dineshkumar@gmail.com',pas='meghana')
# 	db.session.add(p)
# 	db.session.commit()
# 	return redirect('/')

#home
@app.route('/')
def home():
	return render_template('index.html')
# def update():
# 	start_date=datetime(2020,9,9)
# 	if(today>start_date):
# 		return("yes")
# 	start_date=today

#admin login
@app.route('/admin')
def admin():
    return render_template('admin.html')


#user login
@app.route('/user')
def user():
    return render_template('user.html')


#User Authentication
@app.route('/verifyuser',methods=['GET','POST'])
def verifyuser():
	user_name = request.form.get("email")
	pas = request.form.get("pas")
	users = User.query.all()
	flag=1
	u=User()
	u.password=pas
	for data in users:  
		if(data.email == user_name and u.verify_password(pas)):
			status=data.status
			session['user']=data.first_name
			flag=0
			return redirect(url_for('sess'))
			
	if(flag):
		return render_template('user.html',login_result="Invalid Username or Password")


@app.route('/sess')
def sess():
    if 'user' in session:
        user_name=session['user']
        # name=User.query.all()
        # for data in name:
            # if(data.email==user_name):
        return render_template("user_home.html",b=True,name=user_name,msg="Welcome aboard, Hope you are doing well!",head= "Free Covid Precaution Dose" ,msg1="Now Precaution dose for 18-59 age group free at Government Vaccination Centre.")
    else:
        return redirect(url_for('verifyuser'))


@app.route('/reg')
def reg():
	return render_template('register.html')

# register users to database
@app.route('/register', methods=["POST"])
def register():
	first_name = request.form.get("first_name")
	last_name = request.form.get("last_name")
	age = request.form.get("age")
	gender = request.form.get("gender")
	email = request.form.get('email')
	pas=request.form.get('pas')
	u=User()
	u.password=pas
	try:
		if first_name != '' and last_name != '' and age is not None and email != '' and pas != '' :
			p = User(first_name=first_name, last_name=last_name, age=age,gender=gender,email=email,pas=u.pas,status=True)
			db.session.add(p)
			db.session.commit()
			session['user']=first_name
			return redirect(url_for('sess'))
		else:
			return render_template('register.html',login_result="Enter Valid Details")
	except:
		return render_template('register.html',login_result="email was already registered")

@app.route('/searchcentres',methods=['POST'])
def searchcentres():
	if 'user' in session:
		name = request.form.get("centre")
		centres = Centre.query.all()
		return render_template('searchcentres.html',centres=centres,idd=int(name))
	else:
		return redirect('verifyuser')

@app.route('/apply/<int:id>')
def apply(id):

	if 'user' in session:
		user_name=session['user']
		data=Centre.query.get(id)
		if(data.dose<10):
			data.dose+=1
			db.session.commit()
			return render_template('searchcentres.html',n=user_name,response="Applied Successfully",msg="Success ")
		else:
			return render_template('searchcentres.html',responsefailed="Sorry for the Inconvenience, Daily limit was Exceeded for this particular centre")


	else:
		return render_template('searchcentres.html',response="Applied Successfully")


		

	
@app.route('/book')
def book():
	if 'user' in session:
		user_name=session['user']
		centres = Centre.query.all()
		return render_template('searchcentres.html',n=user_name,centres=centres,msg="Book Your Slot")
	return redirect('verifyadmin')




#Admin Authentication
@app.route('/verifyadmin',methods=['GET','POST'])
def verifyadmin():
	user_name = request.form.get("email")
	pas = request.form.get("pas")
	admins = Admin.query.all()
	flag=1
	for data in admins:
		if(data.email == user_name and data.pas==pas):
			session['user']=user_name
			flag=0
			return redirect(url_for('sessadmin'))
			
	if(flag):
		return render_template('admin.html',login_result="Invalid Username or Password")

@app.route('/sessadmin')
def sessadmin():
    if 'user' in session:
        user_name=session['user']
        return render_template("admin_home.html",sum=sum)
    else:
        return redirect(url_for('verifyadmin'))

@app.route('/adhome')
def adhome():
	if 'user' in session:
		centres=Centre.query.all()
		sum=0
		for data in centres:
			sum+=data.dose
		return render_template('ad_home.html',sum=sum)
	else:
		return redirect('verifyadmin')

@app.route('/update')
def update():
	if 'user' in session:
		centres=Centre.query.all()
		for data in centres:
			data.dose=0
			db.session.commit()
		return render_template('admin_home.html',update_result='Updated Successfully')
	# return render_template('searchcentres.html',response="Applied Successfully",msg="Success ")
	else:
		return redirect('verifyadmin')

@app.route('/Add_VC')
def Add_VC():
	
	if 'user' in session:
		return render_template("Add_VC.html")
	else:
		return redirect('verifyadmin')
	
@app.route('/VC',methods=['POST'])
def VC():
	try:
		if 'user' in session:
			dose=request.form.get("dose")
			id = request.form.get("id")
			Name = request.form.get("Name")
			Address = request.form.get("Address")
			pincode = request.form.get("pincode")
			
			# create an object of the Profile class of models and
			# store data as a row in our datatable
			if Address != '' and Name != '' and pincode is not None:
				vc = Centre(id=id,Name=Name,dose=dose, Address=Address,pincode=pincode)
				db.session.add(vc)
				db.session.commit()
				return render_template("Add_VC.html",addresult='Added Successfully')
			else:
				return render_template("Add_VC.html",addresult="Enter Valid Details")

		else:
			return redirect('verifyadmin')
	except:
		return render_template("Add_VC.html",addresult="Centre ID was already created")


# @app.route('/Remove_VC',methods=['POST'])
# def Remove_VC():
	
# 	return render_template('rem.html')

@app.route('/RVC')
def RVC():
	if 'user' in session:
		centres = Centre.query.all()

		return render_template('Remove_VC.html', centres=centres) 
	else:
		return redirect('verifyadmin')

@app.route('/search',methods=['POST'])
def search():
	if 'user' in session:
		name = request.form.get("centre")
		centres = Centre.query.all()
		return render_template('rem.html',centres=centres,name=int(name))
	else:
		return redirect('verifyadmin')

@app.route('/dosage')
def dosage():
	if 'user' in session:
		centres = Centre.query.all()
		return render_template('dosage.html',centres=centres) 
	else:
		return redirect('verifyadmin')


@app.route('/logout')
def logout():
	session.pop('user',None)
	return render_template('index.html')


#for deleting row in model or table
@app.route('/delete/<int:id>')
def delete(id):
	if 'user' in session:
		# deletes the data on the basis of unique id and
		# directs to home page
		data = Centre.query.get(id)
		db.session.delete(data)
		db.session.commit()
		return render_template('Remove_VC.html',update_result='Removed Successfully')
	else:
		return redirect('verifyadmin')



@app.route('/user_admin_tables')
def user_admin_tables():
	users = User.query.all()
	return render_template('user_admin_tables.html',users=users)

if __name__ == '__main__':
	app.run()

