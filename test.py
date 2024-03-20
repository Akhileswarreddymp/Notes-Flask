from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy(app)

class Note(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']
        new_note = Note(title=title, description=description)
        db.session.add(new_note)
        db.session.commit()
    data = Note().query.all()
    print(data) 
    return render_template('index.html',data=data)


@app.route('/delete/<int:sno>')
def delete(sno):
    notedata = Note().query.filter_by(sno=sno).first()
    db.session.delete(notedata)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']
        notedata = Note().query.filter_by(sno=sno).first()
        notedata.title = title
        notedata.description = description
        db.session.add(notedata)
        db.session.commit()
        return redirect("/")
    notedata = Note().query.filter_by(sno=sno).first()
    return render_template('update.html',notedata = notedata)

if __name__ == '__main__':
    app.run(debug=True)
