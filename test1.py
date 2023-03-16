from flask import Flask, render_template, request

app = Flask(__name__)

# Load the dataset
#df = pd.read_csv('dataset.csv')

# Define the routes for the different tasks
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
