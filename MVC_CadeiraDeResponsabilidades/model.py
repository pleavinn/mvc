from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# ======================================================================================
# CLASSES DE DADOS
# ======================================================================================

class Aluno:
    """Representa um aluno com seus dados pessoais e resultados dos testes"""
    
    def __init__(self, nome: str, idade: int, sexo: str):
        self.nome = nome
        self.idade = idade
        self.sexo = sexo  # 'M' ou 'F'
        
        # Dados cardiovasculares
        self.peso: Optional[float] = None
        self.altura: Optional[float] = None
        self.imc: Optional[float] = None
        self.distancia_corrida: Optional[int] = None  # metros em 6 minutos
        
        # Dados musculoesqueléticos
        self.sentar_alcancar: Optional[float] = None  # centímetros
        self.abdominais: Optional[int] = None  # repetições em 1 minuto
        
        # Resultados das avaliações
        self.status_cardiovascular: Optional[str] = None  # 'saudavel' ou 'risco'
        self.status_musculoesqueletico: Optional[str] = None  # 'saudavel' ou 'risco'
        self.cluster_cardiovascular: Optional[int] = None  # Cluster K-Means (0=risco, 1=saudável)
        self.cluster_musculoesqueletico: Optional[int] = None  # Cluster K-Means (0=risco, 1=saudável)
        self.cluster_geral: Optional[int] = None  # Cluster geral (0=risco, 1=saudável)
        
        # Detalhes dos resultados
        self.detalhes_imc: Dict = {}
        self.detalhes_corrida: Dict = {}
        self.detalhes_flexibilidade: Dict = {}
        self.detalhes_abdominais: Dict = {}
    
    def calcular_imc(self):
        """Calcula o IMC se peso e altura estão disponíveis"""
        if self.peso and self.altura:
            self.imc = self.peso / (self.altura ** 2)
    
    def __repr__(self):
        return f"Aluno({self.nome}, {self.idade} anos, {self.sexo})"


# ======================================================================================
# CADEIA DE RESPONSABILIDADE - CLASSE BASE
# ======================================================================================

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


# ======================================================================================
# ELO 01 - AVALIAÇÃO DE IMC
# ======================================================================================

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


# ======================================================================================
# ELO 02 - AVALIAÇÃO DE RESISTÊNCIA CARDIORRESPIRATÓRIA (CORRIDA)
# ======================================================================================

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


# ======================================================================================
# ELO 03 - AVALIAÇÃO DE FLEXIBILIDADE (SENTAR E ALCANÇAR)
# ======================================================================================

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


# ======================================================================================
# ELO 04 - AVALIAÇÃO DE FORÇA ABDOMINAL
# ======================================================================================

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


# ======================================================================================
# ELO 05 - CONSOLIDAÇÃO DOS RESULTADOS
# ======================================================================================

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


# ======================================================================================
# ANALISADOR K-MEANS
# ======================================================================================

