import os
from flask import Flask, render_template, request, redirect, url_for, session
from starter.forms import MyForm
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from sqlalchemy.exc import IntegrityError
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database credentials
username = "postgres"
password = quote_plus("Vzu542@1988")   # Encodes special characters
host = "localhost"
port = "5432"
database = "postgres"

# App config (use env vars if available, else fallback to local Postgres)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'POSTGRES_URL',
    f"postgresql://{username}:{password}@{host}:{port}/{database}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- MODELS -----------------
class ClinicalVisit(db.Model):
    __tablename__ = "clinical_visits"

    id = db.Column(db.Integer, primary_key=True)
    conditional_procedure = db.Column("Conditional Procedure", db.Text)
    budget = db.Column("Budget", db.Numeric)
    screening_visit = db.Column("Screening Visit", db.Numeric)
    baseline_visit = db.Column("Baseline Visit", db.Numeric)
    visit_1 = db.Column("Visit 1", db.Numeric)
    visit_2 = db.Column("Visit 2", db.Numeric)
    visit_3 = db.Column("Visit 3", db.Numeric)
    visit_4 = db.Column("Visit 4", db.Numeric)
    visit_5 = db.Column("Visit 5", db.Numeric)
    visit_6 = db.Column("Visit 6", db.Numeric)
    visit_7 = db.Column("Visit 7", db.Numeric)
    visit_8 = db.Column("Visit 8", db.Numeric)
    visit_9 = db.Column("Visit 9", db.Numeric)
    visit_10 = db.Column("Visit 10", db.Numeric)
    end_of_treatment = db.Column("End of Treatment", db.Numeric)
    follow_up = db.Column("Follow up", db.Numeric)
    end_of_study = db.Column("End of Study", db.Numeric)
    effective_date = db.Column("effective_date", db.Date)
    term_date = db.Column("term_date", db.Date)
    site_id = db.Column("Site ID", db.BigInteger)

    def __repr__(self):
        return f"<ClinicalVisit site_id={self.site_id}>"

# ----------------- DB INIT -----------------
with app.app_context():
    db.create_all()

# ----------------- EXAMPLE POSTS -----------------
posts = {
    1: {'title': 'https://pseudotrial.com/', 'content': 'Visit our homepage'},
    2: {'title': 'Clinical Trial Payment and Reconciliation Solution', 'content': 'Learn more about our solution here.'}
}

# ----------------- ROUTES -----------------
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/title')
def title():
    return render_template("index.html")

@app.route('/navigation')
def navigation():
    return render_template("navigation.html")

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = posts.get(post_id)
    if not post:
        return '<h1>404: Post Not Found</h1>'
    return f"<h1>{post['title']}</h1><p>{post['content']}</p>"

@app.route('/form_dashboard', methods=['GET', 'POST'])
def form_dashboard():
    form = MyForm()
    if form.validate_on_submit():
        form_data = {
            'conditional_procedure': form.conditional_procedure.data,
            'budget': form.budget.data,
            'screening_visit': form.screening_visit.data,
            'baseline_visit': form.baseline_visit.data,
            'end_of_treatment': form.end_of_treatment.data,
            'follow_up': form.follow_up.data,
            'end_of_study': form.end_of_study.data,
            'effective_date': form.effective_date.data,
            'term_date': form.term_date.data,
            'site_id': form.site_id.data,
        }
        for i in range(1, 11):
            form_data[f'visit_{i}'] = getattr(form, f'visit_{i}').data

        session['form_data'] = form_data
        return redirect(url_for('dashboard'))

    return render_template('form.html', form=form)

@app.route('/dashboard')
def dashboard():
    data = session.get('form_data')
    return render_template('dashboard.html', data=data)

@app.route('/form_success', methods=['GET', 'POST'])
def form_success():
    if request.method == 'POST':
        form_data = {key: request.form.get(key) for key in [
            'conditional_procedure', 'budget', 'screening_visit', 'baseline_visit',
            'end_of_treatment', 'follow_up', 'end_of_study',
            'effective_date', 'term_date', 'site_id'
        ]}
        for i in range(1, 11):
            form_data[f'visit_{i}'] = request.form.get(f'visit_{i}')

        if form_data['effective_date']:
            form_data['effective_date'] = datetime.datetime.strptime(
                form_data['effective_date'], "%Y-%m-%d").date()
        if form_data['term_date']:
            form_data['term_date'] = datetime.datetime.strptime(
                form_data['term_date'], "%Y-%m-%d").date()

        new_visit = ClinicalVisit(**form_data)
        try:
            db.session.add(new_visit)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "⚠️ Unique constraint failed! Maybe this site_id already exists."

        return render_template('success.html', data=form_data)

    return render_template('form.html', form=MyForm())

@app.route('/chart')
def chart():
    labels = ["Site A", "Site B", "Site C", "Site D"]
    values = [20000, 35000, 15000, 50000]
    return render_template("chart.html", labels=labels, values=values)

# ----------------- MAIN -----------------
if __name__ == "__main__":
    app.run(debug=True)

