import difflib

headlines = []
headlines.append("BBC Reporter on Royal Baby Watch: We Report, None of it News...But That Won't Stop Us! | Video Cafe")
headlines.append("Jahlil Beats The Ghost | OnSMASH")
headlines.append("About Those 'Strong Fundamentals'... | Zero Hedge")
headlines.append("UK duchess gives birth to baby boy - Europe - Al Jazeera English")
headlines.append("Governor General reacts to the news of the royal birth - Canada - CBC News")
headlines.append("Insolvent Spain Forced To 'Borrow' From Social Security Fund To Pay Pensions | Zero Hedge")
headlines.append("BBC News - Royal baby: What does the future hold for the Cambridge prince?")
headlines.append("HA, HA! Sky News Reporter Lost For Words When Man In Crowd Says 'Its A Black Boy' - YouTube")
headlines.append("Royal baby born; William and Kate announce arrival of son | Daily Brew - Yahoo! News Canada")
headlines.append("BREAKING NEWS:THE ROYAL CHILD IS BORN AND HE IS A BOY, PRINCE WILLIAMS AND KATE WELCOME THE NEW KING | WELCOME TO TATAFO NAIJA ......d talk talk place")
headlines.append("Napalm Storm Enters The Studio - in Metal News ( Metal Underground.com )")
headlines.append("Cannabis plants spring up all over German town after campaigners plant thousands of seeds in protest against the 'demonisation' of the drug | Mail Online")
headlines.append("Viz's Shonen Jump to Run 'Bench' 1-Shot by Naruto's Kishimoto - News - Anime News Network")
headlines.append("OK! Magazine: First For Celebrity News :: Latest Celebrity News :: Kate Middleton and Prince William welcome baby boy - BBC News")
headlines.append("BBC News - Pope Francis arrives in Rio de Janeiro on Brazil visit")
headlines.append("Kate Middleton Gives Birth to the Royal Baby! | E! Online")
headlines.append("Royal Baby Boy Is Here! See the Easel Set Up Outside Buckingham Palace with the Official Announcement | E! Online")
headlines.append("Microsoft and LEGO Education demonstrate development possibilities on Windows 8.1 with SentryBot")
headlines.append("Urban Meyer's holier-than-thou routine is harder to justify these days - Yahoo! Sports")
headlines.append("Royal baby: Duchess of Cambridge gives birth to healthy boy and future King with proud Prince William by her side | Mail Online")
headlines.append("Cyclist, 12, goes the distance for sake of children (From Worcester News)")
headlines.append("Stylish New Airspace Lounge at JFK's Terminal 5 | Fodor's")
headlines.append("BBC News - Royal baby boy: BBC News coverage")
headlines.append("News - 5 Cool Organic Living Quotes To Get Inspired By")
headlines.append("United Stationers Reports Record Second Quarter 2013 Earnings Per Share - Yahoo! News")
headlines.append("Grant offers up free smoke alarms, including deaf-specific | wcsh6.com - Wonderful News")
headlines.append("Tottenham send Baldini to negotiate Soldado deal with Valencia - Goal.com")
headlines.append("WRTC 2014 Station Test A Valuable Experience, Organizers Say")
headlines.append("Al-Shabaab setting up fresh units - News - nation.co.ke")
headlines.append("MTV Geek SDCC 2013: Sideshow Collectibles Comic-Con Prize Pack Giveaway")
headlines.append("The Royal Baby Is Here! - Cosmopolitan")
headlines.append("KaleidoCamera teaches your DSLR new light field tricks: Digital Photography Review")
headlines.append("Was Afghanistan Worth the Cost? - To the Point on KCRW")
headlines.append("Fremantle Relocates Pets Channel from YouTube to Blip | Variety")
headlines.append("A Royal Baby: What Next For The Monarchy?")
headlines.append("Breaking News: Its a Royal Baby boy! - News - Diss Mercury")
headlines.append("Fashion Poll: Which of Sofia Vergara's Monokinis Is Your Favorite? | E! Online")
headlines.append("Kate, Duchess of Cambridge, delivers royal baby boy - World - CBC News")
headlines.append("S&P 500 ends at record, McDonald's weighs on Dow - Yahoo! News")
headlines.append("Five Surprising Facts About Daydreaming")
headlines.append("It's a boy for Kate and William | News.com.au")
headlines.append("Johnsonville Sausage's Brattender Croons to Promote Proper Grilling | ClickZ")
headlines.append("I Do...Recommend We Have The Organist Rehearse | E! Online")
headlines.append("Upsetting look from Cecil Fielder helped Tigers' Prince Fielder forge his iron man approach - Yahoo! Sports - Info and Stats")
headlines.append("Forget Royal Baby: A Horse Walks Into McDonalds Tops UK News")
headlines.append("Mix Speaker's,Inc. Provides Theme Song for Anime - koroshiya-san")
headlines.append("Demi Lovato Is 'Really, Really Good Friends' With Nick Jonas - Music, Celebrity, Artist News | MTV.com - July 22, 2013 - RT News")
headlines.append("Kate & Prince William Welcome First Child | ETonline.com")
headlines.append("UMW-News - Nazgul William")
headlines.append("Irene McCormack Jackson accusing Mayor Filner of sexual harassme - San Diego, California News Station - KFMB Channel 8 - cbs8.com")
headlines.append("'Stars Dance' Review: Selena Gomez's Debut Solo Studio Album Misses The Mark")
headlines.append("Britains Kate gives birth to royal baby boy: palace - thenews.com.pk")
headlines.append("Trayvon Martin and George Zimmerman: Race, Faith and Sin")
headlines.append("Royal baby: Duchess of Cambridge gives birth to a boy live coverage | UK news | guardian.co.uk")
headlines.append("When notebooks squeeze Intel out | Business Tech - CNET News")
headlines.append("Tame Impala form new band to raise money for friend | News | NME.COM")
headlines.append("Jackson's mother resumes testimony in LA courtroom - Yahoo! News")
headlines.append("Only Christian faith schools are acceptable: Amartya Sen - The Economic Times on Mobile Dow Bands")
headlines.append("Vancouver bookstore opening bucks trend - British Columbia - CBC News")
headlines.append("Brave soldier who searched for bombs in Afghanistan left homeless after being denied a council house | Mail Online")
headlines.append("Men - 2013 FINA World C'Ships Week 1: Gallant Aussies fall to Serbs - Australian Water Polo Inc:")
headlines.append("BBC News - Online pornography to be blocked by default, PM announces")
headlines.append("BBC News - Plain cigarette packs 'encourage smokers to quit'")
headlines.append("Ailsa Anderson Nails It! Makes Royal Baby History - Babies, The Royals, Carole Middleton, Kate Middleton, Michael Middleton, Prince Charles, Prince William, Queen Elizabeth II, Cover Galleries : People.com")
headlines.append("How to filter royal baby news out of your Twitter timeline")
headlines.append("Consulates in Spain assist more than 4,600 Britons last year - Euro Weekly News Spain")
headlines.append("Reno officials working to stop sex trafficking")
headlines.append("Glenn Beck Responds to Geraldo Rivera's Semi-Nude Selfie With His Own Towel Pic | E! Online")
headlines.append("News - StreamOrganic Newsroom - Follow the stream!")
headlines.append("African students allege racial discrimination in Bangalore - The Hindu")
headlines.append("Wall Street Commodity Trading in Jeopardy Amid Fed Review - Bloomberg")
headlines.append("Duchess gives birth to a son - ITV News")
headlines.append("Forgotten Tomb Releasing 'Vol. 5' On Vinyl - in Metal News ( Metal Underground.com )")
headlines.append("Brewing Up a Batch: Plant City Winemakers Venture Into Craft Beer | TheLedger.com")
headlines.append("Kate Middleton Gives Birth Baby Boy: Future King Born - UsMagazine.com")
headlines.append("When college diversity delivers benefits")
headlines.append("Dennis Farina Death: Celebs Tweet Reactions in Wake of Late Actor's Passing | E! Online")
headlines.append("George Zimmerman Emerged From Hiding for Truck Crash Rescue - Yahoo!")
headlines.append("#ROYALBABY: The Prince Is HERE!!!! | SIRKENAYO | Your One Stop Entertainment Hub")
headlines.append("Instagram")
headlines.append("New This Week in Video Games - Shadowrun, Stealth Inc, and Smurfs | Attack of the Fanboy")
headlines.append("Royal Baby: Hollywood's Best Tweets - The Hollywood Reporter")
headlines.append("I have no reason to leave PSG, says Ibra - Goal.com")
headlines.append("Pope Francis touches down in Brazil - Americas - Al Jazeera English")
headlines.append("George Zimmerman rescues family from truck crash last week, police say | Fox News")
headlines.append("BBC News - Lynton Crosby firm denies NHS 'conflict of interest' claims")
headlines.append("5 Pinterest-like education sites worth trying out | Education Dive")
headlines.append("Nokia Lumia 625 leaks in full ahead of its launch - GSMArena.com news")
headlines.append("BBC News - Royal baby: Kate gives birth to boy")
headlines.append("Georgia decides against offering Common Core standardized test | www.ajc.com")
headlines.append("Prince Charles on Royal Baby's Birth: 'My Wife and I Are Overjoyed' - UsMagazine.com")
headlines.append("Labor MP Bryan Green confirms he willl seek a fifth term - ABC News (Australian Broadcasting Corporation)")
headlines.append("Its a boy! William and Kate welcome first born | Globalnews.ca")
headlines.append("George Zimmerman helps rescue family from car wreck")
headlines.append("Should government be more transparent? Mackinac Center to host town hall on topic | MLive.com - Royal")
headlines.append("NEWS: Whos Wants to Lose Weight Now? Dubai Offering Gold in Exchange for Weight Loss | Official Blog Of Dj Bobby Trends")
headlines.append("MAXON Computer to Exhibit at SIGGRAPH 2013, Booth 315, July 23 - 25, 2013, in Anaheim, CA, US | EON: Enhanced Online News")
headlines.append("Royal Baby: It's A Boy For Kate And William")
headlines.append("Royals News, Pictures, and Videos | E! Online")
headlines.append("Send your congratulations to William and Kate on the royal baby birth - Your Community")
headlines.append("Jaguars waive Jordan Rodgers, Aaron's brother - NFL.com")
headlines.append("Prince William Duchess Kate royal baby")
headlines.append("We Want Your Great Panel Ideas: Level UP at the SXSW Gaming Expo! | SXSW 2013")
headlines.append("Spot the Photoshop Mistakes - Likes")
headlines.append("Mystery at Ballinrobe as stewards withdraw gamble | Horse Racing News | Racing Post")
headlines.append("Selena Gomez's 21st Birthday Plans Revealed! - Music, Celebrity, Artist News | MTV.com")
headlines.append("Judge Rules Jesse Ventura Can Proceed With Lawsuit Against Deceased Navy Seal")
headlines.append("UT chemists turn seawater into fresh water with a battery - Houston Chronicle")
headlines.append("UPDATED: Duchess of Cambridge gives birth to a boy (Bournemouth Echo)")
headlines.append("The Oval Zone - Issue 8 - 22nd July - is out today! - Mid Wales District Rugby Union")
headlines.append("Dennis Farina Dead; Actor Was 69 | Movies News | Rolling Stone")

