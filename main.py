import textwrap
import datetime
import sheets_api
import flask
import time
import os
import random
import string
app = flask.Flask(__name__, static_url_path='')

#################### Initialize ####################

app.secret_key = '.d1.g52@F4d0f.s53FF350F.sd40##'

DOMAIN = 'chaitanyapy.ml:2783'
gauth = sheets_api.authorize()

anonymous_urls = ['/favicon.ico', '/clear_test_cookies', '/logo.png', '/background.png']
desktop_agents = ['Macintosh', 'Windows', 'Linux']

client_req_times = {}

#################### Utility Functions ####################

def get_user_data(id):
    try:
        with open('user_data/'+id) as f:
            fdata = f.read()
        data = eval(fdata)
        return data
    except FileNotFoundError:
        return False

def row_to_column(sheet):
    output = []
    row_len = len(sheet[0])
    for _ in range(row_len):
        output.append([])
    for i in range(row_len):
        for o in range(len(sheet)):
            try:
                c_cell = sheet[o][i]
            except IndexError:
                c_cell = ''
            output[i].append(c_cell)
    return output

def convert(sheet):
    try:
        sheet = sheet[1:]
        sheet = row_to_column(sheet)
        output = {}
        output['test_name'] = sheet[0][0]
        output['subject'] = sheet[0][1]
        output['tags'] = sheet[1]
        output['questions'] = {"easy": [], "medium": [], "hard": []}
        for i in range(len(sheet[2])):
            if sheet[2][i] == '':
                continue
            c_a_i = eval(sheet[4][i])-1
            if sheet[5][i] == '':
                output['questions']['easy'].append({"question": sheet[2][i], "answers": sheet[3][i].split('\n'), "correct_answer_index": c_a_i})
            else:
                output['questions']['easy'].append({"question": sheet[2][i], "answers": sheet[3][i].split('\n'), "correct_answer_index": c_a_i, "image": sheet[5][i]})
        for i in range(len(sheet[6])):
            if sheet[6][i] == '':
                continue
            c_a_i = eval(sheet[8][i])-1
            if sheet[9][i] == '':
                output['questions']['medium'].append({"question": sheet[6][i], "answers": sheet[7][i].split('\n'), "correct_answer_index": c_a_i})
            else:
                output['questions']['medium'].append({"question": sheet[6][i], "answers": sheet[7][i].split('\n'), "correct_answer_index": c_a_i, "image": sheet[9][i]})
        for i in range(len(sheet[10])):
            if sheet[10][i] == '':
                continue
            c_a_i = eval(sheet[12][i])-1
            try:
                sheet[13]
                if sheet[13][i] == '':
                    output['questions']['hard'].append({"question": sheet[10][i], "answers": sheet[11][i].split('\n'), "correct_answer_index": c_a_i})
                else:
                    output['questions']['hard'].append({"question": sheet[10][i], "answers": sheet[11][i].split('\n'), "correct_answer_index": c_a_i, "image": sheet[13][i]})
            except:
                output['questions']['hard'].append({"question": sheet[10][i], "answers": sheet[11][i].split('\n'), "correct_answer_index": c_a_i})
        return output
    except:
        return 'ERROR'

def create_new_test_sheet(owner):
    dt = datetime.datetime.now()
    c_time = str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second)
    c_date = str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)
    test_list = [f for f in os.listdir('test_data') if os.path.isfile(os.path.join('test_data', f))]
    while 1:
        r_id = id_generator()
        if r_id in test_list:
            pass
        else:
            break
    test_id = r_id
    sheet_id = sheets_api.create_sheet(test_id, gauth.load_credentials())
    with open('test_data/'+test_id+'.json', 'w') as f:
        f.write('')
    with open('test_metadata/'+test_id+'.json', 'w') as f:
        f.write(str({"owner": owner, "time": c_time, "date": c_date, "sheet_id": sheet_id}))
    return (test_id, sheet_id)

