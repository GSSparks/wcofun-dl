#! /bin/python

import sys
import os
import argparse
import requests
from urllib.parse import urlparse
from urllib.parse import unquote
from clint.textui import progress
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

def downloadFile(name, videoFile):
    parsed_url = urlparse(videoFile) # Host changes. Set host depending on videoFile value.
    host = parsed_url.hostname
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': host,  # set this as needed
        'Range': 'bytes=0-',
        'Referer': 'https://embed.watchanimesub.net/',
        'Sec-Fetch-Dest': 'video',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': user_agent,  # get this from the findMedia function
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    max_retries=5
    for attempt in range(max_retries):
        try:
            response = requests.get(videoFile, headers=headers, stream=True)

            if response.status_code == 206:
                with open(name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Successfully downloaded {name}", flush=True)
                return  # Exit the function if successful
            else:
                print(f"Failed to download file: Status code {response.status_code}", flush=True)

        except requests.RequestException as e:
            print(f"Error occurred: {e}", flush=True)

        # Wait before retrying
        if attempt < max_retries - 1:
            print(f"Retrying in 5 seconds... (Attempt {attempt + 1})", flush=True)
            time.sleep(5)

    print(f"Failed to download file {name} after {max_retries} attempts.", flush=True)

def fileExists(name, videoFile):
    if os.path.isfile(name):
        print(f"{name} already exists. Skipping download.", flush=True)
    else:
        downloadFile(name, videoFile)

def findMedia(url, counter):
    # get name of movie
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(options=fireFoxOptions)

    global user_agent  # get the user_gent to use in headers
    user_agent = driver.execute_script("return navigator.userAgent;")

    driver.get(url)
    page = driver.page_source
    getpage = BeautifulSoup(page, 'html.parser')
    items = getpage.find('div', {'class', 'video-title'})
    title = items.text.strip()
    clean_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', title)
    name = clean_title.lower().replace(" ", "_") + '.mp4'.strip()
    print('Video name: ' + name, flush=True)

    # search for mp4 in iframe document. The iframe id will change. Find and get the id using BeautifulSoup
    iframe = getpage.find('iframe')
    if iframe:
        iframe_id = iframe.get('id') if iframe else None
        driver.switch_to.frame(iframe_id)
        time.sleep(4)
        page = driver.page_source
        getpage = BeautifulSoup(page, 'html.parser')

        items = getpage.find('video', {'class', 'vjs-tech'})
        if items and 'src' in items.attrs:
            videoFile = items['src']
            if yesDownload is not False:
                fileExists(name, videoFile)
            else:
                print(videoFile, flush=True)
        elif counter >= 4:
            driver.quit()
            print("Didn't find any media files. :'( ", flush=True)
            return
        else:
            counter = counter+1
            print('Attempting try #' + str(counter), flush=True)
            findMedia(url, counter)
    else:
        print("No iframe found on this page.", flush=True)
        driver.quit()
        return

    driver.quit()

def findPage(url, counter):
   # get name of movie
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(options=fireFoxOptions)
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # Find all episode links
    episode_links = soup.select('div#sidebar_right3 .cat-eps a')
    if not episode_links:
        findMedia(url, counter)

    # Extract URLs
    links = [a['href'] for a in episode_links]

    if yesDownload is not False:
        # Process each link
        counter = 1
        for link in links:
            print(f"Processing link: {link}", flush=True)
            findMedia(link, counter)
            counter += 1
    else:
        for link in links:
            writeFile(link)

    driver.quit()

def getArguments():
    global url, batchFile, yesDownload

    parser  =   argparse.ArgumentParser(description='Downloads media from wcofun.net')

    parser.add_argument('-d',
                        action='store_true',
                        dest='yesDownload',
                        default=False,
                        help='Downloads videos',
                        required=False
                        )

    parser.add_argument('--batch',
                        action='store_true',
                        dest='batchFile',
                        default=False,
                        help='Run using a batch of urls.',
                        required=False
                        )

    parser.add_argument('URL',
                        type=str,
                        help='<Required> url link'
                        )

    results     =   parser.parse_args()
    url         =   results.URL.strip().rstrip('/')
    batchFile   =   results.batchFile
    yesDownload =   results.yesDownload
    return

def main():
    counter=1
    getArguments()
    if batchFile is True:
        with open(url, "r") as f:
            for content in f.readlines():
                print('Finding files for ' + content.strip(), flush=True)
                findMedia(content.strip(), counter)
            print('Done!', flush=True)
            exit()
    else:
        findPage(url, counter)
        print('Done!', flush=True)
        exit()

def writeFile(videoFile):
    print('Writing ' + videoFile, flush=True)
    f = open('wcofun-batch.txt', "a")
    f.write(videoFile)
    f.write("\n")
    f.close()

if __name__ == "__main__":
    main()
