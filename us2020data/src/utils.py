import html
import unicodedata
import re
import regex
import ipdb
from us2020data.src.quotes import OPENQUOTES, CLOSEQUOTES
import string
import time
import pandas as pd

# dialogue or not addressing mainly the public but rather a member of staff
patternremtext = re.compile(r'.*?(PRESIDENT DUDA|MRS. TRUMP|INTERIM PRESIDENT GUAIDÓ|CHIEF BIEHL|ADMINISTRATOR MCMAHON|MILITARY AIDE|SHERIFF O\'CONNOR|SECRETARY AZAR|LIEUTENANT COLONEL TIMOTHY REDHAIR|TO THE SENATE OF THE UNITED STATES|INTERPRETER ON BEHALF OF|MRS. GLORIA GUILLÉN|MS. KHAWAM|MS. PETERS|SHERIFF BETH|SECRETARY BERNHARDT|AMBASSADOR PENCE|MR. GIULIANI|GOVERNOR DESANTIS|BISHOP JACKSON|SENIOR CHIEF PETTY OFFICER SCHAEFFER|MR. TURNER|SECRETARY CARSON|MRS PENCE|MS DAVIS|SECRETARY MNUCHIN|MS. BROWNLEE|TO THE CONGRESS OF THE UNITED STATES|GOVERNOR ABBOTT|GOVERNOR BURGUM|ADMINISTRATOR BRIDENSTIN|HOUSE MAJORITY LEADER HOYER|LIEUTENANT GENERAL LINNINGTON|MR. ROSS|DR. LAFFER|DR. GEORGE|SECRETARY POMPEO|ACTING ADMINISTRATOR GAYNOR|GENERAL MILLEY|MR. GALLOGLY):', re.DOTALL)
# introduction of speaker at the beginning of the speech
patternbegin = re.compile(r'^\s*?(THE VICE PRESIDENT|THE PRESIDENT|PRESIDENT TRUMP|VICE PRESIDENT PENCE|VICE PRESIDENT HARRIS|VICE PRESIDENT|PRESIDENT):', re.DOTALL)
patternbeginharris = re.compile(r'^\s*.*?(U.S. Senator Kamala D. Harris (D-CA), a member of the Senate Judiciary Committee, on Monday released the following statement on her vote against the confirmation of Judge Amy Coney Barrett to be Associate Justice of the Supreme Court of the United States|A full transcript of Harris\' statement, as delivered: HARRIS|Full transcript of Harris\' remarks below|Full transcript of Harris\' remarks|HARRIS):', re.DOTALL)
patternremovetrump = re.compile(r'(PRES. TRUMP:|Mr. Trump:|GUEST:|MR. TRUMP:|PRESIDENT TRUMP::|TRUMP:|PRESIDENT TRUMP:)', re.DOTALL)
patternremovepence = re.compile(r'(V.P. PENCE:|VICE PRES. PENCE:|PENCE:|VICE PRESIDENT PENCE:)', re.DOTALL)
patternremovebiden = re.compile(r'(VICE PRESIDENT BIDEN:|VP BIDEN:|FRMR V.P. BIDEN:|JOE BIDEN:|FORMER VP BIDEN:|VICE-PRESIDENT BIDEN:|VICE PRES. BIDEN:|FMR. VP BIDEN:|PRESIDENT-ELECT BIDEN:)', re.DOTALL)
# end signatures
patternend = re.compile(r'(\bEND\b(?=\s*\.|$)|FOR FURTHER INFORMATION MEDIA SHOULD CONTACT).*$', re.DOTALL)
patternendwithtime = re.compile(r'\s*END\s*\b(?:[0-1]?[0-9]|2[0-3]):[0-5]\d\b\s*(A.M.|P.M.)\s*(?!,).*$', re.DOTALL)
patternstartwithtime = re.compile(r'^(.*?\s*(\b(?:[0-1]?[0-9]|2[0-3]):[0-5]\d\b)\s*(A.M.|P.M.)\s*\b\w+\b\s*(THE VICE PRESIDENT|THE PRESIDENT|PRESIDENT TRUMP|VICE PRESIDENT PENCE|VICE PRESIDENT HARRIS):)', re.DOTALL)
patternjrbjr = re.compile(r'(. JOSEPH R. BIDEN JR.|.JOSEPH R. BIDEN JR.|.DONALD J. TRUMP|. DONALD J. TRUMP)(?!,).*$', re.DOTALL)
# remove Q&A session
patternqs = re.compile(r' Q (?:Thank you, Mr. President|Mr. President|.*?)(?=\n|$)', re.DOTALL)
# remove audience interruptions
patterninbetween = re.compile(r'AUDIENCE:.*? THE PRESIDENT:', re.DOTALL)
patterninbetweendialogue = re.compile(r' (DR.|MS.|MR.|THE VICE|REPRESENTATIVE|GOVERNOR|STATE ATTORNEY GENERAL)* \b(\w+):.*? (THE PRESIDENT|THE VICE PRESIDENT):', re.DOTALL)
patternsen = re.compile(r'Sen\.\s(?:[A-Z])')
def replace_beginwithtime(text) : return re.sub(patternstartwithtime, '', text)
def replace_allup2vp(text) : return re.sub(patternbegin, '', text)
def replace_allup2harris(text) : return re.sub(patternbeginharris, '', text)
def remove_alltext(text): return "" if len(re.findall(patternremtext, text)) > 0 else text
def remove_qsession(text) : return re.sub(patternqs, '', text)
def remove_audiencesession(text) : return re.sub(patterninbetween, '', text)        
def replace_proclamation(text) : return re.sub("^\s*BY THE PRESIDENT OF THE UNITED STATES OF AMERICA A PROCLAMATION", '', text)
def replace_transcript_init(text) : return re.sub(r'^\s*Transcript[^\n.]*[.!?]', '', text)
def replace_contentwarning_init(text) : return re.sub(r'^\s*Content warning:[^\n.]*[.!?]', '', text)
def replace_exec_order(text) : return re.sub("\(The executive order is signed.\)", '', text)
def replace_breaktranscript(text) : return re.sub("(BREAK IN TRANSCRIPT|Read Vice President Mike Pence's speech from the 2020 Republican National Convention, as prepared for delivery:)", '', text)
def remove_url(text) : return re.sub(r'https?://\S+|www\.\S+|\S+\.com/\S*|\S+\.org/\S*|\S+\.net/\S*', '', text)
def remove_interruptionsession(text) : return re.sub(patterninbetweendialogue, '', text)
def remove_square_brackets(text) : return re.sub(r'\[.*?\]', '', text)
def remove_round_brackets(text) : return re.sub(r'\(.*?\)', '', text) 
def replace_senator(text): return re.sub(patternsen, "Senator ", text)
def replace_endwithtime(text) : return re.sub(patternendwithtime, '', text)
def remove_bidenend(text) : return re.sub(patternjrbjr, '', text)
def replace_allafterend(text) : return re.sub(patternend, '', text)         
def remove_hashprint(text) : return text.replace("### Print", "")
def remove_hashprint2(text) : return text.replace("###", "")
def remove_hashprint3(text) : return text.replace("Bill text can be found HERE. A one-pager on the bill can be found HERE.", "")
def remove_hashprint4(text) : return text.replace("For further background on the bill, click here. For full bill text, click here.", "")
def replace_ps(text) : return re.sub(r'\s*P.S.*YouTube.(?=\s|$)', '', text)
def replace_ps2(text) : return re.sub(r'^\s*P.S. [^\n.]*[.!?](?=\s|$)', '', text)       
def remove_dots(x) : return x.replace("…", "").replace("--", "")
def remove_trump(text) : return re.sub(patternremovetrump, '', text)    
def remove_pence(text) : return re.sub(patternremovepence, '', text)
def remove_biden(text) : return re.sub(patternremovebiden, '', text)    
    

