from app import app

# Basic route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', current_title= 'Custom Title')

@app.route('/about')
def about():
    return render_template('about.html')