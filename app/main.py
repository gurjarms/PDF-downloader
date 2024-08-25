import sys, io 
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

import os,socket, shutil, eel,  requests
from googlesearch import search
from urllib.parse import urlparse
from func_timeout import func_timeout, FunctionTimedOut
from threading import Thread, Lock
from time import sleep

# Redirect stdout and stderr to a log file
log_file = open('log.txt', 'w')
sys.stdout = log_file
sys.stderr = log_file

# Handle the base path for resources like HTML files
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle (frozen)
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

eel.init(os.path.join(base_path, 'web'))

MAIN_RESPONSE = [1, [], [], []]
lock = Lock()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def savePdf(link, location, downloaded, notDownloaded, pdf_name):
    file_path = os.path.join(location, pdf_name)
    try:
        response = requests.get(link, stream=True, timeout=30, headers=headers)  # request for pdf page
        if response.status_code == 200:
            content_length = response.headers.get('Content-Length')
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            # Ensure the downloaded file size matches the content length
            if os.path.getsize(file_path) != int(content_length):x=5+"fng"		
            with lock:
                status = f'Downloaded pdf:- {link}'
                eel.update_status(status)
                downloaded.append(link)
            return
        else:
            if os.path.exists(file_path):
                os.remove(file_path)
            else:...
            with lock:
                notDownloaded.append(link)
            return

    except Exception as e:
        with lock:
            notDownloaded.append(link)
            status = f'NOT downloaded: {link}.'
            eel.update_status(status)
        # Delete partially downloaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        else:...

def goto_savePdf(link, location, downloaded, notDownloaded, pdf_name):
    try:
        func_timeout(60, savePdf, args=[link, location, downloaded, notDownloaded, pdf_name])
    except FunctionTimedOut:
        with lock:
            notDownloaded.append(link)
            status = f'NOT downloaded (timeout): {link}'
            eel.update_status(status)
    except Exception as e:
        with lock:
            notDownloaded.append(link)
            status = f'NOT downloaded (timeout or other error): {link}'
            eel.update_status(status)

def scrapping(topic_name, location):
    status = f'Finding for \"{topic_name}\"'
    eel.update_status(status)

    status = f'Initializing....'
    eel.update_status(status)

    try:
        topic_location = os.path.join(location, topic_name)
        os.makedirs(topic_location, exist_ok=True)
    except Exception as e:...

    status = f"Searching for PDF's...."
    eel.update_status(status)

    # Simulate Google search
    links_list = []
    try:
        for j in search(topic_name, tld="co.in", num=200, stop=200, pause=3, user_agent=headers['User-Agent']):
            is_pdf = j[-4:]
            if is_pdf == ".pdf":
                links_list.append(j)
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 429:
            return [0, 'Return with Error code- 429 "Too many requests please try again after 1 hour" ']

    # Remove duplicates
    links_list = set(links_list)

    downloaded = []
    notDownloaded = []
    threads = []

    status = f"Fetching PDF links...."
    eel.update_status(status)

    for link in links_list:
        parsed_url = urlparse(link)
        pdf_name = parsed_url.path.split('/')[-1]
        try:
            pdf_name = pdf_name.replace(':', "_")
        except:
            pass
        try:
            t = Thread(target=goto_savePdf, args=(link, topic_location, downloaded, notDownloaded,pdf_name))
            t.start()
            threads.append(t)
        except Exception as e:...
    for t in threads:
        t.join()

    response = [2, list(links_list), list(downloaded), list(notDownloaded)]
    MAIN_RESPONSE[1].extend(links_list)
    MAIN_RESPONSE[2].extend(downloaded)
    MAIN_RESPONSE[3].extend(notDownloaded)
    for pdf in notDownloaded:
            path = f'{location}/{topic_name}/{pdf_name}'
            try:
                if os.path.exists(path):
                        os.remove(path)
            except Exception as e :...
    
    return response

def delete_dirs(location):
    try:
        files = os.listdir(location)
        for item in files:
            path = f'{location}/{item}'
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            else:...
    except OSError as e:...

@eel.expose
def sendData():
    return MAIN_RESPONSE

@eel.expose
def scrape(pdf_names, location):
    location = location.replace('\\', '/')
    pdf_names = pdf_names.replace(':', '_')
    pdf_names = pdf_names.split(',')
    MAIN_RESPONSE[1].clear()
    MAIN_RESPONSE[2].clear()
    MAIN_RESPONSE[3].clear()
    try:
        socket.create_connection(("1.1.1.1", 80))
    except:
            return [0,'Oops! No internet connection. Please check your connection and try again.']
    try:
        delete_dirs(location)
    except OSError as e:
        response = [0, 'path not found']
        return response

    try:
        response = []
        for pdf_name in pdf_names:
            pdf_name = pdf_name.strip()
            if pdf_name[-3:] != "pdf":
                pdf_name = pdf_name + " pdf"
            response = scrapping(pdf_name, location)
        return response
    except Exception as e:
        response = [1, 'Somthing went wrong please try again']
        return response

# Check available port
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def start_eel():
    try:
        port = find_free_port()
        eel.start('main.html', mode='chrome',
                  host='localhost',
                  port=port,        
                  block=True,
                  size=(550, 650),
                  position=(300, 50),
                  disable_cache=True,
                  cmdline_args=['--browser-startup-dialog',
                                '--incognito', '--no-experiments'])
    except Exception as e:
        pass

if __name__ == '__main__':
    start_eel()