def apply_unicode_normalisation(text, unicode_class):

    # convert all named and numeric character references (e.g. &gt;, &#62;, &#x3e;) in the string text
    # to the corresponding Unicode characters.        
    text = html.unescape(text)

    # Apply Unicode normalisation according to given Unicode class        
    text = unicodedata.normalize(unicode_class, text)

    return text

def clean_char_repetitions(text) -> str:
            
    def replace_newlines(x) : return re.sub(r'[\n*\xa0*\n*]', ' ', x)
    def replace_spaces(x) : return re.sub(r'\s+', ' ', x)
    def replace_tabs(x) : return re.sub(r'\t+', '\t', x)
    def replace_ret(x) : return re.sub(r'\r+', '\r', x)
    
    tmp_text = text
    remove_repetitions = re.compile(r"([a-zA-Z])\1\1+")
    match = remove_repetitions.search(tmp_text)
    while match:
        text_part = match.group(0)
        rep_part = remove_repetitions.sub(r"\1", text_part)
        tmp_text = tmp_text.replace(text_part, rep_part)
        match = remove_repetitions.search(tmp_text)

    tmp_text = replace_newlines(tmp_text)
    tmp_text = replace_spaces(tmp_text)
    tmp_text = replace_tabs(tmp_text)
    tmp_text = replace_ret(tmp_text)

    tmp_text = tmp_text.strip()

    return tmp_text

def clean_speech_texts(data, cleaner, unicode_class):
    
    def clean_with_encodingclass(x) : return cleaner(x, unicode_class)
    data["CleanText"] = data.RawText.apply(clean_with_encodingclass)
    dataclean = data
    df_out = dataclean[dataclean["CleanText"] != ""].reset_index(drop=True)

    return df_out

def unicode_cleanup(text):
                
    def replace_apostr(x) : return re.sub(r'[\']+', '\'', x)
    def same_dash(x) : return regex.sub("\p{Pd}+", "-", x)    #  - 

    # replace all quotes with apostrophes - note that , is included in OPENQUOTES and we want to keep it
    text = "".join([i if (i not in OPENQUOTES and i not in CLOSEQUOTES) or i == "," else "'" for i in text])
    text = replace_apostr(text)
    text = same_dash(text)
    
    # remove non-unicode characters (default) or any character not in character_set
    # Replace unencodable character with '\ufffd'
    
    try:
        text_tmp = text.encode("utf-8", errors="ignore").decode("utf-8", "replace")
        if len(text_tmp) != len(text):
            raise AttributeError
    except UnicodeDecodeError:
        import warnings
        print(text)
        warnings.warn("UnicodeDecodeError while trying to remove non-unicode characters - Check your input!")
    except AttributeError:
        import warnings
        print(text)
        warnings.warn("Spurious input? Better check!")
    
    # replace all chars that are not in admissible lists with "\ufffd" to apply a common rule for cleanup later
    character_set = string.printable.replace('`', '')
    extra_admissible_chars = []
    special_chars  = []
    all_admissible = "{}{}{}".format(character_set, extra_admissible_chars, special_chars)
    def remove_inadmissible(x) : return [i if i in all_admissible else "\ufffd" for i in text]
    text = "".join(remove_inadmissible(text))        

    return text

def tidy_up_sentence(text):
                
        text = text.strip()
        if text[0] == "'" and text[-1] == "'":
            text = text[1:-1]
        elif text[-1] == "," or text[-1] == ":":
            text = text[0:-1] + "."
        if text[-1] != "." and text[-1] != "?" and text[-1] != "!" and text[-1] != ";":
            text = text + "."
        
        def replace_spaces(x) : return re.sub(r'\s+', ' ', x)        
        def commas_spaces(x) : return re.sub(r'\s,', ',', x)
        text = commas_spaces(text)
        text = replace_spaces(text)
        text = text.strip()

        return text

