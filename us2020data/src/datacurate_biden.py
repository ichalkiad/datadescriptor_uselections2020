import ipdb
import pandas as pd
from us2020data.src.utils import textclean_votesmart, textclean_miller, \
                                    textclean_medium, clean_miller, \
                                    clean_votesmart, clean_cspan, clean_medium
import pathlib

if __name__ == "__main__":
    
    drop_column = "SpeechID"
    potus = "JoeBiden"
    toplevel = pathlib.Path.cwd()
    
    # Vote Smart
    directoryin = "{}/us2020data/data/votesmart/".format(toplevel)
    directoryout = "{}/us2020data/data_clean/votesmart/".format(toplevel)
    pathlib.Path("{}/{}/".format(directoryout, potus)).mkdir(parents=True, exist_ok=True)    
    drop_speechID = pd.read_csv("{}/{}/drop_speech_id.tsv".format(directoryin, potus), sep="\t")   
    drop_speechID = drop_speechID.SpeechIDdrop.values.tolist()
    clean_votesmart(directoryin, directoryout, potus, textclean_votesmart, "NFC", True, drop_speechID, drop_column)
    
    # The Miller Center
    directoryin = "{}/us2020data/data/millercenter/".format(toplevel)
    directoryout = "{}/us2020data/data_clean/millercenter/".format(toplevel)
    pathlib.Path("{}/{}".format(directoryout, potus)).mkdir(parents=True, exist_ok=True)          
    clean_miller(directoryin, directoryout, potus, textclean_miller, unicode_class="NFC", show=True)

    # C-SPAN
    directoryin = "{}/us2020data/data/cspan/".format(toplevel)
    directoryout = "{}/us2020data/data_clean/cspan/".format(toplevel)
    pathlib.Path("{}/{}".format(directoryout, potus)).mkdir(parents=True, exist_ok=True)   
    cspan = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")            
    drop_speechID = pd.read_csv("{}/{}/drop_speech_id.tsv".format(directoryin, potus), sep="\t")       
    drop_speechID = drop_speechID.SpeechIDdrop.values.tolist()    
    cspan = cspan[~cspan[drop_column].isin(drop_speechID)] 
    cspan = cspan.reset_index(drop=True)  
    cspan.to_csv("{}/{}/rawtext_droptitles_{}.tsv".format(directoryin, potus, potus), index=False, sep="\t")   

    #####################################
    # At this point, some manual curation was needed before proceeding to the next cleaning steps,
    # to identify which speeches were captioned well-enough, their starting and ending points
    # and the speakers segments.
    #####################################

    # remove: TAKE ON THE OIL AND GAS LOBBYISTS, NOT TO BE TIED DOWN BY CAMPAIGNS OWNERS. - 22
    # 25 : interrupted, conversational, baq quality transcription    
    
    biden_remove = {"CSPANJB33202058": ["LET HER STAY!, LET HER GO! LET HER GO! [CHANTING]"], "CSPANJB18102020116": [">> --"], "CSPANJB412021150": ["WE LOVE YOU."]}
    speechbounds = [("HEY, FOLKS. HOW ARE YOU? GOD, I LOVE YOU.", "I MEAN IT. DON'T GIVE UP! KEEP IT GOING! WHEN JOB SHOULD BE ENOUGH. THANK YOU."),
                    ("THAT'S HOW I'M KNOWN BACK HOME.", "THERE IS NOT A SINGLE THING BEYOND OUR CAPACITY, NOT A SINGLE THING. SO GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS! THANK YOU!"),
                    ("I LOVE THIS CITY, MY FAMILY DOES", "GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU. THANK YOU. THANK YOU, THANK YOU, THANK YOU, IT IS GOOD TO BE BACK."),                    
                    ("Good to be back into Hampshire thank you", "tell me I can take some credit I'm going to give you a microphone."),                    
                    ("PARENTS WHO COULD NOT AFFORD TO TAKE CARE OF THEIR CHILDREN'S HEALTH CARE.", "[APPLAUSE] WE ARE THE UNITED STATES OF AMERICA. [APPLAUSE] THERE IS NOT A SINGLE THING WE CANNOT DO IF WE DO IT TOGETHER."),
                    None,
                    ("IT'S SO GOOD TO SEE YOU. JIM IS A GREAT-GREAT FRIEND, I'VE KNOWN HIM FOR A LONG TIME.", "THERE'S NOT A SINGLE THING BEYOND OUR CAPACITY TO DO. TOGETHER, GOD BLESS YOU ALL. AND MAY GOD PROTECT OUR TROOPS. THANK YOU-THANK YOU-THANK YOU."),
                    ("THANK YOU. MY TIME'S RUNNING. HEY, THANK YOU, EVERYBODY.", "GOD BLESS YOU, AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU. THANK YOU, APPRECIATE IT."),
                    ("THANK YOU, REVEREND. WELL, I AM HERE TO INTRODUCE, ANOTHER BIDEN", "SO LADIES AND GENTLEMEN, WE HAVE TO REMEMBER WHO WE ARE, PICK OUR HEADS UP, AND GOD BLESS YOU ALL, AND GOD BLESS OUR. TROOPS. THANK YOU. [APPLAUSE]"),                   
                    ("MR. MAYOR, THANK YOU VERY MUCH. HOW MANY OF YOU HAVE LOST SOMEONE TO CANCER OR ARE FIGHTING IT NOW?", "MAY GOD BLESS YOU AND MAY GOD PROTECT OUR COUNTRY. THANK YOU. WE CAN DO THIS. I PROMISE YOU. [APPLAUSE] [INAUDIBLE CONVERSATIONS]"),                    
                    ("MR. PRESIDENT, CHANCELLOR, THANK YOU FOR HOSTING US AND FOR WELCOMING GENERATIONS, LITERALLY GENERATIONS OF NEW AMERICANS TO A WIDER AND BIGGER AND MORE OPTIMISTIC FUTURE.", "THANK YOU FOR LISTENING TO A VERY THOROUGH SPEECH. MAY GOD BLESS YOU ALL, AND MAY GOD PROTECT OUR TROOPS. THANK YOU. [ APPLAUSE ] [ APPLAUSE ]"),
                    ("IT IS REALLY GREAT TO BE HERE. YOU KNOW, THE FACT OF THE MATTER IS THAT I GOT TO TALK TO SOME OF THE FOLKS INSIDE", "BUT REALLY, THANK YOU FOR BEING ENGAGED. EVERY TIME I WALKED OUT OF MY GRANDPA'S HOUSE, KEEP THE FAITH. JOEY, GO SPREAD IT. GO SPREAD THE FAITH."),
                    ("THANK YOU VERY MUCH. FOLKS, THANK YOU VERY, VERY MUCH FOR BEING HERE TO GIVE ME THIS OPPORTUNITY.", "THERE IS NOT A SINGLE THING BEYOND OUR CAPACITY, IF WE STAND TOGETHER AND GET UP AND REMEMBER WHO WE ARE. THIS IS THE UNITED STATES OF AMERICA. PERIOD. THANK YOU, AND MAY GOD PROTECT OUR TROOPS."),
                    ("HELLO, IOWA. GOOD TO SEE YOU ALL. I AM JILL BIDEN'S HUSBAND. I'M GOING TO BE VERY BRIEF AND QUICK WITH YOU. I'M RUNNING FOR THREE REASONS.", "WE MUST DEFEAT THIS PRESIDENT TO CHANGE THE TRAJECTORY OF THIS COUNTRY."),                    
                    ("THANK YOU, THANK YOU, THANK YOU. HELLO, KEENE.", "WE THE PEOPLE ARE CO GOD BLESS YOU ARE AND MAY GOD PROTECT OUR TROOPS. THANKS FOR BEING HERE. I APPRECIATE YOU. THANK YOU, THANK YOU, THANK YOU. WHERE AM I GOING?"),                    
                    ("HELLO, NEW HAMPSHIRE. GREAT TO BE HERE. THANK YOU, THANK YOU, THANK YOU. THEY TOLD ME I HAVE ABOUT 10 MINUTES. I BETTER GET GOING. MY NAME IS JOE BIDEN AND I AM HERE FOR JEANNIE CHICANE.", "THIS IS OUR MOMENT. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU. THANK YOU."),
                    ("A LOT OF YOU HAVE BEEN INVOLVED IN PUBLIC LIFE, SOME OF YOU HAVE RUN, SOME OF YOU HAVE BEEN ELECTED.", "THANK YOU FOR LISTENING. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU."),
                    ("HELLO FOLKS HOW ARE YOU? [CHEERS AND APPLAUSE] THANK YOU. THANK YOU. THANK YOU. I HAVE TO TELL YOU SHE WRITES ABOUT SHE IS SERIOUS AND MEANS A GREAT DEAL TO ME AT THAT TIME SHE WOULD ENDORSE ME.", "THAT'S MY INTENTION. THANK YOU GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS."),
                    ("HELLO FOLKS. HOW ARE YOU DOING? MY NAME IS JOE BIDEN I'M JILL BIDEN'S HUSBAND AND VALERIE'S BROTHER", "THANK YOU FOR PROTECTING THE TROOPS AND THANK YOU FOR HAVING ME."),
                    ("THANK YOU. HELLO, FOLKS. HOW ARE YOU? THANK YOU.", "GOD BLESS YOU ALL AND GOD BLESS OUR TROOPS. THANK YOU. THANK YOU. THANK YOU."),                    
                    ("THANK YOU, HONEY. I APPRECIATE IT. THIS IS A WOMAN WHO HAS BEEN A PROFESSIONAL EDUCATOR", "THANK YOU, THANK YOU FOR BEING HERE. I PROMISE YOU YOU'RE PROBABLY GOING TO SEE MORE OF ME THAN YOU WANT TO SEE, BUT I PLAN ON WINNING IOWA. THANK YOU."),                    
                    ("I WANT TO THANK YOU FOR COMING OUT. YOU HAVE BEEN STANDING OUT HERE A WHILE.", "THANK YOU ALL FOR BEING HERE. I LOVE YOU. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU."),
                    ("THANK YOU, SENATOR. THANK YOU, THANK YOU, THANK YOU. THANK YOU, THANK YOU, THANK YOU. THANK YOU. YOU ARE VERY GRACIOUS.", "THANK YOU FOR LISTENING. THANK YOU FOR HAVING ME. LET ME INTRODUCE TO YOU THE BETTER HALF OF MY FAMILY, DR. JILL BIDEN."),
                    None,
                    ("IT'S GOOD TO BE BACK. GOOD TO BE BACK IN NASHVILLE.", "HE WOULD YELL JODEY, KEEP THE FAITH. SPREAD THE FAITH. WE CAN DO ANYTHING."),
                    ("I HOPE YOU WILL CONSIDER COMING OUT AND CAUCUSING FOR ME ON 43RD.", "PERHAPS MOST IMPORTANTLY OF ALL, THE COUNTRY NEEDS YOU. THANK YOU VERY MUCH."),
                    ("HELLO. [INAUDIBLE] THANK YOU. THANK YOU, THANK YOU, THANK YOU, THANK YOU. MY GOODNESS.", "MY MOTHER WOULD OFTEN SAY JOEY, HUSH UP AND TAKE SOME QUESTIONS."),
                    ("THANK YOU, THANK YOU. THANK YOU. THANK YOU, THANK YOU, THANK YOU. WELL, FOLKS, THE FOLKS IN MY HOME STATE OF DELAWARE AND THE STATE OF CALIFORNIA", "IT IS TIME TO GET UP, TAKE IT BACK, LEADING THE WORLD AGAIN AND GIVE OUR CHILDREN A DIFFERENT LOOK."),
                    ("GOOD AFTERNOON, FOLKS. THANK YOU FOR BEING HERE.", "WE NEED ACTION, MR. PRESIDENT. YOU HAVE TO EXPLAIN WHAT YOU'RE DOING. THANK YOU VERY MUCH."),
                    ("HELLO, CLAREMONT. I COULD BE , THE HISTORY OF CLAREMONT, I COULD BE IN SCRANTON OR CLAREMONT", "GIVE ME A LOOK. OK? THANK YOU, ALL VERY VERY MUCH FOR BEING HERE."),
                    ("HELLO, HELLO, HELLO. SYRACUSE.", "SO I'M GOING TO TRY MY BEST AND IF I'M, NOT GOING TO CALL MY SISTER, GRABBED JOE BY THE AIR AND PULL HIM, OUT BUT I PROMISE YOU, I'M NOT GOING TO. I WOULD TAKE A COUPLE MORE QUESTIONS. YES SIR."),
                    ("THANK YOU, THANK YOU, THANK YOU, THANK YOU. IT'S GOOD TO SEE YOU GUYS AGAIN. THANK YOU FOR BEING HERE.", "AND NO ONE, NOT EVEN THE PRESIDENT OF THE UNITED STATES, WILL BE ABOVE THE LAW, I PROMISE YOU. GOD BLESS YOU ALL, AND MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("IT LOOKS LIKE IT WILL BE A LONG NIGHT, BUT I FEEL GOOD.", "MAY GOD BLESS YOU ALL AND PROTECT OUR TROOPS. THANK YOU. ON TO NEW HAMPSHIRE."),
                    ("HELLO, HELLO, HELLO, HELLO. I AM JOE BIDEN, JILL BIDEN'S HUSBAND AND VALERIE BIDEN'S BROTHER.", "GOD BLESS YOU ALL, MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU. FOR YOUR PATIENCE."),
                    ("THANK YOU. THANK YOU. THANK YOU. I APPRECIATE IT. HELLO, NEW HAMPSHIRE.", "GOD BLESS YOU ALL. MAY GOD PROTECT OUR TROOPS. LET'S GO DO IT NOW. NOW. NOW. THANK YOU ALL SO MUCH."),
                    ("WHOA, HELLO, EVERYBODY. HELLO, HELLO, HELLO, HELLO. IT'S GREAT TO BE IN HUDSON. I, YOU KNOW, I'M HAPPY TO BE HERE.", "MY MOTHER, SHE WOULD SAY JOEY, HUSH UP AND TAKE SOME QUESTIONS."),                    
                    ("THANK YOU. THANK YOU VERY MUCH. WE KNEW THIS WAS GOING TO BE A DIFFICULT RACE BECAUSE OUR POLITICS HAVE GOTTEN SO COARSE", "SO LET'S GET UP AND TAKE BACK THIS COUNTRY, TAKE IT BACK NOW. GOD BUSHY WELL AND MAY GOD PROTECT HER CHILDREN."),                    
                    ("THANK YOU. YOU HAVE NO IDEA HOW GREAT IT IS TO BE BACK IN SOUTH CAROLINA. GREAT TO BE WITH YOU ALL TONIGHT.", "LET'S GET TO WORK. THANK YOU. MAY GOD BLESS YOU ALL AND MAY GOD AFFECT OUR TROOPS."),
                    ("THANK YOU VERY MUCH, GARY.", "WE ARE GOING TO TAKE BACK THIS COUNTRY, AND BECOME THE ENVY OF THE WORLD AGAIN. MAY GOD PROTECT OUR TROOPS."),
                    ("GOOD MORNING, EVERYONE. I WANT TO THANK YOU ALL FOR COMING OUT. THIS BEAUTIFUL LAS VEGAS MORNING.", "THANK YOU FOR LISTENING. I'M GOING TO SPEND SOME TIME WITH THESE FOLKS. THANK YOU."),
                    ("NOW WE ARE GOING ON TO SOUTH CAROLINA AND WIN THE DEMOCRATIC STATE BACK.", "THANK YOU, THANK YOU, THANK YOU! I PLAN ON COMING BACK."),
                    ("THANK YOU. THANK YOU. THANK YOU, THANK YOU, THANK YOU, SOUTH CAROLINA.", "GOD BLESS YOU ALL, AND MAY GOD PROTECT OUR TROOPS."),
                    ("HELLO, NORFOLK.", "GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU. THANK YOU, THANK YOU."),
                    ("THANK YOU. HELLO, DALLAS. AS MY MOM WOULD SAY, I APOLOGIZE FOR MY BACK. IF YOU HAVE MY BACK I PROMISE I WILL HAVE YOURS.", "WE ARE BETTER THAN THIS MOMENT AND BETTER THAN THIS PRESIDENT SO GET UP GRADE THAT'S TAKE BACK THIS COUNTRY FOR THE UNITED STATES OF AMERICA. THERE IS NOT A SINGLE THING WE CANNOT DO IF WE DO IT TOGETHER. GOD BLESS YOU ALL AND PROTECTIVE TROOPS."),
                    ("THANK YOU, THANK YOU, THANK YOU. LET ME START OFF BY THANKING SHEILA JACKSON LEE FOR THE ESCORT INTO TOWN. THANK YOU VERY MUCH.", "WE'RE THE UNITED STATES OF AMERICA. THERE'S NOTHING WE CANNOT DO IF WE DO IT TOGETHER. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. LET'S TAKE IT BACK NOW! NOW, NOW, NOW! [CHEERS AND APPLAUSE] THANK YOU."),
                    ("HELLO, HELLO, HELLO! IT'S A GOOD NIGHT! IT'S A GOOD NIGHT! AND IT SEEMS TO BE GETTING EVEN BETTER!", "THERE IS NOT A SINGLE THING WE CAN'T DO. GOD BLESS YOU AND MAY GOD PROTECT OUR TROOPS! THANK YOU, THANK YOU, THANK YOU!"),
                    ("FOLKS, IT'S GOING TO BE VERY SHORT AND I WANTED TO COME DOWN AND BEGIN BY THANKING EVERYONE FOR BEING HERE.", "I JUST WANTED TO MAKE A STATEMENT BEFORE I HEADED OUT. I'M DOING ANOTHER INTERVIEW IN A MOMENT. BUT I THANK YOU ALL AND I THANK EVERYONE FOR COMING."),
                    ("THANK YOU. THANK YOU FOR EVERYTHING YOU HAVE DONE TO SUPPORT THIS CAMPAIGN", "WE ARE THE UNITED STATES OF AMERICA AND THERE IS NOTHING BEYOND OUR CAPABILITY IF WE DO IT TOGETHER. GOD BLESS YOU ALL, AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU. THANK YOU. THANK YOU."),
                    ("HELLO, DETROIT. THANK YOU ALL FOR COMING OUT TONIGHT I CAN'T TELL YOU HOW MUCH I APPRECIATE IT.", "SO LET'S TAKE THIS BACK NOW. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. TAKE IT BACK. IT'S TIME. THANK YOU."),
                    ("LET ME BEGIN BY SAYING THAT I HAVE A SENSE EXCUSE ME.", "AND THE REASON WE CAN IS BECAUSE OF THE MOMS STANDING BEHIND ME. THANK YOU."),
                    ("BY THE WAY, WE WERE NOT PLANNING A RALLY, BUT OUR HEADQUARTERS IS JUST AROUND THE CORNER", "THAT IS WHAT WE GOING TO DO. GOD BLESS YOU ALL. AND MAY GOD BLESS AMERICA."),
                    ("GOOD AFTERNOON. MY FELLOW AMERICANS, TODAY ACROSS THE NATION MANY OF US ARE FEELING ANXIOUS", "BUT WE HAVE TO MOVE AND MOVE NOW. THANK YOU ALL FOR TAKING THE TIME TO BE HERE AND GOD BLESS OUR TROOPS. THANK YOU."),
                    ("GOOD EVENING, EVERYONE. LAST WEEK, I HAD THE HONOR OF SPEAKING TO ALL OF YOU FROM PHILADELPHIA.", "WE HAVE TO STEP UP AND CARE FOR ONE ANOTHER. THANK YOU ALL FOR LISTENING."),
                    ("GOOD MORNING. I HOPE YOU AND YOUR FAMILY ARE DOING WELL", "MAY GOD PROTECT YOU AND MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("I WISH WE COULD BE TOGETHER IN PERSON, BUT I'M GRATEFUL TO BE ABLE TO CONNECT WITH YOU VIRTUALLY.", "MAY GOD PROTECT OUR TROOPS."),
                    ("I JUST HAD AN OPPORTUNITY TO SPEAK WITH THE FLOYD FAMILY.", "FOLKS, WE HAVE TO STAND UP. WE'VE GOT TO MOVE. GOT TO CHANGE."),
                    ("MR. MAYOR, THANKS FOR YOUR HOSPITALITY, AND TO ALL THE ELECTED OFFICIALS THAT ARE HERE, I BRING YOU GREETINGS.", "MAY GOD BLESS YOU ALL, AND MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("GOOD AFTERNOON, EVERYONE. LET ME BEGIN BY THANKING DR. ALLEN", "THANK YOU FOR LISTENING. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS."),
                    ("GOOD AFTERNOON, EVERYONE. I APOLOGIZE FOR THE SLIGHT DELAY.", "MR. PRESIDENT, WAKE UP. GET TO WORK. THERE'S SO MUCH MORE TO BE DONE."),
                    None,
                    ("GOOD AFTERNOON. TODAY WE ARE IN THE MIDDLE OF THE WORST GLOBAL HEALTH CRISIS", "WE WILL GET THIS DONE I PROMISE. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("I'M A FEW MINUTES LATE. THIS IS MY POLLING PLACE.", "MAY GOD BLESS YOU ALL AND PROTECT OUR TROOPS."),
                    None,
                    ("HELLO, EVERYONE. [APPLAUSE] LET ME START OFF BY SAYING HELLO TO TERESA CASEY AND THE GUY THAT HANGS OUT WITH HER OCCASIONALLY.", "GOD BLESS YOU ALL. MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("GOOD AFTERNOON. I AM HERE TODAY TO TALK ABOUT INFRASTRUCTURE AND JOBS AND ARE CLEAN ENERGY FUTURE", "PUT OUR NATION ON THE ROAD TO NET ZERO EMISSIONS NO LATER THAN 2050. SO LET'S NOT WASTE ANY MORE TIME. LET'S GET TO WORK NOW. NOW. THANK YOU."),
                    ("GOOD AFTERNOON, EVERYBODY. I WANT TO THANK THE COLONIAL EARLY EDUCATION PROGRAM HERE IN CALYX", "THANK YOU FOR HAVING US HERE. APPRECIATE IT VERY, VERY MUCH. THANK YOU."),
                    ("ACTUALLY THAT IS A JOKE. IT IS GREAT TO BE HERE BACK IN A PLACE AND I WANT TO THANK WAYNE JEFFERSON HERE FOR HAVING", "SO TO SCALE UP THE BUSINESS TO INVEST IN THE COMMUNITY THAT IS HEART AND GET AND NEVER GIVES UP AND THAT'S WHO WE ARE THAT IS WHAT THIS ELECTION IS ALL ABOUT. WE ARE AMERICAN. WE DON'T SETTLE. WE ASPIRE AND WE SUCCEED I'M HAPPY TO TAKE YOUR QUESTIONS."),
                    ("GOOD TO SEE YOU AGAIN. I WANT TO SAY A SPECIAL HI TO MY GOOD FRIEND SECRETARY DAILY.", "AT LEAST I HOPE THAT IS THE CASE. I AM GOING TO NEED YOUR HELP TO GET ALL OF THIS DONE. GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("HELLO, HELLO. THANKS FOR BEING HERE.", "THE FLOOR IS YOURS."),
                    ("GOOD AFTERNOON. I WANT TO THINK CARNEGIE MELLON", "I WANT TO THANK YOU ALL. MAY GOD BLESS YOU. MAY GOD PROTECT OUR TROOPS."),
                    ("GOOD AFTERNOON, FOLKS.", "NOW I'M HAPPY TO TAKE QUESTIONS YOU MAY HAVE. I GUESS STAFF IS GOING TO CALL ON WHOEVER, FIRE AWAY."),
                    None,
                    ("GOOD AFTERNOON, FOLKS. SORRY I AM A LITTLE LATE.", "IF WE JUST DO IT TOGETHER. THANK YOU ALL."),
                    ("HELLO, HELLO, HELLO. SINCE I AM SOCIALLY DISTANCE, I AM ALLOWED TO TAKE MY MASK OFF", "GOD BLESS YOU. MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("GOOD AFTERNOON. WELCOME TO THE NATURAL HISTORY MUSEUM.", "MAY GOD PROTECT OUR TROOPS."),
                    ("THANK YOU VERY MUCH. I JUST WANT TO THANK YOU ALL. I UNDERSTAND YOU SPOKE, I COULD NOT HEAR YOU. BISHOP, THANK YOU FOR INVITING ME.", "GOD BLESS YOU AND ALL YOU DO, AND MAY GOD PROTECT OUR TROOPS."),
                    ("I JUST HAVE ONE THING TO SAY. HANG ON HERE.", "I WANT TO THANK YOU ALL, PARTICULARLY THANK THE PEOPLE WHO CAME HERE AND INTRODUCED ME TODAY, AND MAY GOD PROTECT OUR TROOPS. GOD BLESS YOU ALL. THANK YOU."),
                    ("I JUST FINISHED SPEAKING ABOUT THE PANDEMIC, THE STEPS WE NEED TO CURB THE SPREAD OF THE VIRUS", "LINE WORKERS AND MAY GOD PROTECT OUR TROOPS."),
                    ("HELLO, MINNESOTA. IT IS GOOD TO BE BACK.", "SO GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU."),
                    ("GOOD AFTERNOON. WELCOME TO THE CONSTITUTION CENTER.", "MAY GOD PROTECT OUR TROOPS, AND MAY GOD BLESS RUTH BADER GINSBURG. THANK YOU SO MUCH."),
                    ("THANK YOU VERY MUCH. AS THEY SAY, AND PART OF MY CITY, YOUR FAMILY DONE GOOD.", "Y'ALL STAY SAFE AND MAY GOD PROTECT OUR TROOPS. THANK YOU SO MUCH, MR. MAYOR. THANK YOU. AND THANK YOU, MA'AM. APPRECIATE IT."),
                    ("HELLO, HELLO, HELLO, HELLO. MY NAME IS JOE BIDEN. I'M TRYING TO GET A JOB WITH CHRIS.", "AS MY MOTHER WOULD SAY, I'M GOING TO HUSH UP AND TAKE ANY QUESTIONS YOU ALL HAVE. I'VE GOT TO GET OUT OF THE WAY HERE."),
                    ("I CAN SAY THAT I DID IT, YOU KNOW, I RAN FOR THE SENATE BECAUSE WE NEED YOU.", "SO GOD BLESS YOU, MAY GOD PROTECT OUR TROOPS, AND THANK YOU FOR WHAT YOU DO. YOUR JOB IS TOO HARD FOR ME."),
                    ("GOOD AFTERNOON. THE FIRST WOMAN, THE FIRST WOMAN IN HISTORY OF OUR NATION TO LIE IN STATE IN THE U.S. CAPITOL.", "THANK YOU AND GOD BLESS AMERICA, MAY GOD PROTECT OUR TROOPS, AND I WILL TAKE A FEW QUESTIONS."),
                    ("HEY, FOLKS. GOOD AFTERNOON. BEFORE I START, I WANTED TO SLAIN THE DELAY.", "AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU."),
                    ("THANK YOU. ROCK 'N' ROLL. OK. THANK YOU ALL FOR BEING HERE. [CHEERS AND APPLAUSE] THANK YOU.", "GOD BLESS YOU ALL. THANK YOU. WE CAN DO THIS."),
                    ("HELLO, ARIZONA. [APPLAUSE] IT IS GREAT TO BE BACK.", "GOT TO MAKE THE WORLD GO ROUND GIVE US WHAT YOU GET. DON'T LET OUR WORLD GO ROUND."),
                    ("HELLO, HELLO, HELLO. HELLO. THANK YOU, THANK YOU, THANK YOU. HELLO, LAS VEGAS.", "NEVER, NEVER. FOLKS, LET'S STAND UP AND TAKE BACK THIS COUNTRY NOW. THANK YOU. THANK YOU."),
                    ("HELLO. HELLO. HELLO. THANK YOU, THANK YOU, THANK YOU. IT IS GOOD TO BACK HERE IN ERIE.", "WHERE MY GOING? AM I GOING THIS WAY? THANKS EVERYBODY. THANKS A MILLION. THANK YOU!"),
                    ("HELLO TOLEDO . [APPLAUSE] THIS FEEL LIKE COMING HOME .", "GO SPREAD THE FAITH. LET'S WIN THIS THING."),
                    ("HELLO CINCINNATI. IT'S GOOD TO BE BACK.", "MAY GOD BLESS YOU AND GOD BLESS OUR TROOPS"),
                    ("HELLO, HELLO HELLO. GOOD TO SEE YOU ALL.", "JOEY, KEEP THE FAITH AND MY GRANDMA SAID NO JOEY, SPREAD IT. THANKS, EVERYBODY."),
                    ("HELLO, IT'S JOE BIDEN. I WANT TO CONGRATULATE MUSLIM ADVOCATES", "IF WE DO IT TOGETHER SO LET'S SPREAD THE FAITH AND GET TO WORK."),
                    ("HELLO, MICHIGAN. HOW ARE YOU?", "SO, FOLKS, THANK YOU AND MAY GOD BLESS YOU AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU."),
                    ("Well, I'll tell you what, man.", "God bless you all And may God protect our troops. Go get him. We can do this. Thank you. Thank you, Thank you."),
                    ("HELLO. THANK YOU, THANK YOU, THANK YOU.", "GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU, THANK YOU, THANK YOU."),
                    ("LAST NIGHT, WE SAW THE PRESIDENT OF THE UNITED STATES LIED TO THE AMERICAN PEOPLE AND REPEATEDLY LIE ABOUT THE STATE OF THIS PANDEMIC.", "THANK YOU, AND KEEP THE FAITH."),
                    None,
                    ("HELLO, HELLO, HELLO. WHAT A MAGNIFICENT SETTING.", "THANK YOU ALL FOR BEING HERE AND MAY GOD BLESS AMERICA AND MAY GOD PROTECT OUR TROOPS. STAY SAFE AND WEAR YOUR MASK."),
                    ("WE LOOKED AT THE LATEST REPORTED DATA HOW WE ARE ON AN UPWARD SLOPE", "MAY GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("HELLO, TAMPA.", "RETURN YOUR BALLOT TODAY. PRESIDENT KENNY SAID WE REFUSE TO POSTPONE. LET'S NOT POSTPONE AND GET OUT OF THE RAIN. GOD BLESS YOU ALL, THANK YOU."),
                    ("HELLO, MINNESOTA. JESSICA, THANK YOU FOR BEING HERE AND SHARING YOUR STORY.", "GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU. THANK YOU."),
                    ("MR. PRESIDENT, THANK YOU, THANK YOU, THANK YOU.", "GOD BLESS YOU ALL AND MAY GOD TECH OUR TROOPS. THANK YOU, THANK YOU, THANK YOU."),
                    ("HELLO, HELLO, HELLO. [HORNS HONKING] HELLO. HELLO, PHILADELPHIA. IT IS GREAT TO SEE EVERYONE.", "GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. [HORNS HONKING] I LOVE YOU. I LOVE YOU. YOU BROUGHT ME TO THE DANCE. THANK YOU, THANK YOU. THANK YOU. GOD LOVE YOU ALL."),
                    ("Thank you. Thank you. Thank you. A special thanks.", "We could be our best. What were the United States of America? God bless you all And may God protect our troops."),
                    ("Hello, Cleveland. Whoa! Ah, thank you.", "So let's get up and do it. God bless you all. And may God protect our troops. Thank you. Thank you. Thank you."),
                    ("THANK YOU FOR BEING HERE.", "LET'S GET THIS VOTE OUT. MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    None,
                    ("HELLO, PITTSBURGH! I'M JOE BIDEN. LADY GAGA'S FRIEND.", "GOD BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS! THANK YOU, THANK YOU, THANK YOU."),
                    ("HELLO, DELAWARE. GOOD EVENING. YOUR PATIENCE IS COMMENDABLE.", "MY GRANDMA WOULD SAY NO, SPREAD IT. KEEP THE FAITH, GUYS. WE ARE GOING TO SPREAD IT. [CAR HORNS] THANK YOU."),
                    ("GOOD EVENING, MY FELLOW AMERICANS.", "I THANK YOU ALL. MAY GOD BLESS YOU. MAY GOD PROTECT OUR TROOPS. GOOD NIGHT."),
                    ("HELLO. MY FELLOW AMERICANS.", "MAY GOD BLESS AMERICA AND MAY GOD PROTECT OUR TROOPS. THANK YOU."),
                    ("HELLO, HELLO, HELLO. IT'S GOOD TO BE BACK. IT'S GOOD TO BE BACK. LET'S HEAR IT FOR ALLY.", "BLESS YOU ALL AND MAY GOD PROTECT OUR TROOPS. THANK YOU.")] 
    clean_cspan(directoryin, directoryout, potus, "NFC", True, biden_remove, speechbounds)


    # Medium
    directoryin = "{}/us2020data/data/medium/".format(toplevel)
    directoryout = "{}/us2020data/data_clean/medium/".format(toplevel)
    pathlib.Path("{}/{}".format(directoryout, potus)).mkdir(parents=True, exist_ok=True)   
    drop_speechID = pd.read_csv("{}/{}/drop_speech_id.tsv".format(directoryin, potus), sep="\t")       
    drop_speechID = drop_speechID.SpeechIDdrop.values.tolist()            
    clean_medium(directoryin, directoryout, potus, textclean_medium, "NFC", True, drop_speechID, drop_column)