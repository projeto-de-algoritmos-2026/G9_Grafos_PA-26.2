import textwrap

class GrafoCurso:   
    def __init__(self):
        self.materias = {}
        self.adj = {}

    def adicionar_materia(self, id_mat: str, nome: str, creditos: int):
        id_mat = id_mat.strip().upper()
        if not id_mat or not nome or creditos <= 0:
            raise ValueError("Dados inválidos para a matéria.")

        if id_mat not in self.materias:
            self.adj[id_mat] = []

        self.materias[id_mat] = {
            "nome": nome.strip(),
            "creditos": int(creditos)
        }

    def adicionar_prerequisito(self, prereq: str, materia: str):
        prereq, materia = prereq.strip().upper(), materia.strip().upper()

        if prereq not in self.materias or materia not in self.materias:
            raise ValueError("Ambas as matérias precisam estar cadastradas.")
        if prereq == materia:
            raise ValueError("Uma matéria não pode ser pré-requisito dela mesma.")
        if materia in self.adj[prereq]:
            raise ValueError("Este pré-requisito já foi cadastrado.")

        self.adj[prereq].append(materia)

    def tem_ciclo(self) -> bool:
        estado = {m: 0 for m in self.materias}

        def dfs(u):
            estado[u] = 1
            for v in self.adj.get(u, []):
                if estado[v] == 1:
                    return True
                if estado[v] == 0 and dfs(v):
                    return True
            estado[u] = 2
            return False

        for node in self.materias:
            if estado[node] == 0:
                if dfs(node):
                    return True
        return False

    # Ordenação topológica separada em semestres
    def gerar_semestres(self, max_creditos: int) -> list:
        if self.tem_ciclo():
            raise ValueError("O grafo possui ciclos! Remova as dependências circulares antes de gerar a grade.")

        in_degree = {m: 0 for m in self.materias}
        for u in self.adj:
            for v in self.adj[u]:
                in_degree[v] += 1

        graus_restantes = in_degree.copy()
        disponiveis = [m for m, deg in graus_restantes.items() if deg == 0]
        semestres = []

        while disponiveis:
            disponiveis.sort(key=lambda x: self.materias[x]['creditos'], reverse=True)
            
            semestre_atual = []
            creditos_atuais = 0
            proxima_rodada = []

            for m in disponiveis:
                cred = self.materias[m]['creditos']
                if cred > max_creditos:
                    raise ValueError(f"A matéria '{m}' exige {cred} créditos, acima do limite ({max_creditos}).")

                if creditos_atuais + cred <= max_creditos:
                    semestre_atual.append(m)
                    creditos_atuais += cred
                else:
                    proxima_rodada.append(m)

            if not semestre_atual:
                raise ValueError("Limite de créditos insuficiente para alocar as disciplinas restantes.")

            semestres.append(semestre_atual)

            novos_liberados = []
            for m_alocada in semestre_atual:
                for vizinho in self.adj.get(m_alocada, []):
                    graus_restantes[vizinho] -= 1
                    if graus_restantes[vizinho] == 0:
                        novos_liberados.append(vizinho)

            disponiveis = proxima_rodada + novos_liberados

        return semestres
        
    def exportar_dot(self, semestres: list) -> str:
        lines = [
            'digraph Fluxograma {',
            '  rankdir=LR;',
            '  newrank=true;',
            '  bgcolor="transparent";',
            '  compound=true;',
            '  nodesep=0.28;',
            '  ranksep=0.9;',
            '  pad=0.35;',
            '  margin=0.25;',
            '  node [shape=box, style="filled,rounded", fontname="Arial Bold", fontsize=10, fixedsize=true, width=1.4, height=0.45, fillcolor="#2D3748", color="#63B3ED", fontcolor="#F7FAFC", penwidth=1.2];',
            '  edge [color="#90CDF4", penwidth=1.5, arrowsize=0.8];',
            '  ordering=out;'
        ]

        primeiros = []

        for idx, semestre in enumerate(semestres):
            if not semestre:
                continue

            primeiro = semestre[0]
            primeiros.append(primeiro)

            lines.append(f'  subgraph cluster_{idx} {{')
            lines.append(f'    label="{idx + 1}º Semestre";')
            lines.append('    fontname="Arial Bold";')
            lines.append('    fontsize=11;')
            lines.append('    fontcolor="#E2E8F0";')
            lines.append('    style="filled,rounded,dashed";')
            lines.append('    color="#4A5568";')
            lines.append('    fillcolor="#1A202C";')
            lines.append('    margin="0.35,0.45";')

            for m in semestre:
                lines.append(f'    "{m}" [label="{m}"];')

            nodes_str = '; '.join(f'"{m}"' for m in semestre)
            lines.append(f'    {{ rank=same; {nodes_str}; }}')

            for i in range(len(semestre) - 1):
                lines.append(
                    f'    "{semestre[i]}" -> "{semestre[i + 1]}" '
                    '[style=invis, weight=100, constraint=false];'
                )

            lines.append('  }')

        if len(primeiros) > 1:
            for i in range(len(primeiros) - 1):
                lines.append(f'  "{primeiros[i]}" -> "{primeiros[i + 1]}" [style=invis, weight=100];')

        for u in self.adj:
            for v in self.adj[u]:
                lines.append(f'  "{u}" -> "{v}" [weight=1];')

        lines.append('}')
        return "\n".join(lines)


    def para_dict(self) -> dict:
        return {"materias": self.materias, "adj": self.adj}

    def carregar_dict(self, dados: dict):
        if "materias" not in dados or "adj" not in dados:
            raise ValueError("Arquivo JSON inválido para a estrutura do curso.")
        self.materias = dados.get("materias", {})
        self.adj = dados.get("adj", {})