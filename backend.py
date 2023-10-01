from flask import Flask,render_template,url_for,redirect,request,session
from pymongo import MongoClient
import secrets
app=""
# Generate a random 32-character hexadecimal string
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = "4c15ecd572abf8862666257ae104126084a1202187b925bd4dd99e1990ec6254"

    print(app.secret_key)
    app.config['MONGO_URI'] = 'mongodb+srv://maheshduggi456:Mahesh123@murali.ztmq9oy.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'
    return app
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.get_database('Murali')
users_collection = db['Users']
admin_collection = db['admin']
data_collection = db['Brands']
booking_collection  = db['Bookings']

@app.route('/addon',methods=['GET','POST'])
def addon():
    if request.method=='POST':
        data_collection.insert_one(
        {
            "brand" : request.form['bname'],
            "cost" : request.form['bcost']
        })
        return render_template('admin.html',msg="Success")
    else:
        return render_template('admin.html')
@app.route('/changeon',methods=['POST'])
def changeon():
    if request.method=='POST':
        filter_criteria = {"brand": request.form['bname']}
        update_operation = {
        "$set": {
            "brand": request.form['bname'],            # Update the age field
            "cost": request.form['bcost']  # Update the email field
        }
    }

    # Update a single document that matches the filter criteria
    result = data_collection.update_one(filter_criteria, update_operation)

    # Check if the update was successful
    if result.modified_count > 0:
        return render_template('admin.html',msg="Sucess")
    else:
        return render_template('admin.html',msg="Fail")
    




@app.route('/delon',methods=['POST'])
def delon():
    if request.method=='POST':
        filter_criteria = {"brand": request.form['bname']}
        result = data_collection.delete_one(filter_criteria)
        if result.deleted_count > 0:
            return render_template('admin.html',msg="Sucess")
        else:
            return render_template('admin.html',msg="Fail")



@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        u_email = request.form['email']
        u_pass = request.form['passwd']
        u_phone = request.form['Phonenum']
        u_name = request.form['name']
        existing_user = users_collection.find_one({'email': u_email})
        if existing_user:
            return render_template('signin.html',msg="Email exists, Try with different email")
        else:
            # Insert the user into the MongoDB database
            user_data = {'name':u_name,'phone':u_phone  ,'email': u_email, 'password': u_pass}
            users_collection.insert_one(user_data)
            return render_template('login.html',msg="Signup sucess")
            
    return render_template('signin.html')
@app.route('/display_data')
def display_data():
    data = booking_collection.find()
    return render_template('admin.html',bd=data)
@app.route('/book',methods=["POST","GET"])
def book():
    if request.method=="POST":
        print(request.form)
        u_name = request.form['Name']
        t_data ={
            "user_name" : u_name,
            "user_phonenumber" : request.form['Phonenum'],
            "user_email" : request.form['Email'],
            "Brand" : request.form['Brand'],
            "Quantity" : request.form['quantity'],
            "Date" : request.form['Date'],
            "user_Address" : request.form['address']
        }
        booking_collection.insert_one(t_data)
        data = data_collection.find()
        return render_template('index.html',msg="Booking confirmed",Jobs=data)
    else:
        return render_template('Booking.html')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['passwd']
        admin = admin_collection.find_one({'email': email, 'password': password})
        if admin:
            session['username'] = admin['name']
            session['user_logged_in'] = True
            return render_template('admin.html',msg="Hlo!! "+admin['name'])
        else:
            user = users_collection.find_one({'email': email, 'password': password})
            print(user)
            if user:
                session['username'] = user['name']
                session['user_logged_in'] = True
                data = data_collection.find()
                return render_template('index.html',msg="Hlo!! "+user['name'],Jobs=data)
            else:
                return render_template('login.html',msg="Login failed. Please check your email and password.")
            
    return render_template('login.html')
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')
@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    return redirect(url_for('home'))
@app.route('/')
def home():
    data = data_collection.find()
    
    return render_template('index.html',Jobs=data)

if __name__ == "__main__":
    app.run(debug=True)