from app import crate_app, db

app = crate_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
