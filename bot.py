#!/usr/bin/env python
import requests
import logging
import time
import os
from datetime import datetime
import time
from twilio.rest import Client
import difflib


class CheckParameters(object):

    def __init__(self, plant, url, check_string, shop, method):
        """
        method = 'count', 'missing_string'
        """
        self.plant = plant
        self.url = url
        self.check_string = check_string
        self.shop = shop
        self.method = method
        self.return_phrase_success = '{} in stock at {}'.format(self.plant, self.shop)
        self.return_phrase_fail = '{} still out of stock at {}'.format(self.plant, self.shop)
        self.in_stock = False
        self.current = -1

albo = CheckParameters(
    'albo monstera',
    'https://www.logees.com/variegated-mexican-breadfruit-monstera-deliciosa-variegata.html',
    '0 in stock',
    'logees',
    'missing_string',
    )

ppp_logees = CheckParameters(
    'ppp_logees',
    'https://www.logees.com/philodendron-pink-princess-philodendron-erubescens.html',
    '0 in stock',
    'logees',
    'missing_string',
    )

rio = CheckParameters(
    'rio',
    'https://www.gabriellaplants.com/collections/philodendron/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation',
    'in stock',
    'gabriellaplants',
    'count',
    )

silver_sword = CheckParameters(
    'silver_sword',
    'https://www.gabriellaplants.com/collections/philodendron/products/4-silver-sword-philodendron-philodendron-hastatum',
    'in stock',
    'gabriellaplants',
    'count',
    )

ppp_gabriella = CheckParameters(
    'ppp_gabriella',
    'https://www.gabriellaplants.com/products/4-pink-princess-philodendron',
    'in stock',
    'gabriellaplants',
    'count',
    )

verrucosum = CheckParameters(
    'p. verrucosum',
    'https://www.logees.com/ecuador-philodendron-philodendron-ventricosum.html',
    '0 in stock',
    'logees',
    'missing_string',
    )

jessenia = CheckParameters(
    'jessenia',
    'https://www.gabriellaplants.com/collections/pothos/products/4-jessenia-pothos',
    'in stock',
    'gabriellaplants',
    'count',
    )

treubii = CheckParameters(
    'treubii',
    'https://www.gabriellaplants.com/collections/scindapsus-1/products/3-scindapsus-treubii-moonlight',
    'in stock',
    'gabriellaplants',
    'count',
    )

the_list = [
            albo,
            ppp_logees,
            ppp_gabriella,
            verrucosum,
            rio,
            jessenia,
            treubii,
            ]


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
twilio_auth_token=os.environ.get("TWILIO_AUTH_TOKEN")
twilio_sid=os.environ.get("TWILIO_SID")
twilio_phone=os.environ.get("TWILIO_PHONE")
jordan_phone=os.environ.get("PHONE_1")
nancy_phone=os.environ.get("PHONE_2")

def send_text(text):
	client = Client(twilio_sid, twilio_auth_token)
	message = client.messages.create(
                body='Hello Jordan!!!\n\n{}'.format(text),
         		from_=twilio_phone,
         		to=jordan_phone
     	)
	message.sid
	message = client.messages.create(
                body='Hello Nancy!!!\n\n{}'.format(text),
        		from_=twilio_phone,
        		to=nancy_phone
        )
	message.sid

if __name__ == "__main__":
        while True:
            loop_start_time = time.time()
            for plant in the_list:
                try:
                    r = requests.get(plant.url)
                except requests.exceptions.ConnectionError as e:
                    logging.info(e)
                    send_text("unable to ping {}".format(plant.url))
                    break
                if plant.method == 'missing_string':
                    if r.text.lower().find(plant.check_string.lower()) == -1:
                        logging.info(plant.return_phrase_success)
                        if not plant.in_stock:
                            send_text(plant.return_phrase_success)
                            logging.info(r.text)
                            plant.in_stock = True
                    else:
                        logging.info(plant.return_phrase_fail)
                elif plant.method == 'count':
                    previous = plant.current
                    plant.current = r.text.lower().count(plant.check_string.lower())
                    if previous >= 0 and (previous != plant.current):
                        logging.info(plant.return_phrase_success)
                        if not plant.in_stock:
                            send_text(plant.return_phrase_success)
                            logging.info(r.text)
                            plant.in_stock = True
                    else:
                        logging.info(plant.return_phrase_fail)
                    logging.info("  previous={}, current={}".format(previous, plant.current))
                else:
                    logging.info('invalid method for {}'.format(plant.plant))

            now = datetime.now()
            if now.hour == 22 and now.minute == 0:
                in_stock = [plant.plant for plant in the_list if plant.in_stock]
                not_stock = [plant.plant for plant in the_list if not plant.in_stock]
                update_message = 'This is an update from plants for us messaging bot\n\n'

                if in_stock:
                    update_message += 'Good news! Today {} was in stock and '.format(in_stock)
                if not_stock:
                    update_message += 'womp womp, {} are not in stock\n\n'.format(not_stock)
                update_message += "we hope you will continue to use our service"

                send_text(update_message)  


            sleep_time = max(0, 60 - (time.time() - loop_start_time))
            logging.info("sleeping {} seconds".format(sleep_time))
            time.sleep(sleep_time)