def validate_test_data(data_string):
    try:
        data = eval(data_string)
        if type(data['test_name']) != type(''):
            return 'TEST_NAME_INVALID'
        if type(data['subject']) != type(''):
            return 'SUBJECT_INVALID'
        if type(data['tags']) != type([]):
            return 'TAGS_INVALID'
        if type(data['questions']) != type({}):
            return 'QUESTIONS_INAVLID'
        for question in data['questions']['easy']:
            if type(question['question']) != type(''):
                return 'EASY_QUESTION_TEXT_INVALID'
            try:
                for answer in question['answers']:
                    if type(answer) != type(''):
                        return 'EASY_QUESTION_ANSWER_INVALID'
            except:
                return 'EASY_QUESTION_ANSWERS_INVALID'
            if type(question['correct_answer_index']) != type(0):
                return 'EASY_CORRECT_ANSWER_INDEX_INVALID'
            try:
                question['answers'][question['correct_answer_index']]
            except:
                return 'EASY_CORRECT_ANSWER_INDEX_OUTBOUND'
            try:
                if type(question['image']) != type(''):
                    return 'EASY_IMAGE_URL_INVALID'
            except:
                pass
        for question in data['questions']['medium']:
            if type(question['question']) != type(''):
                return 'MEDIUM_QUESTION_TEXT_INVALID'
            try:
                for answer in question['answers']:
                    if type(answer) != type(''):
                        return 'MEDIUM_QUESTION_ANSWER_INVALID'
            except:
                return 'MEDIUM_QUESTION_ANSWERS_INVALID'
            if type(question['correct_answer_index']) != type(0):
                return 'MEDIUM_CORRECT_ANSWER_INDEX_INVALID'
            try:
                question['answers'][question['correct_answer_index']]
            except:
                return 'MEDIUM_CORRECT_ANSWER_INDEX_OUTBOUND'
            try:
                if type(question['image']) != type(''):
                    return 'MEDIUM_IMAGE_URL_INVALID'
            except:
                pass
        for question in data['questions']['hard']:
            if type(question['question']) != type(''):
                return 'HARD_QUESTION_TEXT_INVALID'
            try:
                for answer in question['answers']:
                    if type(answer) != type(''):
                        return 'HARD_QUESTION_ANSWER_INVALID'
            except:
                return 'HARD_QUESTION_ANSWERS_INVALID'
            if type(question['correct_answer_index']) != type(0):
                return 'HARD_CORRECT_ANSWER_INDEX_INVALID'
            try:
                question['answers'][question['correct_answer_index']]
            except:
                return 'HARD_CORRECT_ANSWER_INDEX_OUTBOUND'
            try:
                if type(question['image']) != type(''):
                    return 'HARD_IMAGE_URL_INVALID'
            except:
                pass
        return True
    except:
        return 'SYNTAX_INVALID'

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def load_questions(test_id):
    try:
        with open('test_data/'+test_id+'.json') as f:
            fdata = f.read()
    except FileNotFoundError:
        return 'FILE_NOT_FOUND'
    data = eval(fdata)
    counter = 0
    for q in data["questions"]['easy']:
        q['id'] = counter
        counter += 1
    counter = 0
    for q in data["questions"]['medium']:
        q['id'] = counter
        counter += 1
    counter = 0
    for q in data["questions"]['hard']:
        q['id'] = counter
        counter += 1
    return data