def segment2quotes(text):
        
        segments = []
        seg = ""
        for i in range(len(text)):
            if text[i] == "'" and seg == "":                                    
                seg += text[i]                    
            elif text[i] == "'" and seg != "":
                seg += text[i]      
                if "'A'" == seg or "'gold standard'" == seg or "'eligible child'" == seg or "'Chuy'" == seg\
                    or "'Level 4: Do Not Travel'" == seg or "'real estate investors in President Trump@0@ inner circle.'" == seg:
                    seg = ""
                    continue        
                if "but for" in seg or "but-for" in seg:
                    seg = seg.replace("but for", "")
                    seg = seg.replace("but-for", "")
                if "'People need health insurance that is affordable and covers what they need it to, especially during a pandemic. '" in seg:
                    seg += "By stalling COVID-19 testing and trying to rip health insurance away from people, the president is knowingly putting lives at risk for political gain. Republicans and Democrats have a moral responsibility to speak out against Trump's unprecedented sabotage of Americans' health."
                segments.append(seg)               
                seg = ""
            elif seg != "":    
                seg += text[i]                    
                    
        # concatenate quoted parts if they have max 3 tokens        
        filter_segs = []
        j = 0
        filt_seg = ""
        while j < len(segments):
            s = segments[j]
            if s == "" or s == " ":
                j += 1
                continue
            if s[0] == "'" and s[-1] == "'":
                s_tmp = s.replace("'", "")
                s_tmp = s_tmp.split()
                if len(s_tmp) <= 3:
                   filt_seg += " " + s + " "
                   j += 1
                else:
                    filter_segs.append(filt_seg)                    
                    filt_seg = ""
                    filter_segs.append(s)                    
                    j += 1
            else:
                filt_seg += s + " "
                j += 1
        if filt_seg != "" and filt_seg != " ":
            filter_segs.append(filt_seg)            
        filter_segs = [tidy_up_sentence(i) for i in filter_segs if i != " " and i != ""]      

        return filter_segs

def find_substring(s, s1, s2):
    
    start_index = s.find(s1)
    end_index = s.find(s2, start_index + len(s1))

    if start_index != -1 and end_index != -1:
        result = s[start_index:end_index + len(s2)]
        return result
    else:
        return None

def remove_candidates_dicts(df, removedict, column):
    
    for k in removedict.keys():
        for item in removedict[k]:
            if isinstance(item, str):                
                df.loc[df.SpeechID==k, column].values[0] = df.loc[df.SpeechID==k, column].values[0].replace(item, "")                    
            else:                
                start = item[0]
                end = item[1]
                remstr = find_substring(df.loc[df.SpeechID==k, column].values[0], start, end)
                if remstr is None:
                    print(k)
                    print(start)
                    print(end)
                    print(df.loc[df.SpeechID==k, column].values[0])
                    ipdb.set_trace()                
                df.loc[df.SpeechID==k, column].values[0] = df.loc[df.SpeechID==k, column].values[0].replace(remstr, "")
    
    return df

def extract_sentences_between_single_quotes(text):
    
    if "said Sen. Harris" in text or "issued the following statement" in text or "said Harris" in text or "said Senator Harris" in text or "Senator Harris said" in text\
        or "released the following statement" in text or "released a statement" in text \
        or "said Senator arris" in text or "crack down on gun trafficking and negligent gun dealers, and allow researchers, for the first time" in text:
        contracts = ["\'s", "s\'", "won\'t", "isn\'t", "don\'t", "can\'t", "I\'m", "doesn\'t", "we\'re", "Trump's", "Americans'", "\'ve", "aren\'t", "shouldn\'t"] 
        for i in range(len(contracts)):
            text = text.replace(contracts[i], "@{}@".format(i))        
        segs = segment2quotes(text)
        segs = [seg.replace(",.", ".") for seg in segs]
        quotedtext = " ".join(segs)
        quotedtext = quotedtext.replace("'", "")
        if quotedtext[-2:] == " .":
            quotedtext = quotedtext[:-2]
        if "other than honorable, general discharge dishonorable, t Ask, Don." in quotedtext:
            quotedtext = quotedtext.replace("other than honorable, general discharge dishonorable, t Ask, Don.", "")
        for i in range(len(contracts)):
            quotedtext = quotedtext.replace("@{}@".format(i), contracts[i])
    
        return quotedtext
    else:
        return text


def textclean_medium(text, unicode_class="NFC"):
        
    text = replace_senator(text)
    text = remove_url(text)
    text = replace_ps(text)    
    text = replace_ps2(text)    
    text = replace_transcript_init(text)
    text = replace_contentwarning_init(text)
    text = text.replace("Read Joe Biden's full plan to end gun violence at", "")
    text = text.replace("Thank you,Joseph R. Biden, Jr.47th Vice President of the United States", "")
    text = text.replace("Joe Biden would also support further rule changes to the P that would ensure deserving small businesses get all the help they need for as long as they need, including:", "")
    text = text.replace("He will ensure these workers receive:", "")
    text = text.replace("Specifically, Joe Biden will work with Congress to pass legislation that:Read Biden's full immigration plan at", "")
    text = text.replace("As President, Biden will build upon the historic progress made during the Obama-Biden administration, taking additional steps to support the rights of Black, Brown and Native farmers by:", "")
    text = text.replace("He will:", "")
    txt  = apply_unicode_normalisation(text, unicode_class)
    txt2 = clean_char_repetitions(txt)
    txt3 = unicode_cleanup(txt2)
    txt3 = txt3.strip()

    return txt3


