import traceback
import pprint
from flask import Blueprint, request

callback = Blueprint('price_processor', __name__)


@callback.route('/marketorders', methods=["POST"])
def marketorders():
    try:
        content = request.get_json()
        pprint.pprint(content)
        return "Success", 200
    except:
        print(traceback.format_exc())
