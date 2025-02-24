from mongoengine import Document, StringField

class User(Document):
  name: str = StringField(required=True, max_length=50)
  surname: str = StringField(required=True, max_length=100)
  email: str = StringField(required=False)
  phone_number: str = StringField(required=False)
  role: str = StringField(required=False)
  group_name: str = StringField(required=False)
  secret_code: str = StringField(requred=True)

  def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role.value,
            "group_name": self.group_name,
            "secret_code": self.secret_code
        }