def textclean_votesmart(text, unicode_class="NFC"):

    # remove introductory president announcement
    text = replace_beginwithtime(text)
    text = replace_allup2vp(text)
    text = replace_allup2harris(text)

    # # discard speech if discussion elements are spotted or not addressed to the public/voters
    # if len(re.findall(r'(BIDEN|Joe Biden|Donald Trump|President Donald Trump|PRESIDENT TRUMP):', text)) > 1\
    #         or len(re.findall(r'QUESTION:', text)) > 0\
    #         or len(re.findall(r'MEMORANDUM FOR', text)) > 0\
    #         or len(re.findall(r'^\s*(ACCEPTANCE ON BEHALF OF THE UNITED STATES OF AMERICA|THE FIRST LADY:)', text)) > 0\
    #         or len(re.findall(r'^\s*NATIONAL SECURITY DIRECTIVE', text)) > 0\
    #         or "Q Any reaction to (inaudible)?" in text or "MS. SANDERS:" in text or "PRIME MINISTER JOHNSON:" in text or "PRIME MINISTER PHÚC:" in text or "PRESIDENT TRỌNG:" in text or "PRESIDENT MOON:" in text or "SECRETARY-GENERAL GUTERRES:" in text\
    #         or "SERGEANT ROGERS:" in text or "SECRETARY WILKIE:" in text or "PARTICIPANT:" in text\
    #         or "AMBASSADOR FRIEDMAN:" in text or "PRESIDENT AL SISI:" in text or "PRIME MINISTER ABE:" in text\
    #         or  "PRIME MINISTER MAY:" in text or "HER MAJESTY QUEEN ELIZABETH II:" in text or "AUDIENCE MEMBER:" in text\
    #         or "Good evening. Your Majesties, Prime Minister and Mrs. Abe, distinguished guests: We are profoundly "\
    #             "honored to return to Japan as your nation's first state guests following the enthronement of His Majesty the Emperor." in text\
    #         or "Today, President Donald J. Trump announced many of the esteemed executives, economists, scholars, and industry leaders who together will form various Great American Economic Revival Industry Groups." in text\
    #         or "Today, President Donald J. Trump announced the addition of Kevin Hassett to serve as a Senior Advisor to the President. " in text\
    #         or "Today, President Donald J. Trump and members of his Administration hosted phone calls with Republican and Democrat Members of the House of Representatives and Senate serving on the Opening Up America Again Congressional Group." in text\
    #         or "Today, President Donald J. Trump welcomed President Andrzej Duda of the Republic of Poland to the White House." in text\
    #         or "By the authority vested in me as President by the Constitution and the laws of the United States of America, it is hereby ordered as follows:" in text\
    #         or "On behalf of the American people, the First Lady and I offer our heartfelt appreciation to Their Majesties the Emperor Akihito and Empress Michiko." in text\
    #         or "The First Lady and I send our most profound congratulations on behalf of all Americans to Their Majesties the Emperor Naruhito and Empress Masako on his enthronement as the new Emperor of Japan." in text\
    #         or "Hello, everybody. How are you? Very good numbers, economically. The country is doing really well." in text\
    #         or "Q: What is the REAL ID Act of 2005 and why did Congress pass it?" in text\
    #         or "On behalf of the American people, Melania and I offer our deepest condolences to the people of Japan and to the loved ones of former Prime Minister Yasuhiro Nakasone." in text\
    #         or "After more than three years of being held prisoner in Iran, Xiyue Wang is returning to the United States." in text\
    #         or "9:24 P.M. EST Hello, everybody. Happy New Year. Happy New Year. We're going to have a great year, I predict." in text\
    #         or "THE HONORABLE DONALD J. TRUMP, PRESIDENT OF THE UNITED STATES, HEREBY RESPONDS:" in text\
    #         or "On the occasion of the 60th anniversary of the signing of the United States-Japan Treaty of Mutual Cooperation and Security," in text\
    #         or "Melania and I wish everyone observing Ash Wednesday a peaceful and prayerful day." in text\
    #         or "send my best wishes to those here in America and around the globe celebrating Nowruz." in text\
    #         or "Congressman John Lewis was a great man whose courage and decades of public service changed America forever, and he will be deeply missed." in text\
    #         or "Yesterday, the U.S. Senate passed the HBCU Propelling Agency Relationships Towards a New Era of Results for Students (HBCU PARTNERS) Act, bipartisan legislation co-sponsored" in text\
    #         or "WASHINGTON, D.C. , U.S. Senator Kamala D. Harris (D-CA) on Thursday joined Senator Edward J. Markey (D-Mass.) and 22 of their colleagues to introduce a Senate Resolution to recognize, commemorate, and celebrate the 55th anniversary of the enactment of the landmark Voting Rights Act of 1965." in text\
    #         or "WASHINGTON, D.C. , U.S. Senator Kamala D. Harris (D-CA) on Thursday joined Senators Amy Klobuchar (D-MN), Tammy Duckworth (D-IL), Cory Booker (D-NJ), Brian Schatz (D-HI), and 12 colleagues to send a letter to Senate Majority Leader Mitch McConnell (R-KY) and Senate Democratic Leader Chuck Schumer" in text\
    #         or "WASHINGTON, D.C. , U.S. Senators Kamala D. Harris (D-CA) and Jacky Rosen (D-NV), both members of the Senate Homeland Security and Governmental Affairs Committee (HSGAC), on Thursday led 26 of their colleagues in a letter to Acting U.S. Customs and Border Protection (CBP) Commissioner Mark Morgan" in text\
    #         or "WASHINGTON, D.C. , U.S. Senators Kamala D. Harris (D-CA) and Dianne Feinstein (D-CA) and Congressman Salud Carbajal (D-CA) on Monday called on House and Senate leadership" in text\
    #         or "WASHINGTON, D.C. , U.S. Senator Kamala D. Harris (D-CA) on Monday joined Senator Elizabeth Warren (D-MA) and Representative Lauren Underwood (D-IL), along with Senators Cory Booker (D-NJ), Kirsten Gillibrand (D-NY), and Tina Smith (D-MN), in introducing the Maternal Health Pandemic Response Act" in text\
    #         or "August 21, 2020 The Honorable Donald J. Trump The White House 1600 Pennsylvania Avenue Washington, DC 20500 Dear Mr. President:" in text\
    #         or "Dear Chairman Pai, We write to express our profound frustration that the Federal Communications Commission (FCC) has failed to take forceful action to keep households connected during the COVID-19 pandemic." in text\
    #         or "WASHINGTON, D.C. , U.S. Senators Kamala D. Harris (D-CA), Bob Casey (D-PA), Cory Booker (D-NJ), and Dick Durbin (D-IL) wrote a letter urging the Chairman and Ranking Member of the Senate Finance Committee to draw on their individually proposed maternal health" in text\
    #         or "WASHINGTON, D.C. , U.S. Senator Kamala D. Harris (D-CA), a member of the Senate Judiciary Committee, on Saturday released the following statement following President Trump's nomination of U.S. Circuit Judge Amy Coney Barrett to the Supreme Court of the United States:" in text\
    #         or "WASHINGTON, D.C. , U.S. Senators Kamala D. Harris (D-CA) and Sherrod Brown (D-OH) on Thursday introduced legislation to ensure the safety and health of workers who are exposed to dangerous heat conditions in the workplace." in text\
    #         or "WASHINGTON, D.C. , U.S. Senator Kamala D. Harris (D-CA) on Friday joined Senators Patrick Leahy (D-VT) and Cory Booker (D-NJ) in pressing Judiciary Committee Chairman Lindsey Graham" in text\
    #         or "Hello, everybody. Happy New Year. Happy New Year. We're going to have a great year, I predict." in text\
    #         or "South Lawn5:05 P.M. EDTTHE PRESIDENT: So we'll be going to Camp David." in text\
    #         or "South Lawn 12:30 P.M. EDT THE PRESIDENT: Hello, everybody. So, we have a lot of good things going. We just had a meeting with Mitch McConnell and the group." in text\
    #         or "So we're going to watch the rocket launch." in text\
    #         or "Well, folks, thank you very much for being here. I'm about to sign an executive order, but I want to begin by thanking the Vice President for helping this, but also thank Chairman Milley" in text\
    #         or "With Ricardo Rossello's resignation, Puerto Rico can now begin to move forward and heal." in text\
    #         or "Your Excellencies: It an honor to address this gathering today at a momentous hour for the people of Venezuela and for the progress of freedom in this hemisphere." in text\
    #         or "The accord reached between the United States, Israel, and the United Arab Emirates (UAE) on August 13, 2020, is a courageous step toward a more stable, integrated, and prosperous Middle East. " in text\
    #         or "Today, I am officially recognizing the President of the Venezuelan National Assembly, Juan Guaido, as the Interim President of Venezuela." in text\
    #         or "The United States and Colombia are committed to taking steps to resolve the ongoing democratic and humanitarian crisis in Venezuela. " in text\
    #         or "This year, the United States and Czech Republic mark the 30-year anniversary of the inspiring and world-changing events of the Velvet Revolution." in text\
    #         or "The resignation yesterday of Bolivian President Evo Morales is a significant moment for democracy in the Western Hemisphere. " in text\
    #         or "On November 14, 1979, by Executive Order 12170, the President declared a national emergency with respect to Iran" in text\
    #         or "On November 22, 2015, by Executive Order 13712, the President declared a national emergency to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in Burundi," in text\
    #         or "We, the President of the United States and the Prime Minister of Bulgaria, reaffirm the strong friendship and alliance between our two countries. " in text\
    #         or "On November 27, 2018, by Executive Order 13851, I declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in Nicaragua. " in text\
    #         or "Today, President Donald J. Trump and President Mario Abdo Benitez of Paraguay committed to deepening the partnership between their two countries." in text\
    #         or "Today, President Donald J. Trump met with the President of the Republic of Ecuador, Lenï¿½n Moreno, signaling the historic turn in bilateral ties between our two countries. " in text\
    #         or "On February 25, 2011, by Executive Order 13566, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the actions of Colonel Muammar Qadhafi," in text\
    #         or "On April 1, 2015, by Executive Order 13694, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.) to deal with the unusual and extraordinary threat to the national security, foreign policy, and economy of the United States constituted by the increasing prevalence and severity of malicious cyber-enabled activities originating from, or directed by persons located, in whole or in substantial part, outside the United States. " in text\
    #         or "On April 3, 2014, by Executive Order 13664, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in and in relation to South Sudan," in text\
    #         or "On April 12, 2010, by Executive Order 13536, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the deterioration of the security situation and the persistence of violence in Somalia, and acts of piracy and armed robbery at sea off the coast of Somalia," in text\
    #         or "Today, President Donald J. Trump declared that a major disaster exists" in text\
    #         or "On Friday, April 24, 2020, the President signed into law: H.R. 266, the 'Paycheck Protection Program and Health Care Enhancement Act,' which provides additional fiscal year " in text\
    #         or "April 25, 2020, marks the 75th Anniversary of the historic meeting between American and Soviet troops, who shook hands on the damaged bridge over the Elbe River." in text\
    #         or "A lot of people were betting against it, but they've learned not to bet against us, I suspect. (Laughter.) I know they've learned that in Mexico. The people of Mexico and the United States are joined together by shared values, shared faith, and shared future on this beautiful continent. " in text\
    #         or "As a mark of respect for the memory and longstanding public service of Representative John Lewis, of Georgia, I hereby order, by the authority vested in me by the Constitution and the laws of the United States of America," in text\
    #         or "Well, thank you very much. It's an honor to be with the governor of a fabulous state, Arizona. It's Doug Ducey, and we know him well. " in text\
    #         or "The First Lady and I wish our Jewish brothers and sisters Shana Tova and hope the millions observing this sacred day in America and around the world have a blessed start to the High Holy Days." in text\
    #         or "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the Countering America's Adversaries Through Sanctions Act (Public Law 115-44), the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.) (IEEPA), the National Emergencies Act (50 U.S.C. 1601 et seq.), section 212(f) of the Immigration and Nationality Act of 1952 (8 U.S.C. 1182(f)), and section 301 of title 3, United States Code, I, DONALD J. TRUMP, President of the United States of America, find that: It remains the policy of the United States to counter Iran's malign influence in the Middle East, " in text\
    #         or "I am deeply saddened by the passing of my dear friend, His Highness the Amir of Kuwait," in text\
    #         or "Today, I have signed into law S. 209, the 'PROGRESS for Indian Tribes Act of 2019' (the 'Act'). This Act makes several amendments to enhance tribal self-governance under the Indian Self-Determination and Education Assistance Act of 1975 (ISDEAA) " in text\
    #         or "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the International Emergency Economic Powers Act" in text\
    #         or "On November 27, 2018, by Executive Order 13851, I declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security and foreign policy of the United States constituted by the situation in Nicaragua." in text\
    #         or "Today, our Nation mourns the loss of a true pioneer. General Charles 'Chuck' Yeager served in the Army Air Corps and the United States Air Force for more than 30 years, piloting countless aerial victories in World War II and commanding Airmen during the wars in Korea and Vietnam." in text\
    #         or "On December 20, 2017, by Executive Order 13818, the President declared a national emergency with respect to serious human rights abuse and corruption around the world and, pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq.), took related steps to deal with the unusual and extraordinary threat to the national security, foreign policy, and economy of the United States." in text\
    #         or "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the Federal Vacancies Reform Act " in text\
    #         or "By the authority vested in me as President by the Constitution and the laws of the United States of America, and to improve transparency with respect to the consequences of violating certain regulations and to protect Americans from facing unwarranted criminal punishment for unintentional violations of regulations, it is hereby ordered as follows:" in text\
    #         or "By the authority vested in me as President by the Constitution and the laws of the United States of America,I, DONALD J. TRUMP, President of the United States of America, find that additional actions are necessary to ensure the security of Unmanned Aircraft Systems (UAS) owned, operated, and controlled by the Federal Government;" in text\
    #         or "By the authority vested in me as President of the United States by the Constitution and laws of the United States of America, including section 301 of title 3, United States Code, and sections 3301 and 7301 of title 5, United States Code, it is hereby ordered as follows: " in text\
    #         or "On January 23, 1995, by Executive Order 12947, the President declared a national emergency pursuant to the International Emergency Economic Powers Act (50 U.S.C. 1701-1706) to deal with the unusual and extraordinary threat to the national security, foreign policy, and economy of the United States caused by grave acts of violence committed by foreign terrorists that disrupt the Middle East peace process." in text\
    #         or "The two leaders discussed Ecuador's leadership role in advancing security, prosperity, and democracy in the Western Hemisphere." in text:

    #         return ""
    
    text = remove_alltext(text)
    if text == "":
        return text
    # body
    text = remove_qsession(text)
    text = remove_interruptionsession(text)
    text = remove_audiencesession(text)
    # manual fix
    if "THE PRESIDENT: Come on up, family. Come on up, family." in text:
        text = text.replace("THE PRESIDENT", "")
    if "South Court AuditoriumEisenhower Executive Office Building4:43 P.M. EST THE VICE PRESIDENT:" in text:
        text = text.replace("South Court AuditoriumEisenhower Executive Office Building4:43 P.M. EST THE VICE PRESIDENT:", "")    
    if "For further background, click here." in text:
        text = text.replace("For further background, click here.", text)
    if "For a section-by-section summary, click here." in text:
        text = text.replace("For a section-by-section summary, click here.", text)
    if "For the full text of the legislation, click here." in text:
        text = text.replace("For the full text of the legislation, click here.", text)

    text = replace_proclamation(text)  
    # normally there should be no occurrence of the following from here on
    if len(re.findall(r'(THE VICE PRESIDENT|THE PRESIDENT):', text)) > 0:            
        return ""
    # start                   
    text = replace_transcript_init(text)
    text = replace_contentwarning_init(text)
    # body 
    text = replace_exec_order(text)       
    text = replace_breaktranscript(text)
    text = remove_url(text)        

    #############################################################   CHECK IF NEEDED
    text = replace_senator(text) # for Harris speeches!

    # end
    text = remove_square_brackets(text)
    text = replace_endwithtime(text)
    text = remove_bidenend(text)        
    text = replace_allafterend(text)        
    text = remove_hashprint(text)
    text = remove_hashprint2(text)
    text = remove_hashprint3(text)
    text = remove_hashprint4(text)        
    text = replace_ps(text)    
    text = replace_ps2(text)  
    
    txt = apply_unicode_normalisation(text, unicode_class=unicode_class)
    txt2 = clean_char_repetitions(txt)
    txt3 = unicode_cleanup(txt2)
    txt3 = txt3.strip()
    
    if "Read Democratic presidential nominee Joe Biden's speech to the 2020 Democratic National Convention, as prepared for delivery: " in txt3:        
        txt3 = txt3.replace("Read Democratic presidential nominee Joe Biden's speech to the 2020 Democratic National Convention, as prepared for delivery: ", "")

    # if "joined Senator" in txt3 and not ("said Harris" in txt3 or "said Senator Harris" in txt3 or "Senator Harris said" in txt3) and ("We " in txt3 or " we " in txt3)\
    #         or "letter" in txt3 and ("sent a letter to" in txt3 or "wrote a letter" in txt3 or "Dear Mr. President:" in txt3\
    #                                             or "in a letter to" in txt3 or "wrote the lawmakers" in txt3 or "the senators wrote" in txt3)\
    #                                                 or "The legislation will also bolster the United States Digital Service" in txt3\
    #                                                     or "Harris on Thursday reintroduced the Deterring Espionage by Foreign Entities through National Defense Act, legislation to expand the legal tools" in txt3\
    #                                                         or "Harris and Dianne Feinstein on Wednesday introduced the Protecting Unique and Beautiful Landscapes by Investing in California Lands Act" in txt3\
    #                                                         or "Harris and Congressman Joaquin Castro on Thursday introduced a resolution condemning the presence of white nationalist Stephen Miller in the White House" in txt3\
    #                                                             or "Harris on Wednesday joined Senators Mazie K. Hirono" in txt3\
    #                                                                 or "to introduce the CARES Congressional Oversight Commission Diversity Act" in txt3\
    #                                                                     or "Harris on Tuesday reintroduced the Rent Relief Act, legislation to provide much-needed support to middle class and working Americans" in txt3\
    #                                                                         or "Harris on Friday applauded the advancement of the Safe Housing for Families Act, which requires carbon monoxide detectors in public and publicly subsidized housing." in txt3\
    #                                                                             or "Harris on Monday introduced a Senate resolution affirming the importance of the Civil Rights Act of 1866, Section 1981, one of the country's fundamental anti-discrimination" in txt3\
    #                                                                                 or "Thank you Mr. Chairman. This hearing has brought together more than 50 people to sit inside of a closed door room for hours while our nation is facing a deadly airborne virus." in txt3\
    #                                                                                     or "Chairwoman of the House Financial Services Committee, introduced a companion resolution in the U.S. House of Representatives" in txt3\
    #                                                                                         or "WASHINGTON, D.C. , U.S. Senator Kamala D. Harris (D-CA) and Mark Ghilarducci, Director of the California Governor's Office of Emergency Services" in txt3\
    #                                                                                             or "WASHINGTON, D.C. , U.S. Senator Kamala D. Harris (D-CA) and U.S. Representative Alexandria Ocasio-Cortez (D-NY-14) on Thursday introduced the Climate Equity Act" in txt3\
    #                                                                                                 or "without risk or repercussion,' said Christopher Porter, CTO for Global Cybersecurity Policy, FireEye," in txt3:

    #     return ""

    return txt3


