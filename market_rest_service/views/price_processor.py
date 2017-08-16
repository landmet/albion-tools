import traceback
import pprint
import elasticsearch
from flask import Blueprint, request
from datetime import datetime, timezone

prices = Blueprint('prices', __name__)
last_updated = datetime.now()
order_ids = []
# TODO: Remove hardcoded elasticsearch values
es = elasticsearch.Elasticsearch(["elastic1.lab.grds.io"])


@prices.route('/marketorders', methods=["POST"])
def marketorders():
    global last_updated

    try:
        now_time = datetime.now()
        if (now_time - last_updated).seconds > 900:
            order_ids.clear()
            last_updated = datetime.now()
            print("Order IDs cleared.")

        content = request.get_json()
        for order in content['Orders']:
            if order['Id'] in order_ids:
                pass
            else:
                # TODO: Use Localization data to add friendly names
                # TODO: Add location ID to each index, along with friendly name
                order['timestamp'] = datetime.utcnow().replace(tzinfo=timezone.utc)
                order['UnitPriceSilver'] = order['UnitPriceSilver'] / 1000
                es.index(index="albion_market", doc_type="market_order", body=order)
                order_ids.append(order['Id'])
        return "Success", 200
    except:
        print(traceback.format_exc())


@prices.route('/goldprices', methods=["POST"])
def goldprices():
    # TODO: Store gold prices
    try:
        content = request.get_json()
        # pprint.pprint(content)
        return "Success", 200
    except:
        print(traceback.format_exc())
