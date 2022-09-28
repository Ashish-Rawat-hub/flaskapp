from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://users:userpass@mydb:5432/pgdb3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Names(db.Model):
    __tablename__ = 'names'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    def __init__(self, name, id):
        self.name = name
        self.id = id

db.create_all()
db.session.commit()

@app.route('/get/')
@app.route('/get/<int:pageno>:<int:pagesize>')
def getAll(pageno=1 , pagesize=3):
    pg = pageno
    pgs = pagesize
    page = request.args.get("page", pg , type=int)
    per_page = request.args.get("per-page", pgs, type=int)
    name = Names.query.paginate(page, per_page, error_out=True)
    results = {
        "results": [{"name": m.name, "id": m.id} for m in name.items],
        "pagination": {
            "count": name.total,
            "page": page,
            "per_page": per_page,
            "pages": name.pages,
        },
    }
    return jsonify(results)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/post/", methods=['GET'])
def post():
    return render_template('post.html')

@app.route("/add", methods=['POST'])
def add():
    name = request.form["name"]
    id = request.form["id"]
    entry = Names(name, id)
    db.session.add(entry)
    db.session.commit()

    return 'done'
    #return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)