def get_difficulty(difficulty, completed_questions, questions, prev_q_res):
    if prev_q_res == True:
        if difficulty == 1:
            if len(completed_questions[2]) != len(questions['hard']):
                difficulty = 2
            elif len(completed_questions[1]) != len(questions['medium']):
                difficulty = 1
            elif len(completed_questions[0]) != len(questions['easy']):
                difficulty = 0
            else:
                return 'TEST_COMPLETE'
        elif difficulty == 2:
            if len(completed_questions[2]) != len(questions['hard']):
                difficulty = 2
            elif len(completed_questions[1]) != len(questions['medium']):
                difficulty = 1
            elif len(completed_questions[0]) != len(questions['easy']):
                difficulty = 0
            else:
                return 'TEST_COMPLETE'
        elif difficulty == 0:
            if len(completed_questions[1]) != len(questions['medium']):
                difficulty = 1
            elif len(completed_questions[2]) != len(questions['hard']):
                difficulty = 2
            elif len(completed_questions[0]) != len(questions['easy']):
                difficulty = 0
        else:
            return 'ERROR'
    elif prev_q_res == False:
        if difficulty == 2:
            if len(completed_questions[1]) != len(questions['medium']):
                difficulty = 1
            elif len(completed_questions[0]) != len(questions['easy']):
                difficulty = 0
            elif len(completed_questions[2]) != len(questions['hard']):
                difficulty = 2
            else:
                return 'TEST_COMPLETE'
        elif difficulty == 1:
            if len(completed_questions[0]) != len(questions['easy']):
                difficulty = 0
            elif len(completed_questions[1]) != len(questions['medium']):
                difficulty = 1
            elif len(completed_questions[2]) != len(questions['hard']):
                difficulty = 2
            else:
                return 'TEST_COMPLETE'
    return difficulty

def get_question(completed_questions, questions):
    if len(completed_questions) == len(questions):
        return 'QUESTIONS_COMPLETED'
    while 1:
        q = random.choice(questions)
        if q['id'] in completed_questions:
            pass
        else:
            break
    return q

#################### Reqeust Handlers ####################

@app.before_request
def before_request():
    try:
        prev_time = client_req_times[flask.request.remote_addr]
    except KeyError:
        prev_time = None
    if prev_time:
        c_time = time.time()
    if flask.request.headers['Host'] != DOMAIN:
        return flask.redirect('http://'+DOMAIN+flask.request.path, 301)
    if flask.request.path != '/login' and flask.request.path not in anonymous_urls:
        try:
            username = flask.session['username']
            f = open('user_data/'+username)
            f.close()
        except KeyError:
            flask.session['login_ref'] = flask.request.path
            return flask.redirect('/login')
        except FileNotFoundError:
            flask.session['login_ref'] = flask.request.path
            return flask.redirect('/login')

@app.after_request
def after_request(response):
    response.headers["Server"] = "DAL-Server/0.2"
    response.headers["Developers"] = "Chaitanya, Harsha, Piyush"
    response.headers["Origin-School"] = "Diya Academy of Learning"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

#################### Content Endpoints ####################

@app.route('/')
def home():
    desktop = False
    for agent in desktop_agents:
        if agent in flask.request.headers['User-Agent']:
            desktop = True
    user_data = get_user_data(flask.session['username'])
    if desktop:
        return flask.render_template('home.html', username=flask.session['username'], name=user_data['name'])
    else:
        return flask.render_template('mobile/home.html', username=flask.session['username'], name=user_data['name'])

@app.route('/logout')
def logout():
    flask.session.pop('username')
    return flask.redirect('/login')

@app.route('/clear_test_cookies')
def clear_test_cookies():
    try:
        href = flask.session['error_referrer']
    except KeyError:
        href = '/'
    try:
        flask.session.pop('t')
    except KeyError:
        pass
    return flask.render_template('cookie_cleared.html', href=href)

@app.route('/t/<code>/verify', methods=['POST'])
def t_verify(code):
    data = flask.request.form
    if str(data['answer']) == str(flask.session['t']['c_a_i']):
        flask.session['t']['prev_q_res'] = True
        flask.session['t']['score'] = str(eval(flask.session['t']['score'])+10)
    else:
        flask.session['t']['prev_q_res'] = False
    flask.session.modified = True
    return flask.redirect('/t/'+code)

