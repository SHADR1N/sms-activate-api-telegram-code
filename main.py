import json
from smsactivate.api import SMSActivateAPI
from time import time, sleep
import random

class SmsActivate():
    def __init__(self, token):
        self.token = token
        self.api = SMSActivateAPI(self.token)
        self.country = [0, 1, 2, 51]
        random.shuffle(self.country)
        self.phone = None

    def get_phone(self):
        if self.balance() > 20:
            for country in self.country:
                self.phone = self.api.getNumber(service='tg', country=country, verification=False)
                if 'error' in self.phone:
                    if self.phone['error'] == 'NO_NUMBERS':
                        continue
                elif 'phone' in self.phone and 'activation_id' in self.phone:
                    self.set_status()
                    return self.phone['phone']
            else:
                return False
        else:
            print('Недостаточно средств')
            return False

    def set_status(self, status=1):
        return self.api.setStatus(id=self.phone['activation_id'], status=status)

    def get_code(self, timeout=120):
        start = time()

        while True:
            status = self.api.getStatus(id=self.phone['activation_id'])
            try:
                sms_code = self.api.activationStatus(status)
            except:
                continue
            if 'STATUS_OK' in sms_code['status']:
                self.set_status(status=6)
                return sms_code['status'].split(':')[1].strip()

            if time() - start > timeout:
                self.set_status(status=8)
                return False

            sleep(1)

    def balance(self):
        return float(self.api.getBalanceAndCashBack()['balance'])

    
if __name__ == '__main__':
    api = SmsActivate('YOUR API KEY')
    api.balance()
    phone = api.get_phone()
    if phone:
        code = api.get_code()
    else:
        print('No free phone.')
