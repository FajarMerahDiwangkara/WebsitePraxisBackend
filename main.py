import controller
import model
from secret import secret_data


# config and start server
from server import app, csrf
app.config['SECRET_KEY'] = secret_data['SECRET_KEY']
app.config['databasewebsitepraxis_username'] = \
secret_data['databasewebsitepraxis_username']
app.config['databasewebsitepraxis_password'] = \
secret_data['databasewebsitepraxis_password']
app.run()