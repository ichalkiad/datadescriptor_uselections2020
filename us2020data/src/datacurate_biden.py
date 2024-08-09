
def removeexcerpt(text):
    if "Read Democratic presidential nominee Joe Biden's speech to the 2020 Democratic National Convention, as prepared for delivery: " in text:
            text = text.replace("Read Democratic presidential nominee Joe Biden's speech to the 2020 Democratic National Convention, as prepared for delivery: ", "")
            print(text)
    return text



if __name__ == "__main__":
    

    potus = "JoeBiden"

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