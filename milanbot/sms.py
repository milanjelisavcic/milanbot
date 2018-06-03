# 06xxxxxxxx @ tmomail.net

import yagmail

yag = yagmail.SMTP(user='milan.jelisavcic@gmail.com',
                   oauth2_file='~/projects/milanbot/oauth2_creds.json')
yag.send('0624234759@tmomail.net',
         subject="hello",
         contents='Hello')\
    # ,
    #      attachments="/Users/milanjelisavcic/projects/milanbot/test.csv")