class AnalisadorKMeans:
    """Realiza análise de clusters usando K-Means para classificar alunos"""
    
    def __init__(self, n_clusters: int = 2):
        """
        Inicializa o analisador K-Means
        
        Args:
            n_clusters: Número de clusters (padrão 2: zona saudável e zona de risco)
        """
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans_cardio = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.kmeans_musculo = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.kmeans_geral = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    
    def analisar_cardiovascular(self, alunos: List[Aluno]) -> Dict:
        """
        Analisa e agrupa alunos por saúde cardiovascular usando K-Means
        
        Returns:
            Dicionário com estatísticas dos clusters
        """
        # Filtrar alunos com dados completos
        alunos_completos = [a for a in alunos if a.imc and a.distancia_corrida]
        
        if len(alunos_completos) < 2:
            return {'erro': 'Dados insuficientes para análise (mínimo 2 alunos)'}
        
        # Preparar dados: [IMC, Distância Corrida]
        dados = np.array([[a.imc, a.distancia_corrida] for a in alunos_completos])
        
        # Normalizar dados
        dados_normalizados = self.scaler.fit_transform(dados)
        
        # Aplicar K-Means
        clusters = self.kmeans_cardio.fit_predict(dados_normalizados)
        
        # Identificar qual cluster é saudável (maior média de distância corrida)
        cluster_0_media = np.mean([a.distancia_corrida for a, c in zip(alunos_completos, clusters) if c == 0])
        cluster_1_media = np.mean([a.distancia_corrida for a, c in zip(alunos_completos, clusters) if c == 1])
        
        cluster_saudavel = 1 if cluster_1_media > cluster_0_media else 0
        cluster_risco = 0 if cluster_saudavel == 1 else 1
        
        # Atribuir clusters aos alunos
        for aluno, cluster in zip(alunos_completos, clusters):
            aluno.cluster_cardiovascular = cluster
        
        # Estatísticas
        total = len(alunos_completos)
        count_saudavel = np.sum(clusters == cluster_saudavel)
        count_risco = np.sum(clusters == cluster_risco)
        
        return {
            'total_analisados': total,
            'cluster_saudavel': cluster_saudavel,
            'cluster_risco': cluster_risco,
            'alunos_zona_saudavel': count_saudavel,
            'alunos_zona_risco': count_risco,
            'percentual_saudavel': (count_saudavel / total * 100) if total > 0 else 0,
            'percentual_risco': (count_risco / total * 100) if total > 0 else 0,
            'centroides': self.kmeans_cardio.cluster_centers_.tolist()
        }
    
    def analisar_musculoesqueletico(self, alunos: List[Aluno]) -> Dict:
        """
        Analisa e agrupa alunos por saúde musculoesquelética usando K-Means
        
        Returns:
            Dicionário com estatísticas dos clusters
        """
        # Filtrar alunos com dados completos
        alunos_completos = [a for a in alunos if a.sentar_alcancar and a.abdominais]
        
        if len(alunos_completos) < 2:
            return {'erro': 'Dados insuficientes para análise (mínimo 2 alunos)'}
        
        # Preparar dados: [Flexibilidade, Abdominais]
        dados = np.array([[a.sentar_alcancar, a.abdominais] for a in alunos_completos])
        
        # Normalizar dados
        dados_normalizados = self.scaler.fit_transform(dados)
        
        # Aplicar K-Means
        clusters = self.kmeans_musculo.fit_predict(dados_normalizados)
        
        # Identificar qual cluster é saudável (maior média de abdominais)
        cluster_0_media = np.mean([a.abdominais for a, c in zip(alunos_completos, clusters) if c == 0])
        cluster_1_media = np.mean([a.abdominais for a, c in zip(alunos_completos, clusters) if c == 1])
        
        cluster_saudavel = 1 if cluster_1_media > cluster_0_media else 0
        cluster_risco = 0 if cluster_saudavel == 1 else 1
        
        # Atribuir clusters aos alunos
        for aluno, cluster in zip(alunos_completos, clusters):
            aluno.cluster_musculoesqueletico = cluster
        
        # Estatísticas
        total = len(alunos_completos)
        count_saudavel = np.sum(clusters == cluster_saudavel)
        count_risco = np.sum(clusters == cluster_risco)
        
        return {
            'total_analisados': total,
            'cluster_saudavel': cluster_saudavel,
            'cluster_risco': cluster_risco,
            'alunos_zona_saudavel': count_saudavel,
            'alunos_zona_risco': count_risco,
            'percentual_saudavel': (count_saudavel / total * 100) if total > 0 else 0,
            'percentual_risco': (count_risco / total * 100) if total > 0 else 0,
            'centroides': self.kmeans_musculo.cluster_centers_.tolist()
        }
    
    def analisar_geral(self, alunos: List[Aluno]) -> Dict:
        """
        Analisa e agrupa alunos considerando todos os aspectos (análise geral)
        
        Returns:
            Dicionário com estatísticas dos clusters gerais
        """
        # Filtrar alunos com dados completos
        alunos_completos = [a for a in alunos 
                           if a.imc and a.distancia_corrida and 
                              a.sentar_alcancar and a.abdominais]
        
        if len(alunos_completos) < 2:
            return {'erro': 'Dados insuficientes para análise (mínimo 2 alunos)'}
        
        # Preparar dados: [IMC, Corrida, Flexibilidade, Abdominais]
        dados = np.array([
            [a.imc, a.distancia_corrida, a.sentar_alcancar, a.abdominais] 
            for a in alunos_completos
        ])
        
        # Normalizar dados
        dados_normalizados = self.scaler.fit_transform(dados)
        
        # Aplicar K-Means
        clusters = self.kmeans_geral.fit_predict(dados_normalizados)
        
        # Identificar qual cluster é saudável (análise multifatorial)
        # Usamos média ponderada: corrida e abdominais têm peso maior
        def calcular_score(aluno):
            return (aluno.distancia_corrida * 0.4 + 
                   aluno.abdominais * 10 * 0.4 +  # Multiplicado por 10 para normalizar escala
                   aluno.sentar_alcancar * 10 * 0.2)  # Peso menor para flexibilidade
        
        cluster_0_score = np.mean([calcular_score(a) for a, c in zip(alunos_completos, clusters) if c == 0])
        cluster_1_score = np.mean([calcular_score(a) for a, c in zip(alunos_completos, clusters) if c == 1])
        
        cluster_saudavel = 1 if cluster_1_score > cluster_0_score else 0
        cluster_risco = 0 if cluster_saudavel == 1 else 1
        
        # Atribuir clusters aos alunos
        for aluno, cluster in zip(alunos_completos, clusters):
            aluno.cluster_geral = cluster
        
        # Estatísticas
        total = len(alunos_completos)
        count_saudavel = np.sum(clusters == cluster_saudavel)
        count_risco = np.sum(clusters == cluster_risco)
        
        return {
            'total_analisados': total,
            'cluster_saudavel': cluster_saudavel,
            'cluster_risco': cluster_risco,
            'alunos_zona_saudavel': count_saudavel,
            'alunos_zona_risco': count_risco,
            'percentual_saudavel': (count_saudavel / total * 100) if total > 0 else 0,
            'percentual_risco': (count_risco / total * 100) if total > 0 else 0,
            'centroides': self.kmeans_geral.cluster_centers_.tolist()
        }


