import yagmail

yag = yagmail.SMTP(user='-----@gmail.com',
                   oauth2_file='oauth2_creds.json')
yag.send('-----@gmail.com',
         subject="hello",
         contents='Hello',
         attachments="attachement.file")