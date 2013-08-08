# STYLESHEET defines the name of the css sheet to use
STYLESHEET = 'twitnews'

# How many hours of twitter links to consider in calculating top stores
HOURS = 12

# SEARCH determines what Twitter search to use
SEARCH = 'sap OR oracle OR ibm OR enterprise -"star trek" OR cisco OR qualcomm OR Hewlett OR salesforce OR businessobjects OR jive OR yammer'

# TITLE determines what the title of the site should be
TITLE = 'Enterprise Tech News'

# NUMHEADLINES determines how many headlines to display
# !!! If changing, also change LIMIT parameter in getStories !!!
NUMHEADLINES = 20

# WORDSTOINCLUDE defines a list of words - case-sensitive! - one of which must at least bes present in title
# If empty, not filtering will occur
WORDSTOINCLUDE = ()

WORDSTOEXCLUDE = ('sap', 'Sap', 'Amazon.com','Amazon Kindle:','Amazon.co.uk','Temporarily unavailable.',
				  'Star Trek','Oracle of Delphi','startrek','Instagram','Franzaliscious','social enterprise',
				  'Careers Center','Job Details','job in','Jobs on CareerBuilder.com','Eluta.ca','TheATLJukebox',
				  'Jobsite Job Centre','Feedzilla','Enterprise Financial','Bullhorn Reach','Social enterprise',
				  'Social Enterprise')

# SEARCHCOUNT defines how many search results to fetch from Twitter. Default is 15
SEARCHCOUNT = 100

# LASTFETCHEDTIMEOUT defines how long the last_fetched_status_id stays valid in seconds
LASTFETCHEDTIMEOUT = 30 * 60

# MAXNUMOFURLS defines how many response urls to send to the queue at once
MAXNUMOFURLS = 250

# SIMILARITY defines how similar between 0 and 1 headlines should be for clustering
SIMILARITY = .55