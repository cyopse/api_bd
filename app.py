from datetime import time
from flask import Flask, request
from flask_restful import Resource, Api
from flask_caching import Cache
from werkzeug.wrappers import response
from models import Medicos, Especializacoes, Usuarios
from flask_jwt import JWT, jwt_required

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 100,
    'SECRET_KEY': 'TEST'
}
app = Flask(__name__)
app.config.from_mapping(config)
api = Api(app)
cache = Cache(app)

def verify(username, password):
    if not (username, password):
        return False
    return Usuarios.query.filter(Usuarios.login==username, Usuarios.senha==password).first()

def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}

jwt = JWT(app, verify, identity)

class Medico(Resource):
    #Get
    @cache.cached(timeout=10, key_prefix="medico_dados")
    def get(self, id):
        medico = Medicos.query.filter_by(id=id).first()
        try:
            response = {
                'id':medico.id,
                'nome':medico.nome,
                'idade':medico.idade
            }
            return response
        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Medico nao encontrado'
            }
        return response
    #Put
    @jwt_required()
    def put(self, id):
        medico = Medicos.query.filter_by(id=id).first()
        dados = request.json
        if 'nome' in dados:
            medico.nome = dados['nome']
        if 'idade' in dados:
            medico.idade = dados['idade']
        medico.salvar()
        response = {
            'id':medico.id,
            'nome':medico.nome,
            'idade':medico.idade
        }
        return response
    #Delete
    @jwt_required()
    def delete(self, id):
        medico = Medicos.query.filter_by(id=id).first()
        mensagem = 'Medico {} excluido com sucesso'.format(medico.nome)
        medico.delete()
        return {'status':'sucesso', 'mensagem':mensagem}


class ListaMedicos(Resource):
    #GetAll
    @cache.cached(timeout=20, key_prefix="medicos")
    def get(self):
        medicos = Medicos.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in medicos]
        print(response)
        return response
    #Post
    @jwt_required()
    def post(self):
        dados = request.json
        medico = Medicos(nome=dados['nome'], idade=dados['idade'])
        medico.salvar()
        response = {
            'id':medico.id,
            'nome':medico.nome,
            'idade':medico.idade
        }
        return response

class Especializacao(Resource):
    #Get
    @cache.cached(timeout=10, key_prefix="especializacao_dados")
    def get(self, id):
        especializacao = Especializacoes.query.filter_by(id = id).first()
        
        try:
            response = { 
                'id':especializacao.id,
                'nome':especializacao.nome
            }
            return response
        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Especialização nao encontrada'
            }
        return response
    
    #Put
    @jwt_required()
    def put(self, id):
        especializacao = Especializacoes.query.filter_by(id = id).first()
        dados = request.json

        if 'nome' in dados:
            especializacao.nome = dados['nome']

        especializacao.salvar()

        response = { 
            'id':especializacao.id,
            'nome':especializacao.nome
        }

        return response

    #Delete
    @jwt_required()
    def delete(self, id):
        especializacao = Especializacoes.query.filter_by(id = id).first()
        mensagem = 'Especialização {} excluida com sucesso'.format(especializacao.nome)
        especializacao.delete()
        return {'status':'sucesso', 'mensagem':mensagem}


class ListaEspecializacoes(Resource):
    #GetAll
    @cache.cached(timeout=10, key_prefix="especializacoes")
    def get(self):
        especializacoes = Especializacoes.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'medico':i.medico.nome} for i in especializacoes]
        return response
    #Post
    @jwt_required()
    def post(self):
        dados = request.json
        medico = Medicos.query.filter_by(nome=dados['medico']).first()
        especializacao = Especializacoes(nome=dados['nome'], medico=medico)
        especializacao.salvar()
        response = {
            'medico':especializacao.medico.nome,
            'nome':especializacao.nome,
            'id':especializacao.id
        }
        return response

api.add_resource(Medico, '/medicos/<int:id>/')
api.add_resource(ListaMedicos, '/medicos/')
api.add_resource(Especializacao, '/especializacoes/<int:id>/')
api.add_resource(ListaEspecializacoes, '/especializacoes/')

if __name__ == '__main__':
    app.run(debug=True)