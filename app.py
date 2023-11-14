from flask import Flask, redirect, url_for
from controllers.product import product
from controllers.user import user
from controllers.order import order
from controllers.payment import payment

app = Flask(__name__)

app.secret_key = 'online-store'

app.register_blueprint(product, url_prefix='/products')
app.register_blueprint(user, url_prefix='/users')
app.register_blueprint(order, url_prefix='/orders')
app.register_blueprint(payment, url_prefix='/payments')

@app.route("/")
def home():
    return redirect(url_for('product.get_products'))


if __name__ == "__main__":
	app.run(debug=True)