def textclean_miller(text, unicode_class="NFC"):
        
        # remove introductory president announcement
        text = replace_beginwithtime(text)            
        text = replace_allup2vp(text)
        # body
        text = remove_qsession(text)
        text = remove_interruptionsession(text)
        text = remove_audiencesession(text)
        # manual fix
        if "THE PRESIDENT: Come on up, family. Come on up, family." in text:
            text = text.replace("THE PRESIDENT", "")
        if "AUDIENCE: H.R.3! H.R.3! H.R.3!" in text:
            text = text.replace("AUDIENCE: H.R.3! H.R.3! H.R.3!", "")
        text = replace_proclamation(text)
        # normally there should be no occurrence of the following from here on
        if len(re.findall(r'(THE VICE PRESIDENT|THE PRESIDENT|PRESIDENT TRUMP|PRESIDENT BIDEN):', text)) > 0:            
            return ""
        # start                   
        text = replace_transcript_init(text)
        text = replace_contentwarning_init(text)
        # end
        text = remove_square_brackets(text)            
        text = replace_endwithtime(text)
        text = remove_bidenend(text)
        text = replace_allafterend(text)
        text = remove_hashprint(text)
        text = remove_hashprint2(text)
        text = remove_hashprint3(text)
        text = remove_hashprint4(text)
        text = replace_ps(text)
        text = replace_ps2(text)
        
        txt = apply_unicode_normalisation(text, unicode_class=unicode_class)
        txt2 = clean_char_repetitions(txt)
        txt3 = unicode_cleanup(txt2)
        txt3 = txt3.strip()

        return txt3


