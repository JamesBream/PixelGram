#####################
# PixelGram Backend #
#####################
#       app.py      #
#####################

# Includes
import os, uuid
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

app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Check the uploads folder exists, otherwise create it
print("INFO: Checking if upload folder exists")
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    try:
        print("WARN: Upload folder does not exist, creating it")
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except Exception as e:
        print(e)

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
            cur.close()
            if len(rv) is 0:
                mysql.connection.commit()
                return json.dumps({'message':'User create success!'})
            else:
                return json.dumps({'error':str(rv[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})

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
                return redirect('/showFeed')
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
            _filePath = request.form['filePath']
            
            print (_title, " ", _description, " ", _user)
            
            # Connect to MySQL, set cursor and call proc
            cur = mysql.connection.cursor()
            cur.callproc('sp_newPost', (_title, _description, _user, _filePath))        
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
        
@app.route('/getPostById', methods=['POST'])
def getPostById():
    try:
        if session.get('user'):
            
            _id = request.form['id']
            _user = session.get('user')
            
            cur = mysql.connection.cursor()
            cur.callproc('sp_getPostById', (_id, _user))
            rv = cur.fetchall()
            
            # Convert returned post to list
            post = []
            post.append({'Id':rv[0][0],'Title':rv[0][1],'Description':rv[0][2],'FilePath':rv[0][5]})
            
            return json.dumps(post)
        else:
            return render_template('error.html', error = 'Unauthorised access')
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cur.close()
    
@app.route('/updatePost', methods=['POST'])
def updatePost():
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _post_id = request.form['id']
            _filePath = request.form['filePath']
            
            cur = mysql.connection.cursor()
            cur.callproc('sp_updatePost', (_title, _description, _post_id, _user, _filePath))
            
            rv = cur.fetchall()
            
            if len(rv) is 0:
                mysql.connection.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        # TODO: Fix this so that an error doesn't kill the server
        cur.close()
        
@app.route('/deletePost', methods=['POST'])
def deletePost():
    if session.get('user'):
        _post_id = request.form['id']
        _user = session.get('user')
        
        cur = mysql.connection.cursor()
        cur.callproc('sp_deletePost', (_post_id, _user))
        
        rv = cur.fetchall()
        
        if len(rv) is 0:
            mysql.connection.commit()
            return json.dumps({'status':'OK'})
        else:
            return json.dump({'status': 'Error'})
        cur.close()
    else:
        return render_template('error.html', error = "Unauthorised access!")
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        
        # Determine the extension of the file
        extension = os.path.splitext(file.filename)[1]
        
        # Generate unique filename
        f_name = str(uuid.uuid4()) + extension
        
        # Check the upload folder exists, otherwise create it
        # Check the uploads folder exists, otherwise create it
        print("INFO: Checking if upload folder exists")
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
        try:
            print("WARN: Upload folder does not exist, creating it")
            os.makedirs(app.config['UPLOAD_FOLDER'])
        except Exception as e:
            print(e)
        
        # Save file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        
        return json.dumps({'filename':f_name})
    
@app.route('/showFeed')
def showFeed():
    return render_template('feed.html')

@app.route('/getAllPosts')
def getAllPosts():
    try:
        if session.get('user'):
            _user = session.get('user')
            
            # Open MySQL connnection and call SP
            cur = mysql.connection.cursor()
            cur.callproc('sp_getAllPosts', (_user,))
            rv = cur.fetchall()
            
            # Create data structure for posts from  returned data
            posts_dict = []
            for post in rv:
                post_dict = {
                    'Id': post[0],
                    'Title': post[1],
                    'Description': post[2],
                    'FilePath': post[3],
                    'Like': post[4],
                    'HasLiked': post[5]
                }
                posts_dict.append(post_dict)
                
            cur.close()
            # Return data struct to browser
            return json.dumps(posts_dict)
        else:
            return render_template('error.html', error = "Unauthorised Access")
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/addUpdateLike', methods=['POST'])
def addUpdateLike():
    if session.get('user'):
        _postId = request.form['post']
        _like = request.form['like']
        _user = session.get('user')
        
        cur = mysql.connection.cursor()
        cur.callproc('sp_AddUpdateLikes', (_postId, _user, _like))
        rv = cur.fetchall()
        
        if len(rv) is 0:
            mysql.connection.commit()
            cur.close()
        else:
            cur.close()
            return render_template('error.html', error = "An error occurred!")
        
        cur = mysql.connection.cursor()
        cur.callproc('sp_getLikeStatus', (_postId, _user))
        rv = cur.fetchall()
        cur.close()
        
        return json.dumps({'status':'OK', 'total':rv[0][0], 'likeStatus':rv[0][1]})
        
    else:
        return render_template('error.html', error = "Unauthorised access")
    
# Check if executed file is main program & run app locally for debugging
if __name__ == "__main__":
    app.run(debug=True)