import os, time, creator, utils, sys

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
    primary_display = utils.get_primary_display()
    if primary_display == None:
        print("Failed to get primary display. Please check your display settings.")
        return

    def create_multiple_accounts(positions):
        threads = []
        for i in range(3):
            thread = creator.CreatorThread(positions[i], primary_display.width // 3, primary_display.height, config)
            thread.start()
            threads.append(thread)
            time.sleep(0.5)

        for thread in threads:
            thread.join()

    old_ips = [utils.get_ip_address()]
    if len(sys.argv) > 1 and sys.argv[1] == "-n":
        print("Removing current IP address from list of old IPs...")
        old_ips = []

    start_x = primary_display.x
    step_x = primary_display.width // 3
    positions = [start_x, start_x + step_x, start_x + step_x * 2]

    while True:
        print("Waiting for IP address to change...")
        current_ip = utils.wait_until_ip_changes(old_ips)
        old_ips.append(current_ip)

        print(f"Current IP address: {current_ip}")
        create_multiple_accounts(positions)

if __name__ == "__main__":
    main()
