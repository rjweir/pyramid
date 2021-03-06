from pyramid.configuration import Configurator
from paste.deploy.converters import asbool

from tutorial.models import initialize_sql

def app(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    db_echo = settings.get('db_echo', 'false')
    initialize_sql(db_string, asbool(db_echo))
    config = Configurator(settings=settings)
    config.begin()
    config.add_static_view('static', 'tutorial:static')
    config.add_route('home', '/', view='tutorial.views.view_wiki')
    config.add_route('view_page', '/:pagename',
                     view='tutorial.views.view_page',
                     view_renderer='tutorial:templates/view.pt')
    config.add_route('add_page', '/add_page/:pagename',
                     view='tutorial.views.add_page',
                     view_renderer='tutorial:templates/edit.pt')
    config.add_route('edit_page', '/:pagename/edit_page',
                     view='tutorial.views.edit_page',
                     view_renderer='tutorial:templates/edit.pt')
    config.end()
    return config.make_wsgi_app()

