from flask import Flask,render_template,request,flash,redirect,session
from dbhelper import *

app = Flask(__name__)
app.secret_key="brixespinosa"
upload_folder="static/images"
app.config["UPLOAD_FOLDER"]=upload_folder

@app.route("/upload", methods=['POST','GET'])
def upload():
	if request.method=="POST":
		file = request.files['webcam']
		
		idno = request.args.get("idno")
		lastname = request.args.get("lastname")
		firstname = request.args.get("firstname")
		course = request.args.get("course")
		level = request.args.get("level")
		
		imagename=upload_folder+"/"+idno+".jpg"
		
		file.save(imagename)
		okey: bool = addrecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level,image=imagename)
		return redirect("/")

@app.route("/deletestudent",methods=["GET"])
def deletestudent():
	idno: str = request.args.get("idno")
	okey: bool = deleterecord('student',idno=idno)
	if okey:
		flash("Student "+idno+" is Deleted !")
		return redirect("/main")

		
@app.route("/savestudent",methods=["POST"])
def savestudent():
	idno: str = request.form["idno"]
	lastname: str = request.form["lastname"]
	firstname: str = request.form["firstname"]
	course: str = request.form["course"]
	level: str = request.form["level"]
	images = upload_folder+"/"+"default"+".jpg"
	rows = getrecord('student', idno=idno)
	#
	if rows ==None:
		okey: bool = addrecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level,image=images)			
		if okey:	
			flash("New Student Added ")
			return redirect("/main")
	else:
		okey: bool = updaterecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)		
		if okey:
			flash("Student Updated! ")
			return redirect("/main")

@app.after_request
def after_request(response):
	response.headers["Cache-Control"]="no-cache, no-store,must-revalidate"
	return response

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")


@app.route("/main")
def main():
    if "logged_user" in session:
        header: list = ['idno','lastname','firstname','course','level','action']
        stlist: list = getallrecord('student')
        return render_template("main.html",pagetitle='STUDENT LIST',studentlist=stlist,head=header,topheader='STUDENT LIST')
    else:
        flash("Login Properly! ")
        return redirect("/")

@app.route("/login",methods=['POST'])
def login():
    uname: str = request.form["username"]
    pword: str = request.form["password"]
    user: dict = userlogin('account',username=uname,password=pword)
    if user!=None:
        session["logged_user"]=user["username"]
        flash("Login Successful!")
        return redirect("/main")
    else:
        flash("Login Failed!")
        return redirect("/")

@app.route("/")
def index():
    return render_template("login.html",title='STUDENT LIST')

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
