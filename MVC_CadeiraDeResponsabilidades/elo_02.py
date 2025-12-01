from elo import Elo
from model import Aluno

class Elo02_AvaliacaoCorrida(Elo):
    """Avalia a resistência cardiorrespiratória através do teste de corrida de 6 minutos"""
    
    # Tabelas de referência PROESP-Br - Distância mínima em metros (Zona Saudável)
    TABELA_CORRIDA = {
        6: {'M': 900, 'F': 850},
        7: {'M': 950, 'F': 900},
        8: {'M': 1000, 'F': 950},
        9: {'M': 1050, 'F': 1000},
        10: {'M': 1100, 'F': 1050},
        11: {'M': 1150, 'F': 1100},
        12: {'M': 1200, 'F': 1150},
        13: {'M': 1300, 'F': 1200},
        14: {'M': 1400, 'F': 1250},
        15: {'M': 1500, 'F': 1300},
        16: {'M': 1550, 'F': 1350},
        17: {'M': 1600, 'F': 1400},
    }
    
    def _avaliar(self, aluno: Aluno):
        """Avalia o teste de corrida do aluno"""
        if aluno.distancia_corrida is None or aluno.idade not in self.TABELA_CORRIDA:
            aluno.detalhes_corrida = {
                'status': 'incompleto',
                'mensagem': 'Dados insuficientes para avaliação'
            }
            return
        
        distancia_minima = self.TABELA_CORRIDA[aluno.idade][aluno.sexo]
        
        if aluno.distancia_corrida >= distancia_minima:
            status = 'saudavel'
            mensagem = 'Resistência cardiorrespiratória adequada'
        else:
            status = 'risco'
            diferenca = distancia_minima - aluno.distancia_corrida
            mensagem = f'Abaixo do esperado ({diferenca}m de diferença)'
        
        aluno.detalhes_corrida = {
            'status': status,
            'valor': aluno.distancia_corrida,
            'minimo_ideal': distancia_minima,
            'mensagem': mensagem
        }