def clean_miller(directoryin, directoryout, potus, cleanerfunc, unicode_class="NFC", show=False):
            
    miller = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")    
    print("Miller raw - {}".format(potus))     
    print(len(miller))
    miller = clean_speech_texts(miller, cleanerfunc, unicode_class)
    print("Miller clean - {}".format(potus))     
    print(len(miller))  
    miller = miller.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)

    test = pd.read_csv("/home/ioannis/Dropbox (Heriot-Watt University Team)/PoliticalScienceSpeeches/speechdata_TrumpBiden_allpresidentsspeeches/{}/transcriptdata_cleandata.csv".format(potus), sep=",")
    test = test.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)
    print(test.SpeechSegment == miller.CleanText)    
    assert sum(test.SpeechSegment == miller.CleanText)==len(test)
    return 0

    miller.to_csv("{}{}/cleantext_{}.tsv".format(directoryout, potus, potus), index=False, sep="\t")
    miller.to_parquet("{}/rawtext_{}.parquet".format(directoryout, potus), index=False, compression=None)
    miller.to_json("{}/rawtext_{}.jsonl".format(directoryout, potus), orient='records', lines=True)        
    if show:
        for i, row in miller.iterrows():            
            print(i)
            print(row.SpeechURL)
            print(row.RawText)
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)
    
    return miller


