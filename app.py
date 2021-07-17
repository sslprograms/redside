from flask import *
import json, string, random

app = Flask(__name__)

with open('database.json', 'r') as data:
    data = json.loads(data.read())

accounts = data

@app.route('/')
def index_load():
    for x in accounts['accounts']:
        if x['token'] == request.cookies.get('token'):
            return redirect(url_for('home_page'))
    return render_template('index.html')

@app.route('/join')
def join_page():
    for x in accounts['accounts']:
        if x['token'] == request.cookies.get('token'):
            return redirect(url_for('home_page'))
    return render_template('join.html')

@app.route('/login')
def login_page():
    for x in accounts['accounts']:
        if x['token'] == request.cookies.get('token'):
            return redirect(url_for('home_page'))
    return render_template('login.html')

@app.route('/home')
def home_page():
    for x in accounts['accounts']:
        if x['token'] == request.cookies.get('token'):
            return render_template('home.html', content=x)
    return redirect(url_for('index_load'))

@app.route('/logout')
def logout():
    mr = make_response(redirect(url_for('index_load')))
    mr.set_cookie('token', '')
    return mr    

@app.route('/p/<user>')
def user_profile(user):
    for x in accounts['accounts']:
        if x['token'] == request.cookies.get('token'):
            for user1 in accounts['accounts']:
                if user1['username'] == user:
                    return render_template('profiles.html', content=user1)
            return redirect(url_for('home_page'))
    return redirect(url_for('login_page'))

@app.route('/discover')
def discover_page():
    for x in accounts['accounts']:
        if x['token'] == request.cookies.get('token'):
            choices_ = []
            for i_  in range(50):
                choices_.append(random.choice(accounts['accounts']))
            return render_template('discover.html', content=choices_, random=random)
    return redirect(url_for('index_load'))

# API

@app.route('/api/join', methods=['POST'])
def create_account():
    try:
        username = request.form.get('username').lower()
        password = request.form.get('password')
        for acc in accounts['accounts']:
            if acc['username'] == username:
                mr = make_response('', 400)
                return mr
        token = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=25))
        account_cr = {'token':token, 'username':username, 'password':password, 'plan':'Free', 'followers_count':0, 'following_count':0, 'posts':[], 'following':[], 'followers':[]}
        accounts['accounts'].append(account_cr)
        with open('database.json', 'w') as datab:
            datab.write(str(accounts).replace("'", '"'))
        mr = make_response('', 200)
        mr.set_cookie('token', token)
        return mr
    except:
        mr = make_response('', 400)
        return mr

@app.route('/api/login', methods=['POST'])
def login_account():
    try:
        username = request.form.get('username').lower()
        password = request.form.get('password')
        for acc in accounts['accounts']:
            if acc['username'] == username and acc['password'] == password:
                mr = make_response('', 200)
                mr.set_cookie('token', acc['token'])
                return mr
        mr = make_response('', 400)
        return mr
    except:
        mr = make_response('', 400)
        return mr

@app.route('/api/<user>/following')
def follow_check(user):
    try:
        token = request.cookies.get('token')
        for x in accounts['accounts']:
            if x['token'] == token:
                if user == x['username']:
                    mr = make_response('yes', 200)
                    return mr
                for i in x['following']:
                    if user == i:
                        mr = make_response('yes', 200)
                        return mr
                mr = make_response('no', 200)
                return mr
        mr = make_response('no', 200)
        return mr
    except:
        mr = make_response('no', 200)
        return mr

@app.route('/api/post', methods=['POST'])
def post():
    try:
        token = request.cookies.get('token')
        text = request.form.get('text')
        if len(text) > 160:
            mr = make_response('', 400)
            return mr
        for x in accounts['accounts']:
            if x['token'] == token:
                pos = accounts['accounts'].index(x)
                accounts['accounts'][pos]['posts'].append(text)
                with open('database.json', 'w') as database:
                    database.write(str(accounts).replace("'", '"'))
                mr = {}
                mr = make_response(jsonify(mr), 200)
                return mr
        mr = make_response('', 400)
        return mr
    except:
        mr = make_response('', 400)
        return mr


@app.route('/api/<user>/follow', methods=['PATCH'])
def follow_user(user):
    # try:
    token = request.cookies.get('token')
    for x in accounts['accounts']:
        if x['token'] == token:
            for i in accounts['accounts']:
                for followr in i['followers']:
                    if followr == i['username'] or i == x['username']:
                        mr = make_response(jsonify({}), 200)
                        return mr
                if i['username'] == user:
                    pos = accounts['accounts'].index(x)
                    pos1 = accounts['accounts'].index(i)
                    accounts['accounts'][pos]['following_count'] += 1
                    accounts['accounts'][pos]['following'].append(i['username'])
                    accounts['accounts'][pos1]['followers_count'] += 1
                    accounts['accounts'][pos1]['followers'].append(x['username'])
                    with open('database.json', 'w') as database:
                        database.write(str(accounts).replace("'", '"'))
                    mr = make_response(jsonify({'success':True}), 200)
                    return mr
    mr = make_response(jsonify({}), 200)
    return mr
    # except:
    #     mr = make_response(jsonify({}), 200)
    #     return mr


    



if __name__ == '__main__':
    app.run()
