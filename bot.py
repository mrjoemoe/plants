#!/usr/bin/env python
import requests
import logging
import os
from datetime import datetime
import time
from twilio.rest import Client
import socket

DEBUG = False
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
JORDAN_PHONE = os.environ.get("PHONE_1")
NANCY_PHONE = os.environ.get("PHONE_2")


class User(object):

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.text_header = "Plant update for {}!!!\n\n".format(self.name)


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
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
users = [
    User("Jordan", JORDAN_PHONE),
    User("Nancy", NANCY_PHONE),
]


def twilio_post(text, plant_lover):
    message = client.messages.create(
        body='{}{}'.format(plant_lover.text_header, text),
        from_=TWILIO_PHONE,
        to=plant_lover.phone
    )
    try:
        message.sid
    except socket.gaierror as address_error:
        logging.info("unable to get address info sending text to {}\n{}".format(plant_lover.name,
                                                                                address_error))
        return False
    except Exception as exc:
        logging.info("unable to send text: {}".format(exc))
        return False
    return True


def send_text(text, critical=True):
    for plant_lover in users:
        while not twilio_post(text, plant_lover) and critical:
            logging.info("Unable to send critical message to {}, waiting 30 seconds and trying again".format(
                plant_lover.name))


if __name__ == "__main__":
        while True:
            loop_start_time = time.time()
            for plant in the_list:
                try:
                    r = requests.get(plant.url)
                except requests.exceptions.ConnectionError as e:
                    logging.info(e)
                    send_text("unable to ping {}".format(plant.url), False)
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
                    if plant.current == 0:
                        logging.info("plant count = 0 , setting current count to previous")
                        plant.current = previous
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
            if DEBUG or ((now.hour == 22 or now.hour == 10 or now.hour == 16) and now.minute == 0):
                in_stock = [plant.plant for plant in the_list if plant.in_stock]
                not_stock = [plant.plant for plant in the_list if not plant.in_stock]
                update_message = 'This is an update from plants for us messaging bot\n\n'

                if in_stock:
                    update_message += 'Good news! {} was in stock and '.format(in_stock)
                if not_stock:
                    update_message += 'womp womp, {} are not in stock\n\n'.format(not_stock)
                update_message += "we hope you will continue to use our service"
                send_text(update_message)

                # reset in_stock tickers
                for plant in the_list:
                    plant.in_stock = False

            sleep_time = max(0, 60 - (time.time() - loop_start_time))
            logging.info("sleeping {} seconds".format(sleep_time))
            time.sleep(sleep_time)
