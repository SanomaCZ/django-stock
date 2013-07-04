from os import path
from datetime import datetime

from fabric.api import env
from fabric.operations import sudo, run
from fabric.contrib.files import exists
from fabric.context_managers import prefix


#env.user = 'do' # path.dirname(__file__).split('/')[-1]


SITES_ENABLED = ['stock.conf']

PROJECT_NAME = 'stock'

PIP_INSTALL_FROM_REPO = {
    'pypi': 'pip install -i http://pypi.smdev.cz/simple/ --extra-index-url=http://pypi.python.org/simple/ %s',
    'git': 'pip install -e %s',
}

REPO_SOURCES = {
    'pypi': 'stock',
    #'git': 'git+gitolite@git.smdev.cz:ella-sanoma#egg=%s' % PROJECT_NAME,
}

PROJECT_SOURCE = 'pypi'
#PROJECT_REPO = 'git+gitolite@git.smdev.cz:ella-sanoma#egg=%s' % PROJECT_NAME
PROJECT_REPO = REPO_SOURCES[PROJECT_SOURCE]


SUPERVISOR_NAME = 'stock'

NOW = datetime.now().strftime("%y%m%d_%H%M%S")

WSGI_CONTENT = """
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from raven.contrib.django.middleware.wsgi import Sentry
application = Sentry(application)
""" % PROJECT_NAME


def local():
    env.root_directory = path.dirname(__file__)
    env.project_directory = path.join(env.root_directory, 'project')
    env.virtualenv_directory = path.join(env.root_directory, 'venv')
    #env.virtualenv_activate = '. %s/bin/activate' % env.virtualenv_directory

    env.use_nginx = False


def server():  # abstract
    env.root_directory = '/www/apps'
    env.project_directory = lambda: '/'.join([env.root_directory, PROJECT_NAME])
    env.project_repo = PROJECT_REPO

    env.virtualenv_directory = lambda: '/'.join([env.project_directory(), 'venv'])

    env.virtualenv_directory_raw = lambda: '%s_%s' % (env.virtualenv_directory(), NOW)

    env.app_root = lambda: "%s/src/%s" % (env.virtualenv_directory(), PROJECT_NAME)
    env.conf_root = lambda: "%s/src/%s/conf" % (env.virtualenv_directory_raw(), PROJECT_NAME)

    env.use_nginx = True
    env.forward_agent = True

    env.use_sudo = True

    env.ln_packages = (
        '/usr/lib/python2.6/dist-packages/psycopg2-2.4.2.egg-info',
        '/usr/lib/python2.6/dist-packages/psycopg2',
        #'/usr/lib/python2.6/dist-packages/PIL.pth',
        #'/usr/lib/python2.6/dist-packages/PIL',
    )


def mona():
    server()

    env.hosts= ['stock.mona.cz']
    env.user = 'sshanoma'

    env.minion_user = 'sanoma'

    env.etc_prefix = '/usr/local/etc'

    env.forward_agent = True

    env.ln_packages = (
        '/usr/lib/python2.6/dist-packages/psycopg2-2.4.2.egg-info',
        '/usr/lib/python2.6/dist-packages/psycopg2',
        '/usr/lib/python2.6/dist-packages/PIL.pth',
        '/usr/lib/python2.6/dist-packages/PIL',
    )


def init():
    svc_init()
    app_init()
    app_update()


def update():
    app_init()

    #svc_update()

    app_update()

    do('chown -R %s %s' % (env.minion_user, env.project_directory()))

    svc_reload()


def add_wsgi_file():
    run('''echo "%s" > %s/wsgi.py ''' % (WSGI_CONTENT, env.virtualenv_directory_raw()))


#TODO - start service at a very first time
def app_init():
    print 'app init'
    #TODO - use jenkins'ed package to install
    env_init()

    with prefix('export PIP_DOWNLOAD_CACHE=~/.pip-cache/'):
        with prefix('. %s/bin/activate' % env.virtualenv_directory_raw()):
            for ln in env.ln_packages:
                do('ln -s %s %s/lib/python2.6/site-packages/' % (ln, env.virtualenv_directory_raw()))
            #run('pip install -e %s' % env.project_repo)
            do('%s' % (PIP_INSTALL_FROM_REPO[PROJECT_SOURCE] % env.project_repo))

    do('ln -sfn %s %s' % (env.virtualenv_directory_raw(), env.virtualenv_directory()))
    #add_wsgi_file()


