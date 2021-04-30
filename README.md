# PttKeywordCrawler
Web crawler for www.ptt.cc, the largest BBS online forum in Taiwan. Though there are plenty articles and discussion in various areas, because of the limitation of BBS, it lacks in easy way to retrieve information. PttKeywordCrawler is desigened to overcome these obstacles, and provide simple and user friendly funtionalities for Ptt users to obtain interested information. PttKeywordCrawler supports two types of crawling, PttCrawler and PttKeyword Monitor.

## PttCrawler
PttCrawler serves as a common crawler that craws over a specified board on Ptt. User needs to specify what keyword to look for, and how many totle articles to craw.

For example, users can craw for `board: movie | keyword: joker | numbers of total article: 1000` to retrieve articles with `joker` in title in the most recent `1,000` posts on board `movie`.

### How to Use
Simply run PttCrawler.py on terminal / cmd, the script will prompt for necessary input.
When crawling is done, users are asked if they want to export the result to .csv file, or display the result on the screen.

### User Specified Parameters
  - Broad: which board to craw on Ptt
  - Keyword: what keyword to look for in title
  - Numbers of Totle Articles: numbers of articles to craw

## PttKeywordMonitor
PttKeywordMonitor is designed to solve the lacking function of `subscribe keyword` for the Ptt forum. Ptt users often want to follow certain topic on Ptt, but naturally, it does not support such functionailty. Useres need to preiodically login and connect to Ptt on computer/phone app, or check the webpage to make sure they don't miss, or be late to any article they are interested in. PttKeyworkMonitor continuously runs and craws the latest information, and send the interested articles to users via email.

For example, users can monitor for `board: gamesale | keyword: switch | interval | 1800` to receive updates of articles with `switch` in titile on board `gamesale` every `1,800 seconds (half hour)`. Therefore, useres can get notified for someone selling a Nintendo Switch, and check it before someone buys it!

### How to Use
Simply run PttKeywordMonitor.py on terminal / cmd, the script will prompt for necessary input.
PttKeywordMonitor will continuously run and craw for the latest information every `interval` second, and send an email to the user if there's a new interested article.
The scripts uses smtp server for gmail, if wnats to use a different server, please modify in `CrawlerFunctions.py`. Futhermore, the script default that the reciever email address is the same to the sender's email addres, meaning. If needs to send to a different receiver, please adjust in `CrawlerFunctions.py`
Use `control-C` to terminate the process.

### User Specified Parameters
  Broad: which board to craw on Ptt
  Keyword: what keyword to look for in title
  Interval: how often to check for new articles in second
  Sender Email Address: gmail address (myAccount@gmail.com)
  Sender Email Password: password for the sender gmail account
  

