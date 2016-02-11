#
#PaperLoop Backend
#

#Vulnerable to SQL injection. Needs validation implementing.


from flask import Flask, render_template, json, request
app = Flask(__name__)

# App routing
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    # Read values posted from UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    
    # Validate received values
    if _name and _email and _password:
        # Lazy return for now
        return json.dumps({'html':'<span>All fields good!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

# Check if executed file is main program & run app
if __name__ == "__main__":
    app.run()