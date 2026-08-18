from flask import Flask
from config.database import init_db, db
from controller.product_controller import product_controller

app = Flask(__name__)

init_db(app)

@app.route("/")
def helloworld():
    return "hello world"

app.register_blueprint(product_controller)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)