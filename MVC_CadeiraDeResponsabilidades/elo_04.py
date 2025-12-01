from elo import Elo
from model import Aluno

class Elo04_AvaliacaoAbdominais(Elo):
    """Avalia a força/resistência abdominal através do teste de abdominais em 1 minuto"""
    
    # Tabelas PROESP-Br - Número mínimo de repetições (Zona Saudável)
    TABELA_ABDOMINAIS = {
        6: {'M': 20, 'F': 18},
        7: {'M': 22, 'F': 20},
        8: {'M': 24, 'F': 22},
        9: {'M': 26, 'F': 24},
        10: {'M': 28, 'F': 26},
        11: {'M': 30, 'F': 28},
        12: {'M': 32, 'F': 30},
        13: {'M': 35, 'F': 32},
        14: {'M': 38, 'F': 34},
        15: {'M': 40, 'F': 36},
        16: {'M': 42, 'F': 38},
        17: {'M': 44, 'F': 40},
    }
    
    def _avaliar(self, aluno: Aluno):
        """Avalia a força abdominal do aluno"""
        if aluno.abdominais is None or aluno.idade not in self.TABELA_ABDOMINAIS:
            aluno.detalhes_abdominais = {
                'status': 'incompleto',
                'mensagem': 'Dados insuficientes para avaliação'
            }
            return
        
        minimo = self.TABELA_ABDOMINAIS[aluno.idade][aluno.sexo]
        
        if aluno.abdominais >= minimo:
            status = 'saudavel'
            mensagem = 'Força abdominal adequada'
        else:
            status = 'risco'
            diferenca = minimo - aluno.abdominais
            mensagem = f'Abaixo do esperado ({diferenca} repetições de diferença)'
        
        aluno.detalhes_abdominais = {
            'status': status,
            'valor': aluno.abdominais,
            'minimo_ideal': minimo,
            'mensagem': mensagem
        }
