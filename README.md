# Telegram multi channel surveillance Program

[Previous Upwork Job] as Developer.
"Telegram_multi_channel_surveillance" is a data extraction program written in python, designed for consumer usage, with the purpose of monitoring daily activity &amp; fetch summary-data for up to 14.000+ groups &amp; channels, which is then stored in a PostgreSQL Database. 
The program uses telethon along with a combination of multiprocessing and threading to efficiantly extract up to +14K groups and channels, as quickly as possible, considering the limitations. You'll can read more about the limitiations in "Challanges"



## Project Overview
- Job completed:  April 2022
- Job type:				Development 
- Job categogy:		Bot Development, Data Extraction, Data Mining 
- Language:				Python
- Style:          Functional
- Key practices:  Telethon, Multi-processing, multi-threading, PostgreSQL, 


## Project description
The goal for the project was to make a data Extraction tool much like a previous project I have worked on, except for two things: 
1. Type of data, This time the data should be superficial data about the channels and groups themselves, and the activity on them, and no data on the users. 
2. Scale, The scale of the number of channels being collected at the same time was immensely bigger than I've previously worked with and was definetly a challange.
3. Data storage, In previous work I have been storing data as csv files in a folder, and this project gave me a reason to learn about Databases. 

In this project I were to create a bot that could scrape Telegram fra a list of 14000+ channels and groups, then sort them out by "groups" and "channels", thereafter I were to grab the overview information about the channel, (name, creation date, number of mebers, etc), I would then have to look a little deeper into the chat and measure the amount of daily activity (number of messages, online members any changes to from yesterday). All of this had to be done within a 1-2 hour timeframe. 
Lastly all of that data were made into a dataframe, which was then converted into a JSON format, then stored onto the Postgres Database, then it would have a 24-hour break untill the next session.
Any bad inputs would be put onto a blacklist and removed from the original input list. 


## Challanges 
### PostgreSQL
One of the challanges was of course to learn about using databases, but the database apect of it wasn't very complicated and so even if i stumbled through the syntax a bit, the task was very doable. 

### Scale & Telegram Security. 
This was by far the greatest challenge. 
Telegram has a security system based on time and amount of data streams, and there is not a lot of information about it.
In order to differentiate between "bots" and "humans" they worked with the assumption that a human was only capable on browsing the app "so much" within a certain time period, and if they Account overstepped those limitations then they knew the account was not a human.
Basically; A bot could only scrape X-amount of data for only a Y-length of time, before a flooding alarm was triggered and the account was suspended for 24hours, and since there isn't any official information about it available you would have to guess those limitations yourself, which yes, it made testing a very slow & frustrating process. But I figured out an acceptable amount was extracting 50 channels followed by a 15 minute break, while also having a 0.5 second break in-between each channel scraped.

However, the second level to that challenge was the fact that I only had 1-2 hours to complete the whole data extraction, which doesn't add up.
So I have to solve this issue by two steps: 
1. Using only one account was out of the question, especially in addition to the second part of the solution. So I had my client provide me with 40 accounts, were each of those accounts were to scrape 350 channels each, which is way more achievable. -> 350/50 gives me 7 rounds of scraping, 7 x 15 minutes gives me a total of 1 hour and 45 minutes of breaks and 15 minutes wiggle room for the amount of time it took to do the extraction itself.
2. The second part of the solution was to make all of those 40 accounts work asynchronously, which i achieved by using a combination of multiprocessing and multithreading. 

The main list of 14k channels was divided into 40 chunks (350 each), which was then divided into 7 rounds (50 each).
I used multiprocessing to put each account to work, after each 15min break all of the workers would scrape 50 channels using multithreading in order to scrape them as fast as possible.



### The dataoutput 
My client already had a database and I had to take that into account when I made the datastructure, so I have my client two chioces for data-output:

Option 1 - indexed by the Timestamp;
![image](https://user-images.githubusercontent.com/97392841/174439913-7c98595d-2e11-478c-96cc-d049b0118347.png)

Option 2 - indexed by Channel ID;
![image](https://user-images.githubusercontent.com/97392841/174439923-25b6a875-08da-45cc-8a77-6968fa412ebd.png)

The client chose to go proceed with Option 1, and here is how it looked like inside the database;
![Postgres Data Storage](https://user-images.githubusercontent.com/97392841/174440010-5feec8d1-ea08-469c-a38a-ca89ab9a2e56.JPG)

Dataframe in CSV format;
![image](https://user-images.githubusercontent.com/97392841/178231294-025e5431-9483-498e-927f-c3674117dd0a.png)

## Self Critique
- In hindsight I would critique myself for how i stored the output, as storing it by the timestamp would have probobly been easier to manage.
- I've also should have done a better job in cleaning up all unnessesary cells in the dataframe, where I found alot of repeating data. 
- I don't think the additional multithreading to the scraping proccess was stricly nessesary and made things a bit more complicated then it needed to be, I don't remember my reasoning behind it, but however I at least wanted to challange myself and see if i could do it. 