def clean_votesmart(directoryin, directoryout, potus, cleanerfunc, unicode_class="NFC", show=False, droplist=None, dropcolumn=None):
    
    votesmart = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    print("Votesmart raw - {}".format(potus))            
    print(len(votesmart))      
    if droplist is not None and dropcolumn is not None:
        votesmart = votesmart[~votesmart[dropcolumn].isin(droplist)]    
        votesmart = votesmart.reset_index(drop=True)
    print(len(votesmart))    
    votesmart = clean_speech_texts(votesmart, cleanerfunc, unicode_class)       
    print("Votesmart clean - {}".format(potus))            
    print(len(votesmart))

    ############################## verify if it's needed for all, not just Harris
    votesmart = votesmart.drop_duplicates(subset="CleanText")
    votesmart = votesmart.reset_index(drop=True)
    print("duplits")
    print(len(votesmart))
    ##############################

    if potus == "KamalaHarris":
        votesmart.CleanText = votesmart.CleanText.apply(replace_allup2harris)
        votesmart.CleanText = votesmart.CleanText.apply(extract_sentences_between_single_quotes)
        votesmart = votesmart[votesmart.CleanText != ""]
        votesmart = votesmart.reset_index(drop=True)
    
    votesmart = votesmart.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)

    test = pd.read_csv("/home/ioannis/Dropbox (Heriot-Watt University Team)/PoliticalScienceSpeeches/speechdata_2020elections/{}/transcriptdata_cleandata.csv".format(potus), sep=",")
    test = test.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)
    ipdb.set_trace()
    print(test.RawText == votesmart.CleanText)    
    assert sum(test.RawText == votesmart.CleanText)==len(test)
    return 0

    
    
    votesmart.to_csv("{}{}/cleantext_{}.tsv".format(directoryout, potus, potus), index=False, sep="\t")
    votesmart.to_parquet("{}/rawtext_{}.parquet".format(directoryout, potus), index=False, compression=None)
    votesmart.to_json("{}/rawtext_{}.jsonl".format(directoryout, potus), orient='records', lines=True)
    if show:
        for i, row in votesmart.iterrows():            
            print(i)
            print(row.SpeechURL)
            print(row.CleanText)
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)
    
    return votesmart

