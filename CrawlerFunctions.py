# Class holds needing functions to run the PttCrawler.py
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
    url = domain + "/bbs/" + board
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
    print(board + ": " + keyword)
    for article in result_list:
        print(article['title'], article['link'], article['date'])
    print()