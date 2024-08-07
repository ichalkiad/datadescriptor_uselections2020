import time
import ipdb
import pandas as pd
from us2020data.src.utils import clean_speech_texts, textclean_votesmart,\
                                    textclean_miller, remove_dots, find_substring,\
                                    remove_candidates_dicts, remove_square_brackets, \
                                    remove_round_brackets, remove_containing_speeches
import pathlib
import re

def remove_containing_speeches(text):

    if "The accord reached between the United States, Israel, and the United Arab Emirates (UAE) on August 13, 2020, is a courageous step toward a more stable, integrated, and prosperous Middle East. " in text\
                or "Today, I am officially recognizing the President of the Venezuelan National Assembly, Juan Guaido, as the Interim President of Venezuela." in text\
                or "The United States and Colombia are committed to taking steps to resolve the ongoing democratic and humanitarian crisis in Venezuela. " in text\
                or "This year, the United States and Czech Republic mark the 30-year anniversary of the inspiring and world-changing events of the Velvet Revolution." in text\
                or "The resignation yesterday of Bolivian President Evo Morales is a significant moment for democracy in the Western Hemisphere. " in text\
                or "On November 14, 1979, by Executive Order 12170, the President declared a national emergency with respect to Iran" in text\
                or "On November 22, 2015, by Executive Order 13712, the President declared a national emergency to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in Burundi," in text\
                or "We, the President of the United States and the Prime Minister of Bulgaria, reaffirm the strong friendship and alliance between our two countries. " in text\
                or "On November 27, 2018, by Executive Order 13851, I declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in Nicaragua. " in text\
                or "Today, President Donald J. Trump and President Mario Abdo Benitez of Paraguay committed to deepening the partnership between their two countries." in text\
                or "Today, President Donald J. Trump met with the President of the Republic of Ecuador, Lenï¿½n Moreno, signaling the historic turn in bilateral ties between our two countries. " in text\
                or "On February 25, 2011, by Executive Order 13566, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the actions of Colonel Muammar Qadhafi," in text\
                or "On April 1, 2015, by Executive Order 13694, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.) to deal with the unusual and extraordinary threat to the national security, foreign policy, and economy of the United States constituted by the increasing prevalence and severity of malicious cyber-enabled activities originating from, or directed by persons located, in whole or in substantial part, outside the United States. " in text\
                or "On April 3, 2014, by Executive Order 13664, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in and in relation to South Sudan," in text\
                or "On April 12, 2010, by Executive Order 13536, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the deterioration of the security situation and the persistence of violence in Somalia, and acts of piracy and armed robbery at sea off the coast of Somalia," in text\
                or "Today, President Donald J. Trump declared that a major disaster exists" in text\
                or "On Friday, April 24, 2020, the President signed into law: H.R. 266, the 'Paycheck Protection Program and Health Care Enhancement Act,' which provides additional fiscal year " in text\
                or "April 25, 2020, marks the 75th Anniversary of the historic meeting between American and Soviet troops, who shook hands on the damaged bridge over the Elbe River." in text\
                or "A lot of people were betting against it, but they've learned not to bet against us, I suspect. (Laughter.) I know they've learned that in Mexico. The people of Mexico and the United States are joined together by shared values, shared faith, and shared future on this beautiful continent. " in text\
                or "As a mark of respect for the memory and longstanding public service of Representative John Lewis, of Georgia, I hereby order, by the authority vested in me by the Constitution and the laws of the United States of America," in text\
                or "Well, thank you very much. It's an honor to be with the governor of a fabulous state, Arizona. It's Doug Ducey, and we know him well. " in text\
                or "The First Lady and I wish our Jewish brothers and sisters Shana Tova and hope the millions observing this sacred day in America and around the world have a blessed start to the High Holy Days." in text\
                or "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the Countering America's Adversaries Through Sanctions Act (Public Law 115-44), the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.) (IEEPA), the National Emergencies Act (50 U.S.C. 1601 et seq.), section 212(f) of the Immigration and Nationality Act of 1952 (8 U.S.C. 1182(f)), and section 301 of title 3, United States Code, I, DONALD J. TRUMP, President of the United States of America, find that: It remains the policy of the United States to counter Iran's malign influence in the Middle East, " in text\
                or "I am deeply saddened by the passing of my dear friend, His Highness the Amir of Kuwait," in text\
                or "Today, I have signed into law S. 209, the 'PROGRESS for Indian Tribes Act of 2019' (the 'Act'). This Act makes several amendments to enhance tribal self-governance under the Indian Self-Determination and Education Assistance Act of 1975 (ISDEAA) " in text\
                or "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the International Emergency Economic Powers Act" in text\
                or "On November 27, 2018, by Executive Order 13851, I declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in Nicaragua." in text\
                or "Today, our Nation mourns the loss of a true pioneer. General Charles 'Chuck' Yeager served in the Army Air Corps and the United States Air Force for more than 30 years, piloting countless aerial victories in World War II and commanding Airmen during the wars in Korea and Vietnam." in text\
                or "On December 20, 2017, by Executive Order 13818, the President declared a national emergency with respect to serious human rights abuse and corruption around the world and, pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.), took related steps to deal with the unusual and extraordinary threat to the national security, foreign policy, and economy of the United States." in text\
                or "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the Federal Vacancies Reform Act " in text\
                or "By the authority vested in me as President by the Constitution and the laws of the United States of America, and to improve transparency with respect to the consequences of violating certain regulations and to protect Americans from facing unwarranted criminal punishment for unintentional violations of regulations, it is hereby ordered as follows:" in text\
                or "By the authority vested in me as President by the Constitution and the laws of the United States of America,I, DONALD J. TRUMP, President of the United States of America, find that additional actions are necessary to ensure the security of Unmanned Aircraft Systems (UAS) owned, operated, and controlled by the Federal Government;" in text\
                or "By the authority vested in me as President of the United States by the Constitution and laws of the United States of America, including section 301 of title 3, United States Code, and sections 3301 and 7301 of title 5, United States Code, it is hereby ordered as follows: " in text\
                or "On January 23, 1995, by Executive Order 12947, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security, foreign policy, and economy of the United States caused by grave acts of violence committed by foreign terrorists that disrupt the Middle East peace process." in text\
                or "The two leaders discussed Ecuador's leadership role in advancing security, prosperity, and democracy in the Western Hemisphere." in text:
        print(text)
        return ""
    else:
        return text




