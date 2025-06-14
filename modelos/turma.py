from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base, session


class Turma(Base):
    __tablename__ = 'turmas'

    nome = Column(String, primary_key=True)
    periodo = Column(String)

    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")

    def __init__(self, nome, periodo):
        self.nome = nome
        self.periodo = periodo

    @classmethod
    def criar_turma(cls):
        try:
            nome = input("Digite o nome da turma: ").strip()
            periodo = input("Digite o período: ").strip()

            if not nome or not periodo:
                raise ValueError("Nome e período da turma não podem estar vazios.")

            turma_existente = session.query(cls).filter_by(nome=nome).first()
            if turma_existente:
                raise ValueError("Já existe uma turma com esse nome.")

            nova_turma = cls(nome=nome, periodo=periodo)
            session.add(nova_turma)
            session.commit()

            print(f"Turma '{nome}' criada com sucesso.")

        except Exception as e:
            session.rollback()
            print(f"Erro ao criar turma: {e}")

    @classmethod
    def excluir_turma(cls):
        try:
            nome = input("Digite o nome da turma que deseja excluir: ").strip()

            turma = session.query(cls).filter_by(nome=nome).first()
            if not turma:
                raise ValueError("Turma não encontrada.")

            session.delete(turma)
            session.commit()

            print(f"Turma '{nome}' excluída com sucesso.")

        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir turma: {e}")

    @classmethod
    def listar_turmas(cls):
        try:
            turmas = session.query(cls).all()
            if not turmas:
                print("Nenhuma turma cadastrada.")
                return

            print("\nLista de Turmas:")
            for turma in turmas:
                print(f"Turma: {turma.nome} | Período: {turma.periodo}")
                if turma.alunos:
                    print("Alunos:")
                    for aluno in turma.alunos:
                        print(f" - {aluno.nome} (CPF: {aluno.cpf})")
                else:
                    print(" - Nenhum aluno cadastrado nesta turma.")
                print("----------------------------")

        except Exception as e:
            print(f"Erro ao listar turmas: {e}")
