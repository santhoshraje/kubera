 <p align="center"><img src="https://github.com/santhoshraje/kubera/blob/master/logo.png"></p>
<h4 align="center">A smart personal assistant for retail stock traders</h4>

<p align="center">
<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
<img src="https://img.shields.io/github/v/release/santhoshraje/kubera" />
<img src="https://img.shields.io/github/release-date/santhoshraje/kubera" />
<img src="https://img.shields.io/badge/telegram-%40kubera__bot-blue" />
<img src="https://img.shields.io/github/last-commit/santhoshraje/kubera/master" />
<img src="https://img.shields.io/badge/license-MIT-orange" />
</p>

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#Deployment">Deployment</a> •
  <a href="#Libraries">Libraries</a> •
  <a href="#License">License</a> •
  <a href="#special-thanks">Special Thanks</a> 
</p>
<p align="center"><img src="https://github.com/santhoshraje/kubera/blob/master/screenshot.png"></p>

 ## Overview

Features: 
 - Upcoming dividends. Display all upcoming dividend payouts 
 - Dividend summary. Summary of dividends paid by a company over the last 5 years
 - Dividend estimation. Estimate total dividends earned this year using data from last year
 - Post market analysis. Receive an automatically generated report of the top losers, gainers and highest volumes to the user after market close everyday.

Data sources:
 - dividends.sg
 - Yahoo! Finance

Supported markets:
 - Singapore

Supported platforms:
 - Telegram (bot)
  
 ## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development, testing and deployment purposes.

### Prerequisites
```
pip install -r requirements.txt
```

### Usage

start the bot:

```
python main.py
```
bot will run until you stop it with CTRL + C / CMD + C

## Deployment

You may host the bot on any server that has python 3 installed

## Libraries

 - pandas
 - python-telegram-bot
 - sqlite3
 - pandas-datareader
 - millify
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Special Thanks

 - <a href ="https://github.com/mmdaz/mvc_model_bot_developing">mmdaz</a> - Basic structure for MVC bot architecture
 - <a href ="https://github.com/xlanor/SIM-UoW-Timetable-bot">xlanor</a> - Great example of a telegram bot with MVC architecture
 - <a href ="https://www.freelogodesign.org/">vecteezy.com</a> - Cool logo



