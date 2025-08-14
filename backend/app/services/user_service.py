from app.extensions import db
from app.models.user import User

class UserService:
    def get_all_users(self):
        return User.query.all()

    def create_user(self, username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    
    def update_user(self, user_id, username=None, email=None):
        user = User.query.get(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if email:
            user.email = email
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True
