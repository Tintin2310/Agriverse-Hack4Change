from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'

farms = []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'farmer' and password == 'farmer':
            session['user'] = 'farmer'
            return redirect(url_for('farmer'))
        elif username == 'buyer' and password == 'buyer':
            session['user'] = 'buyer'
            return redirect(url_for('buyers'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/farmer', methods=['GET', 'POST'])
def farmer():
    if 'user' not in session or session['user'] != 'farmer':
        return redirect(url_for('login'))
    if request.method == 'POST':
        farm = {
            'farm_name': request.form['farm_name'],
            'crop_name': request.form['crop_name'],
            'quantity': request.form['quantity'],
            'rate': request.form['rate'],
            'latitude': request.form['latitude'],
            'longitude': request.form['longitude']
        }
        farms.append(farm)
        return jsonify({'status': 'success'})
    return render_template('farmer.html')

@app.route('/buyers')
def buyers():
    if 'user' not in session or session['user'] != 'buyer':
        return redirect(url_for('login'))
    return render_template('buyers.html', farms=farms)

@app.route('/api/farms', methods=['GET'])
def get_farms():
    return jsonify(farms)

if __name__ == '__main__':
    app.run(debug=True)
