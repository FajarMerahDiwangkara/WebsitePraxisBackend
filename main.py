import controller
import model
from secret import secret_data


# config and start server
from server import app, csrf
for key in secret_data.keys():
    app.config[key] = secret_data[key]
app.run()