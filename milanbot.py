#!/usr/local/bin/python3
#-*- encoding: Utf-8 -*-

import yagmail

import pywikibot as pwb
import milanbot.logger as log

logger = log.terminal_logger()
file_logger = log.file_logger("test.csv")

def main():
    """
    Main function
    :return:
    """
    logger.info("Starting the bot...")
    repo = pwb.Site('wikidata', 'wikidata')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down the bot...")
        yag = yagmail.SMTP(user='-----@gmail.com',
                           oauth2_file='oauth2_creds.json')
        yag.send('-----@gmail.com',
                 subject="hello",
                 contents='Hello')