def clean_votesmart(directoryin, potus, directoryout, cleanerfunc, unicode_class="NFC", show=False, extra2remove=None):
    
    pathlib.Path("{}/{}/".format(directoryin, potus)).mkdir(parents=True, exist_ok=True)
    votesmart = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    print("Votesmart raw - {}".format(potus))            
    print(len(votesmart))      
    votesmart = clean_speech_texts(votesmart, cleanerfunc, unicode_class)
    print(len(votesmart))
    
    if extra2remove is not None:
        votesmart.RawText = votesmart.RawText.apply(extra2remove)       
        votesmart = votesmart[votesmart.RawText != ""]
        votesmart = votesmart.reset_index(drop=True)   
    

    print("Votesmart clean - {}".format(potus))            
    print(len(votesmart))
    votesmart.to_csv("{}{}/cleantext_{}.tsv".format(directoryout, potus, potus), index=False, sep="\t")
    if show:
        for i, row in votesmart.iterrows():            
            print(i)
            print(row["RawText"])
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)
    
    return votesmart


def clean_miller(directoryin, potus, directoryout, cleanerfunc, unicode_class="NFC", show=False):
        
    miller = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    miller = clean_speech_texts(miller, cleanerfunc, unicode_class)
    print("Miller raw - {}".format(potus))     
    print(len(miller))
    miller.to_csv("{}{}/cleantext_{}.tsv".format(directoryout, potus, potus), index=False, sep="\t")
    if show:
        for i, row in miller.iterrows():            
            print(i)
            print(row["RawText"])
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)
    
    return miller