headlines2 = []
headlines2.append("Cisco coughs $2.7bn for Sourcefire The Register")
headlines2.append("Octopi! Spinal Tap! How Cult RPG EarthBound Came to America | Game|Life | Wired.com")
headlines2.append("HIP HOP VIDEOS | Angela Yee interviews Tech N9ne at SOBs NYC")
headlines2.append("Mobile-Only Flipboard Lands on Desktops for the First Time | Gadget Lab | Wired.com")
headlines2.append("5 Ways To Use a Tablet To Boost Your Acting Career | Voice Recording, Picture & Video Editing Tech Tips | Career Tips | Backstage | Backstage")
headlines2.append("Royal baby announcement forces House of Windsor to adapt tradition for the internet age - CBS News")
headlines2.append("Should Facebook offer a paid, ad-free version? - CNN.com")
headlines2.append("Apple eyes way to entertain your iPhone callers on hold | Apple - CNET News")
headlines2.append("Flipboard Brings Its Mobile Magazines To The Web | TechCrunch")
headlines2.append("8 Creative Ways to Connect With Customers on Facebook")
headlines2.append("Apple Q3 Earnings Preview: What to Expect")
headlines2.append("Reuters Next How big tech stays offline on tax")
headlines2.append("Wall Street Aims For Fresh Highs After Earnings From DuPont, United Tech")
headlines2.append("Healthcare data breaches: Reviewing the ramifications | HealthITSecurity.com")
headlines2.append("Suvoltas energy-saving tech cuts an ARM chips power consumption in half Tech News and Analysis")
headlines2.append("10 Cool Home Innovations From PSFK's Pop-Up Gallery")
headlines2.append("Georgia Techs Computer Science MOOC: The super-cheap masters degree that could change American higher education. - Slate Magazine")
headlines2.append("11 Vintage Selfies Too Fabulous for Filters")
headlines2.append("Remix artist Pogo explains how he morphs classics films into hit electronic jams | The Verge")
headlines2.append("Symantec snaps up PasswordBank, touts SSO logins to biz The Register")
headlines2.append("hack{cyprus} 2013")
headlines2.append("Shopkick Adds In-App Purchases To Help Retailers Fight Amazon: We Are The Anti-Amazon Coalition | TechCrunch")
headlines2.append("Google Groups")
headlines2.append("PRESS RELEASE: Investors Tap Latest Tech Tools to Power Up Commercial Real Estate Values | NREIWire content from National Real Estate Investor")
headlines2.append("Flurry: China Accounts For 24% Of The Worlds Connected Devices, With 261.3M Active Smartphones And Tablets | TechCrunch")
headlines2.append("SanDisk Connect Flash Drive Wirelessly Sends Files to Your Phone")
headlines2.append("Special report: How big tech stays offline on tax | Reuters")
headlines2.append("Flipboard brings magazines to the web, launches 'Big Ideas'")
headlines2.append("Tech experts lobby for more computing classes to boost future economy | Financial Post")
headlines2.append("Will Jackson impersonates Paul Johnson | Georgia Tech sports | www.ajc.com")
headlines2.append("Apple's dual-sensor imaging patent promises higher quality iPhone pictures")
headlines2.append("Ember for Mac: a digital scrapbook from the makers of Clear | The Verge")
headlines2.append("The Webs longest nightmare ends: Eolas patents are dead on appeal | Ars Technica")
headlines2.append("LittleSnapper Becomes Ember As Realmac Software Overhauls Its Mac App For Digital Creatives | TechCrunch")
headlines2.append("5 Ed Tech Resources I Used While Working in a Low-Income Class")
headlines2.append("DataStax Readies For IPO, Raises $45M For Modern Database Platform Suited To New Data Intensive World | TechCrunch")
headlines2.append("Why opt-in porn filters havent arrived in Canada - The Globe and Mail")
headlines2.append("LinkedIn Expands Ad Program With Launch Of Sponsored Updates Program | TechCrunch")
headlines2.append("Bullish on aerospace, United Tech lifts 2013 forecast | Reuters")
headlines2.append("Akamai: There Are Now 734M IP Addresses Worldwide, Up 10% Y-o-Y, 1B+ Internet Users; U.S. Is 9th Fastest Broadband Country | TechCrunch")
headlines2.append("Electronic Skin Responds to Your Fingertips - ABC News")
headlines2.append("Not Your Grandma's Knitting: 20 Incredible Yarn Bombs")
headlines2.append("Nokia unveils biggest-ever Lumia phone")
headlines2.append("New Android apps worth downloading: Pimp Your Screen with Widgets, Spaceteam, M&M Clash of Heroes - Android app article - Phil Hornshaw | Appolicious Android App Directory")
headlines2.append("Apple's 1 Billion Podcasts and Other News You Need to Know")
headlines2.append("New iPhone apps worth downloading: Seeking Alpha Portfolio and Narr8 updates, Hero of Many - iPhone app article - Phil Hornshaw | Appolicious iPhone and iPad App Directory")
headlines2.append("Amazon-Acquired Goodreads Says It Has 20M Members, Doubling In Less Than A Year | TechCrunch")
headlines2.append("This NFC Ring Puts Wireless Transfer Tech On Your Finger So You Can Fist-Bump Phones | TechCrunch")
headlines2.append("New movie server lets you watch films instantaneously")
headlines2.append("Big tech shelled out for Gangs immigration push - POLITICO.com")
headlines2.append("Cisco scoops up security firm Sourcefire for $2.7B")
headlines2.append("Give a Slacker Colleague a Unique Task to Force Them to Carry Weight")
headlines2.append("Cisco coughs $2.7bn for Sourcefire The Channel")
headlines2.append("Investors still waiting for Apple's next big device")
headlines2.append("Alibaba Pursues New Smart TV OS To Grow Its E-Commerce Play | TechCrunch")
headlines2.append("Incredible tech: How to find life on Mars | Fox News")
headlines2.append("BBC News - US court rules web patent claim invalid")
headlines2.append("Wantworthy Debuts Fresh, A Mobile Companion Featuring New Arrivals From Your Favorite Stores | TechCrunch")
headlines2.append("Apple Patents On-Hold Media Sharing, Dual Sensor Imaging For iPhone, iPad And Mac | TechCrunch")
headlines2.append("Chinese Tech Giant Sina Focuses On Social Commerce. Plans To Roll Out An Online Banking Platform")
headlines2.append("peHUB | Private equity and venture capital news, data and community")
headlines2.append("Successful Tech People Who Wake Up Early - Business Insider")
headlines2.append("Tech News 7/23/13 | Tech News Condensed")
headlines2.append("Uniqul allows you to pay with your face | Tech | Gear")
headlines2.append("Flipboard Brings Your Magazines to the Browser")
headlines2.append("Wall Street Is Punishing Adtech Players For Failing To Make Money (MM, VELT, MRIN, AUGT, TRMR) | Patriot Radio Network")
headlines2.append("U.S. Share Of Mobile Ad Impressions Dips Below 50% On Worldwide Surge, Opera Finds | TechCrunch")
headlines2.append("A Peek Inside Science Inc.s Santa Monica Tech Startup Studio [TCTV] | TechCrunch")
headlines2.append("Google Inc (GOOG) & Apple Inc. (AAPL): Tech Firms Need to Watch out for Watchdogs - Insider Monkey")
headlines2.append("Netflix, Cisco take early tech spotlight - MarketWatch")
headlines2.append("Instagram")
headlines2.append("Interview with Gardner Dozois: The Years Best Science Fiction: Thirtieth Annual Collection Adventures in SciFi Publishing")
headlines2.append("5 Exciting Tech Companies You've Probably Never Heard Of")
headlines2.append("Cisco to buy security software maker Sourcefire for $2.7 billion - Yahoo! News")
headlines2.append("Top 25 most influential people under 40 in gov and tech - FedScoop")
headlines2.append("This African Smart Card Helps Catch Disease Outbreaks")
headlines2.append("Most big U.S. tech groups slip European tax net | Reuters")
headlines2.append("The Dell buy-out: Decision time | The Economist")
headlines2.append("Chris Devore Talks Up Seattle As A Solid Tech Hub | TechCrunch")
headlines2.append("LG files trademarks for GPad, G Watch, G Glass | Mobile - CNET News")
headlines2.append("All eyes on Apple Inc. - Apple 2.0 -Fortune Tech")
headlines2.append("Fitness Repair Tech (All Areas) | deClassifieds")
headlines2.append("Tech Companies Cool Their Lobbying Expenditures in Q2 - SocialTimes")
headlines2.append("Netflix compares itself to HBO, but won't offer viewership numbers to back it up | The Verge")
headlines2.append("Robot air freshener blows bubbles for future homes - tech - 23 July 2013 - New Scientist")
headlines2.append("Syncronys International, Inc. - SNTL | Hot Stock CafeHot Stock Cafe")
headlines2.append("Glitch Moment/ums - From tech accident to artistic expression - we make money not art")
headlines2.append("Facebook confirms men dont care about the #RoyalBaby - Silicon Valley Business Journal")
headlines2.append("Domestic oil production on rise in Western states due to technology, private land production | Fox News")
headlines2.append("How to Use Tabs in Gmail")
headlines2.append("The Week in iOS Accessories: Get on the horn | Macworld")
headlines2.append("Bullish on Apple? Heres What to Look for in Earnings Report | Breakout - Yahoo! Finance")
headlines2.append("LG and Samsung Bring Curved OLED TVs to the U.S.")
headlines2.append("Tech Writing Handbook - Dozuki")
headlines2.append("Alibaba develops Smart TV OS, will use it to sell you things")
headlines2.append("Developer Learning Session - Zurmo Forums")
headlines2.append("Google's Street View takes you up Mount Fuji, crampon free")
headlines2.append("On the sly: most top US tech companies avoid European taxes RT Business")
headlines2.append("10 Disney Princesses Who Can Twerk Better Than You")
headlines2.append("Samsung announces developers conference for October - Tech News - Digital Spy")
headlines2.append("Browse Forbes Tech with Nextly")
headlines2.append("Verizon's NYC Droid event is today at noon ET, get your liveblog here!")
headlines2.append("U.K. Predicted to Have 2 Billion Internet Trade Surplus in 2013 - Tech Europe - WSJ")
headlines2.append("EGM on E-Participation: Empowering People through ICTs")
headlines2.append("Learning with 'e's: Technology won't replace teachers, but...")
headlines2.append("More women in tech - one PyLadies workshop at a time | Usersnap Blog")

