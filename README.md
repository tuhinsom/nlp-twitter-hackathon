# nlp-twitter-hackathon
Participation Techgig Hackathon

1. The following URIs are to considered as the entry point:

a. http://localhost:5000/             : Homepage

b. http://localhost:5000/tweetsearch  : Automatic feed update page. Page pulls twitter home_timeline feeds into MongoDB and shows in the UI.

c. http://localhost:5000/tweetanalyze : This page is the basic analysis page, this is to be extended with required functionality. Pulls the Historical Feeds from the MongoDB and gets it ready for analysis. Search Historic feeds by date range and popuate the data in Pandas dataframe and click oneach row to open Modal for further analysis.

MongoDB is to be setup with DB name "tweetnlp2018db" and collection "tweet_collection"

The python app in built on top of Flask resful API package. Hence the server can be started by the command 
python tweeterpy_txt_analys/flaskserver.py
required packages are pandas,nltk, and matplotlib (not yet used)

Can be accessed via browserby the URIs mentioned above.

The data structure of the historical feeds that can be used for analysis is: 


[  
   {  
      "text":"Submit your best #data story about something that happened in 2017, using #PowerBI &amp; win a Surface Pro!\u2026 https://t.co/sUCfcwQEz",
      "created_at":"2018-01-03T20:15:11",
      "profile_image_url":"http://pbs.twimg.com/profile_images/821834838659346432/m1mSM9Q_normal.jpg",
      "text_tokens":[  
         "Submit",
         "best",
         "#data",
         "story",
         "something",
         "happened",
         "2017,",
         "using",
         "#PowerBI",
         "amp",
         "win",
         "Surface",
         "Pro",
         "\u2026",
         "https://t.co/sUCfcwQEz"
      ],
      "from_user":"Power BI",
      "favorite_count":0,
      "text_counts":{  
         "most_common":[  
            [  
               "story",
               1
            ],
            [  
               "amp",
               1
            ],
            [  
               "\u2026",
               1
            ],
            [  
               "win",
               1
            ],
            [  
               "Pro",
               1
            ]
         ],
         "terms_mentions":[  
               // the Tweeter mentions reside here
         ],
         "terms_hash":[  
               // the Tweeter Hashcode reside here
            "#data",
            "#PowerBI"
         ]
      }
   },
...
]



