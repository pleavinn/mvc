from elo import Elo
from model import Aluno

class Elo05_Consolidacao(Elo):
    """Consolida todos os resultados e define o status geral do aluno"""
    
    def _avaliar(self, aluno: Aluno):
        """Consolida os resultados das avaliações cardiovascular e musculoesquelética"""
        
        # Avaliação Cardiovascular (IMC + Corrida)
        imc_ok = aluno.detalhes_imc.get('status') == 'saudavel'
        corrida_ok = aluno.detalhes_corrida.get('status') == 'saudavel'
        
        if imc_ok and corrida_ok:
            aluno.status_cardiovascular = 'saudavel'
        else:
            aluno.status_cardiovascular = 'risco'
        
        # Avaliação Musculoesquelética (Flexibilidade + Abdominais)
        flex_ok = aluno.detalhes_flexibilidade.get('status') == 'saudavel'
        abd_ok = aluno.detalhes_abdominais.get('status') == 'saudavel'
        
        if flex_ok and abd_ok:
            aluno.status_musculoesqueletico = 'saudavel'
        else:
            aluno.status_musculoesqueletico = 'risco'