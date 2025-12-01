from elo import Elo
from model import Aluno

class Elo03_AvaliacaoFlexibilidade(Elo):
    """Avalia a flexibilidade através do teste de sentar e alcançar"""
    
    # Tabelas PROESP-Br - Valor mínimo em centímetros (Zona Saudável)
    TABELA_FLEXIBILIDADE = {
        6: {'M': 20, 'F': 22},
        7: {'M': 21, 'F': 23},
        8: {'M': 22, 'F': 24},
        9: {'M': 23, 'F': 25},
        10: {'M': 24, 'F': 26},
        11: {'M': 25, 'F': 27},
        12: {'M': 26, 'F': 28},
        13: {'M': 27, 'F': 29},
        14: {'M': 28, 'F': 30},
        15: {'M': 29, 'F': 31},
        16: {'M': 30, 'F': 32},
        17: {'M': 31, 'F': 33},
    }
    
    def _avaliar(self, aluno: Aluno):
        """Avalia a flexibilidade do aluno"""
        if aluno.sentar_alcancar is None or aluno.idade not in self.TABELA_FLEXIBILIDADE:
            aluno.detalhes_flexibilidade = {
                'status': 'incompleto',
                'mensagem': 'Dados insuficientes para avaliação'
            }
            return
        
        minimo = self.TABELA_FLEXIBILIDADE[aluno.idade][aluno.sexo]
        
        if aluno.sentar_alcancar >= minimo:
            status = 'saudavel'
            mensagem = 'Flexibilidade adequada'
        else:
            status = 'risco'
            diferenca = minimo - aluno.sentar_alcancar
            mensagem = f'Flexibilidade abaixo do ideal ({diferenca:.1f}cm de diferença)'
        
        aluno.detalhes_flexibilidade = {
            'status': status,
            'valor': aluno.sentar_alcancar,
            'minimo_ideal': minimo,
            'mensagem': mensagem
        }