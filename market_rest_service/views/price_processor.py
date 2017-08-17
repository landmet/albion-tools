import traceback
import pprint
import elasticsearch
import configparser
from flask import Blueprint, request
from datetime import datetime, timezone
from elasticsearch.exceptions import NotFoundError
from libs import albion_items

prices = Blueprint('prices', __name__)
last_updated = datetime.now()
order_ids = []
gold_timestamps = []
gold_last_updated = datetime.now()

# Setup Config
config = configparser.RawConfigParser()
config.read('config.conf')

# Setup Elastic
es_server = config.get("Elastic", "server")
es = elasticsearch.Elasticsearch([es_server])

# Setup Item Localization Lookup
item_dict = albion_items.build_localization_lookup()


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
                order_ids.append(order['Id'])
                # Query to see if Id is already in DB
                id_query = {
                    "query": {
                        "bool": {
                            "must": [
                                {"range": {"timestamp": {"gte": "now-7d", "lte": "now"}}},
                                {"term": {"Id": order['Id']}}
                            ]
                        }
                    }
                }
                try:
                    result = es.search(index="albion_market", doc_type="market_order", body=id_query)
                except NotFoundError as e:
                    print("Elasticsearch index not created.")
                    result = {'hits': {'total': 0}}

                # If there's no IDs that match in the last 7d
                if result['hits']['total'] <= 0:
                    try:
                        # Try to convert tier to int, if it fails then assign 0
                        try:
                            order['tier'] = int(order["ItemTypeId"].split("_")[0].replace("T", ""))
                        except:
                            order['tier'] = 0

                        itemstr = order['ItemTypeId'].split("@")[0]
                        order['timestamp'] = datetime.utcnow().replace(tzinfo=timezone.utc)
                        order['UnitPriceSilver'] = order['UnitPriceSilver'] / 1000
                        order['loc_en_us'] = item_dict["@ITEMS_"+itemstr]
                        es.index(index="albion_market", doc_type="market_order", body=order)

                    except:
                        pprint.pprint(order)
                        print(traceback.format_exc())

        return "Success", 200
    except:
        print(traceback.format_exc())


@prices.route('/goldprices', methods=["POST"])
def goldprices():
    # Convert shitty mysql datetime (seconds since year 0)
    epoch = datetime(1970, 1, 1)
    first = datetime(1, 1, 1)
    epoch_delta = epoch - first
    total_seconds = epoch_delta.total_seconds()
    ms_divide = 10000000


    try:
        # Local gold timestamp cache
        global gold_last_updated
        now_time = datetime.now()
        if (now_time - gold_last_updated).seconds > 80000:
            order_ids.clear()
            gold_last_updated = datetime.now()
            print("Gold Timestamps cleared.")

        content = request.get_json()

        for i in range(0, len(content['prices'])):
            price = content['prices'][i]/10000
            gold_timestamp = content['timestamps'][i]

            if gold_timestamp in gold_timestamps:
                pass
            else:
                gold_timestamps.append(gold_timestamp)

                # Query to see if gold timestamp is already in DB
                id_query = {
                    "query": {
                        "bool": {
                            "must": [
                                {"range": {"timestamp": {"gte": "now-7d", "lte": "now"}}},
                                {"term": {"gold_timestamp": gold_timestamp}}
                            ]
                        }
                    }
                }
                try:
                    result = es.search(index="albion_market", doc_type="gold_price", body=id_query)
                except NotFoundError as e:
                    print("Elasticsearch index not created.")
                    result = {'hits': {'total': 0}}

                # If the gold_timestamp wasn't found in elastic
                if result['hits']['total'] <= 0:
                    timestamp = datetime.utcfromtimestamp((gold_timestamp/ms_divide) - total_seconds)
                    gold_price = {
                        "price": price,
                        "gold_timestamp": gold_timestamp,
                        "timestamp": timestamp
                    }

                    es.index(index="albion_market", doc_type="gold_price", body=gold_price)

        return "Success", 200
    except:
        print(traceback.format_exc())