def clean_cspan(directoryin, directoryout, potus, unicode_class="NFC", show=False, dropsegments=None, speechbounds=None):

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
    cspandf = pd.DataFrame.from_dict(cspandf).sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)
    cspandf.to_csv("{}/{}/rawtext_droptitles_{}_edit2.tsv".format(directoryin, potus, potus), sep="\t", index=False)
    if dropsegments is not None:
        cspandf = remove_candidates_dicts(cspandf, dropsegments, "CleanText")     
    if potus == "DonaldTrump":   
        cspandf.CleanText = cspandf.CleanText.apply(remove_trump)
    if potus == "MikePence":   
        cspandf.CleanText = cspandf.CleanText.apply(remove_pence)       
    if potus == "JoeBiden":   
        cspandf.CleanText = cspandf.CleanText.apply(remove_biden)       
    cspandf.CleanText = cspandf.CleanText.apply(remove_dots)
    cspandf.CleanText = cspandf.CleanText.apply(remove_square_brackets)
    cspandf.CleanText = cspandf.CleanText.apply(remove_round_brackets)    

    test = pd.read_csv("/home/ioannis/Dropbox (Heriot-Watt University Team)/PoliticalScienceSpeeches/speechdata_2020elections_cspan/{}/transcriptdata_cleandata.csv".format(potus), sep="\t")
    test = test.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)
    ipdb.set_trace()
    print(test.SpeechSegment == cspandf.CleanText)    
    assert sum(test.SpeechSegment == cspandf.CleanText)==len(test)
    return 0

    def clean_with_encodingclass(x) : return apply_unicode_normalisation(x, unicode_class)
    def clean_strip(x) : return x.strip()
    cspandf.CleanText = cspandf.CleanText.apply(clean_with_encodingclass)    
    cspandf.CleanText = cspandf.CleanText.apply(clean_char_repetitions)        
    cspandf.CleanText = cspandf.CleanText.apply(unicode_cleanup)        
    cspandf.CleanText = cspandf.CleanText.apply(clean_strip)        

    cspandf = cspandf.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)

    cspandf.to_csv("{}/{}/cleantext_{}.tsv".format(directoryout, potus, potus), sep="\t", index=False)
    cspan.to_parquet("{}/rawtext_{}.parquet".format(directoryout, potus), index=False, compression=None)
    cspan.to_json("{}/rawtext_{}.jsonl".format(directoryout, potus), orient='records', lines=True)
    if show:    
        for i, row in cspandf.iterrows():        
            print(i)
            print(row.SpeechURL)
            print(row.CleanText)
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)

def clean_medium(directoryin, directoryout, potus, cleanerfunc, unicode_class="NFC", show=False, droplist=None, dropcolumn=None):

    medium = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    print("Medium raw - {}".format(potus))            
    print(len(medium))      
    if droplist is not None and dropcolumn is not None:
        medium = medium[~medium[dropcolumn].isin(droplist)]    
        medium = medium.reset_index(drop=True)
    medium = clean_speech_texts(medium, cleanerfunc, unicode_class)
    print("Medium clean - {}".format(potus))
    print(len(medium)) 
    medium = medium.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)

    if potus=="KamalaHarris":
        test = pd.read_csv("/home/ioannis/Dropbox (Heriot-Watt University Team)/PoliticalScienceSpeeches/transcriptdatafull_kamalamedium_cleandata.csv".format(potus), sep=",")
    else:
        test = pd.read_csv("/home/ioannis/Dropbox (Heriot-Watt University Team)/PoliticalScienceSpeeches/transcriptdatafull_bidenmedium_cleandata.csv".format(potus), sep=",")
    test = test.sort_values(by=["Date", "SpeechID"]).reset_index(drop=False)
    print(test.RawText == medium.CleanText)    
    assert sum(test.RawText == medium.CleanText)==len(test)
    return 0

    medium.to_csv("{}/cleantext_{}.csv".format(directoryout, potus), index=False)
    medium.to_parquet("{}/rawtext_{}.parquet".format(directoryout, potus), index=False, compression=None)
    medium.to_json("{}/rawtext_{}.jsonl".format(directoryout, potus), orient='records', lines=True) 
    if show:
        for i, row in medium.iterrows():
            print(i)
            print(row.SpeechURL)
            print(row.CleanText)
            print("\n")
            print("\n")
            print("\n")
            time.sleep(3)

