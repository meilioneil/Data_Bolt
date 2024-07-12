from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/information')
def information():
    return render_template('information.html')

if __name__ == '__main__':
    app.run(debug=True)
