from flask import Flask
from flask import render_template, redirect, request, abort
from data import db_session
from flask_login import LoginManager
from data.users import User
from data.packs import Pack
from data.packs_resources import PackResource
from data.forms import LoginForm, RegisterForm, GameForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Api
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
api.add_resource(PackResource, '/api/v2/packs/<int:pack_id>')


@app.route("/")
def index():
    session = db_session.create_session()
    game_id = session.query(Pack).filter(Pack.id).all()[-1].id + 1
    return render_template('base.html', game_id=game_id)


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


@app.route('/game/<int:game_id>/rounds/<int:round>/category', methods=['GET', 'POST'])
def game(game_id, round):
    session = db_session.create_session()
    game_form = GameForm()
    # submit field is pressed
    if game_form.validate_on_submit() and game_form.category_submit.data:
        if not session.query(Pack).filter((Pack.id == game_id)).first():
            with open(f'games/{game_id}.json', 'w') as f:
                data = {
                    "rounds": [
                        {
                            "categories": [

                            ]
                        }
                    ]
                }
                json.dump(data, f, indent=4)
                pack = Pack(
                    game=f'games/{game_id}.json',
                    user_id=current_user.id
                )
                session.add(pack)
                session.commit()
        category_data = ({
                             "name": game_form.category.data,
                             "description": game_form.description.data,
                             "questions": [
                                 {
                                     "text": game_form.text.data,
                                     "par": game_form.par.data,
                                     "correct_answers": game_form.answers.data,
                                     "answer_time": game_form.time.data
                                 },
                                 {
                                     "text": game_form.text_1.data,
                                     "par": game_form.par_1.data,
                                     "correct_answers": game_form.answers_1.data,
                                     "answer_time": game_form.time_1.data
                                 },
                                 {
                                     "text": game_form.text_2.data,
                                     "par": game_form.par_2.data,
                                     "correct_answers": game_form.answers_2.data,
                                     "answer_time": game_form.time_2.data
                                 },
                                 {
                                     "text": game_form.text_3.data,
                                     "par": game_form.par_3.data,
                                     "correct_answers": game_form.answers_3.data,
                                     "answer_time": game_form.time_3.data
                                 },
                                 {
                                     "text": game_form.text_4.data,
                                     "par": game_form.par_4.data,
                                     "correct_answers": game_form.answers_4.data,
                                     "answer_time": game_form.time_4.data
                                 }
                             ]
                         },)
        with open(f'games/{game_id}.json') as f:
            data = json.load(f)
        data["rounds"][round - 1]["categories"] += list(category_data)
        with open(f'games/{game_id}.json', 'w') as f:
            json.dump(data, f, indent=4)
        return redirect(f'/game/{game_id}/rounds/{round}/category')
    elif game_form.validate_on_submit() and game_form.round_submit.data:
        round_data = ({
                          "categories": [
                          ]
                      },)
        with open(f'games/{game_id}.json') as f:
            data = json.load(f)
        data["rounds"] += list(round_data)
        with open(f'games/{game_id}.json', 'w') as f:
            json.dump(data, f, indent=4)
        category_data = ({
                             "name": game_form.category.data,
                             "description": game_form.description.data,
                             "questions": [
                                 {
                                     "text": game_form.text.data,
                                     "par": game_form.par.data,
                                     "correct_answers": game_form.answers.data,
                                     "answer_time": game_form.time.data
                                 },
                                 {
                                     "text": game_form.text_1.data,
                                     "par": game_form.par_1.data,
                                     "correct_answers": game_form.answers_1.data,
                                     "answer_time": game_form.time_1.data
                                 },
                                 {
                                     "text": game_form.text_2.data,
                                     "par": game_form.par_2.data,
                                     "correct_answers": game_form.answers_2.data,
                                     "answer_time": game_form.time_2.data
                                 },
                                 {
                                     "text": game_form.text_3.data,
                                     "par": game_form.par_3.data,
                                     "correct_answers": game_form.answers_3.data,
                                     "answer_time": game_form.time_3.data
                                 },
                                 {
                                     "text": game_form.text_4.data,
                                     "par": game_form.par_4.data,
                                     "correct_answers": game_form.answers_4.data,
                                     "answer_time": game_form.time_4.data
                                 }
                             ]
                         },)
        with open(f'games/{game_id}.json') as f:
            data = json.load(f)
        data["rounds"][round - 1]["categories"] += list(category_data)
        with open(f'games/{game_id}.json', 'w') as f:
            json.dump(data, f, indent=4)
        return redirect(f'/game/{game_id}/rounds/{round + 1}/category')
    elif game_form.validate_on_submit() and game_form.finish_submit.data:
        category_data = ({
                             "name": game_form.category.data,
                             "description": game_form.description.data,
                             "questions": [
                                 {
                                     "text": game_form.text.data,
                                     "par": game_form.par.data,
                                     "correct_answers": game_form.answers.data,
                                     "answer_time": game_form.time.data
                                 },
                                 {
                                     "text": game_form.text_1.data,
                                     "par": game_form.par_1.data,
                                     "correct_answers": game_form.answers_1.data,
                                     "answer_time": game_form.time_1.data
                                 },
                                 {
                                     "text": game_form.text_2.data,
                                     "par": game_form.par_2.data,
                                     "correct_answers": game_form.answers_2.data,
                                     "answer_time": game_form.time_2.data
                                 },
                                 {
                                     "text": game_form.text_3.data,
                                     "par": game_form.par_3.data,
                                     "correct_answers": game_form.answers_3.data,
                                     "answer_time": game_form.time_3.data
                                 },
                                 {
                                     "text": game_form.text_4.data,
                                     "par": game_form.par_4.data,
                                     "correct_answers": game_form.answers_4.data,
                                     "answer_time": game_form.time_4.data
                                 }
                             ]
                         },)
        with open(f'games/{game_id}.json', encoding='utf-8') as f:
            data = json.load(f)
        data["rounds"][round - 1]["categories"] += list(category_data)
        with open(f'games/{game_id}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('game.html', title='Game editing', game_form=game_form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/si_game.sqlite")
    port = int(os.environ.get("PORT", 11000))
    app.run(host='10.128.0.16', port=port)


if __name__ == '__main__':
    main()
