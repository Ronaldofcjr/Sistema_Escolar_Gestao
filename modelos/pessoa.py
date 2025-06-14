from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, cpf=None, nome=None):
        if cpf is not None:
            self.cpf = cpf
        if nome is not None:
            self.nome = nome

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        cpf_str = str(cpf)
        if len(cpf_str) == 11 and cpf_str.isdigit():
            self._cpf = int(cpf_str)
        else:
            raise ValueError("CPF inválido. Deve ter 11 dígitos numéricos.")

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        if nome.strip() != "":
            self._nome = nome
        else:
            raise ValueError("Nome não pode ser vazio.")

    @abstractmethod
    def consultar_notas(self):
        pass