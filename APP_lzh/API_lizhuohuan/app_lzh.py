from flask import Flask
from flask_jwt_extended import JWTManager

import lizhuohuan.lzh_learn as lzh



app=Flask(__name__)
app.config['JWT_SECRET_KEY']='super-secret'
jwt=JWTManager(app)

app.register_blueprint(lzh.api_lzh)



if __name__=='__main__':
    app.run()