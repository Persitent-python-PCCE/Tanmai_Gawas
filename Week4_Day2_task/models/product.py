from config.database import db

class Product(db.Model):
    __tablename__="product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "category" : self.category,
            "price" : self.price,
            "quantity":self.quantity,
            "description":self.description
        }