from flask import Flask
from flask import render_template, redirect, request, abort
from data import db_session
from flask_login import LoginManager
from data.users import User
from data.packs import Pack
from data.forms import LoginForm, RegisterForm, CategoryForm, QuestionForm
from flask_login import login_user, logout_user, login_required, current_user
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect Login or Password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="User already exists")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/game/<int:game_id>/category/<int:category_num>', methods=['GET', 'POST'])
def game(game_id, category_num):
    session = db_session.create_session()
    form_category_1 = CategoryForm()
    form_question_1_1 = QuestionForm()
    form_question_1_2 = QuestionForm()
    form_question_1_3 = QuestionForm()
    form_question_1_4 = QuestionForm()
    form_question_1_5 = QuestionForm()
    with open(f'/Users/alekseyostrovskiy/Desktop/sigamebot/games/{game_id}.json', 'w', encoding='utf-8') as f:
        pack = Pack(
            game=f'/Users/alekseyostrovskiy/Desktop/sigamebot/games/{game_id}.json'
        )
        session.add(pack)
        session.commit()

        data = json.loads(f.read())
        data['categories'][category_num]['name'] = form_category_1.category.data
        data['categories'][category_num]['description'] = form_category_1.description.data

        data['categories'][category_num]['questions'][0]['text'] = form_question_1_1.text.data
        data['categories'][category_num]['questions'][0]['par'] = form_question_1_1.par.data
        data['categories'][category_num]['questions'][0]['correct_answers'] = form_question_1_1.answers.data.split(', ')
        data['categories'][category_num]['questions'][0]['answer_time'] = form_question_1_1.time.data

        data['categories'][category_num]['questions'][1]['text'] = form_question_1_2.text.data
        data['categories'][category_num]['questions'][1]['par'] = form_question_1_2.par.data
        data['categories'][category_num]['questions'][1]['correct_answers'] = form_question_1_2.answers.data.split(', ')
        data['categories'][category_num]['questions'][1]['answer_time'] = form_question_1_2.time.data

        data['categories'][category_num]['questions'][2]['text'] = form_question_1_3.text.data
        data['categories'][category_num]['questions'][2]['par'] = form_question_1_3.par.data
        data['categories'][category_num]['questions'][2]['correct_answers'] = form_question_1_3.answers.data.split(', ')
        data['categories'][category_num]['questions'][2]['answer_time'] = form_question_1_3.time.data

        data['categories'][category_num]['questions'][3]['text'] = form_question_1_4.text.data
        data['categories'][category_num]['questions'][3]['par'] = form_question_1_4.par.data
        data['categories'][category_num]['questions'][3]['correct_answers'] = form_question_1_4.answers.data.split(', ')
        data['categories'][category_num]['questions'][3]['answer_time'] = form_question_1_4.time.data

        data['categories'][category_num]['questions'][4]['text'] = form_question_1_5.text.data
        data['categories'][category_num]['questions'][4]['par'] = form_question_1_5.par.data
        data['categories'][category_num]['questions'][4]['correct_answers'] = form_question_1_5.answers.data.split(', ')
        data['categories'][category_num]['questions'][4]['answer_time'] = form_question_1_5.time.data
        print(json.dumps(data, ensure_ascii=False, indent=4))

    return render_template('game.html', title='Game editing',
                           form_category_1=form_category_1,
                           form_question_1_1=form_question_1_1,
                           form_question_1_2=form_question_1_2,
                           form_question_1_3=form_question_1_3,
                           form_question_1_4=form_question_1_4,
                           form_question_1_5=form_question_1_5
                           )


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/si_game.sqlite")
    app.run()


if __name__ == '__main__':
    main()
