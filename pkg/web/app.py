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

# Code from dice game web app. Replicate imports for accounting system
# from . forms import (DiceHold,
#                      DiceHoldWeb,
#                      )

# from .. diceroll.dice import (die_roll,
#                               dice_png,
#                               )

# from .. gameprocessing.play_game import (start_game,
#                                          game_status,
#                                          )
# from .. scorekeeping.scorepad import Scorepad_


# from .. web.webgame.webgame import webgame_bp
# from .. web.temptest.temptest import temptest_bp  # Test only - Remove

# # Remove after HTML complete
# from .. scorekeeping.scoredisplay import show_current_score


app = Flask(__name__)

app.config['SECRET_KEY'] = 'toASMuE59soIk7de34fJ&&'

app.register_blueprint(accounting_app_bp, url_prefix='/accounting_app')


@app.route('/')
def index():
    """Index page for accounting system"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
