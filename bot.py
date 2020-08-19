import requests
import logging
import os
from datetime import datetime
import time
import socket
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
send_time = time.time() - 30 * 60  # set a default

# shorturl.at/dwBU3
class User(object):

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.text_header = f"Plant update for {self.name}!!!\n\n"


class CheckParameters(object):

    def __init__(self, plant, url, check_string, shop, method, short_url, force=False):
        """
        method = 'count', 'missing_string'
        """
        self.plant = plant
        self.url = url
        self.check_string = check_string
        self.shop = shop
        self.method = method
        self.return_phrase_success = f"{self.plant} in stock at {self.shop} {short_url}"
        self.return_phrase_fail = f"{self.plant} still out of stock at {self.shop}"
        self.in_stock = False
        self.current = -1
        self.force = force  # force return in stock


albo = CheckParameters(
    'albo monstera',
    'https://www.logees.com/variegated-mexican-breadfruit-monstera-deliciosa-variegata.html',
    ['0 in stock', '0  in stock'],
    'logees',
    'missing_string',
    'https://bit.ly/3kzsQpm',
    )
ppp_logees = CheckParameters(
    'ppp_logees',
    'https://www.logees.com/philodendron-pink-princess-philodendron-erubescens.html',
    ['0 in stock', '0  in stock'],
    'logees',
    'missing_string',
    'https://bit.ly/3gMCYcd',
    )
rio = CheckParameters(
    'rio',
    'https://www.gabriellaplants.com/collections/philodendron/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation',
    'in stock',
    'gabriellaplants',
    'count',
    'https://bit.ly/2DRbPX2',
    )
silver_sword = CheckParameters(
    'silver_sword',
    'https://www.gabriellaplants.com/collections/philodendron/products/4-silver-sword-philodendron-philodendron-hastatum',
    'in stock',
    'gabriellaplants',
    'count',
    'https://bit.ly/33T3H3j',
    )
ppp_gabriella = CheckParameters(
    'ppp_gabriella',
    'https://www.gabriellaplants.com/products/4-pink-princess-philodendron',
    'in stock',
    'gabriellaplants',
    'count',
    'https://bit.ly/30LeL0r',
    )
verrucosum = CheckParameters(
    'p. verrucosum',
    'https://www.logees.com/ecuador-philodendron-philodendron-ventricosum.html',
    ['0 in stock', '0  in stock'],
    'logees',
    'missing_string',
    'https://bit.ly/2DTVOPS',
    )
jessenia = CheckParameters(
    'jessenia',
    'https://www.gabriellaplants.com/collections/pothos/products/4-jessenia-pothos',
    'in stock',
    'gabriellaplants',
    'count',
    'https://bit.ly/2XNHyPI',
    )
treubii = CheckParameters(
    'treubii',
    'https://www.gabriellaplants.com/collections/scindapsus-1/products/3-scindapsus-treubii-moonlight',
    'in stock',
    'gabriellaplants',
    'count',
    'https://bit.ly/33LE5Fp',
    )
melano = CheckParameters(
    'melano',
    'https://www.logees.com/black-gold-philodendron-philodendron-melanochrysum-2181.html',
    ['0 in stock', '0  in stock'],
    'logees',
    'missing_string',
    'https://bit.ly/3fLXXKT',
    )
kerrii = CheckParameters(
    'kerrii',
    'https://www.gabriellaplants.com/products/4-hoya-kerri-reverse-variegated',
    'in stock',
    'gabriellaplants',
    'count',
    'https://bit.ly/3iuQrWE',
    )
monstera_peru = CheckParameters(
    'monstera_peru',
    'https://www.nsetropicals.com/product/monstera-sp-peru/',
    'out of stock',
    'nse_tropicals',
    'count',
    'https://bit.ly/3add1A0',
    )
rof = CheckParameters(
    'ring_of_fire',
    'https://www.nsetropicals.com/product/philodendron-ring-of-fire/',
    'out of stock',
    'nse_tropicals',
    'count',
    'https://bit.ly/3gLMz35',
    )
red_syngonium = CheckParameters(
    'red_syngonium',
    'https://stevesleaves.com/product/syngonium-erythrophyllum-llano-carti-road/',
    ['out of stock'],
    'steves_leaves',
    'missing_string',
    'https://bit.ly/3islamV',
    )
yellow_syngonium = CheckParameters(
    'yellow_syngonium',
    'https://www.gabriellaplants.com/collections/syngonium/products/4-variegated-nepthytis-emerald-gem-green-variegation',
    'in stock',
    'gabriellaplants',
    'count',
    'https://bit.ly/3kxb1Ya',
    )
el_choco_red = CheckParameters(
    'el_choco_red',
    'https://www.ecuagenera.com/epages/ecuagenera.sf/en_US/?ObjectPath=/Shops/ecuagenera/Products/PRE2244-003',
    ['out of stock'],
    'ecuagenera',
    'missing_string',
    'https://bit.ly/3kF5yib',
    )
queen_anthurium = CheckParameters(
    'queen_anthurium',
    'https://www.ecuagenera.com/epages/ecuagenera.sf/en_US/?ObjectPath=/Shops/ecuagenera/Products/PIE2101',
    ['out of stock'],
    'ecuagenera',
    'missing_string',
    'https://bit.ly/31E4rqa',
    )

the_list = [
            albo,
            ppp_logees,
            ppp_gabriella,
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
            el_choco_red,
            queen_anthurium,
]

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
users = [
    User("Jordan", JORDAN_PHONE),
    User("Nancy", NANCY_PHONE),
]


def no_internet():
    return socket.gethostbyname(socket.gethostname()) == "127.0.0.1"


def twilio_post(text, plant_lover):
    if no_internet():
        logging.info("unable to send text, no internet connection, sleeping 1 minute")
        time.sleep(60 * 1)
        return False
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
        logging.info("----- START -----")
        while True:
            if no_internet():
                logging.info("no internet connection, five minute rest")
                time.sleep(5 * 60)
            else:
                loop_start_time = time.time()
                for plant in the_list:
                    if plant.force:
                        logging.info(f"sending found text for {plant.plant}")
                        send_text(plant.return_phrase_success)
                        next
                    try:
                        header = Headers(headers=False).generate()
                        r = requests.get(plant.url, header)
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
                            check_strings.append("502 Bad Gateway")
                            check_strings.append("504: Gateway time-out")
                            check_strings.append("502: Bad gateway")
                            found = True
                            for string in check_strings:
                                # = -1 means did not find
                                if r.text.lower().find(string.lower()) != -1:
                                    logging.info(f"found '{string}', so {plant.plant} not in stock")
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
