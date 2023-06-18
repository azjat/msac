import os, time, creator, utils

def main():
    os.system("cls || clear")
    utils.logo()

    config = utils.load_config()
    print("Loaded config:")
    print(f"Webdriver: {str(config['webdriver'])}")
    print(f"Country: {str(config['country_code'])}")

    utils.install_webdriver(config)
    create_accounts(config)


def create_accounts(config):
    def create_multiple_accounts(positions):
        threads = []
        for i in range(3):
            thread = creator.CreatorThread(positions[i], config)
            thread.start()
            threads.append(thread)
            time.sleep(0.5)

        for thread in threads:
            thread.join()

    # TODO: make this positions dynamic
    positions = [0, 640, 1280]
    create_multiple_accounts(positions)

    # TODO: cleanup this mess
    ip_address = None
    while ip_address is None:
        ip_address = utils.get_ip_address()
        if ip_address is None:
            print("Retrying to get IP address...")
            time.sleep(1)

    print(f"Current IP address: {ip_address}")

    while True:
        time.sleep(1)
        new_ip_address = utils.get_ip_address()
        if new_ip_address != ip_address:
            if new_ip_address != None:
                print("IP address changed. Creating new accounts...")
                create_multiple_accounts(positions)
                ip_address = new_ip_address

if __name__ == "__main__":
    main()