headlines3 = []
headlines3.append("Cisco coughs $2.7bn for Sourcefire The Register")
headlines3.append("Chinedu Echeruo On Navigating Tech Business Success [Watch]")
headlines3.append("LocalResponse Founder Nihal Mehta Cedes CEO Role | Digital - Advertising Age")
headlines3.append("HIP HOP VIDEOS | Angela Yee interviews Tech N9ne at SOBs NYC")
headlines3.append("Should Facebook offer a paid, ad-free version? - CNN.com")
headlines3.append("LinkedIn Introduces Sponsored Updates for Companies")
headlines3.append("How Often Do You Upgrade Your Cell Phone?")
headlines3.append("8 Creative Ways to Connect With Customers on Facebook")
headlines3.append("With Launch Of Lemon Network, Wallet App Maker Lemon Prepares To Take On PayPal, Google, Venmo & Others | TechCrunch")
headlines3.append("Reuters Next How big tech stays offline on tax")
headlines3.append("BlackBerry Q10 hits Sprint August 30th, Samsung's ATIV S Neo arrives August 16th")
headlines3.append("Google, Amazon Prevail in Web Tech Patent Fight With Eolas | News & Opinion | PCMag.com")
headlines3.append("Yaptas price tracking tech could save corporations millions on airfare | VentureBeat")
headlines3.append("Varney & Co. | Fox Business")
headlines3.append("Suvoltas energy-saving tech cuts an ARM chips power consumption in half Tech News and Analysis")
headlines3.append("DingDong! Heres The New Craze In Photo Messaging Apps And Its Addictive | TechCrunch")
headlines3.append("Georgia Techs Computer Science MOOC: The super-cheap masters degree that could change American higher education. - Slate Magazine")
headlines3.append("12 Weirdest Laws in the United States [VIDEO]")
headlines3.append("Nintendo Stock Highest in 2 Years Thanks to 'Animal Crossing'")
headlines3.append("WSJ Reporter Heads to Ex-Colleague's New Journalism Startup - Mike Isaac - Media - AllThingsD")
headlines3.append("LiveMinutes Raises $1.4M Seed Round For Its Real-Time Collaboration Service, Announces Partnership With Evernote | TechCrunch")
headlines3.append("Tech N9ne Gives New York An Early Taste Of 'Something Else' - XXL")
headlines3.append("SanDisk Connect Flash Drive Wirelessly Sends Files to Your Phone")
headlines3.append("Born to Die Electronics Dissolve When Wet")
headlines3.append("Special report: How big tech stays offline on tax | Reuters")
headlines3.append("B Tech Food Technology Semester IV Syllabus")
headlines3.append("Minyanville: 'Facebook for Every Phone' a huge success")
headlines3.append("COA - Bender (Remix) ft. Tech N9ne, Mac Lethal, Irv Da Phenom, JL, Joey Cool, Dutch Newman, Godemis - YouTube")
headlines3.append("Tech experts lobby for more computing classes to boost future economy | Financial Post")
headlines3.append("Verizon Reveals The $99 Motorola Droid Mini, $199 Droid Ultra, And The $299 Droid Maxx | TechCrunch")
headlines3.append("Tech N9ne Reveals Missed Collabos with Eminem, Nas & Jay-Z (VIDEO) | AllHipHop.com")
headlines3.append("Researchers Create Near-Exhaustive, Ultra-Realistic Cloth Simulation | TechCrunch")
headlines3.append("Sugar Water Radio Tech N9ne Reveals Missed Collabos with Eminem, Nas & Jay-Z (VIDEO) | Sugar Water Radio")
headlines3.append("Bungalo Records/Universal Music Group Distribution Electric Pop Recording Artist Melissa B. Releases Her Single Addicted Today")
headlines3.append("Is ARPA-E The Future Of American Energy Innovation? Exclusive Q&A With Deputy Director Cheryl Martin")
headlines3.append("The Webs longest nightmare ends: Eolas patents are dead on appeal | Ars Technica")
headlines3.append("How an Astronomical Mystery Was Explained by High-Tech Photography")
headlines3.append("SF's district attorney: iOS 7's Activation Lock offers 'clear improvements' in anti-theft tech | TUAW - The Unofficial Apple Weblog")
headlines3.append("Grooveshark Makes The Google Autosuggest Blacklist, Joining The Pirate Bay And Others | TechCrunch")
headlines3.append("World chuckles about #RoyalBaby - CNN.com")
headlines3.append("Bullish on aerospace, United Tech lifts 2013 forecast | Reuters")
headlines3.append("Chinese made easy with 'Chineasy' by Noma Bar and ShaoLan Hseuh | Art | Wallpaper* Magazine: design, interiors, architecture, fashion, art")
headlines3.append("The Droid Maxx - The rise of Verizon's new Droids (pictures) - CNET Reviews")
headlines3.append("Tech N9ne, Birdman And Mack Maine On RapFix Live Jul 24")
headlines3.append("Earth Strikes a Pose Beneath Saturn's Rings - Yahoo! News")
headlines3.append("DROID mini official as successor to RAZR M for Verizon - SlashGear")
headlines3.append("Apple's 1 Billion Podcasts and Other News You Need to Know")
headlines3.append("18 Best Free Apps for the Samsung Galaxy S3")
headlines3.append("This NFC Ring Puts Wireless Transfer Tech On Your Finger So You Can Fist-Bump Phones | TechCrunch")
headlines3.append("Insert Coin: Beacon Audio Blazar Bluetooth speaker brings back Play 360 memories (hands-on)")
headlines3.append("New movie server lets you watch films instantaneously")
headlines3.append("IBM Extends Its Banking Tech Expertise Into Emerging Markets")
headlines3.append("Motorola Clears The Pipes With New Verizon Droids Time For The Google Era To Begin In Earnest | TechCrunch")
headlines3.append("Report Offers 'Index' for Evaluating Ed-Tech - Digital Education - Education Week")
headlines3.append("Cisco scoops up security firm Sourcefire for $2.7B")
headlines3.append("ET6NATION (EpicTeam6): (VIDEO) ANGELA YEE INTERVIEWS TECH N9NE (EME TAKEOVER)")
headlines3.append("Brainstorm Tech Spotlight: Philip Abram, Chief Infotainment Officer of GM - Fortune Tech")
headlines3.append("Investors still waiting for Apple's next big device")
headlines3.append("Brands Try, Fail to Capitalize on Royal Baby Hype")
headlines3.append("BBC News - US court rules web patent claim invalid")
headlines3.append("Motorola Droid Mini for Verizon eyes-on")
headlines3.append("How Crunchbase Data Compares To Other Industry Sources | TechCrunch")
headlines3.append("'Female' Chromosome May Play Unexpected Role in Male Biology - Wired Science")
headlines3.append("Carbon Dioxide Turned Into Electricity : Discovery News")
headlines3.append("Apple Patents On-Hold Media Sharing, Dual Sensor Imaging For iPhone, iPad And Mac | TechCrunch")
headlines3.append("Octopuses inspire 3D-printed propulsion systems for boats : TreeHugger")
headlines3.append("Kremlin Intrigue Threatens Russia's Silicon Valley - Businessweek")
headlines3.append("Verizon NYC Droid event liveblog")
headlines3.append("Google handles 25 percent of North America's Web traffic - CNN.com")
headlines3.append("Successful Tech People Who Wake Up Early - Business Insider")
headlines3.append("Travelport touts customisable flight search tech | Tnooz")
headlines3.append("Flipboard Brings Your Magazines to the Browser")
headlines3.append("The Blazar by Beacon Audio - Cool Hunting")
headlines3.append("A Peek Inside Science Inc.s Santa Monica Tech Startup Studio [TCTV] | TechCrunch")
headlines3.append("How to Choose a Right Outsourcing Partner | Globality Consulting")
headlines3.append("Verizon Unveils Three New Droid Phones")
headlines3.append("NASA releases image of Earth taken from 1.4B kilometres away | CTV News")
headlines3.append("Instagram")
headlines3.append("Enterprise Social Network Platform Hall Raises $5.5M In Series A Funding | TechCrunch")
headlines3.append("Cisco to acquire FIRE for $2.7 billion - Triangle Business Journal")
headlines3.append("5 Exciting Tech Companies You've Probably Never Heard Of")
headlines3.append("10 Reasons Why Android Beats Apple iOS | News, Facts & Other Information You Love - UncoverDiscover.com")
headlines3.append("Tech N9ne Songs - That's My Kid")
headlines3.append("Top 25 most influential people under 40 in gov and tech - FedScoop")
headlines3.append("Most big U.S. tech groups slip European tax net | Reuters")
headlines3.append("The Dell buy-out: Decision time | The Economist")
headlines3.append("Google Lets You Climb Mount Fuji With Street View")
headlines3.append("Chris Devore Talks Up Seattle As A Solid Tech Hub | TechCrunch")
headlines3.append("Watch The Trailer For New RPG 'Kanye Quest 3030' - XXL")
headlines3.append("TECH TIP: Shut off in-app purchases before letting your kids play with a smartphone or tablet | FAVES + CO.")
headlines3.append("All eyes on Apple Inc. - Apple 2.0 -Fortune Tech")
headlines3.append("Device puffs virtual objects into reality, lets you feel phantom objects floating in air | Fox News")
headlines3.append("Tech N9ne Ft. Cee Lo Green, Big K.R.I.T. & Kutt Calhoun Thats My Kid | AllHipHop.com")
headlines3.append("17th-century gadget gives up secrets to 3D printer - tech - 23 July 2013 - New Scientist")
headlines3.append("Tech Companies Cool Their Lobbying Expenditures in Q2 - SocialTimes")
headlines3.append("Brainstorm Tech Startup Idol: And this year's winner is... - Fortune Tech")
headlines3.append("NSA says it cant search its own e-mails | Ars Technica")
headlines3.append("TECH: Hundreds Of Millions Of Mobile Users Are At Risk!! | Official Blog Of Dj Bobby Trends")
headlines3.append("Domestic oil production on rise in Western states due to technology, private land production | Fox News")
headlines3.append("How to Use Tabs in Gmail")
headlines3.append("NYSE Big Stage")
headlines3.append("MIDUFINGA AMERICA : YOUNG BARZ FEAT TECH 9 & CRAIG - SUPERSTAR REMIX (OFFICIAL VIDEO)")
headlines3.append("Study: Cyberattacks Pile Up $300 Billion in Losses Each Year")
headlines3.append("'OK Google Now' comes to Verizon's 2013 Droid trio")
headlines3.append("New Music: Tech N9ne ft. Cee Lo Green, Big K.R.I.T. & Kutt Calhoun - That's My Kid | DDotOmen")
headlines3.append("Bentley plans to build ultra-luxury SUV - Jul. 23, 2013")
headlines3.append("Learning with 'e's: Technology won't replace teachers, but...")
headlines3.append("Transcript: James Murdoch - Fortune Tech")
headlines3.append("We're Number 9! US Broadband Speeds Rise, But Slower Than Many Other Countries' - Slashdot")



