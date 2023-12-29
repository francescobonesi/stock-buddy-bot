import datetime
import json

from config import Config
from portfolio import Portfolio
from sender import telegram_bot_send
from ticker import TickerData

ERROR_IN_REQUEST = "Error in request!"

config = Config()


def inject_and_send_message(func):
    def inner():
        now_or_last_updated_price_data = TickerData(config.ticker()).get_now_or_last_updated_price()
        now_or_last_updated_price = now_or_last_updated_price_data.get('price')
        p_data = Portfolio().elaborate(now_or_last_updated_price)

        message = func(now_or_last_updated_price_data, now_or_last_updated_price, p_data)

        telegram_bot_send(config.token(), config.chat_id(), message)
        return message

    return inner


@inject_and_send_message
def info(now_or_last_updated_price_data=None, now_or_last_updated_price=None, p_data=None):
    increment = now_or_last_updated_price_data.get('increment_percentage')
    return f"[{now_or_last_updated_price_data.get('date')}] " \
           f"{round(now_or_last_updated_price, 2)} USD " \
           f"({increment} from previous market day)\n" \
           + suggest_to_sell_message(p_data)


@inject_and_send_message
def cashed(_0=None, _1=None, p_data=None):
    return f"Total sold {p_data.get('sell')} shares\n" \
           f"Original value {p_data.get('cashed_original_value')} USD\n" \
           f"Cashed value {p_data.get('cashed')} USD " \
           f"({p_data.get('cashed_increment_percentage')} w.r.t. original value)\n" \
           f"Cashed gain {p_data.get('cashed_gain')} USD"


@inject_and_send_message
def portfolio(_0=None, _1=None, p_data=None):
    return f"Total hold {p_data.get('hold')} shares, " \
           f"bought at {p_data.get('hold_original_value')} USD\n" \
           f"Now they value {p_data.get('hold_current_value')} USD " \
           f"({p_data.get('increment_on_hold_percentage')} w.r.t. original value)\n" \
           f"Current gain on hold {p_data.get('gain_on_hold')} USD"


def suggest_to_sell_message(p_data):
    suggest_to_sell = p_data.get('is_suggested_to_sell')
    if suggest_to_sell:
        return f"Sell {p_data('suggested_shares_to_sell')} shares to get the gain!"
    else:
        return "Don't sell for now"


@inject_and_send_message
def analysis(_, now_or_last_updated_price=None, p_data=None):
    return f"Current price {round(now_or_last_updated_price,2)} USD\n" \
           f"Total bought {p_data.get('buy')} shares " \
           f"at {p_data.get('bought_original_value')} USD\n" \
           f"Total hold {p_data.get('hold')} shares " \
           f"that now value {p_data.get('hold_current_value')} USD " \
           f"({p_data.get('increment_on_bought_percentage')} w.r.t. bought)\n" \
           f"Current gain on bought {p_data.get('gain_on_bought')} USD\n" \
           + suggest_to_sell_message(p_data)


@inject_and_send_message
def wrong_command(*_):
    return "Wrong command!"


commands = {
    "info": info,
    "cashed": cashed,
    "portfolio": portfolio,
    "analysis": analysis
}


def extract_from_body(request):
    secret_header = 'X-Telegram-Bot-Api-Secret-Token'
    secret_received = request.headers.get(secret_header)
    print(secret_received)
    body = json.loads(request.data)
    print(f"Request body: {body}")
    message = body.get("message", {})
    chat_id = message.get('chat', {}).get('id', None)
    text = message.get('text', '')
    print(f"Received text: {text}")
    return message, chat_id, text, secret_received


def is_input_allowed(chat_id):
    if chat_id is None:
        print("Missing Chat Id in Request Body")
        return False
    print(f"Chat ID: {chat_id}")
    if chat_id != config.chat_id():
        print("Chat not allowed")
        return False
    return True


def is_secret_allowed(received_secret):
    if received_secret is None or received_secret != config.secret():
        print("Secret not allowed")
        return False
    return True


def bot_function(request):
    message, chat_id, text, received_secret = extract_from_body(request)
    if not is_input_allowed(chat_id):
        return ERROR_IN_REQUEST
    if not is_secret_allowed(received_secret):
        return ERROR_IN_REQUEST

    text = str(text).lower()
    text = text[1:] if text.startswith('/') else text
    print(f"Command: {text}")
    message = commands.get(text, wrong_command)()
    print(f"Sent message: {message}")

    return "DONE"


def send_updates(_):
    print(f"Scheduled update on {str(datetime.date.today())}")
    return info()


if __name__ == '__main__':
    class Fake:
        def __init__(self, what):
            self.headers = {
                "X-Telegram-Bot-Api-Secret-Token": config.secret()
            }
            self.data = '{"update_id":339746117,' \
                        '"message":{"message_id":73,' \
                        '"from":{"id":166659083,"is_bot":false,"first_name":"Francesco",' \
                        '"last_name":"Bonesi","username":"frabon0","language_code":"it"},' \
                        '"chat":{"id":166659083,"first_name":"Francesco","last_name":"Bonesi",' \
                        '"username":"frabon0","type":"private"},"date":1702739493,' \
                        '"text":"' + what + '"}}'


    print(config.chat_id())
    print(config.token())
    print(config.secret())
    print(config.ticker())
    bot_function(Fake("info"))
    bot_function(Fake("cashed"))
    bot_function(Fake("portfolio"))
    bot_function(Fake("analysis"))
    bot_function(Fake("xxx"))
