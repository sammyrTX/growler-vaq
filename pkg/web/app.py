"""framework for accounting system web app"""

from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   request,
                   Blueprint,
                   )

from .. web.accounting_app.accounting_app import accounting_app_bp
from .. web.accounting_app.accounting_app_journals import accounting_app_journals_bp
from .. web.accounting_app.accounting_app_gl import accounting_app_gl_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'toASMuE59soIk7de34fJ&&'

app.register_blueprint(accounting_app_bp, url_prefix='/accounting_app')
app.register_blueprint(accounting_app_journals_bp, url_prefix='/accounting_app')
app.register_blueprint(accounting_app_gl_bp, url_prefix='/accounting_app')


@app.route('/')
def index():
    """Index page for accounting system"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
