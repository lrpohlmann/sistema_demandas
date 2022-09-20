from typing import Any, Callable
import flask_login


def carregar_usuario_factory(
    login_manager: flask_login.LoginManager,
    carregar_usuario_callable: Callable[[Any], Any],
):
    @login_manager.user_loader
    def load_user(id_usuario):
        return carregar_usuario_callable(id_usuario)

    return load_user