def app_update():
    print 'app update'
    #TODO - create a package via jenkins and deploy it instead of pip install
    with prefix('source %s/bin/activate' % env.virtualenv_directory()):
        #do('%s/manage.py syncdb --noinput' % env.app_root())
        #do('%s/manage.py migrate' % env.app_root())
        #do('%s/manage.py collectstatic -c --noinput' % env.app_root())
        # lines below use entry point sanoma_manage :)
        do('stock-manage syncdb --noinput')
        do('stock-manage migrate')
        do('stock-manage collectstatic -c --noinput')


def svc_reload():
    print 'services reload'
    if not env.use_nginx:
        print('`use_nginx` is not set, NOT reloading services')
        return

    do('supervisorctl update')
    #do("supervisorctl restart base:nginx")
    do("supervisorctl restart %s" % SUPERVISOR_NAME)


def svc_init():
    print 'services init'
    #TODO - check if nginx's repo is already added
    #do('echo "deb http://debian-dotdeb.mirror.web4u.cz/ stable all" >> /etc/apt/sources.list')

    #TODO: line below does not contain uwsgi that is we have own,
    # and sudo will be probably exist on the target machine !!!
    #do('apt-get install nginx-full supervisor sudo python-virtualenv')  #gcc python-dev
    #do('mkdir -p %s/nginx' % env.etc_prefix)
    #do('cp /etc/nginx/uwsgi_params %s/nginx/' % env.etc_prefix)
    #do('mkdir -p %s/nginx/sites-available' % env.etc_prefix)
    #do('mkdir -p %s/nginx/sites-enabled' % env.etc_prefix)
    #do('mkdir -p %s/sanoma/' % env.etc_prefix)
    #do('mkdir -p %s/supervisor/conf.d' % env.etc_prefix)
    do('mkdir -p /var/log/stock')
    do('chown %s /var/log/stock' % env.minion_user)

    do('mkdir -p %s' % env.project_directory())

    do('chown %s %s' % (env.minion_user, env.project_directory()))

    static_dir = '/www/static/%s' % PROJECT_NAME
    media_dir = '/www/media/%s' % PROJECT_NAME
    wanted_dirs = (media_dir, static_dir)
    for d in wanted_dirs:
        do('mkdir -p %s' % d)
        do('chown %s %s' % (env.minion_user, d))

    print """
    Please copy your manually crafted django's config file into expected location
    It's somewhere in %s/sanoma/
    """ % env.etc_prefix
    raw_input("press any key to continue")


def svc_update():
    print 'services update'
    if not env.use_nginx:
        print('`use_nginx` not set, not deploying sites')
        return

    do('cp %s/nginx/* %s/nginx/sites-available/' % (env.conf_root(), env.etc_prefix), use_sudo=True)
    #TODO - enable disabling sites
    for one in SITES_ENABLED:
        sudo('ln -sfn %s/nginx/sites-available/%s %s/nginx/sites-enabled/' % (env.etc_prefix, one, env.etc_prefix))

    sudo('cp %s/supervisor/* %s/supervisor/conf.d/' % (env.conf_root(), env.etc_prefix))
    do('supervisorctl update')


def env_init():
    print 'creating virtualenv ...'
    if getattr(env, 'static_env', False):
        print 'Actually, static env is set to True, I\'m out'
        return
    
    do('virtualenv --no-site-packages %s' % env.virtualenv_directory_raw())

def env_exists(name):
    if env.host_string:
        return exists(name)
    else:
        return path.exists(name)


def collectstatic():
    print 'Collecting static files ...'
    run('cd %s && ./run collectstatic -c --noinput' % env.project_directory())


def do(*args, **kwargs):
    use_sudo = kwargs.pop('use_sudo', env.use_sudo)

    if use_sudo:
        sudo(*args, **kwargs)
    else:
        run(*args, **kwargs)
