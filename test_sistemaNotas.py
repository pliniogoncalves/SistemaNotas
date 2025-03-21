import unittest
from unittest.mock import MagicMock
from sistemaNotas import SistemaEstudantes

class TestSistemaEstudantes(unittest.TestCase):
    def setUp(self):
        self.listbox_ranking = MagicMock()
        self.sistema = SistemaEstudantes(self.listbox_ranking)

        # Mock dos elementos da interface gráfica
        self.entry_nome = MagicMock()
        self.entry_nota1 = MagicMock()
        self.entry_nota2 = MagicMock()
        self.entry_nota3 = MagicMock()

        # Simular os valores retornados pelos elementos da interface
        self.entry_nome.get.return_value = "João Silva"
        self.entry_nota1.get.return_value = "7"
        self.entry_nota2.get.return_value = "8"
        self.entry_nota3.get.return_value = "9"

    def test_validar_nome_vazio(self):
        with self.assertRaises(ValueError, msg="O nome não pode estar vazio."):
            self.sistema.criar_validador(lambda notas: notas)("", "7", "8", "9")

    def test_validar_nome_invalido(self):
        with self.assertRaises(ValueError, msg="O nome não pode conter números ou caracteres especiais."):
            self.sistema.criar_validador(lambda notas: notas)("João123", "7", "8", "9")

    def test_validar_notas_vazias(self):
        with self.assertRaises(ValueError, msg="Todos os campos de notas precisam ser preenchidos."):
            self.sistema.criar_validador(lambda notas: notas)("João Silva", "", "8", "9")

    def test_adicionar_estudante(self):
        adicionar_estudante = self.sistema.criar_adicionador()
        adicionar_estudante(self.entry_nome, self.entry_nota1, self.entry_nota2, self.entry_nota3)
        self.assertEqual(len(self.sistema.estudantes), 1, "Deve haver 1 estudante na lista após a adição.")
        self.assertEqual(self.sistema.estudantes[0]['nome'], "João Silva", "O nome do estudante deve ser 'João Silva'.")
        self.assertEqual(self.sistema.estudantes[0]['media'], 8.0, "A média do estudante deve ser 8.0.")

    def test_classificacao_estudantes(self):
        self.sistema.estudantes.append({'nome': 'João', 'media': 8})
        self.sistema.estudantes.append({'nome': 'Maria', 'media': 6})
        self.sistema.estudantes.append({'nome': 'Pedro', 'media': 4})
        self.sistema.atualizar_ranking()

        melhores = [e['nome'] for e in self.sistema.estudantes if e['media'] >= 7]
        recuperacao = [e['nome'] for e in self.sistema.estudantes if 5 <= e['media'] < 7]
        reprovados = [e['nome'] for e in self.sistema.estudantes if e['media'] < 5]

        self.assertEqual(melhores, ['João'], "João deve estar na lista de melhores.")
        self.assertEqual(recuperacao, ['Maria'], "Maria deve estar na lista de recuperação.")
        self.assertEqual(reprovados, ['Pedro'], "Pedro deve estar na lista de reprovados.")

    def test_notas_fora_do_intervalo(self):
        with self.assertRaises(ValueError, msg="As notas devem estar entre 1 e 10."):
            self.sistema.criar_validador(lambda notas: notas)("João Silva", "0", "8", "9")  # Nota 1 fora do intervalo
        with self.assertRaises(ValueError, msg="As notas devem estar entre 1 e 10."):
            self.sistema.criar_validador(lambda notas: notas)("João Silva", "7", "11", "9")  # Nota 2 fora do intervalo

    def test_nome_com_caracteres_especiais(self):
        with self.assertRaises(ValueError, msg="O nome não pode conter números ou caracteres especiais."):
            self.sistema.criar_validador(lambda notas: notas)("João@Silva", "7", "8", "9")  # Nome com caractere especial
        with self.assertRaises(ValueError, msg="O nome não pode conter números ou caracteres especiais."):
            self.sistema.criar_validador(lambda notas: notas)("João 123", "7", "8", "9")  # Nome com números

    def test_classificacao_media_exata(self):
        self.sistema.estudantes.append({'nome': 'Ana', 'media': 5})  # Média exatamente 5 (recuperação)
        self.sistema.estudantes.append({'nome': 'Carlos', 'media': 7})  # Média exatamente 7 (aprovado)
        self.sistema.atualizar_ranking()

        melhores = [e['nome'] for e in self.sistema.estudantes if e['media'] >= 7]
        recuperacao = [e['nome'] for e in self.sistema.estudantes if 5 <= e['media'] < 7]
        reprovados = [e['nome'] for e in self.sistema.estudantes if e['media'] < 5]

        self.assertEqual(melhores, ['Carlos'], "Carlos deve estar na lista de melhores.")
        self.assertEqual(recuperacao, ['Ana'], "Ana deve estar na lista de recuperação.")
        self.assertEqual(reprovados, [], "Nenhum estudante deve estar reprovado.")

if __name__ == "__main__":
    unittest.main()