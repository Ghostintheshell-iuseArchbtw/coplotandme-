import os
import os
import re
import subprocess
import logging
import signal
import sys
import configparser
import time
import signal
import time

# Constants
CONFIG_FILE_PATH = "/etc/script_config.ini"
SNORT_LOG_PATH = "/var/log/snort/snort.log"
BLACKLIST_FILE = "/etc/blacklisted_ips.txt"
SCRIPT_SERVICE_NAME = "my_script.service"
SNORT_SERVICE_NAME = "snort.service"
IPTABLES_SERVICE_NAME = "iptables.service"

# Initialize configuration parser
config = configparser.ConfigParser()

# Function to create the configuration file with a template if it doesn't exist
def create_config_file():
    if not os.path.isfile(CONFIG_FILE_PATH):
        config['Paths'] = {
            'SNORT_LOG_PATH': SNORT_LOG_PATH,
            'BLACKLIST_FILE': BLACKLIST_FILE,
        }
        config['Services'] = {
            'SCRIPT_SERVICE_NAME': SCRIPT_SERVICE_NAME,
            'SNORT_SERVICE_NAME': SNORT_SERVICE_NAME,
            'IPTABLES_SERVICE_NAME': IPTABLES_SERVICE_NAME,
        }
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

# Function to gracefully stop services
def stop_service(service_name: str) -> None:
    try:
        subprocess.check_call(["systemctl", "stop", service_name])
        subprocess.check_call(["systemctl", "disable", service_name])
    except subprocess.CalledProcessError as e:
        logging.exception(f"Error stopping/disabling service {service_name}: {e}")

# Function to handle script termination gracefully
def handle_termination(signal, frame):
    logging.info("Received termination signal. Stopping services and exiting gracefully.")
    stop_service(SNORT_SERVICE_NAME)
    stop_service(IPTABLES_SERVICE_NAME)
    sys.exit(0)

# Function to parse Snort logs and find offending IPs
def parse_snort_logs() -> set:
    IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    offending_ips = set()
    try:
        with open(SNORT_LOG_PATH, "r") as log_file:
            for line in log_file:
                match = IP_PATTERN.search(line)
                if match:
                    ip = match.group(0)
                    offending_ips.add(ip)
    except FileNotFoundError:
        logging.error(f"Snort log file not found at {SNORT_LOG_PATH}")
    return offending_ips

# Function to load the previously blacklisted IPs
def load_blacklisted_ips(file_path: str) -> set:
    blacklisted_ips = set()
    try:
        with open(file_path, "r") as file:
            for line in file:
                blacklisted_ips.add(line.strip())
    except FileNotFoundError:
        pass
    except UnicodeDecodeError:
        logging.exception(f"Error decoding file at {file_path}")
    return blacklisted_ips

# Function to blacklist an IP using iptables
def blacklist_ip(ip: str) -> None:
    try:
        subprocess.check_call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        logging.info(f"IP {ip} has been blacklisted.")
    except subprocess.CalledProcessError as e:
        logging.exception(f"Error blacklisting IP {ip}: {e}")

# Function to check if a systemd service is enabled and running
def is_service_enabled_and_running(service_name: str) -> bool:
    try:
        subprocess.check_call(["systemctl", "is-active", "--quiet", service_name])
        subprocess.check_call(["systemctl", "is-enabled", "--quiet", service_name])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to create a systemd service file if it doesn't exist
def create_service_file(service_path: str, service_content: str) -> None:
    if not os.path.isfile(service_path):
        os.makedirs(os.path.dirname(service_path), exist_ok=True)
        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to configure and start Snort in daemon mode
