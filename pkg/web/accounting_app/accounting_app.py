"""Blueprint for accounting app"""

# put routes and import accounting app functions here.

from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   )

accounting_app_bp = Blueprint('accounting_app_bp',
                              __name__,
                              template_folder='templates',
                              static_folder='static',
                              static_url_path='accounting_app')
