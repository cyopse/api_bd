from datetime import time
from flask import Flask, request
from flask_restful import Resource, Api
from flask_caching import Cache
from werkzeug.wrappers import response
from models import Medicos, Especializacoes, Usuarios
from flask_httpauth import HTTPBasicAuth

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 100
}
auth = HTTPBasicAuth()
app = Flask(__name__)
app.config.from_mapping(config)
api = Api(app)
cache = Cache(app)

@auth.verify_password
def verificacao(login, senha):
    print('validação de usuário')
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class Medico(Resource):
    #Get
    @auth.login_required
    @cache.cached(timeout=10, key_prefix="medico_dados")
    def get(self, nome):
        medico = Medicos.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome':medico.nome,
                'idade':medico.idade,
                'id':medico.id
            }
            return response
        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Medico nao encontrado'
            }
        return response
    #Put
    @auth.login_required
    def put(self, nome):
        medico = Medicos.query.filter_by(nome=nome).first()
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
    @auth.login_required
    def delete(self, nome):
        medico = Medicos.query.filter_by(nome=nome).first()
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
    @auth.login_required
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
    @auth.login_required
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
    @auth.login_required
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
    @auth.login_required
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

api.add_resource(Medico, '/med/<string:nome>/')
api.add_resource(ListaMedicos, '/med/')
api.add_resource(Especializacao, '/specs/<int:id>/')
api.add_resource(ListaEspecializacoes, '/specs/')

if __name__ == '__main__':
    app.run(debug=True)