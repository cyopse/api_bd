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


class ListaEspecializacoes(Resource):
    #GetAll
    @cache.cached(timeout=10, key_prefix="especializacoes")
    def get(self):
        especializacoes = Especializacoes.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'medico':i.medico.nome} for i in especializacoes]
        return response
    #Post
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
api.add_resource(ListaEspecializacoes, '/specs/')

if __name__ == '__main__':
    app.run(debug=True)