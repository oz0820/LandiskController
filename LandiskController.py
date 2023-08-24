import copy
import sys
import requests


class Landisk:
    cookies = {}
    session = requests.session()

    def __init__(self, ip_address, password):
        self.ip_address = ip_address
        self.password = password

        self.login()

    def login(self):
        login_data = {'login': 'ログイン', 'password': self.password}
        res_before_login = self.session.get(f'http://{self.ip_address}/login')
        login_data['csrfmiddlewaretoken'] = res_before_login.cookies.get('csrftoken')

        res_after_login = self.session.post(f'http://{self.ip_address}/login', data=login_data)
        self.cookies = res_after_login.cookies

        write_file('t1.html', res_after_login.content)

        if not self.is_logged_in():
            sys.exit(-2)

    def shutdown(self):
        payload = copy.deepcopy(self.cookies)
        payload['execute'] = "実行"
        res_shutdown = self.session.post(f'http://{self.ip_address}/admin/system/power/shutdown/shutdownconfirm',
                                             data=payload)
        self.cookies = dict(res_shutdown.cookies)
        if res_shutdown.status_code == 200:
            print("Shutdown succeeded.")
        else:
            print('Shutdown failed.')
        write_file('shutdown.txt', res_shutdown.content)

    def reboot(self):
        payload = copy.deepcopy(self.cookies)
        payload['execute'] = "実行"
        res_shutdown = self.session.post(f'http://{self.ip_address}/admin/system/power/shutdown/rebootconfirm',
                                         data=payload)
        self.cookies = dict(res_shutdown.cookies)
        if res_shutdown.status_code == 200:
            print("Reboot succeeded.")
        else:
            print('Reboot failed.')
        write_file('reboot.txt', res_shutdown.content)

    def is_logged_in(self):
        res_status = self.session.get(f'http://{self.ip_address}/admin/status', data=self.cookies)
        self.cookies = dict(res_status.cookies)

        if res_status.status_code != 200:
            print("login failed.")
            return False
        else:
            print('login succeeded.')
            return True

    def get_status(self):
        res_status = self.session.get(f'http://{self.ip_address}/admin/status', data=self.cookies)
        self.cookies = dict(res_status.cookies)
        write_file('status.txt', res_status.content)


def write_file(name, content):
    with open(name, 'wb') as f:
        f.write(content)


if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 3:
        print("Invalid argument.")
        print("LandiskController <ip_address> <passsword>")
        sys.exit(-1)

    ld = Landisk(arguments[1], arguments[2])
    ld.shutdown()

    print()

