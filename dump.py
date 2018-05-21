
import dataset
db = dataset.connect('sqlite:///book.sqlite')
Users = db['user'].all()
print(Users)
