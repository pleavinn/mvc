from elo import Elo
from model import Aluno

class Elo01_AvaliacaoIMC(Elo):
    """Avalia o IMC do aluno segundo os critérios do PROESP-Br"""
    
    # Tabelas de referência do PROESP-Br para IMC (simplificadas)
    # Formato: {idade: {'M': (min_saudavel, max_saudavel), 'F': (min_saudavel, max_saudavel)}}
    TABELA_IMC = {
        6: {'M': (14.5, 17.5), 'F': (14.3, 17.2)},
        7: {'M': (14.7, 17.9), 'F': (14.5, 17.6)},
        8: {'M': (14.9, 18.4), 'F': (14.7, 18.1)},
        9: {'M': (15.1, 18.9), 'F': (14.9, 18.7)},
        10: {'M': (15.4, 19.5), 'F': (15.2, 19.4)},
        11: {'M': (15.8, 20.2), 'F': (15.6, 20.2)},
        12: {'M': (16.2, 21.0), 'F': (16.1, 21.1)},
        13: {'M': (16.7, 21.8), 'F': (16.7, 22.0)},
        14: {'M': (17.3, 22.6), 'F': (17.3, 22.8)},
        15: {'M': (17.9, 23.3), 'F': (17.8, 23.4)},
        16: {'M': (18.4, 23.9), 'F': (18.2, 23.8)},
        17: {'M': (18.8, 24.3), 'F': (18.5, 24.0)},
    }
    
    def _avaliar(self, aluno: Aluno):
        """Avalia o IMC do aluno"""
        if not aluno.imc or aluno.idade not in self.TABELA_IMC:
            aluno.detalhes_imc = {
                'status': 'incompleto',
                'mensagem': 'Dados insuficientes para avaliação'
            }
            return
        
        faixa = self.TABELA_IMC[aluno.idade][aluno.sexo]
        min_saudavel, max_saudavel = faixa
        
        if min_saudavel <= aluno.imc <= max_saudavel:
            status = 'saudavel'
            mensagem = 'IMC dentro da zona saudável'
        else:
            status = 'risco'
            if aluno.imc < min_saudavel:
                mensagem = 'IMC abaixo da zona saudável (baixo peso)'
            else:
                mensagem = 'IMC acima da zona saudável (sobrepeso/obesidade)'
        
        aluno.detalhes_imc = {
            'status': status,
            'valor': round(aluno.imc, 1),
            'faixa_ideal': f"{min_saudavel} - {max_saudavel}",
            'mensagem': mensagem
        }
