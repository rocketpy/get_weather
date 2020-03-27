import scrapy
from scrapy.crawler import CrawlerProcess
from flask_login import LoginManager
from flask_login import login_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from flask_user import login_required, current_user



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/signup', methods=['POST', 'GET'])
def signup_post():
    form = SignUp()  # (csrf_enabled=False)

    name = request.form.get('name')  # request.form['name']
    surname = request.form.get('surname')
    email = request.form.get('email')
    sex = request.form.get('sex')
    birthday = request.form.get('birthday')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if form.validate_on_submit():
        new_user = User(name=name, surname=surname, email=email, sex=sex, birthday=birthday,
                        password=generate_password_hash(password, method='sha256'))
        if user:
            flash('Email address already exists')
            return render_template('login.html', form=form)

        db.session.add(new_user)  # adding a new user to db
        db.session.commit()
        flash('New user created !')
        return render_template('profile.html')  # return redirect('/success')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_post():
    form = LoginForm()
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if form.validate_on_submit():
        login_user(user, remember=remember)
        flash('Logged in successfully.')
        return redirect(url_for('add_post', form=form))

    if user:  # or not check_password_hash(user.password, password):
        flash('Please check your login details and try again !')
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/weather', methods=['GET', 'POST'])
@login_required
def show_weather():
    night_temperature = []
    day_temperature = []
    #if request.method == 'POST'

    class MySpider(scrapy.Spider):
        name = "weather_spider"
        allowed_domains = ['gismeteo.ua']
        start_urls = ['https://www.gismeteo.ua/weather-zaporizhia-5093/']

        def parse(self, response):
            values = response.css('div.value')
            night_temp = values.css('span.unit.unit_temperature_c::text')[0].extract()
            day_temp = values.css('span.unit.unit_temperature_c::text')[1].extract()
            night_temperature.append(night_temp)
            day_temperature.append(day_temp)

    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(MySpider)
    process.start()

    return render_template('weather.html', night_temperature=night_temperature[-1],
                           day_temperature=day_temperature[-1])

# from scrapy import cmdline
# cmdline.execute("scrapy crawl myspider".split())


@app.route('/add', methods=['POST', 'GET'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_post = UserPost(name=name, email=email, message=message)  # date_posted=datetime.now()
        db.session.add(new_post)
        db.session.commit()
        flash('Post added as successfully.')
        return redirect(url_for('add_post'))

    return render_template('post.html', form=form)


@app.route('/posts')
@login_required
def post():
    posts = UserPost.query.all()
    return render_template('posts.html', posts=posts)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_error.html', title='404'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500_error.html', title='500'), 500


# app.register_blueprint(auth)
# app.register_blueprint(main)

login_manager = LoginManager()
login_manager.login_view = 'login.html'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
