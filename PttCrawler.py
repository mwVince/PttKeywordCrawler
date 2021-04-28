# Runable scripts to execute the PttCralwer
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
    num_articles = input('How many articles to craw: ')
    if num_articles.isdigit() == False:
        print('Please enter a positive integer\n')
        continue
    else:
        num_articles = int(num_articles)
        break

result = board_reader(board, keyword, num_articles)
print('Finished crawing: ' + str(result[1]) + ' articles are crawed and ' + str(len(result[0])) + ' contain the keyword ' + keyword)

# Prompts for exporting to csv or display on screen
if input('Export to csv? (Y: Export / N: Display on Screen): ').lower() == 'y':
    export_csv(board, keyword, result[0])
else:
    display_result(board, keyword, result[0])

quit()