def similarity(a,b):
	''' Returns how similar strings a and b are, between 0 and 1. '''
	return difflib.SequenceMatcher(None,a.lower(),b.lower()).ratio()

def edges(l,t=0):
	''' Returns a sorted list of string index pairs and their similarity in the form of [[a,b,s],...],
	as well as a hashtable of in the form of {(a,b):s,...}. 
	If threshhold t is given, it will only return edges where similarity is > t'''
	# Init return values
	edges = []
	edges_ht = {}

	for a in l:
		a_i = l.index(a)
		for b in l[a_i + 1:]: # prevent looking up (a,b) and (b,a)
			b_i = l.index(b)
			sab = similarity(a, b)
			if sab >= t:
				edges.append([a_i, b_i, sab])
				edges_ht[(a_i,b_i)] = edges_ht[(b_i,a_i)] = sab

	edges = sorted(edges, key=lambda x: x[2], reverse = True)

	return (edges,edges_ht)

def clusters(e,eht,t=0):
	''' Returns a list of clusters in the form of {cid:[a,b,c],...}
	where cid = cluster id and a, b, and c are headline IDs or indeces.
	Also returns a hash table in the form of {a:cid,...}
	Take a matching list and hash table of edges, as well as 
	threshold t as a minimum similarity.'''
	# Init return val
	clusters = {}
	clusters_ht = {}
	cid = 0

	for edge in e:
		a = edge[0] # first point
		b = edge[1] # second point
		s = edge[2] # similarity of (a,b)

		if s >= t:
			caid = clusters_ht.get(a)
			cbid = clusters_ht.get(b)

			# 1. a or b is already part of a cluster; add a and b to cluster
			if caid or cbid:
				cid = caid and caid or cbid

			# 2. Neither a nor b is part of a cluster (and there are clusters already); 
			#    Check a and b against existing cluster members, add if s >= t against any member
			if not caid and not cbid:
				if clusters_ht:
					similar = False
					for xid, clid in clusters_ht.iteritems():
						if eht.get((caid,xid)) >= t or eht.get((cbid,xid)) >= t:
							cid = clid
							similar = True
					if not similar:
						# 3. a and b aren't part of any cluster and have no similarity to any cluster members;
						#    Add to new cluster
						cid = len(set(clusters_ht.values()))
			
			clusters_ht[a] = clusters_ht[b] = cid

	for xid, cid in clusters_ht.iteritems():
		if not clusters.get(cid): clusters[cid] = []
		clusters[cid].append(xid)

	return (clusters, clusters_ht)



