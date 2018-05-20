# milanbot
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0edc77e69ce44c198c8bd93e5c1d9e66)](https://www.codacy.com/app/milan.jelisavcic/milanbot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=milanjelisavcic/milanbot&amp;utm_campaign=Badge_Grade)

This suite of bots interact with Wikidata and Wikipedia using the Pywikibot library.

## Setup
```bash
git clone https://github.com/milanjelisavcic/milanbot.git
cd milanbot
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Log-in to `meta.wikimedia.org` with the account that will use `MilanBot` and 
visit [Special:OAuthConsumerRegistration/propose](https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration/propose)
to get OAuth tocken.
Create `user-config.py` and add the following lines:
```python
family = 'wikipedia'  # or other Wikimedia project
mylang = 'en'  # or 'wikidata' or other language code

usernames['wikipedia']['en'] = \
    usernames['wikidata']['wikidata'] = \
    usernames['commons']['commons'] = \
    ...
        u'ExampleBot'

authenticate['*.wikipedia.org'] = \
    authenticate['*.wikidata.org'] = \
    authenticate['*.commons.org'] = \
    ...
    ('<consumer_key>',
     '<consumer_secret>',
     '<access_key>',
     '<access_secret>')
```
After the users credentials are properly added, the bot can access and edit 
the Wikimedia projects.

## Getting Started
TBA