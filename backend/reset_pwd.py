from app import app, db, User, bcrypt

def reset_pwd(username, password):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.commit()
            print(f"Password for {username} reset to {password}")
        else:
            print(f"User {username} not found")

if __name__ == "__main__":
    reset_pwd("umar", "umar123")
