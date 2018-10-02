from flask import Blueprint, render_template
from classPlay.main.forms import LoginForm
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    return render_template('login.html', form=form)


@main.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')
