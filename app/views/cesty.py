from app import app

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'