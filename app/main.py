import sys, io
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

import eel
import os
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from time import sleep
from func_timeout import func_timeout
from random import randrange
from threading import Thread, Lock
import shutil

eel.init('web')  # The directory containing your HTML files

MAIN_RESPONSE = [1, [], [], []]
lock = Lock()

@eel.expose
def scrape(pdf_names, location):
    location = location.replace('\\', '/')
    pdf_names = pdf_names.replace(':', '_')
    pdf_names = pdf_names.split(',')
    MAIN_RESPONSE[1].clear()
    MAIN_RESPONSE[2].clear()
    MAIN_RESPONSE[3].clear()

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
        print(e)
        response = [1, 'cant download pdf']
        return response


@eel.expose
def sendData():
    return MAIN_RESPONSE

def savePdf(link, location, downloaded, notDownloaded):
    parsed_url = urlparse(link)
    pdf_name = parsed_url.path.split('/')[-1]
    try:
        pdf_name = pdf_name.replace(':', "_")
    except:...
    file_path = os.path.join(location, pdf_name)
    try:
        response = requests.get(link, stream=True, timeout=30)  # request for pdf page
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

def goto_savePdf(link, location, downloaded, notDownloaded):
    try:
        x = func_timeout(60, savePdf, [link, location, downloaded, notDownloaded])  # 60 seconds timeout for savePdf() function
        print(x)
        return True
    except Exception as e:...

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

    except OSError as e:
        os.makedirs(location, exist_ok=True)
def scrapping(topic_name, location):
    status = f'Finding for \"{topic_name}\"'
    eel.update_status(status)

    status = f'Initializing....'
    eel.update_status(status)

    try:
        topic_location = os.path.join(location, topic_name)
        os.makedirs(topic_location, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory {topic_location}: {e}")

    # Simulate Google search
    search_url = f"https://www.google.com/search?q={topic_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = bs(response.text, 'html.parser')
    
    status = f"Searching for PDF's...."
    eel.update_status(status)
    # find all pages links
    next_pages = soup.select('a[aria-label^="Page"]')

    url =f"https://www.google.com{next_pages[0]['href']}"
    next_pages_links = []
    for num in range(1, 20):
        if num != 1:
            old = f'start={num * 10 - 10}'
        else:
            old = f'start={num * 10}'
        new = f'start={num * 10}'
        url = url.replace(old, new)
        next_pages_links.append(url)

    status = f"Fetching PDF links...."
    eel.update_status(status)

    links_list = []
    threads = []

    def extract_pdf_links(page_url):
        page_response = requests.get(page_url, headers=headers)
        page_soup = bs(page_response.text, 'html.parser')
        pdf_links = page_soup.select('a[href$=".pdf"]')
        with lock:
            for link in pdf_links:
                href = link['href']
                links_list.append(href)

    for page_url in next_pages_links:
        thread = Thread(target=extract_pdf_links, args=(page_url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Remove duplicates
    links_list = set(links_list)

    downloaded = []
    notDownloaded = []
    threads = []

    for link in links_list:
        try:
            t = Thread(target=goto_savePdf, args=(link, topic_location, downloaded, notDownloaded))
            t.start()
            threads.append(t)
        except Exception as e:
            print(f"Error starting thread for {link}: {e}")
    for t in threads:
        t.join()

    response = [2, list(links_list), list(downloaded), list(notDownloaded)]
    MAIN_RESPONSE[1].extend(links_list)
    MAIN_RESPONSE[2].extend(downloaded)
    MAIN_RESPONSE[3].extend(notDownloaded)
    return response


def start_eel():
    try:
        eel.start('main.html', mode='chrome',
                  host='localhost',
                  port=27000,
                  block=True,
                  size=(500, 480),
                  position=(300, 50),
                  disable_cache=True,
                  cmdline_args=['--browser-startup-dialog',
                                '--incognito', '--no-experiments'])
    except Exception as e:
        print(f"Error starting Eel: {e}")

if __name__ == '__main__':
    start_eel()



# for page_url in next_pages_links:
#         try:
#             t = Thread(target=extract_pdf_links, args=(page_url))
#             t.start()
#             threads.append(t)
#         except Exception as e:
#             print(e)
#     for t in threads:
#         t.join()