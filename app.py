#####################
# PixelGram Backend #
#####################

# Includes
from flask import Flask, render_template, json, redirect, session, request
from flask.ext.mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()

# 504 bit session key
app.secret_key  = '?KzNp>j0-7ec;4c9zG]@tjrBy3uCZNeEsDFm*!%buG7A97?#3ANL*97;D?(jpe9'

# Config MySQL
# Don't run as root in production!

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pythondev'
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

@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        
        # Read values posted from page
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
    
        # Validate received values
        if _name and _email and _password:
        
            # Contact MySQL and set cursor
            # MySQLdb handles opening and closing the connection as needed
            cur = mysql.connection.cursor()
        
            # We need to hash a salted password to store it securely
            _hashed_password = generate_password_hash(_password)
        
            # Call MySQL procedure to create user
            cur.callproc('sp_createUser', (_name, _email, _hashed_password))
        
            # Fetch from cursor
            rv = cur.fetchall()
            
            if len(rv) is 0:
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

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    
    # Read values posted from page
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
    
        # Connect to MySQL, set cursor and call proc
        cur = mysql.connection.cursor()
        cur.callproc('sp_validateLogin', (_username,))
    
        # Fetch from cursor
        rv = cur.fetchall()
    
        # If entry exists, check password matches stored hash
        if len(rv) > 0:
            if check_password_hash(str(rv[0][3]), _password):
                
                # Set user session id and redirect
                session['user'] = rv[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html', error = 'Invalid Email/Password combination.')
        else:
            return render_template('error.html', error = 'Invalid Email/Password combination.')
        
    except Exception as e:
        return render_template('error.html', error = str(e))
    
    finally:
        cur.close()
        
@app.route('/userHome')
def userHome():
    
    # Only allow logged in users
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error = 'Please Login to access the user home.')
@app.route('/logout')
def logout():
    
    # Set user session to null
    session.pop('user', None)
    return redirect('/')

@app.route('/showNewPost')
def showNewPost():
    return render_template('newPost.html')

@app.route('/addNewPost', methods=['POST'])
def addNewPost():
    try:
        if(session.get('user')):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
            
            print (_title, " ", _description, " ", _user)
            
            # Connect to MySQL, set cursor and call proc
            cur = mysql.connection.cursor()
            cur.callproc('sp_newPost', (_title, _description, _user))        
            # Fetch from cursor
            rv = cur.fetchall()
            
            if len(rv) is 0:
                mysql.connection.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html', error = 'An error occurred!')
        else:
            return render_template('error.html', error = 'Unauthorised Access!')
        
    except Exception as e:
        print (str(e))
        return render_template('error.html', error = str(e))
    
    finally:
        cur.close()

@app.route('/getPost')
def getPost():
    try:
        if session.get('user'):
            _user = session.get('user')
            
            # Connect to MySQL and fetch all posts for user
            cur = mysql.connection.cursor()
            cur.callproc('sp_getPostByUser', (_user,))
            posts = cur.fetchall()
            
            posts_dict = []
            for post in posts:
                post_dict = {
                    'Id': post[0],
                    'Title': post[1],
                    'Description': post[2],
                    'Date': post[4]}
                posts_dict.append(post_dict)

            return json.dumps(posts_dict)
        else:
            # This is a poor way to return an error, need to return JSON and have ajax check for it
            return render_template('error.html', error = 'Unauthorised access')
        
    except Exception as e:
        return render_template('error.html', error = str(e))
    
    finally:
        cur.close()
    
# Check if executed file is main program & run app locally for debugging
if __name__ == "__main__":
    app.run(debug=True)