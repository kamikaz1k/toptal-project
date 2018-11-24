from create_app import create_app, db

if __name__ == '__main__':

    app = create_app()
    with app.app_context():
        # import models...
        db.create_all()