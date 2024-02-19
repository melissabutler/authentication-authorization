from models import User, connect_db, db, Feedback
from app import app

db.drop_all()
db.create_all()

user1 = User.register(username="missakat", password="catbutts", email="missakat@gmail.com", first_name="Missa", last_name="Kat")

db.session.add(user1)

db.session.commit()

feedback = Feedback(title="Test", content="Testing Content", username="missakat")

db.session.add(feedback)
db.session.commit()