def configure_and_start_snort():
    # Check if Snort is installed
    if not os.path.exists("/usr/sbin/snort"):
        logging.info("Snort is not installed. Installing...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "snort", "-y"], check=True)

    # Check if Snort service is enabled and running
LOG_FILE_PATH = "/var/log/script_log.txt"
WAIT_TIME_MINUTES = 30
IPTABLES_SERVICE_NAME = "iptables.service"
LOG_FILE_PATH = "/var/log/script_log.txt"
WAIT_TIME_MINUTES = 30

# Initialize configuration parser
config = configparser.ConfigParser()

# Function to create the configuration file with a template if it doesn't exist
def create_config_file():
    if not os.path.exists(CONFIG_FILE_PATH):
        config['Paths'] = {
            'SNORT_LOG_PATH': SNORT_LOG_PATH,
            'BLACKLIST_FILE': BLACKLIST_FILE,
        }
        config['Services'] = {
            'SCRIPT_SERVICE_NAME': SCRIPT_SERVICE_NAME,
            'SNORT_SERVICE_NAME': SNORT_SERVICE_NAME,
            'IPTABLES_SERVICE_NAME': IPTABLES_SERVICE_NAME,
        }
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

# Function to gracefully stop services
def stop_service(service_name):
    try:
        subprocess.run(["systemctl", "stop", service_name], check=True)
        subprocess.run(["systemctl", "disable", service_name], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error stopping/disabling service {service_name}: {e}")

# Function to handle script termination gracefully
def handle_termination(signal, frame):
    logging.info("Received termination signal. Stopping services and exiting gracefully.")
    stop_service(SNORT_SERVICE_NAME)
    stop_service(IPTABLES_SERVICE_NAME)
    sys.exit(0)

# Function to parse Snort logs and find offending IPs
def parse_snort_logs():
    offending_ips = set()
    try:
        with open(SNORT_LOG_PATH, "rb") as log_file:
            for line in log_file:
                line = line.decode('utf-8', errors='ignore')
                match = IP_PATTERN.search(line)
                if match:
                    ip = match.group(1)
                    offending_ips.add(ip)
    except FileNotFoundError:
        logging.error(f"Snort log file not found at {SNORT_LOG_PATH}")
    return offending_ips

# Function to load the previously blacklisted IPs
def load_blacklisted_ips(file_path):
    blacklisted_ips = set()
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            for line in file:
                blacklisted_ips.add(line.strip())
    except FileNotFoundError:
        pass
    except UnicodeDecodeError:
        logging.error(f"Error decoding file at {file_path}")
    return blacklisted_ips

# Function to blacklist an IP using iptables
def blacklist_ip(ip):
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        logging.info(f"IP {ip} has been blacklisted.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blacklisting IP {ip}: {e}")

# Function to check if a systemd service is enabled and running
def is_service_enabled_and_running(service_name):
    try:
        subprocess.run(["systemctl", "is-active", "--quiet", service_name], check=True)
        subprocess.run(["systemctl", "is-enabled", "--quiet", service_name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to create a systemd service file if it doesn't exist
def create_service_file(service_path, service_content):
    if not os.path.exists(service_path):
        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

# Function to configure and start Snort in daemon mode
def configure_and_start_snort():
    # Check if Snort is installed
    if not os.path.exists("/usr/sbin/snort"):
        logging.info("Snort is not installed. Installing...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "snort", "-y"], check=True)

    # Check if Snort service is enabled and running
    if not is_service_enabled_and_running(SNORT_SERVICE_NAME):
        logging.info("Snort is not running as a daemon. Configuring and starting...")
IPTABLES_SERVICE_NAME = "iptables.service"
LOG_FILE_PATH = "/var/log/script_log.txt"
WAIT_TIME_MINUTES = 30

# Initialize configuration parser
config = configparser.ConfigParser()

# Function to create the configuration file with a template if it doesn't exist
def create_config_file():
    if not os.path.exists(CONFIG_FILE_PATH):
        config['Paths'] = {
            'SNORT_LOG_PATH': SNORT_LOG_PATH,
            'BLACKLIST_FILE': BLACKLIST_FILE,
        }
        config['Services'] = {
            'SCRIPT_SERVICE_NAME': SCRIPT_SERVICE_NAME,
            'SNORT_SERVICE_NAME': SNORT_SERVICE_NAME,
            'IPTABLES_SERVICE_NAME': IPTABLES_SERVICE_NAME,
        }
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

# Function to gracefully stop services
def stop_service(service_name):
    try:
        subprocess.run(["systemctl", "stop", service_name], check=True)
        subprocess.run(["systemctl", "disable", service_name], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error stopping/disabling service {service_name}: {e}")

# Function to handle script termination gracefully
def handle_termination(signal, frame):
    logging.info("Received termination signal. Stopping services and exiting gracefully.")
    stop_service(SNORT_SERVICE_NAME)
    stop_service(IPTABLES_SERVICE_NAME)
    sys.exit(0)

# Function to parse Snort logs and find offending IPs
def parse_snort_logs():
    offending_ips = set()
    try:
        with open(SNORT_LOG_PATH, "rb") as log_file:
            for line in log_file:
                line = line.decode('utf-8', errors='ignore')
                match = IP_PATTERN.search(line)
                if match:
                    ip = match.group(1)
                    offending_ips.add(ip)
    except FileNotFoundError:
        logging.error(f"Snort log file not found at {SNORT_LOG_PATH}")
    return offending_ips

# Function to load the previously blacklisted IPs
def load_blacklisted_ips(file_path):
    blacklisted_ips = set()
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            for line in file:
                blacklisted_ips.add(line.strip())
    except FileNotFoundError:
        pass
    except UnicodeDecodeError:
        logging.error(f"Error decoding file at {file_path}")
    return blacklisted_ips

# Function to blacklist an IP using iptables
def blacklist_ip(ip):
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        logging.info(f"IP {ip} has been blacklisted.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blacklisting IP {ip}: {e}")

# Function to check if a systemd service is enabled and running
def is_service_enabled_and_running(service_name):
    try:
        subprocess.run(["systemctl", "is-active", "--quiet", service_name], check=True)
        subprocess.run(["systemctl", "is-enabled", "--quiet", service_name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to create a systemd service file if it doesn't exist
def create_service_file(service_path, service_content):
    if not os.path.exists(service_path):
        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

# Function to configure and start Snort in daemon mode
def configure_and_start_snort():
    # Check if Snort is installed
    if not os.path.exists("/usr/sbin/snort"):
        logging.info("Snort is not installed. Installing...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "snort", "-y"], check=True)

    # Check if Snort service is enabled and running
    if not is_service_enabled_and_running(SNORT_SERVICE_NAME):
        logging.info("Snort is not running as a daemon. Configuring and starting...")
        # Configure Snort here
        snort_service_content = f"""
[Unit]
Description=Snort Intrusion Detection System
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/snort -q -u snort -g snort -c /etc/snort/snort.conf -i eth0
Restart=always

[Install]
WantedBy=multi-user.target
"""
        create_service_file(f"/etc/systemd/system/{SNORT_SERVICE_NAME}", snort_service_content)
        subprocess.run(["systemctl", "enable", SNORT_SERVICE_NAME], check=True)
        subprocess.run(["systemctl", "start", SNORT_SERVICE_NAME], check=True)

# Function to configure iptables using UFW
def configure_iptables_with_ufw():
    # Check if UFW is installed
    if not os.path.exists("/usr/sbin/ufw"):
        logging.info("UFW is not installed. Installing...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "ufw", "-y"], check=True)

    # Enable and start UFW
    try:
        subprocess.run(["ufw", "enable"], check=True, input="y\n", text=True)
        subprocess.run(["ufw", "status"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error enabling UFW: {e}")

# Function to display blacklisted IPs
def display_blacklisted_ips(file_path):
    blacklisted_ips = load_blacklisted_ips(file_path)
    if blacklisted_ips:
        print("Blacklisted IPs:")
        for ip in blacklisted_ips:
            print(ip)
    else:
        print("No blacklisted IPs found.")

# Main function
def main():
    create_config_file()  # Create the config file if it doesn't exist

    # Read configuration values from the config file
    config.read(CONFIG_FILE_PATH)

    global IP_PATTERN
    IP_PATTERN = re.compile(r"(\d+\.\d+\.\d+\.\d+)")

    try:
        # Check and configure Snort
        configure_and_start_snort()

        # Check and configure iptables with UFW
        configure_iptables_with_ufw()

        # Display blacklisted IPs
        display_blacklisted_ips(config.get("Paths", "BLACKLIST_FILE"))

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def handle_termination(signal, frame):
    logging.info("Termination signal received. Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_termination)
    while True:
        try:
            main()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        logging.info(f"Waiting for {WAIT_TIME_MINUTES} minutes before the next run...")
        time.sleep(WAIT_TIME_MINUTES * 60)  # Convert to seconds
        time.sleep(WAIT_TIME_MINUTES * 60)  # Convert to seconds
        time.sleep(WAIT_TIME_MINUTES * 10)  # Convert to seconds



import subprocess

def burn_ventoy(image_path, target_device):
    try:
        # Run the dd command to burn the Ventoy image to the target device
        subprocess.run(['dd', 'if=' + image_path, 'of=' + target_device, 'bs=4M', 'status=progress'], check=True)
        print("Ventoy burned successfully!")
    except subprocess.CalledProcessError as e:
        print("Error burning Ventoy:", e)

# Specify the path to the Ventoy image file and the target device
image_path = '/path/to/ventoy.img'
target_device = '/dev/sdX'  # Replace 'sdX' with the appropriate device identifier

# Call the burn_ventoy function with the image path and target device
burn_ventoy(image_path, target_device)
 