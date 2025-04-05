from flask import Flask, request, render_template, redirect, url_for
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# Redirect to login page as the default route
@app.route('/')
def index():
    return redirect(url_for('login'))

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication logic (replace with actual logic)
        if username == 'Ujjal' and password == '123':
            return redirect(url_for('hello_world'))
        else:
            error = "Invalid username or password."
            return render_template('login.html', error=error)
    return render_template('login.html')

# Route for the forest fire prediction page
@app.route('/hello_world')
def hello_world():
    return render_template("forest_fire.html")

# Route to handle predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the form data and convert them into an array of integers
    int_features = [int(x) for x in request.form.values()]
    final = [np.array(int_features)]
    
    # Predict the probability of the forest fire
    prediction = model.predict_proba(final)
    output = prediction[0][1]  # The probability of forest fire occurring (1 = fire, 0 = no fire)

    # Compare the probability to 0.5 (threshold for prediction)
    if output > 0.5:
        message = "Your Forest is in Danger."
    else:
        message = "Your Forest is safe."

    # Render the result on the same page
    return render_template('forest_fire.html', alert_message=message)


# Route for Contact Us page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle the form submission logic here (e.g., save to a database or send an email)
        success_message = "Thank you for reaching out! We will get back to you soon."
        return render_template('contact.html', success_message=success_message)
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