def clean_cspan(directoryin, directoryout, show=False):
    
    patternremovetrump = re.compile(r'(PRES. TRUMP:|Mr. Trump:|GUEST:|MR. TRUMP:|PRESIDENT TRUMP::|TRUMP:|PRESIDENT TRUMP:)', re.DOTALL)
    def remove_trump(text) : return re.sub(patternremovetrump, '', text)    

    droptitles = ["New Chair of Joint Chiefs of Staff General Milley Swearing-in Ceremony",
                  "U.S.-China Trade Deal",
                  "President and First Lady Celebrate Earth Day and Arbor Day",
                  "Restaurant Executives Meeting at the White House",
                  "President Trump Receives Update on Border Wall Construction",
                  '"Latinos for Trump" Roundtable in Las Vegas',
                  'President Trump Hosts "Latinos for Trump" Roundtable in Phoenix',
                  'President Trump Hosts "Latinos for Trump" Roundtable in Miami',
                  "President Trump Meeting with Industry Executives",
                  "President Trump Holds Roundtable with Industry Executives",
                  "President Trump Remarks on National Day of Prayer",
                  "President Trump on COVID-19 and School Safety"]
    
    cspantrump = pd.read_csv("{}/DonaldTrump/rawtext_DonaldTrump.tsv".format(directoryin), sep="\t")
    print(len(cspantrump))
    cspantrump = cspantrump[~cspantrump["SpeechTitle"].isin(droptitles)]
    cspantrump = cspantrump.reset_index(drop=True)
    print(len(cspantrump))
    cspantrump.to_csv("{}/DonaldTrump/rawtext_droptitles_DonaldTrump.tsv".format(directoryout), index=False, sep="\t")

    #####################################
    # At this point, some manual curation was needed before proceeding to the next cleaning steps,
    # to identify which speeches were captioned well-enough, their starting and ending points
    # and the speakers segments.
    #####################################

    # trump
    # remove those of low transcript quality? e.g. l ow tr anscrip t quali ty
    # check speeches from white house, south lawn etc: kept? probably audience was press, politicians, etc         
    
    trump_remove = {"CSPANDT27420193": ["YELLING] LOCK HER UP! LOCK HER UP!", "USA! USA! USA! USA!", "SARAH! SARAH! SARAH! SARAH!-THANK YOU, MR. PRESIDENT, FOR LEADING OUR COUNTRY. [CHEERS]",
                                        "FOUR MORE YEARS! FOUR MORE YEARS! FOUR MORE YEARS! FOUR MORE YEARS!", "USA! USA! USA! USA! USA! USA!", "THE WALL! BUILD THE WALL! BUILD THE WALL! BUILD THE WALL! THAT WHILE -- BUILD THE WALL!"],
                    "CSPANDT8520195" : ["USA, USA."],
                    "CSPANDT20520196" : ["FOUR MORE YEARS. [CHANTING] FOUR MORE YEARS. [CHANTING] FOUR MORE YEARS.", "WE LOVE YOU PRESIDENT TRUMP."],
                    "CSPANDT1110201917": ["THANK YOU ALL FOR THE SUPPORT. [CHEERING]"],
                    "CSPANDT1710201918": ["USA USA. USA.", "USA! USA! USA! USA! USA!"],
                    "CSPANDT611201922": [("THANK YOU, THANK YOU SO MUCH. BEFORE I GET STARTED, I WANT TO SAY THIS. CONGRESSMAN ABRAHAM", "GO TIGERS!"), 
                                         ("HELLO, LOUISIANA. THANK YOU MR. PRESIDENT FOR VISITING OUR STATE. IN THREE SHORT YEARS", "AND GOD BLESS THE UNITED STATES OF AMERICA. [CHEERS AND APPLAUSE]"), 
                                        ("THANK YOU SO MUCH. THANK YOU, THANK YOU SO MUCH. MR. PRESIDENT, THANK YOU FOR COMING TO MONROE, LOUISIANA.", "PUT THE HORSE IN THE BARN AND GO WIN A BALLGAME. THANK YOU."), 
                                        ("I GOT IT DOWN TO THIS", "LET'S GO, EDDIE.")],
                    "CSPANDT1411201924": [("WE LOVE PRESIDENT TRUMP, AND HE LOVES LOUISIANA.", "TURN LOUISIANA AROUND AND SUPPORT OUR PRESIDENT IN 2020. GOD BLESS YOU."),
                                          ("HELLO, SHREVEPORT-BOSSIER.", "VOTE FOR EDDIE, AND LET'S GET THIS THING DONE. THANK YOU. [APPLAUSE AND CHEERS]")],                    
                    "CSPANDT141202030": ["USA!", ("WE RAN A TOUGH CAMPAIGN IN WISCONSIN AND I WAS TIRED.", "WE LOVE PRESIDENT TRUMP, GOD BLESS YOU, PRESIDENT TRUMP. [CHEERING AND APPLAUSE]")],
                    "CSPANDT281202033": [("HOW ABOUT HAVING THE PRESIDENT RIGHT HERE IN SOUTH JERSEY?", "OR ARE WE GOING TO KEEP AMERICA GREAT? [CHEERING] I SAY TO ALL OF YOU, MAY GOD BLESS SOUTH JERSEY, MAY GOD BLESS OUR PRESIDENT, AND MAY GOD BLESS THE UNITED STATES OF AMERICA. [CHEERING] [APPLAUSE] [CHEERING] USA. USA. USA. USA."),
                                         ("AND I LOVE YOU BACK. MR. PRESIDENT, I THINK SOUTH JERSEY IS TRUMPED", "LIFE IS GREAT EVERYONE, GOD BLESS YOU. [CHEERING]"),
                                         ("[CHEERS AND APPLAUSE] FOUR MORE YEARS. [CHANTING] FOUR MORE YEARS. [CHANTING] FOUR MORE YEARS. [CHANTING]")],                    
                    "CSPANDT102202036": ["USA. USA. USA. USA. USA."],
                    "CSPANDT192202037": ["CHANTS 'U.S.A.'],AND APPLAUSE],CHANTING 'U.S.A.'],AND APPLAUSE] [CROWD CHANTING 'FOUR MORE YEARS']",
                                         "MR. PRESIDENT, WE ARE GOING TO KEEP ARIZONA RED IN 2020. WE ARE GOING TO RETURN DONALD , PRESIDENT DONALD TRUMP AND VICE PRESIDENT MIKE PENCE TO THE WHITE HOUSE. WE ARE GOING TO RETURN , WE ARE GOING TO KEEP OUR REPUBLICAN MAJORITY IN OUR CONGRESSIONAL DELEGATION AND OUR STATE CHAMBERS. MR. PRESIDENT, THANK YOU FOR WHAT YOU HAVE DONE FOR THE CAUSE OF LIFE. FOR WHAT YOU HAVE DONE FOR OUR ECONOMY AND REDUCING REGULATIONS AND FOR WHAT YOU HAVE DONE FOR THE UNITED STATES SUPREME COURT. WE ARE LOOKING FORWARD TO WORKING WITH YOU FOR FOUR MORE YEARS.",
                                         ("THANK YOU. THANK YOU, EVERYBODY. THANK YOU, MR. PRESIDENT.", "PRESIDENT TRUMP, AND WE WILL WIN IN NOVEMBER. THANK YOU."),
                                         ],
                    "CSPANDT212202039": ["WELCOME. FLU THE WHOLE TEAM OUT FOR THE WEEKEND AND WE OBVIOUSLY THANK THE PEOPLE OF LAS VEGAS FOR HAVING US AND LOOK FORWARD TO CELEBRATING A SPECIAL TIME. IT IS A GREAT HONOR. THANKS FOR HAVING US.",
                                         "YES, WHATEVER YOU SAY. [NO AUDIO]"],
                    "CSPANDT23202041": ["BLUE BOO BOO.", "USA, USA, USA, USA, USA.", "YOU LINDSAY >> USA, USA, USA, USA, USA, USA, USA.", 
                                        ("THANK YOU MISTER PRESIDENT. THANK YOU ALL AGAIN FOR BEING HERE.", "I REPRESENT GET HIM ELECTED FOR FOUR MORE YEARS.")],
                    "CSPANDT249202070": ["FOUR MORE YEARS. FOUR MORE YEARS. FOUR MORE YEARS.", "FOUR MORE YEARS.", "USA. USA. [INDISCERNIBLE]", "USA. USA."],
                    "CSPANDT259202072": ["12 MORE YEARS! 12 MORE YEARS!", "FILL THAT SEAT! FILL THAT SEAT! FILL THAT SEAT! FILL THAT SEAT!"],
                    "CSPANDT309202075": ["FILL THAT SEAT! FILL THAT SEAT! THEFILL THAT SEAT!", "[CHANTING 'FOUR MORE YEARS!'"],
                    "CSPANDT1010202076": ["USA! USA! USA!", "Booo -", "It's not going to happen!", "Four more years! Four more years! Four more years!", "Communist!", "We love you! We love you! We love you!"],
                    "CSPANDT1210202077": ["WE LOVE YOU.", "FOUR FOR MORE YEARS. FOUR MORE YEARS. FOUR MORE YEARS. FOUR MORE YEARS.", "USA. USA."],
                    "CSPANDT1910202087": [("DONALD TRUMP WIN ARIZONA. DONALD TRUMP WILL BE REELECTED PRESIDENT", "VOTE YES FOR DONALD TRUMP AND MIKE PENCE TO GO BACK TO THE WHITE HOUSE. [CHEERING AND APPLAUSE]")],                    
                    "CSPANDT2710202096": [("THE SUBURBS TODAY ARE NOT THE SUBURBS OF HALF A CENTURY AGO.", "IF YOU WANT TO BE SAFE IN YOUR HOME AND YOU WANT YOUR CHILDREN SAFE, SO DONALD TRUMP. (music)"),
                                          "WONDERFUL.", "BACON, BACON, BACON."],
                    "CSPANDT2810202099": ["USA!", "[CHANTING] WE WANT TRUMP EXCAVATION.! WE WANT TRUMP! [CHANTING]", 
                                          ("EVERY TIME I CALL THE PRESENT HE'S GOTTEN ON THE LINE QUICKLY", "THEIR MEMORY IS NOT VERY GOOD QUITE FRANKLY . "),
                                          "USA, USA . ", "WE LOVE YOU, WE LOVE YOU."],                    
                    "CSPANDT31102020103": ["FOUR MORE YEARS! FOUR MORE YEARS!", "LOCK THEM UP! LOCK THEM UP!",
                                            "WE LOVE YOU! WE LOVE!", "USA! USA! USA! USA! USA! USA!"],
                    "CSPANDT1112020105": [("MY PROBLEM IS I VOTED FOR NAFTA.", "I WILL LEAD AN EFFECTIVE STRATEGY TO MOBILIZE. [CHEERS AND APPLAUSE]"),
                                          "AND I WOULD LIKE TO TAKE A SECOND TO PRAY FOR THIS MAN. OUR FATHER AND OUR GOD, WE PRAY FOR OUR PRESIDENT. PROTECT HIM AND HIS FAMILY, AND PROTECT OUR NATION. WE PRAY THIS IN JESUS' NAME, AMEN."],
                    "CSPANDT2112020108": ["FOUR MORE YEARS, FOUR MORE YEARS, FOUR MORE YEARS, FOUR MORE YEARS, FOUR MORE YEARS.", "USA, USA, USA, USA, USA, USA.", "WE LOVE YOU, WE LOVE YOU, WE LOVE YOU, WE LOVE YOU, WE LOVE YOU.",
                                          "[INDISCERNIBLE] (music) [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE] [INDISCERNIBLE]WE HAVE TO DO SEVERAL THINGS. [INDISCERNIBLE] THE CASES BEFORE [INDISCERNIBLE] ENVIRONMENTAL JUSTICE [INDISCERNIBLE] GOT A LOT OF WORK TO DO. [INDISCERNIBLE] WE CANNOT LET THIS COME WE CANNOT [INDISCERNIBLE] CIVIL WAR STRAIGHT THROUGH THE -- TO THE PANDEMIC. WE HAVE NEVER LET OUR DEMOCRACY [INDISCERNIBLE] RECORD OF PUBLIC HEALTH. [INDISCERNIBLE] HERE COMES THE TRAIN. [INDISCERNIBLE] ANYWAY, I'M VERY WILLING TO LET THE AMERICAN PUBLIC JUDGE MY PHYSICAL AND MENTAL BUSINESS. [INDISCERNIBLE] (music)"]}         
         
    # CSPANDT23202041 missing bit at the end, ~7mins, CSPANDT1812201927 missing bit at the end, ~ 20mins     
    cspantrump = pd.read_csv("{}/DonaldTrump/rawtext_droptitles_DonaldTrump_edit1.tsv".format(directoryout), sep="\t")
    
    speechbounds = [("THAT'S REALLY NICE. THANK YOU.", "GOD BLESS YOU, AND GOD BLESS AMERICA. THANK YOU VERY MUCH. THANK YOU."),
                    None,
                    ("THANK YOU. THANK YOU, EVERYBODY. THANK YOU. THANK YOU VERY MUCH, GRAND RAPIDS. IT IS GREAT TO BE BACK. RIGHT HERE IN AMERICA'S HEARTLAND.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU. THANK YOU VERY MUCH. THANK YOU, MICHIGAN."),                    
                    ("UNBELIEVABLE. THANK YOU, HELLO, GREEN BAY. THANK YOU.", "WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, WISCONSIN. THANK YOU."),                    
                    None,
                    ("THANK YOU VERY MUCH EVERYBODY. THANK YOU VERY MUCH. WHAT A CROWD. LOOK AT THAT, THANK YOU.", "WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, FLORIDA."),
                    ("HELLO PENNSYLVANIA. [CHEERS AND APPLAUSE] I AM THRILLED TO BE BACK IN THE STATE THAT GAVE US AMERICAN INDEPENDENCE.", "WE WILL MAKE AMERICA STRONG AGAIN WE WILL MAKE AMERICA SAFE AGAIN AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU. THANK YOU VERY MUCH."),
                    ("WHAT A GROUP. THIS IS A BIG DEAL. THANK YOU VERY MUCH JEFF YOU ARE FANTASTIC. WE APPRECIATE IT.", "I WANT TO THANK IOWA FOR BEING SO GOOD TO ME AND I WILL SAY TONIGHT, GOD BLESS YOU AND GOD BLESS AMERICA. THANK YOU VERY MUCH EVERYBODY. THANK YOU VERY MUCH."),
                    ("PRES. TRUMP: WE HAD SUCH LUCK IN ORLANDO. WE LOVE BEING IN ORLANDO.", "THANK YOU, ORLANDO. THANK YOU, FLORIDA."),
                    ("THANK YOU VERY MUCH. THANK YOU. THANK YOU. THANK YOU TO GREENVILLE, NORTH CAROLINA.", "SO WE WILL KEEP THAT AROUND OUT OF MY HEART THE LOVE OF THAT EXPRESSION BUT OUR NEW PHRASE FOR THE 2020 CAMPAIGN IS KEEP AMERICA GREAT. THANK YOU, NORTH CAROLINA. THANK YOU."),
                    ("THANK YOU ALL, THANK YOU VERY MUCH. THANK YOU TO VICE PRESIDENT MIKE PENCE. AND HELLO, CINCINNATI.", "WE ARE MAKING AMERICA GREAT AGAIN AND WITH YOUR VOTE IN 2020 2020, WE WILL KEEP AMERICA GREAT. THANK YOU, OHIO."),
                    ("THANK YOU VERY MUCH, EVERYBODY, THANK YOU. I WILL NEVER, EVER LET YOU DOWN, THAT I CAN TELL YOU.", "THANK YOU, NEW HAMPSHIRE. THANK YOU."),
                    ("TAKE YOUR TIME PLEASE. TAKE YOUR TIME. THANK YOU DOCTOR. TAKE YOUR TIME.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU EVERYBODY, THANK YOU"),
                    None,
                    ("That's very nice. Thank you. A lot of spirit.", "Remember that. God bless you all. And God Bless America. Thank you."),                    
                    ("THANK YOU. THANK YOU VERY MUCH. THANK YOU MINNESOTA, THIS IS A GREAT STATE.", "WE WILL MAKE THANK YOU MINNESOTA, THANK YOU."),
                    ("I WANT TO THANK THE PEOPLE OF LOUISIANA.", "THANK YOU, LOUISIANA. GET OUT AND VOTE TOMORROW. THANK YOU."),                    
                    ("THANK YOU VERY MUCH. HELLO, DALLAS.", "AND WE WILL MAKE AMERICA GREAT AGAIN! THANK YOU, TEXAS. THANK YOU."),
                    None,
                    ("WELL, THANK YOU VERY MUCH, AND HELLO, TUPELO.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU MISSISSIPPI. THANK YOU."),
                    ("THANK YOU VERY UP. , THANK YOU VERY MUCH. THANK YOU, LEE. I WANT TO SAY HELLO, KENTUCKY.", "THANK YOU, KENTUCKY. THANK YOU. GO OUT AND VOTE."),
                    ("YOU HAVE SPIRIT. HELLO, LOUISIANA.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, LOUISIANA. THANK YOU."),
                    ("THANK YOU. WHAT A GROUP. THANK YOU. I WANT TO THANK YOU ALL. IT IS A BIG CROWD OF PEOPLE.", "THANK YOU ALL VERY MUCH. GOD BLESS AMERICA."),                    
                    ("THANK YOU, VERY MUCH. HELLO, LOUISIANA. HELLO, LOUISIANA.", "WE WILL MAKE AMERICA SAFE AGAIN. HOW WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU. THANK YOU VERY MUCH, LOUISIANA, THANK YOU."),
                    ("WOW. MAN, THIS IS A BIG PLACE. THANK YOU VERY MUCH. THANK YOU TO VICE PRESIDENT MIKE PENCE.", "WE WILL MAKE AMERICA SAFE AGAIN. AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, FLORIDA. THANK YOU VERY MUCH."),
                    ("WILL THANK YOU VICE PRESIDENT PANS, THANK YOU MIKE, AND HELLO PENNSYLVANIA. HELLO.", "BECAUSE TOGETHER WE WILL MAKE AMERICA WEALTHY AGAIN, WE WILL MAKE AMERICA STRONG AGAIN, WE WILL MAKE AMERICA PROUD AGAIN, WE WILL MAKE AMERICA SAFE AGAIN AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU PENNSYLVANIA."),
                    ("THANK YOU. THANK YOU. THANK YOU TO VICE PRESIDENT PENCE, HE IS A GOOD GUY", "AND THEY WERE INTERVIEWING THE PEOPLE, I WILL NEVER FORGET, IT WON AN ISIS AND, REPORTING OUR REPORTER, AND WHAT DID YOU DO?"),
                    ("THANK YOU, VERY MUCH. THAT WAS BEAUTIFUL. THAT WAS BEAUTIFUL. MOST POWERFUL PEOPLE IN THE WORLD.", "THANK YOU, GOD BLESS YOU AND GOD BLESS AMERICA. THANK YOU, THIS WAS A GREAT HONOR. THANK YOU VERY MUCH."),
                    ("THANK YOU VERY MUCH VICE PRESIDENT MIKE PENCE FOR A GOOD JOB YOU'RE DOING. HELLO TOLEDO, WE LOVE TOLEDO.", "WE WILL MAKE AMERICA GREAT AGAIN. IN QUEUE, TOLEDO. THANK YOU."),
                    ("THANK YOU, THANK YOU. HELLO, MILWAUKEE, HELLO.", "WE WILL MAKE AMERICA SAFE AGAIN, AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, WISCONSIN."),
                    ("Well, thank you very much and thank you, Jeanne.", "And God bless America. Thank you all. Thank you."),
                    ("I LOVE NEW JERSEY AND I'M THRILLED TO BE BACK.", "THANK YOU, NEW JERSEY. THANK YOU."),
                    ("YOU JUST GOT TO OF THE GREATEST TRADE DEALS. ADD JAPAN TO IT.", "WE WILL MAKE AMERICA PROUD AGAIN. WE WILL MAKE AMERICA SAFE AGAIN. AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, IOWA. THANK YOU."),
                    None,
                    ("HELLO MANCHESTER, I AM THRILLED TO BE IN THE GREAT STATE OF NEW HAMPSHIRE WHAT THOUSANDS OF HARD-WORKING PATRIOTS", "THANK YOU, NEW HAMPSHIRE, THANK YOU. THANK YOU, NEW HAMPSHIRE!"),
                    ("THANK YOU VERY MUCH, PHOENIX. WE WILL BE BACK A LOT. WE WILL WIN THAT ELECTION, THANK YOU VERY MUCH.", "AND WE WILL MAKE AMERICA GREAT AGAIN! THANK YOU VERY MUCH. THANK YOU, ARIZONA. THANK YOU."),
                    ("THANK YOU. [APPLAUSE] WHERE ELSE WOULD YOU LIKE TO BE BUT I TRUMP RALLY", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, PEOPLE OF COLORADO."),
                    ("THANK YOU VERY MUCH AND LOW LAS VEGAS. THEY HAVE A BIG ELECTION TOMORROW.", "THANK YOU VERY MUCH, EVERYBODY, THANK YOU NEVADA, THANK YOU LAS VEGAS, WE LOVE LAS VEGAS. THANK YOU, EVERYBODY, THANK YOU."),
                    ("THANK YOU. THANK YOU. THANK YOU.", "WE WILL MAKE AMERICA SAFE AGAIN, AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, SOUTH CAROLINA. THANK YOU."),
                    ("I WANT TO THANK YOU NORTH CAROLINA WANT TO THANK YOU VERY MUCH.", "WE WILL DEFEND PRIVACY, FREE SPEECH, RELIGIOUS LIBERTY AND THE RIGHT TO KEEP AND BEAR ARMS."),
                    ("THANK YOU. SO WE BEGIN.", "THANK YOU. THANK YOU, OKLAHOMA. THANK YOU."),
                    ("Thank you very much. Thank you. Thank you very much. Go ahead. Sit down.", "And God bless America. Thank you very much. Thank you."),
                    ("We're here today to celebrate and expand our historic campaign to rescue American workers from job-killing regulations.", "Great job. Thank you very much. Thank you, everybody."),
                    ("thank you very much wow.", "we will win and we will make America great again"),
                    ("WELL, THANK YOU VERY MUCH, MINNESOTA.", "THANK YOU VERY MUCH. I WILL BE BACK, NOVEMBER 3, WE HAVE TO WIN, GOD BLESS YOU, GOD BLESS THE GREAT STATE OF MINNESOTA, GOD BLESS AMERICA. THANK YOU ALL VERY MUCH."),
                    ("THANK YOU VERY MUCH IN CONSIDERING WE SAW PRESIDENT OBAMA AND SLIPPAGE OF CAMPAIGN SPYING ON OUR CAMPAIGN WE WILL PROBABLY BE ENTITLED TO ANOTHER FOUR MORE YEARS.", "WE WILL NEVER LET YOU DOWN. GOVERNORS THANK YOU. GO OUT AND WHEN RATED BOAT MCSALLY."),
                    ("THANK YOU VERY MUCH. THIS IS GREAT. WE LOVE THE STATE.", "WE ARE GOING TO HAVE A VICTORY THAT WILL EQUAL OR SURPASS WHAT WE DID IN 2016. THANK YOU ALL VERY MUCH. THANK YOU VERY MUCH. THANK YOU."),
                    ("YOU ARE REALLY FANTASTIC. THANK YOU VERY MUCH.", "AND I HAVE NO DOUBT THAT OUR COUNTRY WILL BE GREATER THAN EVER BEFORE. THANK YOU, ALL, VERY MUCH."),
                    ("THANK YOU, PENNSYLVANIA. I AM THRILLED TO BE HERE IN THE HOME OF THE LATE GREAT, MY FRIEND, ARNOLD PALMER.", "THANK YOU, PENNSYLVANIA."),
                    ("THANK YOU VERY MUCH. IT'S A GREAT HONOR TO BE IN NORTH CAROLINA.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU."),
                    ("WE BROUGHT YOU A LOT OF CAR PLANTS, MICHIGAN.", "THANK YOU, MICHIGAN. WE LOVE YOU, MICHIGAN. THANK YOU."),
                    ("BEAUTIFUL. WOULD A CROWD THIS ONE IS.", "WE WILL MAKE AMERICA SAFE AGAIN AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU VERY MUCH, EVERYBODY. THANK YOU."),
                    ("Well, thank you very much. Thank you. Thank you. Great to be with you and a very special. Hello, Nevada.", "On we will make America great again. Thank you. Thank you, everybody. Thank you."),
                    None,
                    ("THANK YOU. THANK YOU VERY MUCH. [CHANTING U.S.A.] [CHEERS] THANK YOU VERY MUCH. THAT IS A BEAUTIFUL SIGHT RIGHT BEHIND ME, RIGHT?", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, WISCONSIN. THANK YOU."),
                    ("THIS IS A LOT OF PEOPLE. THANK YOU VERY MUCH.", "WE WILL MAKE AMERICA SAFE AGAIN. AND WE WILL MAKE AMERICA GREAT AGAIN."),
                    ("WHAT A CROWD. WHAT A CROWD. GET THOSE PEOPLE OVER HERE, LET'S GIVE THEM A HAND.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU VERY MUCH. GET OUT AND VOTE. VOTE. VOTE. VOTE."),
                    ("THANK YOU VERY MUCH OHIO, THANK YOU VERY MUCH, THANK YOU.", "WE LOVE OHIO, WE LOVE DANE, GOD LAST YEAR, GOD BLESS OHIO, AND GOD BLESS AMERICA."),
                    ("Wow. Brown is a big ground. Yeah, thank you very much. Everybody and hello to Swanton and hello to Toledo.", "We will make America great again. Thank you, Ohio."),
                    ("THANK YOU VERY MUCH, PITTSBURGH. YOU HAVE ALWAYS TREATED ME WELL.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU. THANK YOU, PENNSYLVANIA. THANK YOU."),
                    None,
                    ("HELLO, JACKSONVILLE. WE LOVE JACKSONVILLE.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, FLORIDA. THANK YOU, FLORIDA"),
                    ("Yeah, thank you very much. Hello, Newport News.", "Thank you, Virginia. Thank you. Get out and vote. Thank you."),
                    ("THANK YOU. AND THANK YOU TO HERSCHEL. I DON'T KNOW ABOUT HERSCHEL.", "GOD BLESS YOU AND GOD BLESS AMERICA."),
                    ("WELL, WE WON PENNSYLVANIA LAST TIME AND WE ARE GOING TO WIN IT BY A LOT MORE THIS TIME.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, VERY MUCH. THANK YOU, PENNSYLVANIA. GO OUT AND VOTE."),
                    ("HELLO, EVERYBODY. HELLO, DULUTH. WE ARE GOING TO WIN MINNESOTA.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, MINNESOTA."),                    
                    ("WELL, THANK YOU VERY MUCH AND KEEP THAT ENTHUSIASM GOING.", "GET OUT AND VOTE, AND I LOVE YOU. THANK YOU. THANK YOU VERY MUCH. THANK YOU."),                    
                    ("HELLO EVERYBODY. IT IS GREAT TO BE WITH YOU. THANK YOU. THANK YOU. YOU KNOW OUR COMPETITORS AT A RALLY TODAY PRACTICALLY NOBODY SHOWED UP.", "BECAUSE WE ARE ONE MOVEMENT, ONE MOVEMENT, ONE FAMILY ONE GLORIOUS NATION UNDER GOD."),
                    ("HELLO, JOHNSTOWN. IT'S INCREDIBLE TO BE BACK IN PENNSYLVANIA, THE PROUD HOME OF AMERICAN INDEPENDENCE, THE AMERICAN CONSTITUTION, AND AMERICAN FREEDOM.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU VERY MUCH PENNSYLVANIA. GET OUT AND VOTE."),
                    ("THANK YOU VERY MUCH EVERYBODY. HELLO DES MOINES.", "THANK YOU, IOWA. THANK YOU. THANK YOU VERY MUCH."),
                    None,
                    ("THANK YOU VERY MUCH . THANK YOU, LET'S SEE . IT'S 1:30. THIS IS A HELL OF A CROWD FOR 1:30 IN THE AFTERNOON .", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU EVERYBODY. GO OUT AND VOTE."),
                    ("Thank you very much. Unbelievable. Can you believe how many people look behind the fake news?", "We will make America safe again. On we will make America great again. Thank you. Get out and vote."),
                    ("I LOVE GEORGIA. I LOVE BEING WITH YOU. THIS IS GEORGIA. THANK, GEORGIA. WE WON GEORGIA.", "WE WILL MAKE AMERICA SAFE AGAIN. AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU."),
                    ("THANK YOU VERY MUCH, THANK YOU. WHAT A CROWD.", "THANK YOU, MICHIGAN. GO OUT AND VOTE."),                    
                    ("Thank you. Very well. This is great. Hello, How are you?", "We have made America safe again. And we will make America great again. Thank you, Wisconsin."),
                    ("You see what's going on to the road all the way up here? We have people all the way up.", "We have made America safe again And we will make America great again. Get out and vote. Thank you."),
                    ("THANK YOU, THANK YOU. WHAT A CROWD. THANK YOU, TUCSON. THANK YOU, TUCSON.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU VERY MUCH. THANK YOU, ARIZONA. GET OUT AND VOTE. GET OUT AND VOTE. THANK YOU."),
                    ("Thank you very much. Hello, Eerie. Remember that great victory", "Go out and vote. Go out and vote. Thank you, Pennsylvania."),
                    ("WELL, THIS IS A BIG CROWD. THIS IS ONE HELL OF A BIG CROWD.", "THANK YOU, NORTH CAROLINA. THANK YOU. GO AND VOTE. THANK YOU VERY MUCH."),
                    ("IT'S GREAT TO BE WITH YOU. IT'S SOMETHING I'VE WANTED TO DO, I WAS HERE FOUR YEARS AGO IN SOME LITTLE BALLROOM THAT HELD ABOUT 400 PEOPLE, AND I SAID, I WANT TO BE WITH THE VILLAGES.", "THANK YOU, VILLAGES. WE LOVE YOU, VILLAGES. THANK YOU. GREAT TO BE HERE. THANK YOU. THANK YOU. GET OUT AND VOTE."),
                    ("Hello, Pensacola. Hello Florida way.", "Thank you, Florida. Thank you, Alabama."),
                    ("THANK YOU VERY MUCH, AND HELLO, CIRCLEVILLE.", "WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU."),
                    ("THANK YOU VERY MUCH. THANK YOU. WHAT A GROUP, WHAT A GROUP. WE LOVE THIS PLACE.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, NEW HAMPSHIRE. THANK YOU."),                    
                    ("THANK YOU, VERY MUCH. HELLO. HELLO. WE TRIED TO COME HERE VERY LOW-KEY.", "WE HAVE MADE AMERICA SAFE AGAIN AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, PENNSYLVANIA. THANK YOU VERY MUCH."),
                    ("I want to start off by saying a very big. Hello, Wisconsin.", "Thank you, Wisconsin. Thank you very much. Get out and vote."),
                    ("THAT'S A LOT OF PEOPLE. LOOK AT THAT.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, NEBRASKA, THANK YOU IOWA, THANK YOU, GET OUT AND VOTE."),
                    ("Well, thank you very much. Thank you. I feel so guilty awaiting out here in the rain.", "Thank you, Michigan. Go out and vote."),
                    ("Hello, Phoenix. Six days.", "Thank you very much. Thank you, Arizona. Go out and vote. Thank you."),
                    ("THANK YOU VERY MUCH. WHAT A CROWD. THIS IS QUITE A CROWD. HELLO, ARIZONA.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU VERY MUCH . GO OUT AND DEVOTE TO GO OUT AND VOTE. THANK YOU EVERYBODY"),
                    ("THANK YOU VERY MUCH. THAT WAS A LITTLE BIT OF A SURPRISE", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU. GET OUT AND VOTE. THANK YOU."),
                    ("THANK YOU VERY MUCH, I APPRECIATE IT. AND, HELLO ROCHESTER, THANK YOU FOR BEING HERE, FOUR DAYS FROM NOW WE ARE GOING TO WIN THE STATE OF MINNESOTA.", "GOD BLESS YOU, GOD BLESS MINNESOTA, AND GOD BLESS AMERICA. THANK YOU FOR BEING HERE. WE APPRECIATE IT. THANK YOU. THANK YOU, EVERYBODY. [APPLAUSE] THANK YOU, EVERYBODY. NICE SEEING YOU, MATT. THANK YOU, EVERYBODY."),                    
                    ("Thank you very much. Hello, Pennsylvania. Let's go, Pennsylvania.", "Thank you, Pennsylvania. Thank you. Thank you very much. Go out and vote. Thank you, everybody."),                    
                    ("WOW. GOOD CROWD. THIS IS A HELL OF A CROWD. THANK YOU. THANK YOU. WOW.", "AND WE WILL MAKE AMERICA GRETAT AGAIN. THANK, PENNSYLVANIA. , THANK YOU VERY MUCH, PENNSYLVANIA. THANK YOU VERY MUCH."),
                    ("Wow, there's a big crowd. There's a very big yeah, look at all those cameras over there. Can you show the crowd? You know, Could you show this crib?", "Thank you, Pennsylvania. Go out and vote."),
                    ("THANK YOU VERY MUCH. WOW. THIS IS A VERY BIG CROWD. WHILE, LOOK AT THIS. HELLO, NORTH CAROLINA.", "WE HAVE MADE AMERICA PROUD AGAIN. WE HAVE MADE AMERICA SAFE AGAIN. AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, NORTH CAROLINA. GO OUT AND VOTE. THANK YOU. THANK YOU."),
                    ("Well, thank you very much. And hello, Kenosha.", "We have made America safe again and we will make America great again. Thank you, Wisconsin. Thank you, Wisconsin. Go out and vote. Thank you."),
                    ("Thank you. Wow. There's a big crowd. We have a lot of big crowds, but there's a big This is Thank you very much. Hello, Traverse City.", "And we will make America great again. Thank you, Michigan. Go out and vote. Thank you very much."),
                    ("THANK YOU VERY MUCH. THANK YOU. THANK YOU VERY MUCH. THANK YOU. THIS DOES NOT LOOK LIKE A SECOND-PLACE FINISH.", "WE HAVE MADE AMERICA SAFE AGAIN. AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, PENNSYLVANIA. THANK YOU, PENNSYLVANIA."),
                    ("Thank you very much. Tomorrow we are going to win this state and we're going to win four more years and our great White House With your vote", "We have made America proud again. We have made America safe again on we will make America great again. Thank you, North Carolina. Thank you. Go out and vote"),                    
                    None,                    
                    ("Good evening. I'd like to provide the American people with an update on our efforts to protect the integrity of our very important 2020 election.", "But there's been a lot of shenanigans, and we can't stand for that in our country. Thank you very much."),
                    ("WE HAVE ELECTION DAYS, WEEKS AND MONTHS AND LOTS OF BAD THINGS HAPPENED DURING THIS RIDICULOUS PERIOD OF TIME", "WE WILL RESTORE TRUST IN OUR SYSTEM OF GOVERNMENT. THANK YOU. GOD BLESS YOU. AND GOD BLESS AMERICA."),
                    ("THANK YOU. A VERY POPULAR FIRST LADY, I HAVE TO SAY. THANK YOU VERY MUCH AND THANK YOU, MELANIA.", "AND WE WILL MAKE AMERICA GREAT AGAIN. THANK YOU, GEORGIA. GET OUT AND VOTE. GET OUT AND VOTE."),
                    ("I WANT TO THANK YOU VERY MUCH. HELLO, GEORGIA. BY THE WAY, THERE IS NO WAY WE LOST GEORGIA.", "GO GET 'EM DAVID. GO GET 'EM KELLY. GO GET 'EM. TOMORROW."),
                    ("Media will not show the magnitude of this crowd. Even I When I turned on today, I looked on.", "And God bless America. Thank you all for being here. This is incredible. Thank you very much. Thank you.")] 
    trumpdf = {"SpeechID": [],	"POTUS": [], "Date": [], "SpeechTitle": [],	"RawText": [],	"SpeechURL": [], "Summary": [], "Source": [], "Type": [], "SpeechSegment": []}
    for i, row in cspantrump.iterrows():       
        remainingstr = None
        if speechbounds[i] is None:
            print(i+2) # csv _edit1 row 
            print(row.SpeechURL)                                            
            continue
        if row.RawText == row.SpeechID:
            with open("{}DonaldTrump/specialcleanneeded/{}.txt".format(directoryin, row.SpeechID), "r") as f:
                content = f.read()
                row.RawText = content                
        if row.RawText is None:
            ipdb.set_trace()
        s1, s2 = speechbounds[i]
        remainingstr = find_substring(row.RawText, s1, s2)       
        if s1 not in row.RawText or s2 not in row.RawText or remainingstr is None:
            print(i+2) # csv _edit1 row 
            print(row.SpeechURL)
            print(row.RawText)
            print(speechbounds[i])            
            ipdb.set_trace()                
        if remainingstr is not None:
            row["SpeechSegment"] = remainingstr
            trumpdf["SpeechID"].append(row["SpeechID"])
            trumpdf["POTUS"].append(row["POTUS"])
            trumpdf["Date"].append(row["Date"])
            trumpdf["SpeechTitle"].append(row["SpeechTitle"])
            trumpdf["RawText"].append(row["RawText"])
            trumpdf["SpeechURL"].append(row["SpeechURL"])
            trumpdf["Summary"].append(row["Summary"])
            trumpdf["Source"].append(row["Source"])
            trumpdf["Type"].append(row["Type"])
            trumpdf["SpeechSegment"].append(row["SpeechSegment"])
    trumpdf = pd.DataFrame.from_dict(trumpdf).sort_values(by=["Date"]).reset_index(drop=False)
    trumpdf.to_csv("{}/DonaldTrump/rawtext_droptitles_DonaldTrump_edit2.tsv".format(directoryout), sep="\t", index=False)
    trumpdf = remove_candidates_dicts(trumpdf, trump_remove)        
    trumpdf.SpeechSegment = trumpdf.SpeechSegment.apply(remove_trump)
    trumpdf.SpeechSegment = trumpdf.SpeechSegment.apply(remove_dots)
    trumpdf.SpeechSegment = trumpdf.SpeechSegment.apply(remove_square_brackets)
    trumpdf.SpeechSegment = trumpdf.SpeechSegment.apply(remove_round_brackets)    
    if show:    
        for i, row in trumpdf.iterrows():        
            print(row.SpeechURL)
            print(row.SpeechSegment)
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)
    trumpdf.to_csv("{}/DonaldTrump/cleantext_DonaldTrump.csv".format(directoryout), sep="\t", index=False)


    
if __name__ == "__main__":
    
    # drop: 'VSDT1612019316', 'VSDT2110202062', 'VSDT2442020167', 'VSDT812202037'
    potus = "DonaldTrump"

    directoryin = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data/votesmart/"
    directoryout = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data_clean/votesmart/"
    clean_votesmart(directoryin, potus, directoryout, textclean_votesmart, unicode_class="NFC", show=True, extra2remove=remove_containing_speeches)

    directoryin = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data/millercenter/"
    directoryout = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data_clean/millercenter/"
    clean_miller(directoryin, potus, directoryout, textclean_miller, unicode_class="NFC", show=True)
    