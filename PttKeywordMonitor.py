# Script which runs in back ground and send email if finds a new article on declared board with intended keyword
from CrawlerFunctions import *

# Prompts for crawing demands
while True:
    board = str(input('Which board to look up: '))
    test = board_name_test(board)
    if test[0] == False:
        print('In-existing board name, please check\n')
        continue
    board = test[1]
    break
keyword = str(input('What keyword to look up (case insensitive!): '))
while True:
    interval = input('Frequency to update in seconds: ')
    if interval.isdigit() == False:
        print('Please enter a positive integer\n')
        continue
    else:
        interval = int(interval)
        break

latest_article = latest_article_on_board(board)
timer_crawler(board, keyword, interval, latest_article)