if __name__ == '__main__':
	headlines = headlines3

	# Config
	SIMILARITY = .50

	edges, edges_ht = edges(headlines)

	clusters, clusters_ht = clusters(edges, edges_ht, SIMILARITY)

	for xid, cid in clusters_ht.iteritems():
		print '%s: %s' % (headlines[xid],cid)

	for cid, cluster in clusters.iteritems():
		print 'id: %s' % (cid,)
		for c in cluster:
			print '%s (%s)' % (headlines[c],c)
		print '\n'

	print edges_ht[(104,32)]

	'''clusters = {}
	cluster_id = 0
	for edge in edges:
		if edge[2] > SIMILARITY:
			# if either is part of cluster that's the id
			if clusters.get(edge[0]) or clusters.get(edge[1]):
				#print 'one is there %s' % (cluster_id,)
				cluster_id = clusters.get(edge[0]) and clusters.get(edge[0]) or clusters.get(edge[1])
				clusters[edge[0]] = clusters[edge[1]] = cluster_id

			# if neither is part of cluster, increase id
			if not clusters.get(edge[0]) and not clusters.get(edge[1]):
				#print 'neither is there %s' % (cluster_id,)
				if clusters:
					temp = {}
					for member, cluster_id in clusters.iteritems():
						if similarity(headlines[member], headlines[edge[0]]) > SIMILARITY or similarity(headlines[member], headlines[edge[1]]) > SIMILARITY:
							temp[edge[0]] = temp[edge[1]] = cluster_id
					clusters = dict(clusters.items() + temp.items())
					temp = {}

			if not clusters.get(edge[0]) and not clusters.get(edge[1]):
				cluster_id = len(clusters.values())
				clusters[edge[0]] = clusters[edge[1]] = cluster_id

	cluster_list = []

	for cluster_id in sorted(set(clusters.values())):
		cid_list = []
		for k,v in clusters.iteritems():
			if v == cluster_id:
				cid_list.append(str(k))
		cluster_list.append([cluster_id,cid_list])
		

	for cluster in cluster_list:
		print 'id: %s\n%s' % (cluster[0],','.join(cluster[1]))
		for hid in cluster[1]:
			print headlines[int(hid)]
		print '\n'


	#for t in edges[:100]:
	#	print '%.1f%%\n%s\n%s\n' % (t[2]*100,headlines[t[0]], headlines[t[1]])'''