# ======================================================================================
# MODEL PRINCIPAL
# ======================================================================================

class Model:
    """Model principal do sistema - gerencia alunos e processamento via cadeia"""
    
    def __init__(self):
        self.alunos: List[Aluno] = []
        self.analisador_kmeans = AnalisadorKMeans(n_clusters=2)
        self._construir_cadeia()
    
    def _construir_cadeia(self):
        """Constrói a cadeia de responsabilidade"""
        self.elo01 = Elo01_AvaliacaoIMC()
        self.elo02 = Elo02_AvaliacaoCorrida()
        self.elo03 = Elo03_AvaliacaoFlexibilidade()
        self.elo04 = Elo04_AvaliacaoAbdominais()
        self.elo05 = Elo05_Consolidacao()
        
        # Encadear os elos
        self.elo01.definir_proximo(self.elo02) \
                  .definir_proximo(self.elo03) \
                  .definir_proximo(self.elo04) \
                  .definir_proximo(self.elo05)
    
    def adicionar_aluno(self, nome: str, idade: int, sexo: str) -> Aluno:
        """Adiciona um novo aluno ao sistema"""
        aluno = Aluno(nome, idade, sexo)
        self.alunos.append(aluno)
        return aluno
    
    def processar_aluno(self, aluno: Aluno) -> Aluno:
        """Processa um aluno através da cadeia de responsabilidade"""
        # Calcular IMC se necessário
        aluno.calcular_imc()
        
        # Processar através da cadeia
        return self.elo01.processar(aluno)
    
    def obter_aluno(self, nome: str) -> Optional[Aluno]:
        """Busca um aluno pelo nome"""
        for aluno in self.alunos:
            if aluno.nome == nome:
                return aluno
        return None
    
    def obter_todos_alunos(self) -> List[Aluno]:
        """Retorna todos os alunos cadastrados"""
        return self.alunos
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas gerais do sistema"""
        total = len(self.alunos)
        
        if total == 0:
            return {
                'total': 0,
                'cardio_saudavel': 0,
                'cardio_risco': 0,
                'musculo_saudavel': 0,
                'musculo_risco': 0
            }
        
        cardio_saudavel = sum(1 for a in self.alunos if a.status_cardiovascular == 'saudavel')
        musculo_saudavel = sum(1 for a in self.alunos if a.status_musculoesqueletico == 'saudavel')
        
        return {
            'total': total,
            'cardio_saudavel': cardio_saudavel,
            'cardio_risco': total - cardio_saudavel,
            'musculo_saudavel': musculo_saudavel,
            'musculo_risco': total - musculo_saudavel
        }
    
    def executar_analise_kmeans(self) -> Dict:
        """
        Executa análise completa com K-Means para todos os alunos
        
        Returns:
            Dicionário com resultados das três análises
        """
        resultados = {
            'cardiovascular': self.analisador_kmeans.analisar_cardiovascular(self.alunos),
            'musculoesqueletico': self.analisador_kmeans.analisar_musculoesqueletico(self.alunos),
            'geral': self.analisador_kmeans.analisar_geral(self.alunos)
        }
        
        return resultados
    
    def obter_alunos_por_cluster(self, tipo: str, cluster: int) -> List[Aluno]:
        """
        Retorna alunos de um cluster específico
        
        Args:
            tipo: 'cardiovascular', 'musculoesqueletico' ou 'geral'
            cluster: número do cluster (0 ou 1)
        
        Returns:
            Lista de alunos do cluster
        """
        if tipo == 'cardiovascular':
            return [a for a in self.alunos if a.cluster_cardiovascular == cluster]
        elif tipo == 'musculoesqueletico':
            return [a for a in self.alunos if a.cluster_musculoesqueletico == cluster]
        elif tipo == 'geral':
            return [a for a in self.alunos if a.cluster_geral == cluster]
        return []


# ======================================================================================
# EXEMPLO DE USO
# ======================================================================================

if __name__ == "__main__":
    # Criar o model
    model = Model()
    
    # Adicionar vários alunos para teste do K-Means
    alunos_teste = [
        {"nome": "João Silva", "idade": 12, "sexo": "M", "peso": 45, "altura": 1.55, 
         "corrida": 1150, "flex": 24, "abd": 30},
        {"nome": "Maria Santos", "idade": 12, "sexo": "F", "peso": 42, "altura": 1.50, 
         "corrida": 1100, "flex": 27, "abd": 28},
        {"nome": "Pedro Costa", "idade": 13, "sexo": "M", "peso": 60, "altura": 1.60, 
         "corrida": 950, "flex": 20, "abd": 22},
        {"nome": "Ana Oliveira", "idade": 13, "sexo": "F", "peso": 48, "altura": 1.58, 
         "corrida": 1180, "flex": 29, "abd": 31},
        {"nome": "Lucas Ferreira", "idade": 14, "sexo": "M", "peso": 65, "altura": 1.65, 
         "corrida": 1000, "flex": 23, "abd": 25},
        {"nome": "Beatriz Lima", "idade": 14, "sexo": "F", "peso": 50, "altura": 1.60, 
         "corrida": 1220, "flex": 30, "abd": 33},
    ]
    
    # Adicionar e processar alunos
    for dados in alunos_teste:
        aluno = model.adicionar_aluno(dados["nome"], dados["idade"], dados["sexo"])
        aluno.peso = dados["peso"]
        aluno.altura = dados["altura"]
        aluno.distancia_corrida = dados["corrida"]
        aluno.sentar_alcancar = dados["flex"]
        aluno.abdominais = dados["abd"]
        
        # Processar através da cadeia de responsabilidade
        model.processar_aluno(aluno)
    
    print("=" * 70)
    print("ANÁLISE COM CADEIA DE RESPONSABILIDADE")
    print("=" * 70)
    
    # Exibir resultados da cadeia
    for aluno in model.alunos:
        print(f"\n{aluno.nome} ({aluno.idade} anos, {aluno.sexo})")
        print(f"  Cardiovascular: {aluno.status_cardiovascular}")
        print(f"  Musculoesquelético: {aluno.status_musculoesqueletico}")
    
    print("\n" + "=" * 70)
    print("ANÁLISE COM K-MEANS (CLUSTERING)")
    print("=" * 70)
    
    # Executar análise K-Means
    resultados_kmeans = model.executar_analise_kmeans()
    
    print("\n📊 ANÁLISE CARDIOVASCULAR (K-Means):")
    if 'erro' not in resultados_kmeans['cardiovascular']:
        stats = resultados_kmeans['cardiovascular']
        print(f"  Total analisados: {stats['total_analisados']}")
        print(f"  Zona Saudável: {stats['alunos_zona_saudavel']} ({stats['percentual_saudavel']:.1f}%)")
        print(f"  Zona de Risco: {stats['alunos_zona_risco']} ({stats['percentual_risco']:.1f}%)")
    
    print("\n📊 ANÁLISE MUSCULOESQUELÉTICA (K-Means):")
    if 'erro' not in resultados_kmeans['musculoesqueletico']:
        stats = resultados_kmeans['musculoesqueletico']
        print(f"  Total analisados: {stats['total_analisados']}")
        print(f"  Zona Saudável: {stats['alunos_zona_saudavel']} ({stats['percentual_saudavel']:.1f}%)")
        print(f"  Zona de Risco: {stats['alunos_zona_risco']} ({stats['percentual_risco']:.1f}%)")
    
    print("\n📊 ANÁLISE GERAL (K-Means - Todos os Aspectos):")
    if 'erro' not in resultados_kmeans['geral']:
        stats = resultados_kmeans['geral']
        print(f"  Total analisados: {stats['total_analisados']}")
        print(f"  Zona Saudável: {stats['alunos_zona_saudavel']} ({stats['percentual_saudavel']:.1f}%)")
        print(f"  Zona de Risco: {stats['alunos_zona_risco']} ({stats['percentual_risco']:.1f}%)")
    
    print("\n" + "=" * 70)
    print("CLUSTERS ATRIBUÍDOS POR ALUNO")
    print("=" * 70)
    
    for aluno in model.alunos:
        print(f"\n{aluno.nome}:")
        print(f"  Cluster Cardiovascular: {aluno.cluster_cardiovascular}")
        print(f"  Cluster Musculoesquelético: {aluno.cluster_musculoesqueletico}")
        print(f"  Cluster Geral: {aluno.cluster_geral}")