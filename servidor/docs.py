
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec
from api import get_variants,  get_samples



def register_docs(app):
    """
    Configura y registra la documentación API utilizando Flask-APISpec.

    Parameters:
    - app (Flask): La instancia de la aplicación Flask.

    Returns:
    - FlaskApiSpec: La instancia de FlaskApiSpec configurada.
    """

    # Configuración de la especificación API
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title = 'Canndico API',
            version = 'v0.1',
            openapi_version = '2.0',
            plugins = [MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/api/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/api/'
    })
    # Inicialización de FlaskApiSpec con la aplicación
    docs = FlaskApiSpec(app)

    # Registro de endpoints y blueprints en la documentación
    docs.register(get_variants, blueprint='api', endpoint='get_variants')
    docs.register(get_samples, blueprint='api', endpoint='get_samples')


    return docs
