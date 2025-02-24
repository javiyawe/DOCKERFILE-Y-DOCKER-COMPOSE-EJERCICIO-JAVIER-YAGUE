from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)

# Configuración de PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@postgres:5432/mydatabase'
db = SQLAlchemy(app)

# Configuración de Redis
redis_client = redis.Redis(host='redis', port=6379)

# Ruta básica de prueba
@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
