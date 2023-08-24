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
        self.cookies = dict(res_after_login.cookies)

        if not self.is_logged_in():
            sys.exit(-2)

    def shutdown(self):
        res_shutdown_page = self.session.get(f'http://{self.ip_address}/admin/system/power/shutdown/shutdownconfirm',
                                             cookies=self.cookies)
        if res_shutdown_page.status_code != 200:
            print('Failed to retrieve shutdown page.')
            sys.exit(-3)

        self.cookies = dict(res_shutdown_page.cookies)

        payload = {
            'csrfmiddlewaretoken': self.cookies.get('csrftoken'),
            'execute': '実行'
        }

        res_shutdown = self.session.post(f'http://{self.ip_address}/admin/system/power/shutdown/shutdownconfirm', cookies=self.cookies, data=payload)
        self.cookies = dict(res_shutdown.cookies)
        print("Shutdown succeeded, probably.")

    def reboot(self):
        res_reboot_page = self.session.get(f'http://{self.ip_address}/admin/system/power/shutdown/rebootconfirm',
                                             cookies=self.cookies)
        if res_reboot_page.status_code != 200:
            print('Failed to retrieve reboot page.')
            sys.exit(-3)

        self.cookies = dict(res_reboot_page.cookies)

        payload = {
            'csrfmiddlewaretoken': self.cookies.get('csrftoken'),
            'execute': '実行'
        }

        res_reboot = self.session.post(f'http://{self.ip_address}/admin/system/power/shutdown/shutdownconfirm', cookies=self.cookies, data=payload)
        self.cookies = dict(res_reboot.cookies)
        print("Reboot succeeded, probably.")

    def is_logged_in(self):
        res_status = self.session.get(f'http://{self.ip_address}/admin/status', data=self.cookies)

        if res_status.status_code != 200:
            print("login failed.")
            return False
        else:
            print('login succeeded.')
            return True

    def get_status(self):
        res_status = self.session.get(f'http://{self.ip_address}/admin/status', data=self.cookies)
        self.cookies = dict(res_status.cookies)


if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 3:
        print("Invalid argument.")
        print("LandiskController <ip_address> <passsword>")
        sys.exit(-1)

    ld = Landisk(arguments[1], arguments[2])
    ld.shutdown()

