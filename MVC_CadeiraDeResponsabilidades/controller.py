from typing import Dict, List, Optional, Tuple
from tkinter import messagebox


class Controller:
    """Controller - Coordena a comunicação entre Model e View"""
    
    def __init__(self, view, model):
        """
        Inicializa o controller com referências ao Model e View
        
        Args:
            model: Instância do Model
            view: Instância da View
        """
        self.model = model
        self.view = view
        
        # Conectar eventos da view com métodos do controller
        self._conectar_eventos()
        
        # Aluno atualmente selecionado para exibir detalhes
        self.aluno_selecionado = None
    
    def _conectar_eventos(self):
        """Conecta os eventos da View aos métodos do Controller"""
        # Você pode adicionar callbacks aqui conforme necessário
        # Por exemplo: self.view.btn_salvar_cardio.config(command=self.salvar_dados_cardio)
        pass
    
    # ======================================================================================
    # MÉTODOS PARA AVALIAÇÃO CARDIOVASCULAR
    # ======================================================================================
    
    def salvar_dados_cardiovasculares(self, nome: str, idade: str, sexo: str, 
                                     peso: str, altura: str, distancia: str) -> Tuple[bool, str]:
        print("Nome" ,nome)
        print("idade" ,idade)
        print("sexo" ,sexo)
        print("peso" ,peso)
        print("altura" ,altura)
        print("distancia" ,distancia)

        """
        Salva os dados da avaliação cardiovascular de um aluno
        
        Args:
            nome: Nome do aluno
            idade: Idade em anos
            sexo: 'Masculino' ou 'Feminino'
            peso: Peso em kg
            altura: Altura em metros
            distancia: Distância percorrida em 6 minutos (metros)
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Validar campos vazios
            if not all([nome, idade, sexo, peso, altura, distancia]):
                return False, "Todos os campos devem ser preenchidos!"
            
            # Converter e validar dados
            idade_int = int(idade)
            peso_float = float(peso)
            altura_float = float(altura)
            distancia_int = int(distancia)

            # Converter sexo
            sexo_char = 'M' if sexo == 'Masculino' else 'F'
            
            # Buscar ou criar aluno
            print("self.model.adicionar_aluno",  self.model.adicionar_aluno(nome, idade_int, sexo_char))
            aluno = self.model.adicionar_aluno(nome, idade_int, sexo_char)
            print("aluno", aluno)
            
            # Atualizar dados cardiovasculares
            aluno.peso = peso_float
            aluno.altura = altura_float
            aluno.distancia_corrida = distancia_int
            
            # Processar através da cadeia
            self.model.processar_aluno(aluno)
            
            return True, f"Dados cardiovasculares de {nome} salvos com sucesso!"
            
        except ValueError:
            return False, "Erro: Verifique se os valores numéricos estão corretos!"
        except Exception as e:
            return False, f"Erro ao salvar dados: {str(e)}"
    
    # ======================================================================================
    # MÉTODOS PARA AVALIAÇÃO MUSCULOESQUELÉTICA
    # ======================================================================================
    
    def salvar_dados_musculoesqueleticos(self, nome: str, idade: str, sexo: str,
                                        flexibilidade: str, abdominais: str) -> Tuple[bool, str]:
        """
        Salva os dados da avaliação musculoesquelética de um aluno
        
        Args:
            nome: Nome do aluno
            idade: Idade em anos
            sexo: 'Masculino' ou 'Feminino'
            flexibilidade: Teste sentar e alcançar em cm
            abdominais: Número de repetições em 1 minuto
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Validar campos vazios
            if not all([nome, idade, sexo, flexibilidade, abdominais]):
                return False, "Todos os campos devem ser preenchidos!"
            
            # Converter e validar dados
            idade_int = int(idade)
            flex_float = float(flexibilidade)
            abd_int = int(abdominais)
            
            # Converter sexo
            sexo_char = 'M' if sexo == 'Masculino' else 'F'
            
            # Buscar ou criar aluno
            aluno = self.model.obter_aluno(nome)
            if not aluno:
                aluno = self.model.adicionar_aluno(nome, idade_int, sexo_char)
            
            # Atualizar dados musculoesqueléticos
            aluno.sentar_alcancar = flex_float
            aluno.abdominais = abd_int
            
            # Processar através da cadeia
            self.model.processar_aluno(aluno)
            
            return True, f"Dados musculoesqueléticos de {nome} salvos com sucesso!"
            
        except ValueError:
            return False, "Erro: Verifique se os valores numéricos estão corretos!"
        except Exception as e:
            return False, f"Erro ao salvar dados: {str(e)}"
    
    # ======================================================================================
    # MÉTODOS PARA TELA DE DADOS
    # ======================================================================================
    
    def obter_lista_alunos(self) -> List[Dict]:
        """
        Retorna lista de todos os alunos com seus status formatados para a view
        
        Returns:
            Lista de dicionários com dados dos alunos
        """
        alunos_formatados = []
        
        for aluno in self.model.obter_todos_alunos():
            # Determinar status cardiovascular
            if aluno.status_cardiovascular == 'saudavel':
                status_cardio = 'ok'
            elif aluno.status_cardiovascular == 'risco':
                status_cardio = 'risco'
            else:
                status_cardio = 'pendente'
            
            # Determinar status musculoesquelético
            if aluno.status_musculoesqueletico == 'saudavel':
                status_musculo = 'ok'
            elif aluno.status_musculoesqueletico == 'risco':
                status_musculo = 'risco'
            else:
                status_musculo = 'pendente'
            
            alunos_formatados.append({
                'nome': aluno.nome,
                'idade': aluno.idade,
                'sexo': aluno.sexo,
                'cardio': status_cardio,
                'musculo': status_musculo,
                'objeto': aluno  # Referência ao objeto original
            })
        
        return alunos_formatados
    
    def obter_detalhes_aluno(self, nome: str) -> Optional[Dict]:
        """
        Retorna os detalhes completos de um aluno para exibição
        
        Args:
            nome: Nome do aluno
        
        Returns:
            Dicionário com todos os detalhes do aluno ou None
        """
        aluno = self.model.obter_aluno(nome)
        
        if not aluno:
            return None
        
        # Formatar sexo
        sexo_completo = "Masculino" if aluno.sexo == 'M' else "Feminino"
        
        # Preparar detalhes cardiovasculares
        detalhes_cardio = {
            'status': aluno.status_cardiovascular or 'pendente',
            'imc': self._formatar_detalhes_imc(aluno),
            'corrida': self._formatar_detalhes_corrida(aluno)
        }
        
        # Preparar detalhes musculoesqueléticos
        detalhes_musculo = {
            'status': aluno.status_musculoesqueletico or 'pendente',
            'flexibilidade': self._formatar_detalhes_flexibilidade(aluno),
            'abdominais': self._formatar_detalhes_abdominais(aluno)
        }
        
        # Preparar dados de clusters (K-Means)
        clusters = {
            'cardiovascular': aluno.cluster_cardiovascular,
            'musculoesqueletico': aluno.cluster_musculoesqueletico,
            'geral': aluno.cluster_geral
        }
        
        return {
            'nome': aluno.nome,
            'idade': aluno.idade,
            'sexo': sexo_completo,
            'cardiovascular': detalhes_cardio,
            'musculoesqueletico': detalhes_musculo,
            'clusters': clusters
        }
    
    def _formatar_detalhes_imc(self, aluno) -> Dict:
        """Formata os detalhes do IMC para exibição"""
        if not aluno.detalhes_imc:
            return {'disponivel': False, 'mensagem': 'Avaliação não realizada'}
        
        detalhes = aluno.detalhes_imc
        
        if detalhes.get('status') == 'incompleto':
            return {'disponivel': False, 'mensagem': detalhes.get('mensagem', 'Dados incompletos')}
        
        return {
            'disponivel': True,
            'valor': detalhes.get('valor', 0),
            'faixa_ideal': detalhes.get('faixa_ideal', ''),
            'status': detalhes.get('status', 'pendente'),
            'mensagem': detalhes.get('mensagem', '')
        }
    
    def _formatar_detalhes_corrida(self, aluno) -> Dict:
        """Formata os detalhes do teste de corrida para exibição"""
        if not aluno.detalhes_corrida:
            return {'disponivel': False, 'mensagem': 'Avaliação não realizada'}
        
        detalhes = aluno.detalhes_corrida
        
        if detalhes.get('status') == 'incompleto':
            return {'disponivel': False, 'mensagem': detalhes.get('mensagem', 'Dados incompletos')}
        
        return {
            'disponivel': True,
            'valor': detalhes.get('valor', 0),
            'minimo_ideal': detalhes.get('minimo_ideal', 0),
            'status': detalhes.get('status', 'pendente'),
            'mensagem': detalhes.get('mensagem', '')
        }
    
    def _formatar_detalhes_flexibilidade(self, aluno) -> Dict:
        """Formata os detalhes do teste de flexibilidade para exibição"""
        if not aluno.detalhes_flexibilidade:
            return {'disponivel': False, 'mensagem': 'Avaliação não realizada'}
        
        detalhes = aluno.detalhes_flexibilidade
        
        if detalhes.get('status') == 'incompleto':
            return {'disponivel': False, 'mensagem': detalhes.get('mensagem', 'Dados incompletos')}
        
        return {
            'disponivel': True,
            'valor': detalhes.get('valor', 0),
            'minimo_ideal': detalhes.get('minimo_ideal', 0),
            'status': detalhes.get('status', 'pendente'),
            'mensagem': detalhes.get('mensagem', '')
        }
    
    def _formatar_detalhes_abdominais(self, aluno) -> Dict:
        """Formata os detalhes do teste de abdominais para exibição"""
        if not aluno.detalhes_abdominais:
            return {'disponivel': False, 'mensagem': 'Avaliação não realizada'}
        
        detalhes = aluno.detalhes_abdominais
        
        if detalhes.get('status') == 'incompleto':
            return {'disponivel': False, 'mensagem': detalhes.get('mensagem', 'Dados incompletos')}
        
        return {
            'disponivel': True,
            'valor': detalhes.get('valor', 0),
            'minimo_ideal': detalhes.get('minimo_ideal', 0),
            'status': detalhes.get('status', 'pendente'),
            'mensagem': detalhes.get('mensagem', '')
        }
    
    # ======================================================================================
    # MÉTODOS PARA ANÁLISE K-MEANS
    # ======================================================================================
    
    def executar_analise_kmeans(self) -> Tuple[bool, Dict]:
        """
        Executa a análise completa com K-Means
        
        Returns:
            Tupla (sucesso, resultados)
        """
        try:
            # Verificar se há alunos suficientes
            if len(self.model.alunos) < 2:
                return False, {'erro': 'É necessário ter pelo menos 2 alunos para análise K-Means'}
            
            # Executar análise
            resultados = self.model.executar_analise_kmeans()
            
            return True, resultados
            
        except Exception as e:
            return False, {'erro': f'Erro ao executar análise: {str(e)}'}
    
    def obter_estatisticas_kmeans(self) -> Dict:
        """
        Retorna estatísticas formatadas da análise K-Means
        
        Returns:
            Dicionário com estatísticas formatadas
        """
        sucesso, resultados = self.executar_analise_kmeans()
        
        if not sucesso:
            return resultados
        
        # Formatar resultados para exibição
        stats_formatadas = {
            'cardiovascular': {},
            'musculoesqueletico': {},
            'geral': {}
        }
        
        for tipo in ['cardiovascular', 'musculoesqueletico', 'geral']:
            if 'erro' in resultados[tipo]:
                stats_formatadas[tipo]['erro'] = resultados[tipo]['erro']
            else:
                dados = resultados[tipo]
                stats_formatadas[tipo] = {
                    'total': dados['total_analisados'],
                    'saudavel': dados['alunos_zona_saudavel'],
                    'risco': dados['alunos_zona_risco'],
                    'percentual_saudavel': f"{dados['percentual_saudavel']:.1f}%",
                    'percentual_risco': f"{dados['percentual_risco']:.1f}%"
                }
        
        return stats_formatadas
    
    def obter_alunos_por_cluster(self, tipo: str, zona: str) -> List[Dict]:
        """
        Retorna alunos de uma zona específica (saudável ou risco) segundo K-Means
        
        Args:
            tipo: 'cardiovascular', 'musculoesqueletico' ou 'geral'
            zona: 'saudavel' ou 'risco'
        
        Returns:
            Lista de alunos formatados
        """
        # Executar análise primeiro para garantir clusters atualizados
        sucesso, resultados = self.executar_analise_kmeans()
        
        if not sucesso or 'erro' in resultados.get(tipo, {}):
            return []
        
        # Identificar o número do cluster
        cluster_num = resultados[tipo]['cluster_saudavel'] if zona == 'saudavel' else resultados[tipo]['cluster_risco']
        
        # Obter alunos do cluster
        alunos = self.model.obter_alunos_por_cluster(tipo, cluster_num)
        
        # Formatar para exibição
        return [{'nome': a.nome, 'idade': a.idade, 'sexo': a.sexo} for a in alunos]
    
    # ======================================================================================
    # MÉTODOS AUXILIARES
    # ======================================================================================
    
    def obter_estatisticas_gerais(self) -> Dict:
        """
        Retorna estatísticas gerais do sistema
        
        Returns:
            Dicionário com estatísticas
        """
        return self.model.obter_estatisticas()
    
    def limpar_dados_aluno(self, nome: str) -> Tuple[bool, str]:
        """
        Remove um aluno do sistema
        
        Args:
            nome: Nome do aluno
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        aluno = self.model.obter_aluno(nome)
        
        if not aluno:
            return False, "Aluno não encontrado!"
        
        self.model.alunos.remove(aluno)
        return True, f"Dados de {nome} removidos com sucesso!"
    
    def validar_nome_unico(self, nome: str) -> bool:
        """
        Verifica se o nome do aluno já existe no sistema
        
        Args:
            nome: Nome para verificar
        
        Returns:
            True se o nome já existe, False caso contrário
        """
        return self.model.obter_aluno(nome) is not None