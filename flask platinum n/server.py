from flask import Flask, redirect, render_template, session, request
import random
app = Flask(__name__)
app.secret_key = 'jasdfilaj2489j3q9fj8a9jfda89jsf9asjf98ais'

@app.route('/')
def index():
    if not 'gold' in session: 
        session['gold'] = 0
    if not 'activities' in session:
        session['activities'] = []
    print(session['activities'])
    return render_template('index.html', gold = session['gold'], activities = session['activities'])



@app.route('/gold', methods=['POST'])
def add_gold():
    if request.form['building'] == 'farm':
        gold = random.randint(10,20)
        session['gold'] += gold
    elif request.form['building'] == 'cave':
        gold = random.randint(5,10)
        session['gold'] += gold
    if request.form['building'] == 'house':
        gold = random.randint(2,5)
        session['gold'] += gold
    if request.form['building'] == 'casino':
        gold = random.randint(-50,50)
        session['gold'] += gold
    
    if gold > 0:
        # message = 'You won {} gold.'.format(gold)
        # message_type = 'success'
        new_dict = {
            'message': 'You won {} gold.'.format(gold),
            'type': 'success'
        }
        session['activities'].append(new_dict)
    else:
        # message = 'You lost {} gold.'.format(gold)
        # message_type = 'failure'
        new_dict = {
            'message': 'You lost {} gold.'.format(gold),
            'type': 'failure'
        }
        session['activities'].append(new_dict)

    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


app.run(debug=True)