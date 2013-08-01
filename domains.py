# TITLESPLITMAPPING defines how to split titles for a given domain
TITLESPLITMAPPING = {'gigaom.com':('..Tech',0),
					 'wired.com':3,
					 'forbes.com':5,
					 'boss.blogs.nytimes.com':5,
					 'foreignpolicy.com':1,
					 'getconnect-sap.co.uk':3,
					 'zdnet.com':1,
					 'socialenterprise.guardian.co.uk':1,
					 'pandodaily.com':1,
					 'cloudcomputing.sys-con.com':1,
					 'pcworld.com':1,
					 'timesofindia.indiatimes.com':5,
					 'linux.com':1,
					 'informationweek.com':7,
					 'socialenterprise.org.uk':9,
					 'online.wsj.com':5,
					 'storageioblog.com':1,
					 'techcrunch.com':1,
					 'arstechnica.com':1,
					 'venturebeat.com':1,
					 'sbnation':5,
					 'businessinsider.com':5,
					 'bizjournals.com':5,
					 'schaeffersresearch.com':1,
					 'biv.com':3,
					 'opensource.com':1,
					 'sramanamitra.com':1,
					 'open-logix.com':2,
					 'facebook.com':1,
					 'foxnews.com':1,
					 'puppetlabs.com':1,
					 'careercooler':9,
					 'biztech2.in.com':6,
					 'ibm.com':('20\d\d-\d\d-\d\d',1),
					 'siliconrepublic.com':7,
					 'techmeme.com':18,
					 'adage.com':1,
					 'news-leader.com':3,
					 'techrepublic.com':5,
					 'huffingtonpost.com':1,
					 'youtube.com':5,
					 'mtv.com':5,
					 'internetretailer.com':5,
					 'crn.in':7,
					 'marketwatch.com':7,
					 'techlick.com':5,
					 'blogs.wsj.com':7,
					 'thoughtsoncloud.com':1,
					 'devopsangle.com':1,
					 'europa.eu':8,
					 'finance.yahoo.com':5,
					 'sacbee.com':7,
					 'information-age.com':1,
					 'destinationcrm.com':5,
					 'asugnews.com':5,
					 'readwrite.com':('..ReadWrit',0),
					 'theregister.co.uk':('..The.Registe',0),
					 'datacenterknowledge.com':('..Data.Center.Know',0),
					 'itworldcanada.com':7,
					 'cloudera.com':3,
					 'internetevolution.com':7,
					 'reuters.com':1,
					 'allthingsd.com':7,
					 'linuxtoday.com':6,
					 'seekingalpha.com':5,
					 'theblaze.com':1,
					 'blogs.oracle.com':21,
					 'confio.com':1,
					 'abclocal.go.com':1,
					 'humanipo.com':3,
					 'bbc.co.uk':6,
					 'blogs.hbr.org':7,
					 'fastcompany.com':3,
					 'falseeconomy.org.uk':3,
					 'journalism.co.uk':3,
					 'guardian.co.uk':3,
					 'scn.sap.com':1,
					 'citizenibm.com':1,
					 'goingconcern.com':1,
					 'dataxu.com':1
					 }

# SPLITTYPES is a dictionary of common ways to split the title of a page
SPLITTYPES = {1:('|',),
			  2:('|','left'),
			  3:('|','fromleft'),
			  4:('|','fromright'),
			  5:(' - ',),
			  6:(' - ','left'),
			  7:(' - ','fromleft'),
			  8:(' - ','fromright'),
			  9:('/',),
			  10:('/','left'),
			  11:('/','fromleft'),
			  12:('/','fromright'),
			  13:('--',),
			  14:('--','left'),
			  15:('--','fromleft'),
			  16:('--','fromright'),
			  17:(':',),
			  18:(':','left'),
			  19:(':','fromleft'),
			  20:(':','fromright'),
			  21:('(',),
			  22:('(','left'),
			  23:('(','fromleft'),
			  24:('(','fromright')}