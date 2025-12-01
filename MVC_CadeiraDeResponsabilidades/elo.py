from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from model import Aluno

class Elo(ABC):
    """Classe abstrata base para os elos da cadeia de responsabilidade"""
    
    def __init__(self):
        self._proximo_elo: Optional['Elo'] = None
    
    def definir_proximo(self, elo: 'Elo') -> 'Elo':
        """Define o próximo elo na cadeia"""
        self._proximo_elo = elo
        return elo
    
    def processar(self, aluno: Aluno) -> Aluno:
        """Processa o aluno e passa para o próximo elo"""
        self._avaliar(aluno)
        
        if self._proximo_elo:
            return self._proximo_elo.processar(aluno)
        
        return aluno
    
    @abstractmethod
    def _avaliar(self, aluno: Aluno):
        """Método abstrato que cada elo deve implementar"""
        pass