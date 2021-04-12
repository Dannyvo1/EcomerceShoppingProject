from Final_WatchShoppingWeb import db


class useraccount():
    id = None           #id user
    username = None     #username
    password = None     #password
    firstname = None    #firstname
    lastname = None     #lastname
    contact_no = None   #Phone number
    email = None        #email
    position = None     #position
    age = None          #age
    gender = None       #gender

    def __repr__(self):
        return '<User %r>' % self.username

