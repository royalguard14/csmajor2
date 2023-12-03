from flask import Flask
def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'sgavdfajksbfsaifbjasd'
	


	# all route name:
	from .views import views



	#reg route:
	app.register_blueprint(views, url_prefix = '/')
	return app