from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, session
from modelos.pessoa import Pessoa
from modelos.disciplina import Disciplina
from modelos.nota import Nota
from modelos.aluno import Aluno

class CPFTamanhoError(Exception):
    pass

class ProfessorJaExisteError(Exception):
    pass

class DisciplinaNaoEncontradaError(Exception):
    pass

class CPFInvalidoError(Exception):
    pass

class NotaNaoEncontradaError(Exception):
    pass

class Professor(Base, Pessoa):
    __tablename__ = 'professores'

    cpf = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    disciplina_nome = Column(String, ForeignKey('disciplinas.nome'))

    disciplina = relationship("Disciplina", back_populates="professores")

    def __init__(self, cpf=None, nome=None, disciplina=None, **kwargs):
        super().__init__(cpf=cpf, nome=nome, **kwargs)
        self.disciplina = disciplina

    @classmethod
    def criar_professor(cls):
        try:
            cpf = input("Digite o CPF do professor (somente números): ").strip()
            if not cpf.isdigit():
                raise CPFInvalidoError("CPF inválido, precisa ser numérico.")
            if len(cpf) != 11:
                raise CPFTamanhoError("CPF precisa conter 11 dígitos")
            cpf = int(cpf)

            nome = input("Digite o nome do professor: ").strip()
            disciplina_nome = input("Digite o nome da disciplina: ").strip()

            if session.query(cls).filter_by(cpf=cpf).first():
                raise ProfessorJaExisteError("Já existe um professor com esse CPF!")

            disciplina = session.query(Disciplina).filter_by(nome=disciplina_nome).first()
            if not disciplina:
                raise DisciplinaNaoEncontradaError("Disciplina não encontrada.")

            novo_professor = cls(cpf=cpf, nome=nome, disciplina=disciplina)
            session.add(novo_professor)
            session.commit()

            print(f"Professor {nome} cadastrado com sucesso na disciplina {disciplina_nome}!")

        except (CPFInvalidoError, ProfessorJaExisteError, DisciplinaNaoEncontradaError) as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    @classmethod
    def criar_nota(cls, session):
        try:
            cpf_aluno = input("Digite o CPF do aluno: ").strip()
            if not cpf_aluno.isdigit():
                raise ValueError("CPF inválido.")
            cpf_aluno = int(cpf_aluno)

            disciplina_nome = input("Digite o nome da disciplina: ").strip()

            av1 = input("Digite a nota AV1: ").strip()
            av2 = input("Digite a nota AV2: ").strip()

            try:
                av1 = float(av1)
                av2 = float(av2)
            except ValueError:
                raise ValueError("Notas inválidas, digite números.")

            # Validação com raise
            if not (0 <= av1 <= 10):
                raise ValueError("AV1 deve estar entre 0 e 10.")
            if not (0 <= av2 <= 10):
                raise ValueError("AV2 deve estar entre 0 e 10.")

            aluno = session.query(Aluno).filter_by(cpf=cpf_aluno).first()
            if not aluno:
                raise ValueError("Aluno não encontrado.")

            disciplina = session.query(Disciplina).filter_by(nome=disciplina_nome).first()
            if not disciplina:
                raise ValueError("Disciplina não encontrada.")

            nova_nota = Nota(aluno_cpf=aluno.cpf, disciplina_nome=disciplina.nome, av1=av1, av2=av2)

            session.add(nova_nota)
            session.commit()

            print(f"Nota criada para o aluno {aluno.nome} na disciplina {disciplina.nome}.")

        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    @classmethod 
    def consultar_notas(cls, session):
        try:
            disciplina_nome = input("Digite o nome da disciplina para consultar as notas: ").strip()

            disciplina = session.query(Disciplina).filter_by(nome=disciplina_nome).first()
            if not disciplina:
                print("Disciplina não encontrada.")
                return

            notas = session.query(Nota).filter_by(disciplina_nome=disciplina_nome).all()

            if not notas:
                print(f"Não há notas cadastradas para a disciplina {disciplina_nome}.")
                return

            print(f"\nNotas da disciplina {disciplina_nome}:\n")
            for nota in notas:
                aluno = session.query(Aluno).filter_by(cpf=nota.aluno_cpf).first()
                nome_aluno = aluno.nome if aluno else "Aluno desconhecido"
                av1 = nota.av1 if nota.av1 is not None else "Indisponível"
                av2 = nota.av2 if nota.av2 is not None else "Indisponível"

                if (nota.av1 is not None and nota.av2 is not None):
                    media = nota.media()

                    if media >= 5:
                        situacao = "Aprovado"
                    elif 4 <= media < 5:
                        situacao = "Recuperação"
                    else:
                        situacao = "Reprovado"
                else:
                    media = "Indisponível"
                    situacao = "Situação indefinida (notas incompletas)"

                print(f"Aluno: {nome_aluno} (CPF: {nota.aluno_cpf})")
                print(f"  AV1: {av1}")
                print(f"  AV2: {av2}")
                print(f"  Média: {media}")
                print(f"  Situação: {situacao}\n")

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    @classmethod
    def modificar_nota(cls, session):
        try:
            disciplina_nome = input("Digite o nome da disciplina: ").strip()
            aluno_cpf = input("Digite o CPF do aluno: ").strip()

            if not aluno_cpf.isdigit():
                print("CPF inválido, deve conter somente números.")
                return
            aluno_cpf = int(aluno_cpf)

            disciplina = session.query(Disciplina).filter_by(nome=disciplina_nome).first()
            if not disciplina:
                print("Disciplina não encontrada.")
                return

            nota = session.query(Nota).filter_by(disciplina_nome=disciplina_nome, aluno_cpf=aluno_cpf).first()
            if not nota:
                print("Nota para esse aluno e disciplina não encontrada.")
                return

            def validar_nota(input_str):
                try:
                    valor = float(input_str)
                    if 0 <= valor <= 10:
                        return valor
                    else:
                        print("Nota deve estar entre 0 e 10. Valor ignorado.")
                        return None
                except ValueError:
                    print("Entrada inválida, valor ignorado.")
                    return None

            av1_input = input(f"Digite a nova nota para AV1 (atual: {nota.av1}): ").strip()
            av2_input = input(f"Digite a nova nota para AV2 (atual: {nota.av2}): ").strip()

            av1 = validar_nota(av1_input)
            av2 = validar_nota(av2_input)

            if av1 is not None:
                nota.av1 = av1
            if av2 is not None:
                nota.av2 = av2

            session.commit()
            print("Notas atualizadas com sucesso!")

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    @classmethod
    def excluir_nota(cls, session):
        try:
            cpf_aluno = input("Digite o CPF do aluno: ").strip()
            if not cpf_aluno.isdigit():
                raise ValueError("CPF inválido.")
            cpf_aluno = int(cpf_aluno)

            disciplina_nome = input("Digite o nome da disciplina: ").strip()

            aluno = session.query(Aluno).filter_by(cpf=cpf_aluno).first()
            if not aluno:
                raise ValueError("Aluno não encontrado.")

            disciplina = session.query(Disciplina).filter_by(nome=disciplina_nome).first()
            if not disciplina:
                raise ValueError("Disciplina não encontrada.")

            nota = session.query(Nota).filter_by(aluno_cpf=aluno.cpf, disciplina_nome=disciplina.nome).first()
            if not nota:
                raise ValueError("Nota para este aluno e disciplina não encontrada.")

            session.delete(nota)
            session.commit()
            print(f"Nota da disciplina {disciplina.nome} para o aluno {aluno.nome} excluída com sucesso!")

        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")