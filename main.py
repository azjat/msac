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

    old_ips = []

    # TODO: make this positions dynamic
    positions = [0, 640, 1280]

    while True:
        print("Waiting for IP address to change...")
        current_ip = utils.wait_until_ip_changes(old_ips)
        old_ips.append(current_ip)

        print(f"Current IP address: {current_ip}")
        create_multiple_accounts(positions)

if __name__ == "__main__":
    main()