@app.route('/t/<code>/')
def t_view(code):
    desktop = False
    for agent in desktop_agents:
        if agent in flask.request.headers['User-Agent']:
            desktop = True
    user_data = get_user_data(flask.session['username'])
    try:
        user_data['test_data'][code]
        if code != 'demo':
            return flask.render_template('test_repeat.html'), 406
    except KeyError:
        pass
    question_data = load_questions(code)
    authorized = False
    for tag in user_data['tags']:
        if tag in question_data or tag == 'admin' or tag == 'teacher':
            authorized = True
    if authorized == False:
        return flask.render_template('401.html'), 401
    if question_data == 'FILE_NOT_FOUND':
        return flask.render_template('404.html'), 404
    try:
        flask.session['t']
        flask.session['t']['q']
        flask.session['t']['c_q']
        flask.session['t']['difficulty']
        flask.session['t']['score']
        if flask.session['t']['code'] != code:
            flask.session.pop('t')
            flask.session['t'] = {}
            flask.session['t']['code'] = code
            flask.session['t']['q'] = '0'
            flask.session['t']['c_q'] = [[], [], []]
            flask.session['t']['difficulty'] = 1
            flask.session['t']['score'] = '0'
            flask.session.modified = True
    except KeyError:
        flask.session['t'] = {}
        flask.session['t']['code'] = code
        flask.session['t']['q'] = '0'
        flask.session['t']['c_q'] = [[], [], []]
        flask.session['t']['difficulty'] = 1
        flask.session['t']['score'] = '0'
        flask.session.modified = True
        return flask.redirect('/t/'+code)
    if flask.request.args.get('start') == '':
        try:
            flask.session['t']['q'] = '1'
            flask.session.modified = True
        except KeyError:
            return flask.redirect('/t/'+code)
        return flask.redirect('/t/'+code)
    elif flask.request.args.get('exit') == '':
        flask.session.pop('t')
        flask.session.modified = True
        return flask.redirect('/t/'+code)
    if len(flask.session['t']['c_q'][0]) == len(question_data['questions']['easy']) and len(flask.session['t']['c_q'][1]) == len(question_data['questions']['medium']) and len(flask.session['t']['c_q'][2]) == len(question_data['questions']['hard']):
        score = flask.session['t']['score']
        flask.session.pop('t')
        flask.session.modified = True
        try:
            user_data['test_data'][code] = score
        except KeyError:
            user_data['test_data'] = {}
            user_data['test_data'][code] = score
        if 'teacher' in user_data['tags'] or 'admin'  in user_data['tags']:
            pass
        else:
            with open('user_data/'+flask.session['username'], 'w') as f:
                f.write(str(user_data))
        return flask.render_template('t_completed.html', name=question_data['test_name'], score=score)
    if flask.session['t']['q'] == '0':
        q_n = 0
        for difficulty in question_data['questions']:
            for q in question_data['questions'][difficulty]:
                q_n += 1
        if desktop:
            return flask.render_template('t0.html', code=code, data=question_data, username=flask.session['username'], name=user_data['name'], q_n=q_n, subject=question_data['subject'])
        else:
            return flask.render_template('mobile/t0.html', code=code, data=question_data, username=flask.session['username'], name=user_data['name'], q_n=q_n, subject=question_data['subject'])
    else:
        print(flask.session['t']['c_q'])
        print(flask.session['t']['score'])
        if flask.session['t']['q'] == '1':
            question = get_question(flask.session['t']['c_q'][1], question_data['questions']['medium'])
            if question == 'QUESTIONS_COMPLETED':
                return flask.render_template('500.html'), 500
            flask.session['t']['c_q'][1].append(question['id'])
            q_number = flask.session['t']['q']
            flask.session['t']['q'] = str(eval(flask.session['t']['q'])+1)
            flask.session['t']['c_a_i'] = question['correct_answer_index']
            flask.session.modified = True
            try:
                image_url = question['image']
            except KeyError:
                image_url = None
            height_extend = 0
            if len(question['question']) >= 40:
                temp_question = textwrap.wrap(question['question'], 50)
                for chunk in temp_question:
                    if desktop:
                        height_extend += 10
                    else:
                        height_extend += 20
                question['question'] = temp_question
            else:
                question['question'] = [question['question']]
            o_answers = []
            counter = 0
            for answer in question['answers']:
                o_answers.append({'answer': answer, "id": str(counter)})
                counter += 1
            random.shuffle(o_answers)
            if desktop:
                return flask.render_template('t.html', code=code, question_data=question, ans_range=range(len(question['answers'])), data=question_data, q_number=q_number, image_url=image_url, username=flask.session['username'], name=user_data['name'], total_height=650+height_extend, answers=o_answers)
            else:
                return flask.render_template('mobile/t.html', code=code, question_data=question, ans_range=range(len(question['answers'])), data=question_data, q_number=q_number, image_url=image_url, username=flask.session['username'], name=user_data['name'], total_height=650+height_extend, answers=o_answers)
        else:
            try:
                 prev_q_res = flask.session['t']['prev_q_res']
            except:
                prev_q_res = False
            c_difficulty = get_difficulty(flask.session['t']['difficulty'], flask.session['t']['c_q'], question_data['questions'], prev_q_res)
            print(c_difficulty)
            if c_difficulty == 0:
                question = get_question(flask.session['t']['c_q'][0], question_data['questions']['easy'])
            elif c_difficulty == 1:
                question = get_question(flask.session['t']['c_q'][1], question_data['questions']['medium'])
            elif c_difficulty == 2:
                question = get_question(flask.session['t']['c_q'][2], question_data['questions']['hard'])
            if question == 'QUESTIONS_COMPLETED':
                return flask.render_template('500.html'), 500
            flask.session['t']['c_q'][c_difficulty].append(question['id'])
            q_number = flask.session['t']['q']
            flask.session['t']['q'] = str(eval(flask.session['t']['q'])+1)
            flask.session['t']['c_a_i'] = question['correct_answer_index']
            flask.session.modified = True
            try:
                image_url = question['image']
            except KeyError:
                image_url = None
            height_extend = 0
            if desktop:
                if len(question['question']) >= 40:
                    temp_question = textwrap.wrap(question['question'], 50)
                    for chunk in temp_question:
                        height_extend += 10
                    question['question'] = temp_question
                else:
                    question['question'] = [question['question']]
            else:
                if len(question['question']) >= 30:
                    temp_question = textwrap.wrap(question['question'], 40)
                    for chunk in temp_question:
                        height_extend += 40
                    question['question'] = temp_question
                else:
                    question['question'] = [question['question']]
            o_answers = []
            counter = 0
            for answer in question['answers']:
                o_answers.append({'answer': answer, "id": str(counter)})
                counter += 1
            random.shuffle(o_answers)
            if desktop:
                return flask.render_template('t.html', code=code, question_data=question, ans_range=range(len(question['answers'])), data=question_data, q_number=q_number, image_url=image_url, username=flask.session['username'], name=user_data['name'], total_height=650+height_extend, answers=o_answers)
            else:
                return flask.render_template('mobile/t.html', code=code, question_data=question, ans_range=range(len(question['answers'])), data=question_data, q_number=q_number, image_url=image_url, username=flask.session['username'], name=user_data['name'], total_height=650+height_extend, answers=o_answers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html', error=False, username='')
    else:
        form_data = flask.request.form
        try:
            with open('user_data/'+form_data['username']) as f:
                fdata = f.read()
            data = eval(fdata)
            if data['password'] != form_data['password']:
                return flask.render_template('login.html', error=True, username=form_data['username'])
            else:
                flask.session['username'] = form_data['username']
                try:
                    login_ref = flask.session['login_ref']
                    flask.session.pop('login_ref')
                    return flask.redirect(login_ref)
                except KeyError:
                    return flask.redirect('/')
        except FileNotFoundError:
            return flask.render_template('login.html', error=True, username=form_data['username'])

@app.route('/new_test', methods=['GET', 'POST'])
def new_test():
    if flask.request.method == 'GET':
        return flask.render_template('new_test.html')
    else:
        test_data = create_new_test_sheet(flask.session['username'])
        test_id, sheet_id = test_data
        return flask.redirect('/t/'+test_id+'/edit')

@app.route('/sheets_api_authorize', methods=['GET', 'POST'])
def sheets_api_authorize():
    user_data = get_user_data(flask.session['username'])
    if 'admin' in user_data['tags']:
        if flask.request.method == 'GET':
            creds = gauth.load_credentials()
            if creds:
                if gauth.verify_token(creds):
                    return 'authorized'
                else:
                    url = gauth.get_url()
                    return "<script>window.open('"+url+"')</script><form action='/sheets_api_authorize' method='POST'><input type='text' name='code' placeholder='code' autofocus><input type='submit' value='Enter'></form>"
            else:
                url = gauth.get_url()
                return "<script>window.open('"+url+"')</script><form action='/sheets_api_authorize' method='POST'><input type='text' name='code' placeholder='code' autofocus><input type='submit' value='Enter'></form>"
        else:
            data = flask.request.form
            creds = gauth.verify_code(data['code'])
            if creds != False:
                gauth.save_credentials(creds)
                return 'authorization_complete'
            else:
                return 'authorization_error'
    else:
        return flask.render_template('404.html'), 404

@app.route('/t/<code>/edit/', methods=['GET', 'POST'])
def test_edit(code):
    user_data = get_user_data(flask.session['username'])
    try:
        with open('test_metadata/'+code+'.json') as f:
            data = eval(f.read())
    except:
        return flask.render_template('404.html'), 404
    if data.get('owner'):
        if data['owner'] != flask.session['username'] or 'admin' in user_data['tags']:
            pass
        else:
            if 'teacher' in user_data['tags']:
                return flask.render_template('401.html'), 401
            else:
                return flask.redirect('/t/'+code)
    else:
        if 'teacher' in user_data['tags'] or 'admin' in user_data['tags']:
            pass
        else:
            return flask.redirect('/t/'+code)
    with open('test_data/'+code+'.json') as f:
        test_data = f.read()
    sheet_id = data.get('sheet_id')
    try:
        title = eval(test_data)['test_name']
    except:
        title = 'EDIT TEST'
    if flask.request.method == 'GET':
        sync_arg = flask.request.args.get('sync')
        if sync_arg == '':
            n_test_data = sheets_api.get_values(sheet_id, gauth.load_credentials())
            n_test_data = convert(n_test_data)
            if n_test_data == "ERROR":
                return flask.render_template('t_edit.html', test_data=test_data, sheet_id=sheet_id, title=title, username=flask.session['username'], name=user_data['name'], code=code, alert="Error during parsing spreadsheet")
            test_validation = validate_test_data(str(n_test_data))
            if test_validation == True:
                with open('test_data/'+code+'.json', 'w') as f:
                    f.write(str(n_test_data))
                return flask.redirect('/t/'+code+'/edit')
            else:
                return flask.render_template('t_edit.html', test_data=test_data, sheet_id=sheet_id, title=title, username=flask.session['username'], name=user_data['name'], code=code, alert="Error: "+test_validation)
        else:
            return flask.render_template('t_edit.html', test_data=test_data, sheet_id=sheet_id, title=title, username=flask.session['username'], name=user_data['name'], code=code, alert=None)
    else:
        data = flask.request.form
        v_output = validate_test_data(data['test_data'])
        if v_output == True:
            with open('test_data/'+code+'.json', 'w') as f:
                f.write(data['test_data'])
            return flask.render_template('t_edit.html', test_data=data['test_data'], sheet_id=sheet_id, title=title, username=flask.session['username'], name=user_data['name'], code=code, alert='Test updated')
        else:
            return flask.render_template('t_edit.html', test_data=data['test_data'], sheet_id=sheet_id, title=title, username=flask.session['username'], name=user_data['name'], code=code, alert='Error: '+v_output)

@app.route('/sheets_api_authorize/delete')
def sheets_api_authorize_delete():
    user_data = get_user_data(flask.session['username'])
    if flask.session['username'] == 'admin':
        try:
            os.remove('credentials.pickle')
            return flask.redirect('/sheets_api_authorize')
        except:
            return 'file_not_found'
    else:
        return flask.render_template('404.html'), 404

#################### Static Endpoints ####################

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/background.png')
def background():
    return app.send_static_file('background.png')

@app.route('/logo.png')
def logo():
    return app.send_static_file('logo.png')

#################### Error Handlers ####################

@app.errorhandler(404)
def e_404(e):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def e_500(e):
    flask.session['error_referrer'] = flask.request.path
    return flask.render_template('500.html'), 500

#################### Main ####################

if __name__=='__main__':
    app.run(debug=True, port=2783, host='0.0.0.0', threaded=True)