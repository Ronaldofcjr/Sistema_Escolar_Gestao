from database import session, Base, engine
from modelos.turma import Turma
from modelos.aluno import Aluno
from modelos.professor import Professor
from modelos.disciplina import Disciplina
from modelos.nota import Nota

def menu_principal():
    while True:
        print("\n===== Sistema Escolar =====")
        print("1 - Criar Aluno")
        print("2 - Criar Professor")
        print("3 - Turma")
        print("4 - Disciplina")
        print("5 - Aluno")
        print("6 - Professor")

        
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            Aluno.criar_aluno()
        elif escolha == '2':
            Professor.criar_professor()
        elif escolha == '3':
            menu_turma()
        elif escolha == '4':
            menu_disciplina()
        elif escolha == '5':
            menu_aluno()
        elif escolha == '6':
            menu_professor()
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")
            menu_principal()

def menu_aluno():
    while True:
        print("\n--- Menu Aluno ---")
        print("1 - Consultar Minhas Disciplinas")
        print("2 - Adicionar Aluno a Turma")
        print("3 - Listar Turmas do Aluno")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            Aluno.consultar_notas(session)
        elif escolha == '2':
            Aluno.adicionar_turma(session)
        elif escolha == '3':
            Aluno.listar_turma(session)
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")

def menu_professor():
    while True:
        print("\n--- Menu Professor ---")
        print("1 - Criar Nota")
        print("2 - Consultar Notas")
        print("3 - Modificar Nota")
        print("4 - Excluir Notas")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            Professor.criar_nota(session)
        elif escolha == '2':
            Professor.consultar_notas(session)
        elif escolha == '3':
            Professor.modificar_nota(session)
        elif escolha == '4':
            Professor.excluir_nota(session)
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")

def menu_disciplina():
    while True:
        print("\n--- Menu Disciplina ---")
        print("1 - Criar Disciplina")
        print("2 - Listar Disciplina")
        print("3 - Excluir Disciplina")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            Disciplina.criar_disciplina()
        elif escolha == '2':
            Disciplina.listar_disciplina(session)
        elif escolha == '3':
            Disciplina.excluir_disciplina(session)
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")


def menu_turma():
    while True:
        print("\n--- Menu Turma ---")
        print("1 - Criar Turma")
        print("2 - Excluir Turma")
        print("3 - Listar Turmas")
        print("0 - Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            Turma.criar_turma()
        elif escolha == '2':
            Turma.excluir_turma()
        elif escolha == '3':
            Turma.listar_turmas()
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    menu_principal()