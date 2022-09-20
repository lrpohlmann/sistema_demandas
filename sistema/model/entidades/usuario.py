from dataclasses import dataclass, field
from typing import Optional
import flask_login


@dataclass
class Usuario(flask_login.UserMixin):
    nome: str
    senha: str
    id_usuario: Optional[int] = field(default=None)

    def get_id(self):
        return str(self.id_usuario)
