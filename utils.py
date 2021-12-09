from models import Medicos


def inserir_medicos():
    medico = Medicos(nome='gabriel', idade='18')
    print(medico)
    medico.salvar()

def consultar_medicos():
    medico = Medicos.query.all()
    print(medico)
    medico = Medicos.query.filter_by(nome='gabriel').first()
    print(medico.idade)

def alterar_medicos():
    medico = Medicos.query.filter_by(nome='gabriel').first()
    medico.idade = 19
    medico.salvar()

def excluir_medicos():
    medico = Medicos.query.filter_by(nome='gabriel').first()
    medico.delete()

if __name__ == '__main__':
    #inserir_medicos()
    #alterar_medicos()
    excluir_medicos()
    consultar_medicos()

