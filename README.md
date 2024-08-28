# A text dataset of campaign speeches of the main tickets in the 2020 US presidential election

[![DOI](https://upload.wikimedia.org/wikipedia/commons/d/df/Figshare_logo.svg)](https://10.0.23.196/m9.figshare.26862064)

[![Python 3.8+](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

Unstructured text data have gained popularity in political science, owing to advancements in rigorous *text-as-data* methods that allow extracting insights into election outcomes, candidates' appeal to voters, ideologies and campaign strategies. Existing datasets on US presidential elections campaign speeches are limited in size or source variation, and often contain speeches of different types (debates, rallies, official presidential events, e.g. inauguration, press interviews), thus lacking consistency in their rhetorical content. The introduced dataset comprises the campaign speeches of the Democratic and Republican tickets for the 2020 US presidential election ($1,056$ in total), covering the period between January 2019 and January 2021. Importantly, the dataset dictates specific criteria for the speech rhetorical structure ensuring consistency, critical for quantitative analysis. It has been carefully curated, yet only to the necessary extent as to still be able to inform studies that require semantic or grammatical/syntactical structure. The provided corpus is also hosted on [Figshare](https://10.0.23.196/m9.figshare.26862064) and it aims to enhance timely studies on US presidential elections with high-quality text data.



The dataset contains speeches delivered by the Republican (Donald Trump, Mike Pence) and Democratic (Joe Biden, Kamala Harris) ticket candidates for the presidential and vice-presidential roles during the period of January 2019 - January 2021. This period covers the time between the official launch of Kamala Harris’ campaign (1/2019) and the Inauguration of Joe Biden as newly elected President (1/2021). For this period, text data from candidates' campaign speeches were collected from the following sources:

    1. the Miller Center of the University of Virginia (https://millercenter.org/);
    2. Vote Smart (https://justfacts.votesmart.org/), a non-profit, non-partisan research organization for the collection of information about candidates for public office in the US;
    3. the Cable-Satellite Public Affairs Network (C-SPAN, https://www.c-span.org/), which maintains an archive of televised public campaign speeches;
    4. for the speeches and statements of the Democrats' ticket for the 2020 elections, data were also collected from their personal Medium blogs (https://kamalaharris.medium.com/, https://medium.com/@JoeBiden).


The modalities and style of speeches delivered during a campaign vary and may comprise oral speeches (e.g. debates or Convention speeches), and written statements (e.g. news articles, press releases). To construct a dataset that is coherent in terms of rhetorical structure in the speeches, irrespective of the delivery medium, certain criteria were specified for a speech to be included in the dataset. In particular:

    1. the speeches had to be either oral or written, yet partially or fully scripted; 
    2. the speeches should be destined to an audience of voters, i.e citizens who are not politicians or journalists; 
    3. the speeches had to be delivered and predominantly led by the speaker, rather than a co-host or journalist.

Both the raw and the curated data are provided in three formats to facilitate different processing pipelines:
    
    1. tab-separated file (.tsv) for easy data inspection and format familiarity,
    2. JSONL (.jsonl), i.e. JSON format, one record per file line, for accessibility and easy integration in case of streaming data processing pipelines,
    3. Apache Parquet format (.parquet), which preserves data types and is very useful for Big Data setups and workflows.


### Repository contents

The raw and clean data folders are organized in subfolders, one for each speech source and speaker. The raw data contain the text of the speeches after the initial cleaning (*rawtext\_\{speaker name\}*) and potentially a list of identifiers for speeches that were removed as non-compliant with the dataset criteria (*drop\_speech\_id.tsv*). In the case of C-SPAN, where significant manual curation was needed, the results of the website search are included (*cspan\_\{speaker name\}.csv*) as well as intermediate files (*rawtext\_droptitles\_\{speaker name\}*, *rawtext\_droptitles\_\{speaker name\}\_edit2*, automatically created following the accompanying curation code, *rawtext\_droptitles\_\{speaker name\}\_edit1*, manually created and used by the accompanying curation code), as well as a folder (*specialcleanneeded*) with the transcripts of some particularly long speeches stored individually. The latter was required only for the data curation; these speeches are integrated in the curated dataset folder (*data\_clean*).


The data collection and curation code is included in the *webcollect/* and *src/* folders of the GitHub repository, while supporting topic dictionaries are provided in the folder *lexica/*.

The *webcollect* folder contains the scraping scripts per speech source (site structure at the time of the data collection):

    1. webscrape_bidenmedium.py and webscrape_harrismedium.py: each contains the scraping code for the Medium blog of candidates Joe Biden and Kamala Harris. The latter script contains the function that extracts the speech transcript (get_president_speech), which is common in both scripts.
    2. webscrape_cspan.py: the script loads the spreadsheet extracted from C-SPAN, containing the URLs to potentially relevant dataset speeches. It then iterates over each item and extracts the speech using its transcription URL.
    3. webscrape_miller_daterange.py: the script extracts the list of speeches per president, and scrapes the transcript of each speech that falls in the focus period.
    4. webscrape_votesmart.py: the scripts iterates over the relevant speech types per candidate, obtains the URL of each speech, and subsequently extracts the transcript.

The *src* folder contains the scripts for the data curation. In particular:

    1. quotes.py: auxiliary script containing the Unicode code points for quotation marks. The script is used to ensure that all quotes have a uniform Unicode representation to facilitate their processing.
    2. utils.py: contains all pre-processing code, namely the designed regular expressions, functions that operate on the raw text and pre-process it, as well as wrapper cleaning functions that consider the specificities of each source, apply the corresponding pre-processing steps and store the cleaned data.
    3. datacurate_\{speaker surname$\}.py: one curation script per candidate, calling the cleaning function that corresponds to each source.

The *lexica* folder contains supporting word dictionaries, extracted from the Oxford Dictionaries series for further processing of the text data when needed.


The code for the Structural Topic Model case study is provided in the folder *stm/*. It contains the following files, which are presented in their execution order, as the number in the filename also indicates:

    1. postscrape_elections2020_0.py: the data per speaker are combined to include all speech sources in a single file and the speeches are split into sentences. The script also plots basic summary statistics.
    2. postprocess_elections2020_1.py: the dataset is tokenised, using the provided dictionary, and summary statistics after tokenisation are plotted.
    3. prepare_data_stm_elections2020_2.py: the dataset is split into the time windows where the STM will be applied and the time covariates are constructed. To ensure full control over the text processing, the script also constructs the document-term matrices and vocabulary per time window, which will be loaded in the STM script.
    4. stm_parallel_onepiece_elections2020_3.R: R script that estimates the STM per time window, runs a number of diagnostic routines (check_residuals, sageLabels) and computes metrics for model selection.
    5. gatherresults_stm_elections2020_4.R: summarizes the output of the STM estimation over all time window folders.
    6. postprocess_stm_elections2020_5.py: the script analyses the best topic model per time window, summarizes the STM-discovered topics and outputs a summary spreadsheet.
    7. postprocess_stm_goldtopics_distributionOndictionaries_elections2020_6.py: estimates the distribution of the most representative words per reference topic (identified as described in the previous section) over the dictionaries we utilized.
    8. postprocess_stm_distributionOndictionaries_elections2020_7.py: estimates, for each time window, the distribution of the STM-discovered topics (identified as described in the previous section) over the dictionaries we utilized.
    9. postprocess_stm_goldtopics_match_elections2020_8.py: labels the STM-discovered topics with one of the reference topics for political science.
    10. postprocess_stm_potustopics_elections2020_9.py: summarizes STM and topic labeling output into a spreadsheet for easy visualization and analysis.
    11. postprocess_stm_significance_timecovariate_10.py: assesses the statistical significance of the time covariate by computing the percentage of the coefficients of the spline for the time covariate that were statistically significant at the 5% level.


### Cite the dataset as follows:

Text:

Chalkiadakis, I., d’ Auriac Louise Anglés, Peters, G. W. & Frau-Meigs, D. A text dataset of campaign speeches of the main tickets in the 2020 us presidential election. Figshare https://10.6084/m9.figshare.26862064 (2024).


Bibtex:

@misc{chalkiadakisdauriac2024,
  author = {Chalkiadakis, I. and d' Auriac Louise Angl\'es, and Peters, Gareth W., and Frau-Meigs, Divina},
  year = {2024},
  title = {A text dataset of campaign speeches of the main tickets in the 2020 US presidential election},
  howpublished = {\emph{figshare} \url{https://10.6084/m9.figshare.26862064}}
}

