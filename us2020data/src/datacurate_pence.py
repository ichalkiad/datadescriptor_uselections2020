import time
import ipdb
import pandas as pd
from us2020data.src.utils import clean_speech_texts, textclean_votesmart,\
                                    textclean_miller, remove_dots, find_substring,\
                                    remove_candidates_dicts, remove_square_brackets, \
                                    remove_round_brackets, remove_trump, remove_pence#, clean_votesmart, clean_cspan
import pathlib
import re


def clean_cspan(directoryin, directoryout, potus, show=False, dropsegments=None, speechbounds=None):
    
    # load file, also manually cleaned
    cspan = pd.read_csv("{}/{}/rawtext_droptitles_{}_edit1.tsv".format(directoryin, potus, potus), sep="\t")
    cspandf = {"SpeechID": [], "POTUS": [], "Date": [], "SpeechTitle": [],	"Type": [], 
               "RawText": [], "CleanText": [], "SpeechURL": [], "Summary": [], "Source": [], 
               "Original Source": [], "Location": []}
    for i, row in cspan.iterrows():       
        remainingstr = None
        if speechbounds[i] is None:
            print(i+2) # row in _edit1 tsv
            print(row.SpeechURL)                                            
            continue
        if row.RawText == row.SpeechID:
            with open("{}{}/specialcleanneeded/{}.txt".format(directoryin, potus, row.SpeechID), "r") as f:
                content = f.read()
                row.RawText = content                
        if row.RawText is None:
            raise AttributeError
        s1, s2 = speechbounds[i]
        remainingstr = find_substring(row.RawText, s1, s2)       
        if s1 not in row.RawText or s2 not in row.RawText or remainingstr is None:
            print(i+2) # row in _edit1 tsv
            print(row.SpeechURL)
            print(row.RawText)
            print(speechbounds[i])            
            raise AttributeError            
        if remainingstr is not None:
            row["SpeechSegment"] = remainingstr
            cspandf["SpeechID"].append(row["SpeechID"])
            cspandf["POTUS"].append(row["POTUS"])
            cspandf["Date"].append(row["Date"])
            cspandf["SpeechTitle"].append(row["SpeechTitle"])
            cspandf["RawText"].append(row["RawText"])
            cspandf["SpeechURL"].append(row["SpeechURL"])
            cspandf["Summary"].append(row["Summary"])
            cspandf["Source"].append(row["Source"])
            cspandf["Original Source"].append(None)
            cspandf["Location"].append(None)
            cspandf["Type"].append(row["Type"])
            cspandf["CleanText"].append(row["SpeechSegment"])
    cspandf = pd.DataFrame.from_dict(cspandf).sort_values(by=["Date"]).reset_index(drop=False)
    cspandf.to_csv("{}/{}/rawtext_droptitles_{}_edit2.tsv".format(directoryin, potus, potus), sep="\t", index=False)
    cspandf = remove_candidates_dicts(cspandf, dropsegments, "CleanText")     
    if potus == "DonaldTrump":   
        cspandf.CleanText = cspandf.CleanText.apply(remove_trump)
    if potus == "MikePence":   
        cspandf.CleanText = cspandf.CleanText.apply(remove_pence)
    cspandf.CleanText = cspandf.CleanText.apply(remove_dots)
    cspandf.CleanText = cspandf.CleanText.apply(remove_square_brackets)
    cspandf.CleanText = cspandf.CleanText.apply(remove_round_brackets)    

    if show:    
        for i, row in cspandf.iterrows():        
            print(row.SpeechURL)
            print(row.SpeechSegment)
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)
    cspandf.to_csv("{}/{}/cleantext_{}.csv".format(directoryout, potus, potus), sep="\t", index=False)


