from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


# Start by building our db model and database connection ------------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///projects.db"
db = SQLAlchemy(app)


class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column('Project Title', db.String())
	# TODO: eventually add datetime
	date = db.Column('Completion Date', db.String())
	description = db.Column('Description', db.Text)
	skills = db.Column('Skills', db.String())
	github_url = db.Column('GitHub Link', db. String())
    
	def __repr__(self):
		return f"""<Project (Name: {self.name})>"""


# Next let's create the routing in the website and create the app ---------------------------------
@app.route('/')
def index():
	projects = Project.query.all()
	return render_template('index.html', projects=projects)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/projects/new', methods=['GET', 'POST'])
def add_project():
	projects = Project.query.all()
	if request.form:
		new_project = Project(title=request.form['title'], date=request.form['date'],
                     description=request.form['desc'], skills=request.form['skills'],
                     github_url=request.form['github'])
		db.session.add(new_project)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('projectform.html', projects=projects)


@app.route('/projects/<id>')
def project(id):
	projects = Project.query.all()
	project = Project.query.get_or_404(id)
	return render_template('detail.html', project=project, projects=projects)


@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
	projects = Project.query.all()
	project = Project.query.get_or_404(id)
	if request.form:
		project.title = request.form['title']
		project.date = request.form['date']
		project.description = request.form['desc']
		project.skills = request.form['skills']
		project.github_url = request.form['github']
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('editproject.html', projects=projects, project=project)


@app.route('/projects/<id>/delete')
def delete_project(id):
	project = Project.query.get_or_404(id)
	db.session.delete(project)
	db.session.commit()
	return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', msg=error), 404


if __name__ == "__main__":
	with app.app_context():
		db.create_all()    
	app.run(debug=True, port=8000, host='127.0.0.1') 

