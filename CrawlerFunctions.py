# Class holds needing functions to run the PttCrawler.py and PttKeywordMonitor.py
from re import L
import requests # Allows python to send HTTP Request
from bs4 import BeautifulSoup # Structured crawed information

domain = 'https://www.ptt.cc'

# 0: Return False if incorrect board name
# 1: Returns correct capitalization for the board name
def board_name_test(board):
    session = requests.session()
    session.post('https://www.ptt.cc/ask/over18', data = {'yes': 'yes'})
    response = session.get(domain + '/bbs/' + board)
    if(response.status_code != 200):
        return False, None

    soup = BeautifulSoup(response.text, 'html.parser')
    board_name = soup.find('a', 'board').text.split(' ')[1]
    return True, board_name

# Craws one page of articles
# Returns a list of dictionary {tilte, link, date},
# and a url for next page to craw (previous page).
# If this is the last page, return None for the url
def get_articles(session, url, keyword, num_articles):
    # Creates session to parsists and passes age verification 
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = []
    next_page = None

    # Finds url for next page to craw
    action_bar = soup.find('div', 'action-bar').find('div', 'btn-group-paging')
    for i in action_bar.find_all('a'):
        if '上頁' in i.text:
            # If no previous page, class = ['btn', 'wide', 'disabled']
            # otherwise, ['btn, 'wide']
            if len(i.get('class')) == 2:
                next_page = domain + i.get('href')

    # Iterates through the list of articles, until counter reachs the goal or finishes this page
    # reversed() gives the correct order to read each page from latest to oldest
    global counter
    for i in reversed(soup.find_all('div', 'r-ent')):
        title = i.find('div', 'title').text.strip()
        if '[公告]' in title:
            continue
        
        if keyword.casefold() in title.casefold():
            link = 'https://www.ptt.cc' + i.find('a', href = True)['href'].strip()
            date = i.find('div', 'date').text.strip()
            result.append({'title': title, 'link': link, 'date': date})
            
        counter += 1
        if counter == num_articles:
            break

    return result, next_page

# Repeatedly craws pages until reach article demand or the end of the board
def board_reader(board, keyword, num_articles):
    print('Crawing...')
    session = requests.session()
    session.post('https://www.ptt.cc/ask/over18', data = {'yes': 'yes'})
    url = domain + '/bbs/' + board
    articles = []
    global counter
    counter = 0

    while counter < num_articles:
        craw_result = get_articles(session, url, keyword, num_articles)
        articles += craw_result[0]
        url = craw_result[1]
        
        if url == None:
            print('No more pages to craw')
            break

    return articles, counter

# Exports to csv file with filename broad_keyword.csv
def export_csv(board, keyword, result_list):
    import csv
    import os
    if not os.path.exists('export_file/'):
        os.makedirs('export_file/')

    file_name = board + '_' + keyword + '.csv'
    with open('export_file/' + file_name, mode = 'w', newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        for article in result_list:
            writer.writerow([article['title'], article['link'], article['date']])
    print('Exported\n')

# Displays results on screen
def display_result(board, keyword, result_list):
    print()
    print(board + ': ' + keyword)
    for article in result_list:
        print(article['title'], article['link'], article['date'])
    print()

# Returns the inforamation of the latest article on the board
def latest_article_on_board(board):
    url = domain + '/bbs/' + board
    session = requests.session()
    session.post('https://www.ptt.cc/ask/over18', data = {'yes': 'yes'})
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    latest_article = get_article_list(soup.find('div', 'r-list-container'))[0]
    title = latest_article.find('div', 'title').text.strip()
    link = 'https://www.ptt.cc' + latest_article.find('a', href = True)['href'].strip()
    date = latest_article.find('div', 'date').text.strip()
    
    return {'title': title, 'link': link, 'date': date}

# Repeatedly craws pages until reach the latest article in last stage
def craw_to_latest(board, keyword, latest_article):
    session = requests.session()
    session.post('https://www.ptt.cc/ask/over18', data = {'yes': 'yes'})
    url = domain + '/bbs/' + board

    articles = []
    new_latest_article = latest_article_on_board(board)

    while True:
        craw_result = get_articles_latest(session, url, keyword, latest_article)
        articles += craw_result[0]
        url = craw_result[1]
        if craw_result[2] == False:
            break
        
        if url == None:
            print('No more pages to craw')
            break

    return articles, new_latest_article
    
# Craws one page of articles
# Returns a list of dictionary {tilte, link, date},
# and a url for next page to craw (previous page)
# and boolean if_finish
# If this is the last page, return None for the url
def get_articles_latest(session, url, keyword, latest_article):
    # Creates session to parsists and passes age verification 
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = []
    next_page = None

    # Finds url for next page to craw
    action_bar = soup.find('div', 'action-bar').find('div', 'btn-group-paging')
    for i in action_bar.find_all('a'):
        if '上頁' in i.text:
            # If no previous page, class = ['btn', 'wide', 'disabled']
            # otherwise, ['btn, 'wide']
            if len(i.get('class')) == 2:
                next_page = domain + i.get('href')

    container = soup.find('div', 'r-list-container')
    # Iterates through the list of articles, until counter reachs the last latest article or finishes this page
    # reversed() gives the correct order to read each page from latest to oldest
    for article in get_article_list(container):
        title = article.find('div', 'title').text.strip()
        link = 'https://www.ptt.cc' + article.find('a', href = True)['href'].strip()

        if title == latest_article['title'] and link == latest_article['link']:
            return result, None, True

        if keyword.casefold() in title.casefold():
            date = article.find('div', 'date').text.strip()
            result.append({'title': title, 'link': link, 'date': date})

    return result, next_page, False

# Repeatedly craws every specified seconds to update the latest_article
# Uses Gmail smtp server to send email
def timer_crawler(board, keyword, interval, latest_article):
    import time, smtplib, ssl
    from email.mime.text import MIMEText
    port = 465 # For ssl
    context = ssl.create_default_context()

    # gmail login
    server = smtplib.SMTP_SSL('smtp.gmail.com', port, context = context)
    while True:
        try:
            sender_email_address = input('Enter sender email address: ')
            sender_password = input('Enter password for sender email account: ')
            server.login(sender_email_address, sender_password)
            break
        except:
            print('Incorrect login information, please verify\n')

    # Change if sending to different receiving account
    receiver_email_address = sender_email_address 

    # Repeatedly crawing
    while True:
        print('Crawing...')
        articles, new_latest_article = craw_to_latest(board, keyword, latest_article)
        body_text = ''
        if len(articles) != 0:
            # Preparing message
            for i in articles:
                body_text += (i['title'] + '  ' + i['link'] + '  ' + i['date'] + '\n')
            message = MIMEText(body_text)
            message['subject'] = board + ': ' + keyword
            message['from'] = sender_email_address
            message['to'] = receiver_email_address
            
            # send email
            server.send_message(message)
            print('Keyword found, email sent!')

        # Waits for next crawling round
        latest_article = new_latest_article
        time.sleep(interval)

# Returns list of articles of a page, excluding annoucements
def get_article_list(container):
    all_articles = container.find_all('div', ['r-ent', 'r-list-sep'])
    all_articles.reverse()
    index = 0
    for i in range(len(all_articles)):
        if all_articles[i].get('class')[0] == 'r-list-sep':
            index = i + 1
    return all_articles[index:]