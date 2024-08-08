import time
import ipdb
import pandas as pd
from us2020data.src.utils import clean_speech_texts, textclean_votesmart,\
                                    textclean_miller, remove_dots, find_substring,\
                                    remove_candidates_dicts, remove_square_brackets, \
                                    remove_round_brackets, remove_trump, clean_votesmart, clean_cspan
import pathlib
import re

def clean_votesmart(directoryin, directoryout, potus, cleanerfunc, unicode_class="NFC", show=False, droplist=None, dropcolumn=None):
    
    drops = []

    votesmart = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    print("Votesmart raw - {}".format(potus))            
    print(len(votesmart))      
    if droplist is not None and dropcolumn is not None:
        votesmart = votesmart[~votesmart[dropcolumn].isin(droplist)]    
        votesmart = votesmart.reset_index(drop=True)
    print(len(votesmart))
    for i, row in votesmart.iterrows():
        if textclean_votesmart(row["RawText"], unicode_class="NFC") == "":
            drops.append(row["SpeechID"])

    return drops

    votesmart = clean_speech_texts(votesmart, cleanerfunc, unicode_class)   
    print("Votesmart clean - {}".format(potus))            
    print(len(votesmart))
    pathlib.Path("{}/{}/".format(directoryout, potus)).mkdir(parents=True, exist_ok=True)
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
    
    potus = "MikePence"
    # Vote Smart
    directoryin = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data/votesmart/"
    directoryout = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data_clean/votesmart/"
    # clean_votesmart(directoryin, directoryout, potus, textclean_votesmart, "NFC", True, drop_speechID, drop_column)

    # drop due to not meeting criteria
    drop_speechID = ["Remarks by Vice President Pence at the Warsaw Ministerial Working Luncheon",
                  "Remarks by Vice President Pence to the Lima Group",
                  "Remarks by Vice President Pence at a Breakfast with Prime Minister Varadkar of Ireland",
                  "Remarks by Vice President Pence and First Lady Fabiana Rosales of the Bolivarian Republic of Venezuela Before Bila ...",
                  "Remarks by Vice President Pence at a Special Session of the United Nations Security Council on the Crisis in Venezuela",
                  "Remarks by Vice President Pence at the Hispanic American Police Command Officers Association Aguila Awards Luncheon",
                  "Remarks by Vice President Pence at the Memorial Service for Senator Richard Lugar",
                  "Remarks by Vice President Pence and Prime Minister Trudeau of Canada Before Bilateral Meeting",
                  "Remarks by Vice President Pence Before Canadian Council for the U.S.-Mexico-Canada Agreement Meeting",
                  "Remarks by Vice President Pence at the Commemoration of the 80th Anniversary of the Outbreak of World War II | War ...",
                  "Remarks by Vice President Pence at the Lord Mayor's International Trade Dinner | London, United Kingdom",
                  "Remarks by Vice President Pence and Prime Minister Morrison of Australia at a Luncheon",
                  "Remarks by Vice President Pence at Reception in Honor of the Prime Minister of the Hellenic Republic",
                  "Remarks by Vice President Pence at the Fifth World Holocaust Forum | Jerusalem, Israel",
                  "Remarks by Vice President Pence at a Proton Therapy Institute Roundtable",
                  "Readout from the Vice President's Discussion with Higher Education Leaders",
                  "Readout from the Vice President's Governors Briefing on COVID-19 Response & Recovery",
                  "Readout from the Vice President's Governors Briefing on COVID-19 Response & Best Practices",
                  "Remarks by Vice President Pence After Meeting with Senate Majority Leader Mitch McConnell and Judge Amy Coney Barr ...",
                  "Vice President Pence Statement on the Passing of Sheldon Adelson",
                  "Remarks by Vice President Pence at the 2019 Munich Security Conference"]
    drop_column = "SpeechTitle"
    votesmart = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    votesmart = votesmart[votesmart[drop_column].isin(drop_speechID)]    
    drops = votesmart.SpeechID.values.tolist()
    
    drops1 = clean_votesmart(directoryin, directoryout, potus, textclean_votesmart, "NFC", True, drop_speechID, drop_column)    
    drops.extend(drops1)
    pathlib.Path("{}/{}/".format(directoryout, potus)).mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_dict({"SpeechIDdrop": drops}).to_csv("{}/{}/drop_speech_id.tsv".format(directoryout, potus), sep="\t")
