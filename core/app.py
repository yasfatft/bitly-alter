if __name__ == 'core.app':
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object("core.config")
    app.secret_key = app.config['SECRET_KEY']

    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    import core.models
    db.create_all()

    from core.redis import Redis
    redis_configure = Redis(app.config['REDIS_HOST'], app.config['REDIS_PORT'])
    redis_configure.populate_redis()

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

    from celery import Celery
    client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    client.conf.update(app.config)

    from core.logic import RegexConverter
    app.url_map.converters['regex'] = RegexConverter
    import core.views

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
