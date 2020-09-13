import sys
import requests
import logging
import os
from datetime import datetime
import time
import socket
from twilio.rest import Client
import socket
from fake_headers import Headers


TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
JORDAN_PHONE = os.environ.get("PHONE_1")
NANCY_PHONE = os.environ.get("PHONE_2")
NANXI_PHONE = os.environ.get("PHONE_3")

# very lazy way to turn on debug logging, if any arg is passed to script debug logging is enabled
LOG_LEVEL = logging.DEBUG if len(sys.argv) >= 2 else logging.INFO
SHOW_URL_TEXT_RETURN = True if len(sys.argv) >= 2 else False
SEND_UPDATE_TEXT_EVERY_ITER = False

global send_time
send_time = time.time() - 30 * 60  # set a default


class User(object):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.text_header = f"Plant update for {self.name}!!!\n\n"


SUPER_USERS = [User("Jordan", JORDAN_PHONE), User("Nancy", NANCY_PHONE)]


class CheckParameters(object):
    def __init__(self, plant, url, check_string, shop, method, short_url, recipients=SUPER_USERS, force=False):
        """
        plant: <str> name of plant
        url: <str> url to plant website
        check_string: <str> or <List> check_string to look for in return text from url
        shop: <str> name of plant shop
        method: <str> 'missing_string' or 'count'
        short_url: <str> url to send in text notification
        recipients: <List of Users> to send text notification on plant find
        force: <Bool> if True always send 'plant found' text
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
        self.recipients = recipients
        self.force = force


albo = CheckParameters(
    plant='albo monstera',
    url='https://www.logees.com/variegated-mexican-breadfruit-monstera-deliciosa-variegata.html',
    check_string=['0 in stock', '0  in stock'],
    shop='logees',
    method='missing_string',
    short_url='https://bit.ly/3kzsQpm',
    )
ppp_logees = CheckParameters(
    plant='ppp_logees',
    url='https://www.logees.com/philodendron-pink-princess-philodendron-erubescens.html',
    check_string=['0 in stock', '0  in stock'],
    shop='logees',
    method='missing_string',
    short_url='https://bit.ly/3gMCYcd',
    )
rio = CheckParameters(
    plant='rio',
    url='https://www.gabriellaplants.com/collections/philodendron/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/2DRbPX2',
    )
silver_sword = CheckParameters(
    plant='silver_sword',
    url='https://www.gabriellaplants.com/collections/philodendron/products/4-silver-sword-philodendron-philodendron-hastatum',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/33T3H3j',
    )
ppp_gabriella = CheckParameters(
    plant='ppp_gabriella',
    url='https://www.gabriellaplants.com/products/4-pink-princess-philodendron',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/30LeL0r',
    recipients=[User("Jordan", JORDAN_PHONE), User("Nancy", NANCY_PHONE), User("Nanxi", NANXI_PHONE)],
    )
verrucosum = CheckParameters(
    plant='p. verrucosum',
    url='https://www.logees.com/ecuador-philodendron-philodendron-ventricosum.html',
    check_string=['0 in stock', '0  in stock'],
    shop='logees',
    method='missing_string',
    short_url='https://bit.ly/2DTVOPS',
    )
jessenia = CheckParameters(
    plant='jessenia',
    url='https://www.gabriellaplants.com/collections/pothos/products/4-jessenia-pothos',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/2XNHyPI',
    )
treubii = CheckParameters(
    plant='treubii',
    url='https://www.gabriellaplants.com/collections/scindapsus-1/products/3-scindapsus-treubii-moonlight',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='htstps://bit.ly/33LE5Fp',
    )
melano = CheckParameters(
    plant='melano',
    url='https://www.logees.com/black-gold-philodendron-philodendron-melanochrysum-2181.html',
    check_string=['0 in stock', '0  in stock'],
    shop='logees',
    method='missing_string',
    short_url='https://bit.ly/3fLXXKT',
    )
kerrii = CheckParameters(
    plant='kerrii',
    url='https://www.gabriellaplants.com/products/4-hoya-kerri-reverse-variegated',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/3iuQrWE',
    )
monstera_peru = CheckParameters(
    plant='monstera_peru',
    url='https://www.nsetropicals.com/product/monstera-sp-peru/',
    check_string='out of stock',
    shop='nse_tropicals',
    method='count',
    short_url='https://bit.ly/3add1A0',
    )
rof = CheckParameters(
    plant='ring_of_fire',
    url='https://www.nsetropicals.com/product/philodendron-ring-of-fire/',
    check_string='out of stock',
    shop='nse_tropicals',
    method='count',
    short_url='https://bit.ly/3gLMz35',
    )
red_syngonium = CheckParameters(
    plant='red_syngonium',
    url='https://stevesleaves.com/product/syngonium-erythrophyllum-llano-carti-road/',
    check_string=['out of stock'],
    shop='steves_leaves',
    method='missing_string',
    short_url='https://bit.ly/3islamV',
    )
yellow_syngonium = CheckParameters(
    plant='yellow_syngonium',
    url='https://www.gabriellaplants.com/collections/syngonium/products/4-variegated-nepthytis-emerald-gem-green-variegation',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/3kxb1Ya',
    )
el_choco_red = CheckParameters(
    plant='el_choco_red',
    url='https://www.ecuagenera.com/epages/ecuagenera.sf/en_US/?ObjectPath=/Shops/ecuagenera/Products/PRE2244-003',
    check_string=['out of stock'],
    shop='ecuagenera',
    method='missing_string',
    short_url='https://bit.ly/3kF5yib',
    )
queen_anthurium = CheckParameters(
    plant='queen_anthurium',
    url='https://www.ecuagenera.com/epages/ecuagenera.sf/en_US/?ObjectPath=/Shops/ecuagenera/Products/PIE2101',
    check_string=['out of stock'],
    shop='ecuagenera',
    method='missing_string',
    short_url='https://bit.ly/31E4rqa',
    )
hoya_dekya_3 = CheckParameters(
    plant='hoya_dekya_3',
    url='https://www.gabriellaplants.com/products/3-hoya-deykei',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/3bKhSt8',
    )
hoya_dekya_4 = CheckParameters(
    plant='hoya_dekya_4',
    url='https://www.gabriellaplants.com/products/4-hoya-deykei',
    check_string='in stock',
    shop='gabriellaplants',
    method='count',
    short_url='https://bit.ly/3bPTWou',
    )
hoya_black = CheckParameters(
    plant='hoya_black',
    url='https://gardinonursery.com/product/hoya-krohniana-black-leaves-epc-943-2/',
    check_string='in stock',
    shop='gardinonursery',
    method='count',
    short_url='https://bit.ly/32p4SGn',
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
            # red_syngonium,
            yellow_syngonium,
            el_choco_red,
            queen_anthurium,
            hoya_dekya_3,
            hoya_dekya_4,
            hoya_black,
]

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=LOG_LEVEL)
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


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


def send_text(text, critical=True, recipients=SUPER_USERS):
    global send_time
    last_time = send_time
    send_time = time.time()
    if not critical and ((send_time - last_time) < 30 * 60):
        logging.info(f"not sending {text},  not important")
        return
    for plant_lover in recipients:
        logging.info(f"sending message to {plant_lover.name}")
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
                    # debug line
                    if plant.force:
                        logging.info(f"sending found text for {plant.plant}")
                        send_text(plant.return_phrase_success, recipients=plant.recipients)
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
                    logging.debug(f"PLANT: {plant.plant}")
                    logging.debug(r.text)
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
                                    send_text(plant.return_phrase_success, recipients=plant.recipients)
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
                            if previous == -1:
                                logging.info(f"first iteration for {plant.plant}, ignoring count")
                            elif previous >= 0 and (previous != plant.current):
                                logging.info(plant.return_phrase_success)
                                if not plant.in_stock:
                                    send_text(plant.return_phrase_success, recipients=plant.recipients)
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
                if (SEND_UPDATE_TEXT_EVERY_ITER or 
                    ((now.hour == 22 or now.hour == 10 or now.hour == 16) and now.minute == 0)):
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
