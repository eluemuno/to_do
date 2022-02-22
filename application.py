import os
import datetime
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, VARCHAR, TEXT, TIMESTAMP

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'scratchpad.db')
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    """show index page"""
    rows = Ideas.query.all()
    return render_template("index.html", data=rows)


@app.route('/ideas', methods=['POST'])
def ideas():
    title = request.form.get('title')
    details = request.form.get('details')
    payload = Ideas(title=title, details=details, date=datetime.datetime.now())
    db.session.add(payload)
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:plan_id>', methods=['GET'])
def delete(plan_id: int):
    idea = Ideas.query.filter_by(id=plan_id).first()
    if idea:
        db.session.delete(idea)
        db.session.commit()
        return redirect('/')
    else:
        return 'The given ID does not exist!', redirect('/')


class Ideas(db.Model):
    __tablename__ = 'ideas'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR, nullable=False)
    details = Column(TEXT)
    date = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    app.run(debug=True)
