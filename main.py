from server import app
from secret import secret_data
for key in secret_data.keys():
    app.config[key] = secret_data[key]
from config import config_data
for key in config_data.keys():
    app.config[key] = config_data[key]


import controller
import model

# start server
app.run()