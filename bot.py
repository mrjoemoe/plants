#!/usr/bin/env python
import requests
import logging
import os
from datetime import datetime
import time
from twilio.rest import Client
import socket
from fake_headers import Headers


DEBUG = False
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
JORDAN_PHONE = os.environ.get("PHONE_1")
NANCY_PHONE = os.environ.get("PHONE_2")

global send_time

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="osx",  # Generate ony Windows platform
    headers=True  # generate misc headers
)

class User(object):

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.text_header = f"Plant update for {self.name}!!!\n\n"


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
        self.return_phrase_success = f"{self.plant} in stock at {self.shop}"
        self.return_phrase_fail = f"{self.plant} still out of stock at {self.shop}"
        self.in_stock = False
        self.current = -1


albo = CheckParameters(
    'albo monstera',
    'https://www.logees.com/variegated-mexican-breadfruit-monstera-deliciosa-variegata.html',
    ['0 in stock', '0  in stock'],
    'logees',
    'missing_string',
    )
ppp_logees = CheckParameters(
    'ppp_logees',
    'https://www.logees.com/philodendron-pink-princess-philodendron-erubescens.html',
    ['0 in stock', '0  in stock'],
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
    ['0 in stock', '0  in stock'],
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
melano = CheckParameters(
    'melano',
    'https://www.logees.com/black-gold-philodendron-philodendron-melanochrysum-2181.html',
    ['0 in stock', '0  in stock'],
    'logees',
    'missing_string',
    )
kerrii = CheckParameters(
    'kerrii',
    'https://www.gabriellaplants.com/products/4-hoya-kerri-reverse-variegated',
    'in stock',
    'gabriellaplants',
    'count',
    )
monstera_peru = CheckParameters(
    'monstera_peru',
    'https://www.nsetropicals.com/product/monstera-sp-peru/',
    'out of stock',
    'nse_tropicals',
    'count',
    )
rof = CheckParameters(
    'ring_of_fire',
    'https://www.nsetropicals.com/product/philodendron-ring-of-fire/',
    'out of stock',
    'nse_tropicals',
    'count',
    )
red_syngonium = CheckParameters(
    'red_syngonium',
    'https://stevesleaves.com/product/syngonium-erythrophyllum-llano-carti-road/',
    ['out of stock'],
    'steves_leaves',
    'missing_string',
    )
yellow_syngonium = CheckParameters(
    'yellow_syngonium',
    'https://www.gabriellaplants.com/collections/syngonium/products/4-variegated-nepthytis-emerald-gem-green-variegation',
    'in stock',
    'gabriellaplants',
    'count',
    )

the_list = [
            albo,
            ppp_logees,
            verrucosum,
            rio,
            # jessenia,
            # treubii,
            melano,
            kerrii,
            # monstera_peru,
            # rof,
            red_syngonium,
            yellow_syngonium,
]

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
users = [
    User("Jordan", JORDAN_PHONE),
    User("Nancy", NANCY_PHONE),
]


def twilio_post(text, plant_lover):
    message = client.messages.create(
        body=f"{plant_lover.text_header}{text}",
        from_=TWILIO_PHONE,
        to=plant_lover.phone
    )
    try:
        message.sid
    except socket.gaierror as address_error:
        logging.info(f"unable to get address info sending text to {plant_lover.name}\n{address_error}")
        return False
    except Exception as exc:
        logging.info(f"unable to send text: {exc}")
        return False
    return True


def send_text(text, critical=True):
    global send_time
    last_time = send_time
    send_time = time.time()
    if not critical and ((send_time - last_time) < 30 * 60):
        logging.info(f"not sending {text},  not important")
        return
    for plant_lover in users:
        while not twilio_post(text, plant_lover) and critical:
            logging.info(f"Unable to send critical message to {plant_lover.name}, waiting 30 seconds and trying again")


if __name__ == "__main__":
        global send_time
        send_time = time.time() - 30 * 60  # set a default
        logging.info("----- START -----")
        while True:
            loop_start_time = time.time()
            for plant in the_list:
                try:
                    headers = header.generate()
                    r = requests.get(plant.url, headers)
                except requests.exceptions.ConnectionError as e:
                    logging.info(e)
                    send_text(f"unable to ping {plant.url}", critical=False)
                    break
                except Exception as e:
                    logging.info(f"unable to service request for {plant.plant} - {e}")
                    next
                if plant.method == 'missing_string':
                    try:
                        check_strings = plant.check_string.copy()
                        check_strings.append("a timeout occurred")
                        check_strings.append("error establishing a database connection")
                        found = True
                        for string in check_strings:
                            if r.text.lower().find(string.lower()) != -1:
                                found = False
                                break
                        if found:
                            logging.info(plant.return_phrase_success)
                            if not plant.in_stock:
                                send_text(plant.return_phrase_success)
                                logging.info(r.text)
                                plant.in_stock = True
                        else:
                            logging.info(plant.return_phrase_fail)
                    except Exception as e:
                        logging.info(f"error trying find missing string: {e}")
                        send_text("exception caught trying to calculate missing string", critical=False)
                elif plant.method == 'count':
                    try:
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
                        logging.info(f"  previous={previous}, current={plant.current}")
                    except Exception as e:
                        logging.info(f"error trying count: {e}")
                        send_text("exception caught trying to count", critical=False)
                else:
                    logging.info(f"invalid method for {plant.plant}")

            now = datetime.now()
            if DEBUG or ((now.hour == 22 or now.hour == 10 or now.hour == 16) and now.minute == 0):
                in_stock = [plant.plant for plant in the_list if plant.in_stock]
                not_stock = [plant.plant for plant in the_list if not plant.in_stock]
                update_message = "This is an update from plants for us messaging bot\n\n"

                if in_stock:
                    update_message += f"Good news! {in_stock} was in stock and "
                if not_stock:
                    update_message += f"womp womp, {not_stock} are not in stock\n\n"
                update_message += "we hope you will continue to use our service"
                send_text(update_message)

                # reset in_stock tickers
                for plant in the_list:
                    plant.in_stock = False

            sleep_time = max(0, 60 - (time.time() - loop_start_time))
            logging.info(f"sleeping {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
