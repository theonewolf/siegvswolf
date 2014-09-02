import requests



from flask import Flask, render_template


app = Flask(__name__)

class Hero:
    def __init__(self, stats):
        self.update(stats.items())

    def update(self, data):
        for k,v in data:
            if k == 'class': v = v.replace('-', ' ').title()
            setattr(self, k, v)

@app.route('/')
def hello():
    r = requests.get('https://us.api.battle.net/d3/profile/theonewolf-1275/?locale=en_US&apikey=hgqmvv3kst5q2ng62s6b2d4w4jqsfxxm')
    rjson = r.json()
    
    wolfmax = max([h for h in rjson['heroes'] if h['seasonal'] and h['hardcore']], key=lambda x: x['level'])
    wolfhero = Hero(wolfmax)

    r = requests.get('https://us.api.battle.net/d3/profile/thespoon3-1397/?locale=en_US&apikey=hgqmvv3kst5q2ng62s6b2d4w4jqsfxxm')
    rjson = r.json()

    siegmax = max([h for h in rjson['heroes'] if h['seasonal'] and h['hardcore']], key=lambda x: x['level'])
    sieghero = Hero(siegmax)

    if sieghero.level > wolfhero.level:
        siegclass = 'text-success'
        siegprogressclass = 'progress-bar-success'
        wolfclass = 'text-danger'
        wolfprogressclass = 'progress-bar-danger'
    else:
        siegclass = 'text-danger'
        siegprogressclass = 'progress-bar-danger'
        wolflcass = 'text-success'
        wolfprogressclass = 'progress-bar-success'

    siegprogresswidth = float(sieghero.level) / (sieghero.level + wolfhero.level)
    wolfprogresswidth = float(wolfhero.level) / (sieghero.level + wolfhero.level)

    siegprogresswidth = '%0.0f%%' % (siegprogresswidth * 100)
    wolfprogresswidth = '%0.0f%%' % (wolfprogresswidth * 100)

    return render_template('index.jinja2',
                           wolfhero=wolfhero,
                           sieghero=sieghero,
                           wolfclass=wolfclass,
                           siegclass=siegclass,
                           wolfprogressclass=wolfprogressclass,
                           siegprogressclass=siegprogressclass,
                           wolfprogresswidth=wolfprogresswidth,
                           siegprogresswidth=siegprogresswidth)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