if __name__ == "__main__":

    drop_column = "SpeechID"
    potus = "MikePence"
    
    # Vote Smart
    # directoryin = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data/votesmart/"
    # directoryout = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data_clean/votesmart/"
    # drop_speechID = pd.read_csv("{}/{}/drop_speech_id.tsv".format(directoryin, potus), sep="\t")   
    # drop_speechID = drop_speechID.SpeechIDdrop.values.tolist()
    # clean_votesmart(directoryin, directoryout, potus, textclean_votesmart, "NFC", True, drop_speechID, drop_column)

    # C-SPAN
    directoryin = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data/cspan/"
    directoryout = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data_clean/cspan/"       
    drop_speechID = pd.read_csv("{}/{}/drop_speech_id.tsv".format(directoryin, potus), sep="\t")       
    cspan = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    drop_speechID = drop_speechID.SpeechIDdrop.values.tolist()
    cspan = cspan[~cspan[drop_column].isin(drop_speechID)] 
    cspan = cspan.reset_index(drop=True)
    cspan.to_csv("{}/{}/rawtext_droptitles_{}.tsv".format(directoryout, potus, potus), index=False, sep="\t")   

    #####################################
    # At this point, some manual curation was needed before proceeding to the next cleaning steps,
    # to identify which speeches were captioned well-enough, their starting and ending points
    # and the speakers segments.
    #####################################


    # csv no 22 dropped due to erroneous transcription

    # pence_remove = {"CSPANMP91202075": ["USA. USA. USA. USA.", "FOUR MORE YEARS. FOR MORE YEARS. FOUR MORE YEARS. FOR MORE YEARS.", "BUILDS THAT WALL. A BUILD THAT WALL. BILLS OF THAT WALL."]}     
    # speechbounds = [("Thank you, Acting Secretary Shanahan, Secretary Mark Esper, Secretary Wilson, distinguished members of Congress, members of the Joint Chiefs", "So now it is my high honor and distinct privilege to introduce your Commander-in-Chief, the 45th President of the United States of America, President Donald Trump."),
    #                 None,
    #                 None,
    #                 None,
    #                 None,
    #                 ("Well thank you special agent on and thank you for making us so welcome here at Homeland Security Investigations it is and an honor to be with you all through Governor Kim", "God bless thank you doctor great work"),
    #                 None,
    #                 None,
    #                 None,
    #                 None,
    #                 ("Yeah that today is a momentous day in the life of our nation.", "And our hope is as the discussions continue, that Mexico will step up will take such action action that is necessary to address what the american people know is a real humanitarian and security crisis at the southern border of the United States. Right, thanks. We'll do questions later."),
    #                 ("HELLO CHRISTIANS UNITED FOR ISRAEL . THANK YOU FOR THAT WARM WELCOME .", "HE WILL GUIDE US AND HE WILL SURELY BLESS US. GOD BLESS YOU ALL. MAY GOD BLESS ISRAEL. [APPLAUSE] AND MAY GOD CONTINUE TO BLESS THE UNITED STATES. [CHEERS AND APPLAUSE]"),
    #                 None,
    #                 ("Governor Ron DeSantis, First Lady Casey, Administrator Bridenstine, Director Cabana, General Selva, distinguished members of Congress, Marillyn Hewson, the dedicated men and women of NASA, and especially Rick Armstrong and the members of the Neil Armstrong family, and Apollo 11 astronaut Buzz Aldrin:", "And may God continue to bless the United States of America."),
    #                 ("Well hello Jacksonville. Governor descent this David Long and leaders in business and industry", "your continued support with Governor Rhonda Santas and his allies at the State House with President Donald Trump in the White House and with God's help."),
    #                 ("Thank you all for. Thank you for that very warm welcome it is an honor to be here today", "We've also gone to court to protect the right to religious expression in the public square and the Alliance Defending Freedom has been there every step of the way"),
    #                 None,
    #                 None,
    #                 ("Well, hello, Iowa! (Applause.) To Governor Reynolds;", "Thank you very much. (Applause.) God bless you, Iowa. And God bless America."),
    #                 ("Well hello Fort Hood up it is great to be back in Texas and it is great to be at the great place.", "So thank you. God bless. God bless the forces."),
    #                 None,
    #                 ("Thank you. Thank you. Thank thank you thank you Governor Bev and thank you to the 1st lady to learn.", "God bless you and keep you as you serve the people of this community and this state."),
    #                 ("THIS NATION WILL ALWAYS HONOR THE SERVICE AND SACRIFICE THAT THEY REPRESENT.", "WITH YOUR HARD WORK AND TELLING OUR STORY TO EVERY COMMUNITY, WE WILL PUT PRESIDENT TRUMP BACK IN THE WHITE HOUSE FOR FOUR MORE YEARS AND WE WILL KEEP AMERICA [INAUDIBLE] THANK YOU VERY MUCH. GOD BLESS YOU AND GOD BLESS AMERICA."),
    #                 ("Thank you all for that warm welcome and. Join me in thanking our brand new secretary of labor Eugene Scalia", "We're going to keep America great thanks to everybody."),
    #                 None,
    #                 ("WELL HELLO TOLEDO", "BUT YOU DON'T HAVE TO TAKE MY WORD FOR IT, FOR NOW IT IS MY HIGH HONOR AND DISTINCT PRIVILEGE TO INTRODUCE TO YOU MY FRIENDS, AND THE 45th PRESIDENT OF THE UNITED STATES OF AMERICA, PRESIDENT DONALD TRUMP."),
    #                 None,
    #                 None,
    #                 ("Well Governor McMaster 1st Lady Peggy McMaster deputy secretaries ace.", "God bless America."),                    
    #                 ("My great friend, great, my great friend sonny Purdue the chairman, laura cox and all of you have come here from near and far. It is great to be back in the great lakes state.", "And with President Donald Trump in the White House for four more years and with God's help. we're gonna keep America. Great! Thank you so much michigan. God bless you and God bless America."),                    
    #                 ("Well, hello, Michigan!", "Thanks, everybody. (Applause.) God bless you, and God bless America."),
    #                 None,                    
    #                 ("THANK YOU SO VERY MUCH HOW ABOUT A ROUND OF APPLAUSE. [APPLAUSE] THANK YOU VERY MUCH.", "THANK YOU ALL VERY MUCH, AND GOD BLESS YOU. [APPLAUSE]"),                    
    #                 ("well, thank you all for that very warm welcome.", "So let's pray for America as we open up America because the best is yet to come. Thank you all very much. God bless you."),                    
    #                 ("Well, hello, Iowa! (Applause.) It is great to be in Iowa on this beautiful June day, to see all of you out in the sunshine.", "God bless this state, and God bless America in this great American comeback."),                    
    #                 ("Well, hello, Michigan! (Applause.) And thank you to, really, one of the hardest working members of the President's Cabinet.", "Thank you. God bless you. And God bless the United States."),
    #                 None,                    
    #                 ("Well, hello, Wisconsin! (Applause.) You all look great.", "Thanks, everybody. God bless you, and God bless America."),
    #                 ("Thank you so much. Thank you for the - thank you for the warm welcome.", "Thank you very much. And God bless you."),                    
    #                 ("That might be the 1st time I've ever driven up on stage. And what a beautiful vehicle to do it in the secretary of energy Danbury", "The best days for more town and Ohio and America. Are yet to come thank you very much. God bless."),                                        
    #                 ("It's good to be back in church. (Applause.) Pastor Jeffress, thank you for that overly generous introduction. Thank you for your ministry.", "Thank you for letting me join you today. God bless you. And God bless America."),                    
    #                 ("Hello, Philadelphia! (Applause.) Thank you for that great warm welcome.", "We will always back the blue."),                    
    #                 ("Well, thank you Governor Edwards. Good to be in Louisiana.", "And I'd like to invite them to bring a few remarks."),
    #                 ("HELLO, WISCONSIN. [APPLAUSE] THANK YOU FOR THAT WARM WELCOME.", "FOUR MORE YEARS, WE WILL MAKE AMERICA GREAT AGAIN, AGAIN. THANK YOU. GOD BLESS WISCONSIN AND GOD BLESS AMERICA."),                    
    #                 ("Well, hello, Pennsylvania!", "Thank you very much. (Applause.) God bless you. God bless Pennsylvania and God bless America."),
    #                 None,                    
    #                 ("WELL, HELLO, FLORIDA! [CHEERS AND APPLAUSE] IT'S GREAT TO BE BACK IN THE SUNSHINE STATE.", "THANK YOU VERY MUCH. GOD BLESS YOU. AND GOD BLESS AMERICA."),
    #                 ("WELL, HELLO FLORIDA!", "GOD BLESS YOU FOR ALL YOU DO AND MAY GOD BLESS AMERICA."),
    #                 ("OFFICER JUSTIN HARRIS, TO ALL THE INCREDIBLE MEN AND WOMEN OF THE ARIZONA POLICE ASSOCIATION AND THEIR SUPPORTERS", "THANK YOU ALL VERY MUCH. GOD BLESS THE MEN AND WOMEN OF LAW ENFORCEMENT. AND GOD BLESS AMERICA."),
    #                 ("HELLO, IOWA. IT IS GREAT TO BE BACK IN THE HAWKEYE STATE.", "THANK YOU VERY MUCH. GOD BLESS YOU. GOD BLESS AMERICA."),                    
    #                 ("I want to thank you all for being here and I especially want to thank the cops for Trump", "we're going to make America great again. Again. Thank you very much God bless cops for Trump and God bless America."),
    #                 ("Well, hello, Michigan, man. Oh, man, do you all the great. Are you ready?", "And with your support together we will make America great again. Again. Thank you all very much. God bless you. God bless America. Now let's go get it done. Michigan"),
    #                 ("WELL, HELLO, GEORGIA. [APPLAUSE] THANK YOU ALL FOR COMING OUT IT IS GREAT TO BE BACK IN THE PEACH STATE.", " THANK YOU ALL VERY MUCH, GEORGIA. GOD BLESS YOU. GOD BLESS AMERICA. NOW LET'S GO GET IT DONE. [APPLAUSE]"),
    #                 ("HELLO GEORGIA. [APPLAUSE] IT IS GREAT TO BE IN THE PEACH STATE. THANK YOU ALL FOR COMING OUT, THIS LOOKS LIKE COME JANUARY 5 HERE IN GEORGIA WE ARE GOING TO HAVE US A RODEO.", "THANK YOU ALL MUCH, GOD BLESS YOU, GOD BLESS AMERICA. LET'S GO GET IT DONE, GEORGIA."),                    
    #                 ("Well, hello Georgia. The senator, David Perdue.", "Thank you very much. Georgia. God bless you. God bless America now let's go get it done."),                    
    #                 ("Well hello Georgia. My friend Senator David Perdue. two former governor. Sonny Perdue congressman rick Allen, congressman William timmons. The great state Party chair for the GOP.", "We're going to defend the Senate. We're going to keep making America great again. We will win Georgia and save America. Now let's go get it done. Georgia."),
    #                 None,  
    #                 ("Thank you all for coming out on this blustery december day.", "We're gonna win Georgia, we're going to save America and we're gonna keep making America great again. So let's go get it done."),                    
    #                 ("SENATOR DAVID PERDUE, FUTURE SENATOR KELLY LOEFFLER, FORMER GOVERNOR SONNY PERDUE, REFORM N.C. NATIONAL COMMITTEE WOMAN GINGER HOWARD", "LET'S GO GET IT DONE, GEORGIA. LET'S SEND DAVID PERDUE AND KELLY LOEFFLER BACK TO WASHINGTON, D.C."),
    #                 None,
    #                 ("WELL, HELLO, TURNING POINT. [CHEERING AND APPLAUSE] ALL THE GREAT AMERICANS ARE GATHERED HERE FROM NEAR AND FAR ALL ACROSS THE UNITED EIGHTS OF AMERICA. IT IS GREAT TO BE AT THE STUDENT ACTION SUMMIT.", "THANK YOU ALL VERY MUCH. GOD BLESS YOU. GOD BLESS AMERICA."),
    #                 ("HELLO, GEORGIA. HOW YOU END THE PRAYER. CAN I GET AN AMEN?", "THANK YOU VCH GEORGIA. GOD PLEAS YOU AND DEMROD PLEAS AMERICA. NOW LET'S GET IT DONE!"),
    #                 None,
    #                 None,
    #                 None,
    #                 ("THANK YOU ALL VERY MUCH. HELLO, LEMOORE. [APPLAUSE] THE CAPTAIN, DOUG PETERSON, CAPTAIN AIDEN JASON, CAPTAIN BOBBY MARK A VAGUE.", "MAY GOD BLESS ALL THOSE SERVING IN OUR ARMED FORCES. AND GOD BLESS AMERICA."),
    #                 ("HELLO,FORT DRUM. CONGRESSWOMAN ELISE STAFANIK, GENERAL, ALL OF THE MEMBERS OF THE ARMED FORCES GATHERED HERE, U.S. ARMY STRONG.", "SO, GOD BLESS THE MEN AND WOMEN OF THE 10TH MOUNTAIN HERE AND IT DEPLOYED WITH HIS PROTECTION AS YOU CLIMB FOR GLORY. GOD BLESS ALL THOSE IN THE ARMED FORCES OF THE UNITED STATES. AND GOD BLESS AMERICA.")]  # remove 62 due to quality?
    # clean_cspan(directoryin, directoryout, potus, False, pence_remove, speechbounds)
