#
#PixelGram Backend
#

# Includes
from flask import Flask, render_template, json, request
from flask.ext.mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()

# Config MySQL
# 
# You need to change these details to your own database, user and password.
# Don't run as root in production!

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'uxwlcxxx'
app.config['MYSQL_DB'] = 'PixelGram'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

# App routing
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST','GET'])
def signUp():
    try:
        
        # Read values posted from UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
    
        # Validate received values
        if _name and _email and _password:
        
            # Contact MySQL and set cursor
            #connection = mysql.connect()
            cur = mysql.connection.cursor()
        
            # We need to hash a salted password to store it securely
            _hashed_password = generate_password_hash(_password)
        
            # Call MySQL procedure to create user
            cur.callproc('sp_createUser', (_name, _email, _hashed_password))
        
            # Commit changes to db
            rv = cur.fetchall()
                
            if len(rv) is 0:
                print("Got this far! \n")
                mysql.connection.commit()
                return json.dumps({'message':'User create success!'})
            else:
                return json.dumps({'error':str(rv[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cur.close()

# Check if executed file is main program & run app locally for debugging
if __name__ == "__main__":
    app.run(debug=True)