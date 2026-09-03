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