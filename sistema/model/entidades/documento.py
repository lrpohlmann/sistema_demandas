from pathlib import Path
from pyrsistent import PRecord, field


class TipoDocumento(PRecord):
    id_tipo_documento = field(type=(type(None), int), mandatory=True, initial=None)
    nome = field(type=str, mandatory=True)


class Documento(PRecord):
    id_documento = field(type=(type(None), int), mandatory=True, initial=None)
    identificador = field(type=(type(None), str), mandatory=True, initial=None)
    tipo = field(type=TipoDocumento, mandatory=True)
    nome = field(str, mandatory=True)
    descricao = field(type=(type(None), str), mandatory=True, initial=None)
    arquivo = field(type=(type(None), Path), mandatory=True, initial=None)
