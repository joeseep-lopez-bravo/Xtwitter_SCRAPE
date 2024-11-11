# X(Twitter)_FB

## Setup Instructions

Before you begin, make sure to create the database. You can find the necessary SQL commands in the `xtwitter_db.sql` file. Execute this file in your PostgreSQL environment to create the required tables.

### Database Configuration

Once you have created the database, update the connection parameters in the code (`user`, `password`, `port`, and `localhost`) to match your PostgreSQL database settings.

### Running the Script

To execute the scraping code, run the following command:

```bash
python Execute_twitter_scrape.py
````

## Requirements
To Run this scapre code you'll need to install : 
- Python 
- Seleniuum
- PostgreSQL

### Dependencies
Libraries that you will need:

- **selenium**: 
- **fake_useragent**: 
- **psycopg2**: 
- **pyautogui**:
- **logging**: 
- **configparser**: 
```bash
pip install selenium

pip install fake-useragent

pip install psycopg2

pip install pyautogui

pip install logging 
```
## Appendix

### Links to Scrape

To specify the toopics you want to scrape, enter them in the following files:

- `Topics.conf`


In each of these files, update the `self."type_page"_links` list with the URLs you wish to scrape:

```python
self.perfil_links = [
            "https://x.com/realDonaldTrump",
           # 'https://x.com/WH40kbestof',
           # 'https://x.com/EmergenciasEc',
        ]
````
### Adding Profiles

To add profile credentials, save them in the `credentials.conf` file using the following format:

```conf
emailkey1=blrdmanrique@gmail.com
usernamekey1=AbelardoMa65534
passwordkey1=Abelardo_X_23_01_00

emailkey2=something1
usernamekey2=something2
passwordkey2=something3

emailkey3=some_example@gmail.com
usernamekey3= usernamekey_example
passwordkey3=password_example

emailkey4=some_example1@gmail.com
usernamekey4= usernamekey1_example
passwordkey4=password2_example
````
### Operating Images & Videos
Both `image_procces.py` & `video_procces.py` files transform the links of the PostgreDB in files jpg & mp4 to future use with deep learning
or any other purpose that you have in mind.Those files are saved in their respective folders ,each file inside them has a name obtanied from its id & id publiacion to iddentify them in the db.
 
### Run separately

```bash
py profile_X.py

py process_image.py

py process_video.py
````