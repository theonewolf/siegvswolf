import requests



from bnet.d3 import D3
from flask import Flask, render_template
from os import environ



API_KEY = environ.get('BATTLE_NET_API_KEY', None)
USER_A  = environ.get('USER_A', None)
USER_B  = environ.get('USER_B', None)

app = Flask(__name__)



@app.route('/')
def default():
    bnetconn = D3(api_key=API_KEY)

    profa = bnetconn.get_profile(USER_A)
    profb = bnetconn.get_profile(USER_B)

    try:
        profamax = max([h for h in profa.heroes
                        if h['seasonal'] and h['hardcore']],
                        key=lambda x: x['level'])
    except ValueError:
        profamax = None

    if profamax is not None:
        profahero = bnetconn.get_hero(USER_A, profamax['id'])
    else:
        profahero = None

    try:
        profbmax = max([h for h in profb.heroes
                        if h['seasonal'] and h['hardcore']],
                        key=lambda x: x['level'])
    except ValueError:
        profbmax = None

    if profbmax is not None:
        profbhero = bnetconn.get_hero(USER_B, profbmax['id'])
    else:
        profbhero = None

    if profahero is not None and profbhero is not None:
        if profbhero.level >= profahero.level:
            profbclass = 'text-success'
            profbprogressclass = 'progress-bar-success'
            profaclass = 'text-danger'
            profaprogressclass = 'progress-bar-danger'
        else:
            profbclass = 'text-danger'
            profbprogressclass = 'progress-bar-danger'
            profaclass = 'text-success'
            profaprogressclass = 'progress-bar-success'

        profbprogresswidth = float(profbhero.level) / (profbhero.level + profahero.level)
        profaprogresswidth = float(profahero.level) / (profbhero.level + profahero.level)

        profbprogresswidth = '%0.0f%%' % (profbprogresswidth * 100)
        profaprogresswidth = '%0.0f%%' % (profaprogresswidth * 100)

        return render_template('index.jinja2',
                               profahero=profahero,
                               profbhero=profbhero,
                               profaclass=profaclass,
                               profbclass=profbclass,
                               profaprogressclass=profaprogressclass,
                               profbprogressclass=profbprogressclass,
                               profaprogresswidth=profaprogresswidth,
                               profbprogresswidth=profbprogresswidth)
    if profahero:
        return render_template('index-failed.jinja2',
                               profahero=profahero)
    elif profbhero:
        return render_template('index-failed.jinja2',
                               profbhero=profbhero)
    else:
        return render_template('index-failed.jinja2')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
