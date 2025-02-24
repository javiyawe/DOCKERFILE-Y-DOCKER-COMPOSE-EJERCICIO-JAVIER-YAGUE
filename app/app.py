from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)

# Configuración de PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@postgres:5432/mydatabase'
db = SQLAlchemy(app)

# Configuración de Redis
redis_client = redis.Redis(host='redis', port=6379)

# Modelo de ejemplo
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'<Item {self.name}>'

# Ruta para crear un item
@app.route('/item/<name>')
def create_item(name):
    item = Item(name=name)
    db.session.add(item)
    db.session.commit()
    return f"Item {name} created!"


@app.route('/cached/<name>')
def get_cached_item(name):
    # Intentar obtener del caché
    cached = redis_client.get(name)
    
    if cached:
        return f"From cache: {cached.decode('utf-8')}"
    
    # Si no está en caché, buscar en la base de datos
    item = Item.query.filter_by(name=name).first()
    if item:
        # Guardar en caché para futuras consultas
        redis_client.setex(name, 3600, item.name)  # Expira en 1 hora
        return f"From database: {item.name}"
    
    return "Item not found"
