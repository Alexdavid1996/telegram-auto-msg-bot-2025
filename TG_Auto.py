from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from colorama import init, Fore, Style
import os
import time

init(autoreset=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    print(Fore.CYAN + r"""
 /$$$$$$$  /$$   /$$      /$$$$$$                       /$$$$$$                                     /$$
| $$__  $$|__/  | $$     /$$__  $$                     /$$__  $$                                   | $$
| $$  \ $$ /$$ /$$$$$$  | $$  \__/  /$$$$$$  /$$$$$$$ | $$  \__//$$   /$$  /$$$$$$$  /$$$$$$   /$$$$$$$
| $$$$$$$ | $$|_  $$_/  | $$       /$$__  $$| $$__  $$| $$$$   | $$  | $$ /$$_____/ /$$__  $$ /$$__  $$
| $$__  $$| $$  | $$    | $$      | $$  \ $$| $$  \ $$| $$_/   | $$  | $$|  $$$$$$ | $$$$$$$$| $$  | $$
| $$  \ $$| $$  | $$ /$$| $$    $$| $$  | $$| $$  | $$| $$     | $$  | $$ \____  $$| $$_____/| $$  | $$
| $$$$$$$/| $$  |  $$$$/|  $$$$$$/|  $$$$$$/| $$  | $$| $$     |  $$$$$$/ /$$$$$$$/|  $$$$$$$|  $$$$$$$
|_______/ |__/   \___/   \______/  \______/ |__/  |__/|__/      \______/ |_______/  \_______/ \_______/                                                                                                                                                                                                                                                                                              
""")



    print(Fore.GREEN + "If I’ve helped in any way, subscribe! 👉 https://www.youtube.com/@BitConfused Pretty please? T.T")
    print(Style.RESET_ALL)
    print(Fore.GREEN + "TG Auto MsgBot V1.0")
    print("")

def check_and_create_files():
    if not os.path.exists('Credentials.txt'):
        open('Credentials.txt', 'w').close()
        

    if not os.path.exists('Groups.txt'):
        open('Groups.txt', 'w').close()
        

def save_credentials(api_id, api_hash, phone):
    with open('Credentials.txt', 'w') as file:
        file.write(f'{api_id}\n{api_hash}\n{phone}')
    print(Fore.GREEN + 'Credentials saved successfully.')


def load_credentials():
    if not os.path.exists('Credentials.txt'):
        return None
    with open('Credentials.txt', 'r') as file:
        credentials = file.readlines()
    if len(credentials) >= 3:
        return credentials[0].strip(), credentials[1].strip(), credentials[2].strip()
    else:
        return None


def load_group_urls():
    if not os.path.exists('Groups.txt'):
        return []
    with open('Groups.txt', 'r') as file:
        group_urls = [line.strip() for line in file]
    return group_urls


def send_messages_to_groups(client, group_urls, delay):
    try:
        saved_messages = client(GetHistoryRequest(
            peer='me',
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=1,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not saved_messages.messages:
            print(Fore.RED + 'No messages found in Saved Messages.')
            return
        latest_message = saved_messages.messages[0]

        for group_url in group_urls:
            try:
              
                client.forward_messages(group_url, latest_message.id, from_peer='me')

                print(Fore.GREEN + f'Forwarded message to {group_url}')
                time.sleep(delay)
            except Exception as e:
                print(Fore.RED + f'Failed to forward message to {group_url}: {e}')
    except Exception as e:
        print(Fore.RED + f'Error getting messages: {e}')


def main():
    clear_screen()
    display_banner()
    
    check_and_create_files()
    
    credentials = load_credentials()
    
    if credentials:
        reuse = input(Fore.YELLOW + 'Reuse the same account as last time? (yes/no): ')
        if reuse.lower() == 'yes':
            api_id, api_hash, phone = credentials
        else:
            api_id = input(Fore.YELLOW + 'Enter API ID: ')
            api_hash = input(Fore.YELLOW + 'Enter API HASH: ')
            phone = input(Fore.YELLOW + 'Enter phone number: ')
            save_credentials(api_id, api_hash, phone)
    else:
        api_id = input(Fore.YELLOW + 'Enter API ID: ')
        api_hash = input(Fore.YELLOW + 'Enter API HASH: ')
        phone = input(Fore.YELLOW + 'Enter phone number: ')
        save_credentials(api_id, api_hash, phone)

    session_file = f'{phone}.session'
    client = TelegramClient(session_file, api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        code = input(Fore.RED + 'Please enter the code you received: ')
        client.sign_in(phone=phone, code=code)
    else:
        print(Fore.GREEN + 'Already authorized.')

    confirm = input(Fore.YELLOW + 'Have you already added your URLs to Groups.txt? (yes/no): ')
    if confirm.lower() != 'yes':
        print(Fore.RED + 'Please add your URLs to Groups.txt and run the script again.')
        return

    group_urls = load_group_urls()
    if not group_urls:
        print(Fore.RED + 'No group URLs found in Groups.txt.')
        return
    
    delay = int(input(Fore.RED + 'Enter the delay between successful messages in seconds: '))

    while True:
        clear_screen()
        display_banner()
        send_messages_to_groups(client, group_urls, delay)
        print(Fore.GREEN + 'All messages have been sent successfully. Restarting...')
        time.sleep(10)

if __name__ == '__main__':
    main()
