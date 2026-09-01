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