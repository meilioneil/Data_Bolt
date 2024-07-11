from flask import Flask, render_template

app = Flask(__name__, static_folder="./static")

@app.route("/")

def home():
    
    events = ["archery", "artistic gymnastics", "artistic swimming", "athletics", "badminton", "basketball", "basketball 3x3", "beach volleyball", "boxing", "breaking", "canoe slalom", "canoe sprint", "cycling bmx freestyle", 'cycling bmx racing', 'cycling mountain bike', 'cycling road', 'cycling road', 'cycling track', 'diving', 'equestrian', 'fencing', 'football', 'golf', 'handball', 'hockey', 'judo', 'marathon swimming', 'modern pentathlon', 'rhythmic gymnastics', 'rowing', 'rugby sevens', 'sailing','shooting','skateboaring','sport climbing','surfing','swimming','table tennis', 'taekwando', 'tennis','trampoline', 'triathlon', 'volleyball','water polo', 'weightlifting', 'wrestling']
    
    sections = [f'{i.title()}' for i in events]  # Generate sections dynamically
    return render_template('index.html', sections=sections)

app.run()