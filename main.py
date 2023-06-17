import controller
import model
from secret import secret_data


# config and start server
from server import app, csrf
# https://www.pascallandau.com/blog/git-secret-encrypt-repository-docker/#adding-and-encrypting-files
app.config['SECRET_KEY'] = secret_data['SECRET_KEY']
app.config['databasewebsitepraxis_username'] = \
secret_data['databasewebsitepraxis_username']
app.config['databasewebsitepraxis_password'] = \
secret_data['databasewebsitepraxis_password']
app.run()