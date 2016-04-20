#####################
# PixelGram Backend #
#####################
#   application.py  #
#####################

# Includes
import os, uuid

from flask import Flask, render_template, json, redirect, session, request
from flask.ext.mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash, secure_filename

import resizr

application = Flask(__name__)
mysql = MySQL()

# 504 bit session key
application.secret_key  = '?KzNp>j0-7ec;4c9zG]@tjrBy3uCZNeEsDFm*!%buG7A97?#3ANL*97;D?(jpe9'

# Config MySQL
# Don't run as root in production!

application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = 'pythondev'
application.config['MYSQL_DB'] = 'PixelGram'
application.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(application)

# Define uploads folder and allowed file types - Should not be changed for now!
application.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpg'])

# Check the uploads folder exists, otherwise create it
print("INFO: Checking if upload folder exists")
if not os.path.exists(application.config['UPLOAD_FOLDER']):
    try:
        print("WARN: Upload folder does not exist, creating it")
        os.makedirs(application.config['UPLOAD_FOLDER'])
    except Exception as e:
        print(e)
        
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# App routing
@application.route('/')
def main():
    # If already logged in, redirect to the feed
    if session.get('user'):
        return redirect('/showFeed')
    # Otherwise show the homepage
    else:
        return render_template('index.html')

@application.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@application.route('/signUp', methods=['POST'])
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
                return json.dumps({'message':'User create success! You may now log in.'})
            else:
                return json.dumps({'error':str(rv[0])})
        else:
            return json.dumps({'message':'Error: Enter the required fields'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})

@application.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@application.route('/validateLogin', methods=['POST'])
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
        
@application.route('/userHome')
def userHome():
    
    # Only allow logged in users
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error = 'Please Login to access the user home.')
@application.route('/logout')
def logout():
    
    # Set user session to null
    session.pop('user', None)
    return redirect('/')

@application.route('/showNewPost')
def showNewPost():
    return render_template('newPost.html')

@application.route('/addNewPost', methods=['POST'])
def addNewPost():
    #try:
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
            # Commit the post
            mysql.connection.commit()

            # Resize uploaded image 
            devices = resizr.ResizeForAll(_filePath)

            # Add resized image paths to database
            cur.execute("SELECT post_id FROM tbl_post WHERE post_file_path = %s", (_filePath,))
            postid = cur.fetchall()
            
            for device in devices:
                cur.execute("INSERT INTO tbl_postdevices (post_id, device_id) VALUES (%s, %s)", (postid[0][0], device))
                
            mysql.connection.commit()
            return redirect('/userHome')
        else:
            return render_template('error.html', error = 'An error occurred!')
    else:
        return render_template('error.html', error = 'Unauthorised Access!')
        
    #except Exception as e:
    #    print (str(e))
    #    return render_template('error.html', error = str(e))
    
    #finally:
    #    cur.close()

@application.route('/getPost')
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
        
@application.route('/getPostById', methods=['POST'])
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
    
@application.route('/updatePost', methods=['POST'])
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
                
                # Resize uploaded image 
                devices = resizr.ResizeForAll(_filePath)
                
                # Clear any existing entries
                cur.execute("DELETE FROM tbl_postdevices WHERE post_id = %s", (_post_id,))
                mysql.connection.commit()
 
                for device in devices:
                    cur.execute("INSERT INTO tbl_postdevices (post_id, device_id) VALUES (%s, %s)", (_post_id, device))

                mysql.connection.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        # TODO: Fix this so that an error doesn't kill the server
        cur.close()
        
@application.route('/deletePost', methods=['POST'])
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
    
@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Determine the extension of the file
            extension = os.path.splitext(file.filename)[1]

            # Generate unique filename
            f_name = str(uuid.uuid4()) + extension

            # Check the upload folder exists, otherwise create it
            # Check the uploads folder exists, otherwise create it
            print("INFO: Checking if upload folder exists")
            if not os.path.exists(application.config['UPLOAD_FOLDER']):
                try:
                    print("WARN: Upload folder does not exist, creating it")
                    os.makedirs(application.config['UPLOAD_FOLDER'])
                except Exception as e:
                    print(e)

            # Save file
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], f_name))

            # Resize file 
            #devices = resizr.ResizeForAll(application.config['UPLOAD_FOLDER'] + "/" + f_name)
            #print(devices)

            return json.dumps({'filename':f_name})
        else:
            return json.dumps({'error':'Invalid filetype, JPG only!'})
    
@application.route('/showFeed')
def showFeed():
    return render_template('feed.html')

@application.route('/getAllPosts')
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

@application.route('/addUpdateLike', methods=['POST'])
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
    
@application.route('/getImageSizes', methods=['POST'])
def getImageSizes():
    if session.get('user'):
        # Request the image ID to query
        _post_id = request.form['post']        
        
        # Return the UUID of the post's image
        cur = mysql.connection.cursor()
        cur.execute("SELECT post_file_path FROM tbl_post WHERE post_id = %s", (_post_id,))
        rv = cur.fetchall()
        if len(rv) > 0:
            uuid = os.path.split(rv[0][0])[1]
        else:
            cur.close()
            return json.dumps({'error':'Post does not exist in database'})
        
        # Return available device IDs for post
        cur.execute("SELECT device_id FROM tbl_postdevices WHERE post_id = %s", (_post_id,))
        availableDevices = cur.fetchall()

        # Query devices.json to match device id to device name
        with open('devices.json', 'r') as data_file:
            json_obj = json.load(data_file)
        
        # Create data structure for posts from  returned data
        post_devices_dict = []
        for post in availableDevices:
            
            # Generate device name and file path
            deviceName = json_obj['device'][post[0]]['name']
            filePath = application.config['UPLOAD_FOLDER'] + "/" + str(post[0]) + "/" + uuid
            
            post_dict = {
                'Device': deviceName,
                'FilePath': filePath
            }
            post_devices_dict.append(post_dict)
        cur.close()
        # Return data struct to browser
        return json.dumps(post_devices_dict)        
    
# If running from Python CLI, run on local debugging server
if __name__ == "__main__":
    application.run(debug=True)