from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column( db.String(50) )
    contenido = db.Column( db.String(255) )
    
class Publicacion_Schema(ma.Schema):
    class Meta:
        fields = ("id", "titulo", "contenido")
    
post_schema = Publicacion_Schema()
posts_schema = Publicacion_Schema(many = True)

class RecursoListarPublicaciones(Resource):
    def get(self):
        publicaciones = Publicacion.query.all()
        return posts_schema.dump(publicaciones)
    
    def post(self):
            nueva_publicacion = Publicacion(
                titulo = request.json['titulo'],
                contenido=request.json['contenido']
            )
            db.session.add(nueva_publicacion)
            db.session.commit()
            return post_schema.dump(nueva_publicacion)
     
class RecursoUnaPublicacion(Resource):
    def get(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        return post_schema.dump(publicacion)
    
    def put(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)

        if 'titulo' in request.json:
            publicacion.titulo = request.json['titulo']
        if 'contenido' in request.json:
            publicacion.contenido = request.json['contenido']

        db.session.commit()
        return post_schema.dump(publicacion)

    def delete(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        db.session.delete(publicacion)
        db.session.commit()
        return '', 204

api.add_resource(RecursoListarPublicaciones, '/publicaciones')     
api.add_resource(RecursoUnaPublicacion, '/publicaciones/<int:id_publicacion>')

if __name__ == '__main__':
    app.run(debug=True)
