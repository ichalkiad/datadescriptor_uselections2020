import time
import ipdb
import pandas as pd
from us2020data.src.utils import clean_speech_texts, textclean_votesmart,\
                                    textclean_miller, remove_dots, find_substring,\
                                    remove_candidates_dicts, remove_square_brackets, \
                                    remove_round_brackets, segment2quotes, remove_trump, remove_pence#, clean_votesmart, clean_cspan
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


if __name__ == "__main__":
    
    potus = "KamalaHarris"

    # Vote Smart
    directoryin = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data/votesmart/"
    directoryout = "/home/yannis/Dropbox (Heriot-Watt University Team)/datadescriptor_uselections2020/us2020data/data_clean/votesmart/"


    drop_column = "SpeechTitle"
    votesmart = pd.read_csv("{}/{}/rawtext_{}.tsv".format(directoryin, potus, potus), sep="\t")
    votesmart = votesmart[votesmart[drop_column].isin(drop_speechID)]    
    drops = votesmart.SpeechID.values.tolist()
    
    drops1 = clean_votesmart(directoryin, directoryout, potus, textclean_votesmart, "NFC", False, drop_speechID, drop_column)    
    drops.extend(drops1)
    pathlib.Path("{}/{}/".format(directoryout, potus)).mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_dict({"SpeechIDdrop": drops}).to_csv("{}/{}/drop_speech_id.tsv".format(directoryin, potus), sep="\t")