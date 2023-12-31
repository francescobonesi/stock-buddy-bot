class Config:
    def __init__(self):
        self._token = None
        self._webhook = None
        self._secret = None
        self._chat_id = None
        self._ticker = None
        self._populate()

    def token(self):
        return self._token

    def secret(self):
        return self._secret

    def chat_id(self):
        return self._chat_id

    def ticker(self):
        return self._ticker

    def webhook(self):
        return self._webhook

    def set_webook_cmd(self):
        return f"https://api.telegram.org/bot{self._token}/setWebhook?" \
               f"url={self._webhook}&" \
               f"secret_token={self._secret}"

    def remove_webook_cmd(self):
        return f"https://api.telegram.org/bot{self._token}/setWebhook?" \
               f"remove"

    def get_webook_cmd(self):
        return f"https://api.telegram.org/bot{self._token}/getWebhookInfo"

    def _populate(self):
        import configparser
        config_object = configparser.ConfigParser()
        with open("config.ini", "r") as file:
            config_object.read_file(file)
            output_dict = {s: dict(config_object.items(s)) for s in config_object.sections()}
            telegram_dict = output_dict.get("telegram")
            self._token = telegram_dict.get("token")
            self._secret = telegram_dict.get("secret")
            self._webhook = telegram_dict.get("webhook")
            self._chat_id = int(telegram_dict.get("personal_chat"))
            self._ticker = output_dict.get("ticker", {}).get("name")
