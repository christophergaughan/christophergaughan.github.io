---
layout: post
title: "My Blog Post"
date: 2023-05-06
---
<div id="4b0aa222" class="cell markdown">

# Introduction:

As an undergraduate, I became fascinated by the adaptability of
antibodies to bind to specific parts of a molecule in real-time,
effectively inactivating potential downstream usage of that bound
moiety. This process by which antibodies are refined for such
specificity reflects the evolutionary selection that all organisms
undergo, making it all the more impressive. Antibodies can also interact
with other molecules in the immune system, such as the complement
cascade, which forms a complex signaling network that ultimately
destroys invading pathogens. Antibodies are extremely cool.

It comes as no surprise that monoclonal antibodies (mAbs) have proven to
be valuable in the fight against cancer. Clinical trials offer an
exceptional opportunity to assess the efficacy of biologic agents like
mAbs. Clinical trial data, which is carefully categorized and stored in
archives like the US Government Archives and the NHS in the UK, can
inform decision-making and contribute to the development of successful
trials.

In this series of Jupyter notebooks, we explore clinical trials
involving mAbs on solid tumors, utilizing API calls to
ClinicalTrials.gov and PySpark for efficient data processing and
analysis. Our objective is to perform an exploratory data analysis,
complete3 with graphs and charts. If you've never done such a thing and
are interested, you can look at these databook and use them as a guide.
I will explain the code with interior markups as well as things that you
should be looking for.

**CAUTION**: Yes, we know that chat-GPT is out there and can help you
write code such as I've written here. In fact, I, too, have used
chat-GPT to write code where I was unsure of the best way to approach
things. Further, I cut and pasted code into chat-GPT so it would ,mark
it up in comments.*However: you must learn at least the basics of
Python, libraries such as NumPy, Pandas, plotting libraries such as
Seaborn and matplotlib. If you are going to model, you must learn things
like scikit-learn, and ML theory in general.* The reason you need to
know this is that chat-GPT is error-prone, often writes functions
without calling said functions, can write long form code that doesn't
meet your specifications, Garbage-in: Garbage-out. **SO at the very
least: be good at reading code** You should focus on the library data
form as JSON, the data form most used in the output of such clinical
data is in JSON (which is a library). So if you are a beginner- read on
because I am demonstrating how to get data from a **Public Data Base**.
Public data bases can serve as a fantastic resource into getting
clinical data. Here we focus on clinical cancer data and there are
numerous databases to get very specific information on cancer. There are
several public databases that can serve as a source of clinical data
about cancer. These databases can be used to identify patient
populations, investigate treatment outcomes, and study disease
progression. Some of the most commonly used databases include:

1.  Surveillance, Epidemiology, and End Results (SEER): SEER is a
    program of the National Cancer Institute that collects and publishes
    cancer incidence and survival data from population-based cancer
    registries covering approximately 35% of the U.S. population.

2.  National Cancer Database (NCDB): NCDB is a joint program of the
    American College of Surgeons Commission on Cancer and the American
    Cancer Society. It collects data on cancer incidence, treatment, and
    outcomes from more than 1,500 hospitals across the United States.

3.  CancerLinQ: CancerLinQ is an initiative of the American Society of
    Clinical Oncology (ASCO) that collects and analyzes data from
    electronic health records (EHRs) to improve the quality of cancer
    care. The database currently contains data on over 1 million cancer
    patients.

4.  ClinicalTrials.gov: ClinicalTrials.gov is a registry and results
    database of publicly and privately supported clinical studies of
    human participants conducted around the world. It contains
    information on over 400,000 clinical trials, many of which include
    data on cancer patients.

5.  Cancer Research UK Clinical Trials Database: This database provides
    information on cancer clinical trials conducted in the UK and covers
    all types of cancer, as well as the latest treatment approaches.

These databases can provide valuable insights into the epidemiology,
diagnosis, and treatment of cancer, and can help researchers identify
areas where new research is needed. However, it's important to note that
there may be limitations in the data available in these databases, and
researchers need to be careful to ensure that their analyses are
appropriate for the available data.

You should also know about some shortcoming of using public data-bases:

**Shortcomings of just ClinicalTrials.gov:**

1.  Incomplete information: Although ClinicalTrials.gov is a
    comprehensive database of ongoing and completed clinical trials,
    some trials may not be listed on the site. Additionally, some trials
    may be listed with incomplete or inaccurate information, making it
    difficult to interpret the results.

2.  Bias: ClinicalTrials.gov relies on trial sponsors to submit their
    data, and there may be a bias towards trials that are more likely to
    produce positive results. This can make it difficult to get an
    accurate picture of the efficacy of a particular treatment.

3.  Time lag: There may be a time lag between when a trial is completed
    and when the results are published on ClinicalTrials.gov. This can
    make it difficult to stay up to date with the latest research in a
    particular field.

4.  At first, you can get a cap of 10,000 studies. However, if you keep
    querying the DataBase, you will not not be able to get more than
    ~200 studies. This can cause headaches.

Shortcomings of public databases:

1.  Data quality: The quality of the data in public databases can vary
    widely, depending on the source of the data and the methods used to
    collect it. Researchers need to be careful to verify the accuracy of
    the data before using it in their studies.

2.  Incompatibility: Public databases may use different data formats and
    structures, which can make it difficult to integrate data from
    multiple sources. Researchers may need to spend a significant amount
    of time cleaning and restructuring the data before it can be used.

3.  Limited scope: Public databases may only contain data on a specific
    subset of the population, such as patients with a particular disease
    or participants in a specific clinical trial. This can limit the
    generalizability of the findings and make it difficult to draw
    broader conclusions.

Which brings us to our next topic: We will be carrying out API calls on
ClicicvaslTrials.gov. Thus you need to familarize yourself to with
libraries such as `requests`, `json` and of course `pandas`. Later we
will be using Apache Spark and Pyspark to handle our requests and parse
the data. We will be using files such as parquet files so we can save
disk-space on our local machines. You should familaiarize yourselves
with these tools.

All that said, I performed all these analyses on my Macbook Pro. No
cloud assitance weas needed for these queries. However, we will use such
tools later on in this series.

**NOTE** I have not defined a `random seed` anyplace in this notebook.
So if you try to run it on your own machine, your results might be
different.

**A Note for Prospective Cancer Patients:** This Jupyter notebook is
designed to provide valuable insights and information on clinical trials
involving monoclonal antibodies for solid tumors. If you are a patient
seeking information about your specific condition, this notebook can
serve as a starting point for understanding the landscape of available
clinical trials and potential treatment options. However, it is crucial
to recognize that using code and data analysis without a thorough
understanding of the underlying concepts can lead to inaccurate or
misleading results. It is always best to consult with your healthcare
provider and rely on their guidance before making any decisions about
your treatment. Additionally, remember that the data provided here is
subject to change, as new trials are conducted and new treatments become
available. Always verify the most current information with trusted
sources and seek professional advice to ensure you are making informed
decisions about your health.

</div>

<div id="8b3e3cf6" class="cell markdown">

Our goal is to use large datasets from ClinicalTrials.gov to observe the
construction of clinical trials by identifying common variables that
affect trial status. To achieve this, we will employ a four-step
strategy.

1.  First, we will clean the data by converting arrays to single values,
    handling missing data, and converting data types where necessary.
    Then, we will perform basic exploratory data analysis (EDA) to find
    relationships between variables and trial status.

2.  Next, we will use feature selection to identify a subset of
    variables that might be useful in predicting the trial status.
    Finally, we will use machine learning algorithms to build models
    that predict trial status based on the selected variables.

3.  To obtain our data, we will use API calls to ClinicalTrials.gov and
    parse the data using the PySpark module of Apache Spark. As we
    progress, we will incorporate other databases to further refine our
    analyses.

</div>

<div id="78a6a75b" class="cell code" execution_count="35">

``` python
import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import mannwhitneyu

import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, KBinsDiscretizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import os
```

</div>

<div id="de884e38" class="cell markdown">

**Here is our entry point into the world of clinical trials. The code
below retrieves information about a clinical study from a website using
Python's requests library and parses the response as a JSON (JavaScript
Object Notation) object. Here is a line-by-line explanation:**

url = "<https://tinyurl.com/yc89mccn>" I wanted to make this first
notebook look less formidable, I compressed the url.

- A variable called url is created and assigned the value of the URL for
  the clinical study information. In this case, a shortened URL is used
  for readability. `response = requests.get(url)`

- A GET request is sent to the URL using the requests.get() function
  from the requests library. The response from the server is stored in
  the response variable.
  `response_str = response.content.decode("utf-8")`

- The response content is in bytes format, so it is decoded into a
  string using the decode() method with the "utf-8" encoding. The
  resulting string is stored in the response_str variable.
  `response_json = json.loads(response_str)`

- The decoded string is parsed as a JSON object using the json.loads()
  function from the json library. The resulting JSON object is stored in
  the response_json variable.
  `study_fields = response_json["StudyFieldsResponse"]["StudyFields"]`

The JSON object contains nested dictionaries, and the information about
the study is stored in the "StudyFields" key within the
"StudyFieldsResponse" key. This information is extracted and stored in
the study_fields variable for further processing. Overall, this code
retrieves clinical study information from a website and converts it into
a JSON object for further analysis and manipulation in Python.

</div>

<div id="9f07d8b1" class="cell code" execution_count="41">

``` python
url = "https://tinyurl.com/yc89mccn"  # note I use `tinyurl` to make this readable
response = requests.get(url)

# Convert the byte string to a string we humans read
response_str = response.content.decode("utf-8")

# Parse the string as JSON (think dictionary data form)
response_json = json.loads(response_str)

# Access the study fields
study_fields = response_json["StudyFieldsResponse"]["StudyFields"]
```

</div>

<div id="c905fdb4" class="cell markdown">

**This code retrieves 1000 clinical studies**

</div>

<div id="9e7e33fc" class="cell code" execution_count="44">

``` python
number_of_trials = len(study_fields)
print(number_of_trials)
```

<div class="output stream stdout">

    1000

</div>

</div>

<div id="91cf0332" class="cell code" execution_count="12">

``` python
# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(study_fields)

# Display the first few rows of the DataFrame- just a regular pandas df using the head() function
print(df.head())
```

<div class="output stream stdout">

       Rank          NCTId                                         BriefTitle  \
    0     1  [NCT04895566]  [Phase 0/1 Local Application of the Monoclonal...   
    1     2  [NCT04895137]  [mFOLFOX6+Bevacizumab+PD-1 Monoclonal Antibody...   
    2     3  [NCT05557903]  [Phase Ⅰ Clinical Study of Anti-CD52 Monoclona...   
    3     4  [NCT05039580]  [Programmed Cell Death Protein-1 (PD-1) Monocl...   
    4     5  [NCT04198623]  [Efficacy of Montelukast in Reducing the Incid...   

      OverallStatus            StartDate PrimaryCompletionDate         StudyType  \
    0   [Completed]       [May 24, 2021]      [March 10, 2023]  [Interventional]   
    1  [Recruiting]        [May 1, 2021]         [May 1, 2022]  [Interventional]   
    2  [Recruiting]  [December 20, 2021]   [December 30, 2022]  [Interventional]   
    3  [Recruiting]       [May 15, 2021]      [April 30, 2023]  [Interventional]   
    4  [Recruiting]     [March 20, 2020]  [September 20, 2023]  [Interventional]   

                 Phase EnrollmentCount InterventionType  \
    0  [Early Phase 1]            [10]     [Biological]   
    1        [Phase 2]            [42]           [Drug]   
    2        [Phase 1]            [71]     [Biological]   
    3        [Phase 4]            [36]           [Drug]   
    4        [Phase 2]            [80]           [Drug]   

                                         LeadSponsorName  \
    0                         [SWISS BIOPHARMA MED GmbH]   
    1  [Sixth Affiliated Hospital, Sun Yat-sen Univer...   
    2  [Lanzhou Institute of Biological Products Co.,...   
    3  [The First Affiliated Hospital of Soochow Univ...   
    4          [University of California, San Francisco]   

                                   PrimaryOutcomeMeasure  \
    0  [Objective response rate (ORR) in patients wit...   
    1                                         [PCR rate]   
    2  [Number of participants with treatment-related...   
    3                [Response rate, EBV-DNA viral load]   
    4  [The incidence rates of standard infusion reac...   

                                 SecondaryOutcomeMeasure  
    0  [Duration of response (DoR) of patients with s...  
    1  [Incidence rate of Grade ≥3 PD-1monoclonal ant...  
    2  [Pharmacokinetic (PK) evaluation of anti-CD52 ...  
    3  [Time for treatment works, Toxicity of PD-1 mo...  
    4  [Average infusion duration of each cycle the m...  

</div>

</div>

<div id="2de08420" class="cell markdown">

The
`df = df.applymap(lambda x: x[0] if isinstance(x, list) and len(x) == 1 else x)`
in the next cell is applied to a pandas DataFrame (df) and is used to
convert *list values* containing only a single elements into single
values. This is done using the applymap() function, which applies a
given function to each element of the DataFrame. In this case, the
lambda function checks if the element is a list and has only one item,
and if so, it replaces the element with the single value from the list.

The purpose of this step is to simplify and clean the DataFrame by
removing unnecessary list structures that can make data manipulation and
analysis more complicated. This step can be particularly useful when
working with data that has been scraped from websites, parsed from
various file formats, or processed through APIs, as these processes can
sometimes generate lists containing single elements instead of simple
scalar values.

The print(df.head()) line at the end of the code snippet is used to
display the first few rows of the cleaned DataFrame, allowing you to
verify that the transformation has been applied correctly and observe
the resulting data structure.

</div>

<div id="4d013ef6" class="cell code" execution_count="13">

``` python
# Convert list values to single values
df = df.applymap(lambda x: x[0] if isinstance(x, list) and len(x) == 1 else x)

print(df.head())
```

<div class="output stream stdout">

       Rank        NCTId                                         BriefTitle  \
    0     1  NCT04895566  Phase 0/1 Local Application of the Monoclonal ...   
    1     2  NCT04895137  mFOLFOX6+Bevacizumab+PD-1 Monoclonal Antibody ...   
    2     3  NCT05557903  Phase Ⅰ Clinical Study of Anti-CD52 Monoclonal...   
    3     4  NCT05039580  Programmed Cell Death Protein-1 (PD-1) Monoclo...   
    4     5  NCT04198623  Efficacy of Montelukast in Reducing the Incide...   

      OverallStatus          StartDate PrimaryCompletionDate       StudyType  \
    0     Completed       May 24, 2021        March 10, 2023  Interventional   
    1    Recruiting        May 1, 2021           May 1, 2022  Interventional   
    2    Recruiting  December 20, 2021     December 30, 2022  Interventional   
    3    Recruiting       May 15, 2021        April 30, 2023  Interventional   
    4    Recruiting     March 20, 2020    September 20, 2023  Interventional   

               Phase EnrollmentCount InterventionType  \
    0  Early Phase 1              10       Biological   
    1        Phase 2              42             Drug   
    2        Phase 1              71       Biological   
    3        Phase 4              36             Drug   
    4        Phase 2              80             Drug   

                                         LeadSponsorName  \
    0                           SWISS BIOPHARMA MED GmbH   
    1  Sixth Affiliated Hospital, Sun Yat-sen University   
    2  Lanzhou Institute of Biological Products Co., Ltd   
    3  The First Affiliated Hospital of Soochow Unive...   
    4            University of California, San Francisco   

                                   PrimaryOutcomeMeasure  \
    0  Objective response rate (ORR) in patients with...   
    1                                           PCR rate   
    2  Number of participants with treatment-related ...   
    3                [Response rate, EBV-DNA viral load]   
    4  The incidence rates of standard infusion react...   

                                 SecondaryOutcomeMeasure  
    0  Duration of response (DoR) of patients with se...  
    1  [Incidence rate of Grade ≥3 PD-1monoclonal ant...  
    2  [Pharmacokinetic (PK) evaluation of anti-CD52 ...  
    3  [Time for treatment works, Toxicity of PD-1 mo...  
    4  [Average infusion duration of each cycle the m...  

</div>

</div>

<div id="4d07e215" class="cell markdown">

### However, there are still some cells in the "PrimaryOutcomeMeasure" and "SecondaryOutcomeMeasure" columns that contain lists with multiple values. We will process them further for simplification.

This code converts any lists in the 'PrimaryOutcomeMeasure' and
'SecondaryOutcomeMeasure' columns of the DataFrame into comma-separated
strings, while leaving any other data types unchanged. This is useful
for data cleaning and analysis, as it ensures that the columns contain
consistent data types for further processing.

Here is a line-by-line explanation:

- df\['PrimaryOutcomeMeasure'\] =
  df\['PrimaryOutcomeMeasure'\].apply(lambda x: ', '.join(x) if
  isinstance(x, list) else x) <br>

- This line uses the apply() method on the 'PrimaryOutcomeMeasure'
  column of the DataFrame. The apply() method applies a function to each
  element of the column. In this case, the function is a lambda function
  that takes an input x. <br>

- The lambda function checks if x is a list using the isinstance()
  method. If x is a list, it joins the elements of the list into a
  string separated by commas using the join() method. If x is not a
  list, it returns x. <br>

- The result of the lambda function is assigned to the
  'PrimaryOutcomeMeasure' column of the DataFrame using the indexing
  operator \[ \]. <br>

df\['SecondaryOutcomeMeasure'\] =
df\['SecondaryOutcomeMeasure'\].apply(lambda x: ', '.join(x) if
isinstance(x, list) else x) <br>

- This line is similar to the first line, but it applies the same lambda
  function to the 'SecondaryOutcomeMeasure' column of the DataFrame
  instead.

### Also below you will see some fields that might be new to you in the output. When searching for clinical trials, you may come across various columns that provide information about the study. Here are some common columns you might encounter and what they mean:

**Rank**: The position of the study in the search results based on the
search criteria.

**NCTId**: The unique identifier for the study in the clinical trials
registry. This ID can be used to search for more information about the
study.

**BriefTitle**: A short title that summarizes the study's purpose or
main focus.

**OverallStatus**: The current status of the study, such as recruiting,
active but not recruiting, completed, or terminated.

**StudyType**: The type of study, such as observational, interventional,
or expanded access.

**Phase**: If the study is an interventional study, the phase indicates
the stage of the study, such as *Phase 1, Phase 2, Phase 3, or Phase 4.*

**InterventionType**: The type of intervention being tested, such as
Biological, Drug, Behavioral, or Device.

**LeadSponsorName**: The organization or individual responsible for
leading the study.

**PrimaryOutcomeMeasure**: The main outcome measure(s) the study is
designed to evaluate.

**SecondaryOutcomeMeasure**: Additional outcome measure(s) the study may
evaluate.

Other columns you may encounter can provide additional information about
the study design, eligibility criteria, or results. Understanding the
meaning of these columns can help you evaluate the relevance and
potential benefits of a clinical trial for yourself or a loved one.

</div>

<div id="3c74f22b" class="cell code" execution_count="14">

``` python
# Concatenate list items in the 'PrimaryOutcomeMeasure' and 'SecondaryOutcomeMeasure' columns
df['PrimaryOutcomeMeasure'] = df['PrimaryOutcomeMeasure'].apply(
    lambda x: ', '.join(x) if isinstance(x, list) else x)
df['SecondaryOutcomeMeasure'] = df['SecondaryOutcomeMeasure'].apply(
    lambda x: ', '.join(x) if isinstance(x, list) else x)


print(df.head())
```

<div class="output stream stdout">

       Rank        NCTId                                         BriefTitle  \
    0     1  NCT04895566  Phase 0/1 Local Application of the Monoclonal ...   
    1     2  NCT04895137  mFOLFOX6+Bevacizumab+PD-1 Monoclonal Antibody ...   
    2     3  NCT05557903  Phase Ⅰ Clinical Study of Anti-CD52 Monoclonal...   
    3     4  NCT05039580  Programmed Cell Death Protein-1 (PD-1) Monoclo...   
    4     5  NCT04198623  Efficacy of Montelukast in Reducing the Incide...   

      OverallStatus          StartDate PrimaryCompletionDate       StudyType  \
    0     Completed       May 24, 2021        March 10, 2023  Interventional   
    1    Recruiting        May 1, 2021           May 1, 2022  Interventional   
    2    Recruiting  December 20, 2021     December 30, 2022  Interventional   
    3    Recruiting       May 15, 2021        April 30, 2023  Interventional   
    4    Recruiting     March 20, 2020    September 20, 2023  Interventional   

               Phase EnrollmentCount InterventionType  \
    0  Early Phase 1              10       Biological   
    1        Phase 2              42             Drug   
    2        Phase 1              71       Biological   
    3        Phase 4              36             Drug   
    4        Phase 2              80             Drug   

                                         LeadSponsorName  \
    0                           SWISS BIOPHARMA MED GmbH   
    1  Sixth Affiliated Hospital, Sun Yat-sen University   
    2  Lanzhou Institute of Biological Products Co., Ltd   
    3  The First Affiliated Hospital of Soochow Unive...   
    4            University of California, San Francisco   

                                   PrimaryOutcomeMeasure  \
    0  Objective response rate (ORR) in patients with...   
    1                                           PCR rate   
    2  Number of participants with treatment-related ...   
    3                  Response rate, EBV-DNA viral load   
    4  The incidence rates of standard infusion react...   

                                 SecondaryOutcomeMeasure  
    0  Duration of response (DoR) of patients with se...  
    1  Incidence rate of Grade ≥3 PD-1monoclonal anti...  
    2  Pharmacokinetic (PK) evaluation of anti-CD52 m...  
    3  Time for treatment works, Toxicity of PD-1 mon...  
    4  Average infusion duration of each cycle the mo...  

</div>

</div>

<div id="c4ed85f9" class="cell markdown">

<b>Visualization</b>: We will create visualizations to better understand
the data, such as bar charts showing the number of trials per study
phase or sponsor, or a line chart showing the trend of trial start dates
over time. This can help you identify patterns or trends in the data.
Notice that we have other data than Phases I, II, and III trials

</div>

<div id="53b425e0" class="cell code" execution_count="15">

``` python

# Count the number of trials per study phase
phase_counts = df['Phase'].value_counts()

# Convert index to a list of strings
phase_index = [str(x) for x in phase_counts.index]

# Plot the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=phase_index, y=phase_counts.values)
plt.xlabel('Study Phase')
plt.ylabel('Number of Trials')
plt.title('Number of Trials per Study Phase')
# Rotate the x-axis labels- you can get cute and use < 90 degrees as well
plt.xticks(rotation=90)

# Don't forget this line or nothing will show up
plt.show()

```

<div class="output display_data">

![](/_images/First_Notebook_13_0.png)

</div>

</div>

<div id="7a4a4aa7" class="cell markdown">

### The next code block can be used to create a bar chart showing the number of trials per lead sponsor. This can help identify which sponsors are running the most trials.

</div>

<div id="a74db2fb" class="cell code" execution_count="16">

``` python


# Count the number of trials per lead sponsor
sponsor_counts = df['LeadSponsorName'].value_counts().head(10)

# Convert index to a list of strings
sponsor_index = [str(x) for x in sponsor_counts.index]

# Plot the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=sponsor_counts.values, y=sponsor_index)
plt.xlabel('Number of Trials')
plt.ylabel('Lead Sponsor')
plt.title('Top 10 Lead Sponsors by Number of Trials')

plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_15_0.png)

</div>

</div>

<div id="5a2e7b16" class="cell markdown">

### We create a line chart showing the trend of trial start dates over time. This can help highlight crucial patterns or trends in the data that might have gone overlooked.

- It seems that there is an issue with the data in the 'StartDate'
  column. The error indicates that some values in the column might be
  lists instead of strings or datetime objects. Let's try to identify
  and fix these problematic values.

First, let's find out if there are any non-string values in the
'StartDate' column:

</div>

<div id="feb3702f" class="cell code" execution_count="17">

``` python
non_string_values = df[df['StartDate'].apply(lambda x: not isinstance(x, str))]
print(non_string_values)
```

<div class="output stream stdout">

         Rank        NCTId                                         BriefTitle  \
    27     28  NCT00001105  The Safety and Effectiveness of Human Monoclon...   
    86     87  NCT00040586  Phase II Trial of Monoclonal Antibody (J591) i...   
    90     91  NCT00043706  Safety, Tolerability, and Pharmacokinetics of ...   
    202   203  NCT00000836  A Phase II/III Trial of Human Anti-CMV Monoclo...   
    266   267  NCT00002268  A Randomized, Phase I/II Trial to Assess the S...   
    275   276  NCT00002016  A Phase I/II Trial to Assess the Safety and To...   
    283   284  NCT00650026  Early Access Program of the Safety of Human An...   
    374   375  NCT00311545  S0351, CNTO 328 in Treating Patients With Unre...   
    425   426  NCT04346277  Compassionate Use Open-Label Anti-CD14 Treatme...   
    491   492  NCT00650390  Open Label Study to Assess Efficacy and Safety...   
    494   495  NCT00649545  Study of the Human Anti-TNF Monoclonal Antibod...   
    530   531  NCT01430429  Primary Biliary Cirrhosis: Investigating A New...   
    532   533  NCT00092924  Study of TRM-1(TRAIL-R1 Monoclonal Antibody) i...   
    652   653  NCT00051597  A Safety/Efficacy Study of SGN-30 (Antibody) i...   
    873   874  NCT05067166  Open-Label Expanded Access for Ebola-Infected ...   

                  OverallStatus StartDate PrimaryCompletionDate        StudyType  \
    27                Completed        []                    []   Interventional   
    86                Completed        []                    []   Interventional   
    90                Completed        []                    []   Interventional   
    202               Completed        []                    []   Interventional   
    266               Completed        []                    []   Interventional   
    275               Completed        []                    []   Interventional   
    283  Approved for marketing        []                    []  Expanded Access   
    374               Withdrawn        []                    []   Interventional   
    425     No longer available        []                    []  Expanded Access   
    491  Approved for marketing        []                    []  Expanded Access   
    494  Approved for marketing        []                    []  Expanded Access   
    530              Terminated        []                    []   Interventional   
    532               Completed        []          January 2005   Interventional   
    652               Completed        []                    []   Interventional   
    873               Available        []                    []  Expanded Access   

                      Phase EnrollmentCount InterventionType  \
    27              Phase 1               8             Drug   
    86              Phase 2              []     [Drug, Drug]   
    90   [Phase 1, Phase 2]              []             Drug   
    202             Phase 2             300             Drug   
    266             Phase 1              []             Drug   
    275             Phase 1              []             Drug   
    283                  []              []       Biological   
    374             Phase 2               0       Biological   
    425                  []              []       Biological   
    491                  []              []       Biological   
    494                  []              []       Biological   
    530             Phase 2              []             Drug   
    532             Phase 2              []             Drug   
    652  [Phase 1, Phase 2]              70             Drug   
    873                  []              []             Drug   

                                           LeadSponsorName PrimaryOutcomeMeasure  \
    27   National Institute of Allergy and Infectious D...                         
    86                                       BZL Biologics                         
    90                           Genzyme, a Sanofi Company                         
    202  National Institute of Allergy and Infectious D...                         
    266                                             Sandoz                         
    275                                             Sandoz                         
    283                                             Abbott                         
    374                       SWOG Cancer Research Network                         
    425                                Implicit Bioscience                         
    491                                             Abbott                         
    494                                             Abbott                         
    530              Light Chain Bioscience - Novimmune SA                         
    532                         Human Genome Sciences Inc.                         
    652                                        Seagen Inc.                         
    873                      Ridgeback Biotherapeutics, LP                         

        SecondaryOutcomeMeasure  
    27                           
    86                           
    90                           
    202                          
    266                          
    275                          
    283                          
    374                          
    425                          
    491                          
    494                          
    530                          
    532                          
    652                          
    873                          

</div>

</div>

<div id="d1146d70" class="cell markdown">

#### It looks like there are some rows with empty lists \[\] as the 'StartDate'. We can replace these with None or a specific placeholder value like 'Unknown'. Here's how to replace them with None:

</div>

<div id="276eec33" class="cell code" execution_count="18">

``` python
df['StartDate'] = df['StartDate'].apply(lambda x: None if isinstance(x, list) and not x else x)
```

</div>

<div id="47b7244c" class="cell code" execution_count="19">

``` python
# Convert StartDate to datetime format
df['StartDate'] = pd.to_datetime(df['StartDate'])

# Create a new DataFrame with yearly counts of trials
trial_start_years = df['StartDate'].dt.year.value_counts().sort_index()

# Plot the line chart
plt.figure(figsize=(10, 6))
sns.lineplot(x=trial_start_years.index, y=trial_start_years.values)
plt.xlabel('Year')
plt.ylabel('Number of Trials')
plt.title('Number of Trials Started per Year')
plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_20_0.png)

</div>

</div>

<div id="3ef14041" class="cell markdown">

### The spike in the number of trials during ~ 2020 - 2022 *could* be related to specific research areas like Covid-19, or it could be that more effective treatments (see Checkpoint Inhibitors) have been sudied, or **Both**\*. However there are other possibilities b/c of our search terms. So lets consider the following:

<p></p>
<p></p>

- Visualize the number of trials per research area (based on BriefTitle
  or another relevant column) during the 2019-2020 period.
- Visualize the distribution of intervention types (based on
  InterventionType column) during the 2019-2020 period.
- Visualize the distribution of study phases (based on Phase column)
  during the 2019-2020 period.

<p></p>
<p></p>

#### <i>Let's create a visualization of the distribution of intervention types during the 2019-2020 period as an example:</i>

</div>

<div id="45fbd8de" class="cell code" execution_count="20">

``` python
# Filter the DataFrame for trials started between 2019 and 2020
df_2019_2020 = df[(df['StartDate'].dt.year >= 2019) & (df['StartDate'].dt.year <= 2020)]

# Count the occurrences of each intervention type
intervention_counts = df_2019_2020['InterventionType'].explode().value_counts()

# Plot the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=intervention_counts.index, y=intervention_counts.values)
plt.xlabel('Intervention Type')
plt.ylabel('Number of Trials')
plt.title('Number of Trials by Intervention Type (2019-2020)')
plt.xticks(rotation=90)
plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_22_0.png)

</div>

</div>

<div id="e633faff" class="cell markdown">

**WOW! Look at the number of drug trials (2019-2020) IS it possible that
the high number of drug trials during the 2020 - 2022 period is due to
the COVID-19 pandemic? Many trials were initiated for potential
treatments, including monoclonal antibodies and other drug types.**

Now, let's perform some descriptive analysis on the DataFrame to get a
better understanding of the data. We can calculate summary statistics
like the number of unique interventions, the distribution of study
phases, and the number of trials per sponsor:

</div>

<div id="4826d758" class="cell code" execution_count="21">

``` python
# Number of unique interventions
unique_interventions = df['InterventionType'].explode().nunique()
print(f"Number of unique interventions: {unique_interventions}")

# Distribution of study phases
phase_distribution = df['Phase'].explode().value_counts()
print("\nDistribution of study phases:")
print(phase_distribution)

# Number of trials per sponsor
trials_per_sponsor = df['LeadSponsorName'].value_counts()
print("\nTop 10 sponsors with the most trials:")
print(trials_per_sponsor.head(10))
```

<div class="output stream stdout">

    Number of unique interventions: 10

    Distribution of study phases:
    Phase 1           529
    Phase 2           432
    Phase 3            97
    Not Applicable     25
    Phase 4            14
    Early Phase 1       4
    Name: Phase, dtype: int64

    Top 10 sponsors with the most trials:
    National Cancer Institute (NCI)                                  52
    Memorial Sloan Kettering Cancer Center                           43
    National Institute of Allergy and Infectious Diseases (NIAID)    31
    Shanghai Junshi Bioscience Co., Ltd.                             22
    Shanghai Henlius Biotech                                         21
    Fred Hutchinson Cancer Center                                    17
    City of Hope Medical Center                                      16
    Abbott                                                           15
    Jonsson Comprehensive Cancer Center                              12
    Sinocelltech Ltd.                                                12
    Name: LeadSponsorName, dtype: int64

</div>

</div>

<div id="a3ba5d4c" class="cell markdown">

Completion rate by intervention type: There are 178 unique intervention
types in the dataset. A few examples include:

- Behavioral: 0% completion rate
- Biological: 54.61% completion rate
- Biological, Biological: 71.15% completion rate
- Radiation: 80% completion rate
- Completion rate by study phase:
- Early Phase 1: 75% completion rate
- Not Applicable: 37.5% completion rate
- Phase 1: 55.77% completion rate
- Phase 1, Phase 2: 47.11% completion rate
- Phase 2: 46.26% completion rate
- Phase 2, Phase 3: 47.37% completion rate
- Phase 3: 57.69% completion rate
- Phase 4: 7.14% completion rate

Completion rate by sponsor: There are 402 unique lead sponsor names in
the dataset. A few examples include:

- 3D Medicines (Sichuan) Co., Ltd.: 100% completion rate
- ANRS, Emerging Infectious Diseases: 0% completion rate
- AVEO Pharmaceuticals, Inc.: 100% completion rate
- Aarhus University Hospital: 100% completion rate
- Zhejiang University: 0% completion rate

Keep in mind that the completion rate depends on the number of trials
for each intervention type, study phase, or sponsor, and a small number
of trials may not provide a comprehensive understanding of the
completion rate. This is just some sample output you might get and I
show it for purely educational purposes.

</div>

<div id="61a22e5a" class="cell markdown">

### Below is code to show information as to how many and what polytherapies are being used in this specific search

**Note that success rate is just another way of saying "study is
completed", it does not really reflect the `sucess` of the intervention-
though you should know that some studies will use this as a rough
indicator of success**. There seems to be an error in this chart but it
serves an educational purpose nonetheless.

</div>

<div id="85567c04" class="cell code" execution_count="118">

``` python
# Create a dataframe with polytherapies (more than one intervention per trial)
df_polytherapy = df[df['InterventionType'].str.contains(',')]

# Calculate success rates and trial count for each unique combination of therapies
therapy_data_poly = df_polytherapy.groupby('InterventionType').agg({'IsSuccessful': ['mean', 'count']}).reset_index()
therapy_data_poly.columns = ['InterventionType', 'SuccessRate', 'TrialCount']

# Filter combinations with at least 15 trials
therapy_data_filtered_poly = therapy_data_poly[therapy_data_poly['TrialCount'] >= 15]

# Sort by success rate and select top 20 best results
top20_therapy_data_poly = therapy_data_filtered_poly.sort_values('SuccessRate', ascending=False).head(7)

# Create the Seaborn bar plot
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
ax = sns.barplot(data=top20_therapy_data_poly, x='SuccessRate', y='InterventionType', color='royalblue')
ax.set_xlabel('Success Rate')
ax.set_ylabel('Intervention Type')
ax.set_title('Top 20 Intervention Combinations Success Rates and Trial Counts for Polytherapies (At least 15 trials)')

# Add the number of trials above each bar
for index, row in top20_therapy_data_poly.iterrows():
    ax.text(row['SuccessRate'], index, f" {row['TrialCount']} trials", color='black', ha="left", va="center")

plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_27_0.png)

</div>

</div>

<div id="7a125b6c" class="cell markdown">

**We are mostly concerned with Monoclonal Antibodies as a monotherapy,
let's see what the main monotherapies for cancer are**

</div>

<div id="359f87fb" class="cell code" execution_count="100">

``` python
import seaborn as sns
import matplotlib.pyplot as plt

# Filter the DataFrame for the desired intervention types
desired_interventions = ['Monotherapy', 'Biological', 'Radiation', 'Procedure']
df_filtered = df_top10[df_top10['InterventionType'].isin(desired_interventions)]

# Calculate success rates and trial counts for the selected intervention types
intervention_success = df_filtered.groupby('InterventionType')['IsSuccessful'].mean().reset_index()
trial_counts = df_filtered['InterventionType'].value_counts().rename_axis('InterventionType').reset_index(name='TrialCount')

# Merge success rates and trial counts DataFrames
intervention_data = intervention_success.merge(trial_counts, on='InterventionType')

# Create a Seaborn barplot with a custom color palette
plt.figure(figsize=(12, 6))
palette = sns.color_palette("coolwarm", n_colors=len(intervention_data))
ax = sns.barplot(data=intervention_data, x='InterventionType', y='IsSuccessful', palette=palette, edgecolor='black', linewidth=1)

# Set labels and title
plt.title('Success Rates by Intervention Type- Monotherapies')
plt.xlabel('Intervention Type')
plt.ylabel('Success Rate')

# Annotate the number of trials for Biological and Radiation interventions
for index, row in intervention_data.iterrows():
    if row['InterventionType'] in ['Biological', 'Radiation']:
        ax.text(index, row['IsSuccessful'] + 0.01, f"n={row['TrialCount']}", ha='center', va='bottom', fontsize=12)

# Show the plot
plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_29_0.png)

</div>

</div>

<div id="97f2021b" class="cell code" execution_count="102">

``` python
# Filter the DataFrame to include only Biological intervention types
df_biological = df[df['InterventionType'] == 'Biological']

# Get the unique Biological therapies
unique_biological_therapies = df_biological['InterventionType'].unique()

# Print the unique Biological therapies
print("Unique Biological therapies:")
for i, therapy in enumerate(unique_biological_therapies, start=1):
    print(f"{i}. {therapy}")
```

<div class="output stream stdout">

    Unique Biological therapies:
    1. Biological

</div>

</div>

<div id="85b421e4" class="cell code" execution_count="110">

``` python
import seaborn as sns
import matplotlib.pyplot as plt

# Calculate success rates and trial count for each LeadSponsorName
sponsor_data = df.groupby('LeadSponsorName').agg({'IsSuccessful': ['mean', 'count']}).reset_index()
sponsor_data.columns = ['LeadSponsorName', 'SuccessRate', 'TrialCount']

# Filter sponsors with at least 5 trials
sponsor_data_filtered = sponsor_data[sponsor_data['TrialCount'] >= 15]

# Sort by success rate and select top 20 best results
top20_sponsor_data = sponsor_data_filtered.sort_values('SuccessRate', ascending=False).head(20)

# Create the Seaborn bar plot
plt.figure(figsize=(12, 6))
sns.set_style("darkgrid")
ax = sns.barplot(data=top20_sponsor_data, x='SuccessRate', y='LeadSponsorName', color='royalblue')
ax.set_xlabel('Success Rate')
ax.set_ylabel('Lead Sponsor Name')
ax.set_title('Top 20 Lead Sponsor Success Rates and Trial Counts (At least 15 trials)')

# Add the number of trials above each bar
for index, row in top20_sponsor_data.iterrows():
    ax.text(row['SuccessRate'], index, f" {row['TrialCount']} trials", color='black', ha="left", va="center")

plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_31_0.png)

</div>

</div>

<div id="274a34ac" class="cell markdown">

# Here is a bar plot for the top 20 intervention types with the highest normalized success rates, considering the number of trials for each intervention type.

</div>

<div id="36e290ad" class="cell code" execution_count="113">

``` python
# Calculate the total number of trials
total_trials = df['NCTId'].count()

# Calculate success rates and trial count for each unique combination of therapies
therapy_data = df.groupby('InterventionType').agg({'IsSuccessful': ['mean', 'count']}).reset_index()
therapy_data.columns = ['InterventionType', 'SuccessRate', 'TrialCount']

# Normalize the success rate by the number of trials
therapy_data['NormalizedSuccessRate'] = therapy_data['SuccessRate'] * therapy_data['TrialCount'] / total_trials

# Sort by the normalized success rate
therapy_data_sorted = therapy_data.sort_values('NormalizedSuccessRate', ascending=False)

# Create the Seaborn bar plot
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
ax = sns.barplot(data=therapy_data_sorted.head(20), x='NormalizedSuccessRate', y='InterventionType', color='royalblue')
ax.set_xlabel('Normalized Success Rate')
ax.set_ylabel('Intervention Type')
ax.set_title('Top 20 Intervention Types Normalized Success Rates')

# Add the number of trials above each bar
for index, row in therapy_data_sorted.head(20).iterrows():
    ax.text(row['NormalizedSuccessRate'], index, f" {row['TrialCount']} trials", color='black', ha="left", va="center")

plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_33_0.png)

</div>

</div>

<div id="9b14370b" class="cell markdown">

# Is there a correlation between sucess of an intervention by intervention type or by LeadSponsorName?

We will just perform a linear regression wherein `IsSucessful` is just
another way of saying *The trial has been completed*. Since the model
performs so poorly we will just leave it intead of going into any depth.
Later we will go into a classification trial in much fuller detail.\`

</div>

<div id="d28ab149" class="cell code" execution_count="116">

``` python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

# Encode categorical variables as dummy variables
enc = OneHotEncoder(handle_unknown='ignore')
X_encoded = enc.fit_transform(df[['InterventionType', 'LeadSponsorName']])

# Create target variable
y = df['IsSuccessful']

# Train linear regression model
lr = LinearRegression()
lr.fit(X_encoded, y)

# Print coefficients
coef = lr.coef_
intercept = lr.intercept_
print("Coefficients: ", coef)
print("Intercept: ", intercept)
```

<div class="output stream stdout">

    Coefficients:  [ 0.29763155  0.01372886  0.10240143  0.19318001 -0.12026433  0.11728884
     -0.11048427  0.03311627  0.03329928  0.03123216  0.44875561  0.03331345
      0.29402917  0.40345098  0.40341486  0.29402917  0.50622335  0.66923934
      0.31036935  0.23054561  0.13492669  0.24311433 -0.20596723  1.13486213
     -0.20596723  0.23054561 -0.20596723  0.34461097 -0.08238859 -0.08237843
     -0.40732276 -0.44610313 -0.00857399 -0.54973576 -0.65280832  0.28788215
     -0.35219891  0.31658074 -0.42483094  0.23054561 -0.31906376  0.03663311
      0.31658641 -0.20596723  0.31658074 -0.44610313  0.31658074  0.18056363
     -1.19427306 -0.98628767 -0.31906376  0.12921198  0.2735669   0.26634148
     -0.31906376 -0.68342045  0.16119683  0.19601958  0.12921198  0.12921198
     -0.06936048  1.12921317 -0.40732276  0.31658074 -0.68342045  1.12921317
     -0.08238859  0.11404117  0.19601958  0.31658074  0.31658074 -1.19427306
      0.23054561 -0.08238859  0.23054561  0.0335923   0.31658074  1.31664406
      0.31660316 -0.01066813 -0.68342045  1.08029001  0.14667519  1.12921317
      0.31658074  0.93063719  0.31658074  0.93064071  0.26433291 -1.19427306
     -0.20596723 -0.68342045 -0.41550719  0.04404133 -0.20596723  0.04404789
      0.29402917  0.01371702 -0.46033706 -0.31906376 -0.49377784 -0.20596723
     -0.29020663  0.23054561  0.23054561  0.00559671  0.29758411 -0.20596723
     -0.89750374  0.31658074 -0.19383812 -0.62069484  1.12921317  0.12921198
     -0.60370238 -0.10482597  0.31658074 -0.60370238 -0.07850772  0.21644808
     -0.06395513  0.35444277  0.17359738 -0.82640381 -0.83037096  0.03252086
      0.00560394  0.57325985  0.29402917  0.61677524 -0.61316994  0.29402917
     -0.19427187  1.12921317  0.60242868  0.34700784 -0.19427187  0.29402917
     -0.19427187 -0.20596723 -0.33125883 -0.20596723  0.03252086 -0.31906376
     -0.38493099  0.13842548 -0.9663875  -0.20596723  0.4131663  -0.65539022
     -0.62851899 -0.44610313  0.59267843  0.23054561  0.3402538  -1.19427306
      0.01372886  1.12921317  1.12921317  1.12921317 -1.19427306 -0.28988216
     -0.20596723 -0.19427187 -0.19427187 -1.19427306 -0.20596723 -0.19427187
      0.12921198  0.23054561 -0.34918012 -1.19427306  0.00168908 -0.03081939
     -0.20596723 -1.19427306  0.26401392 -0.19427187  0.57435448 -0.33054929
      0.48567073  0.58246895  0.58246895  0.78190535  0.13929323  0.57435448
      0.59663321 -0.20596723 -0.21809584 -0.42564671  0.57435448 -0.16956189
      0.57435448  0.07840741  0.70833439  0.41844511 -0.5143288   0.57435448
      0.57435448  0.57435448  0.48567073  0.0669687   0.57435119 -0.20596723
     -0.21994847  0.48561309  0.57435448 -0.26276677 -0.42564671 -0.20596723
     -0.41753225 -0.21809584 -0.21809584 -0.42564671  0.58246895  0.554473
     -0.42564671  0.0341771  -0.42564671  0.11224573 -0.51433046 -0.1395145
     -0.42158898 -0.42361206 -0.4256411   0.08956454  0.26704689  0.91934863
     -0.03734424 -0.41753225  0.74685588  0.31020251  0.78190535 -0.51433046
      0.6050965   0.58247579 -0.41753225  0.25765201 -0.44855186 -0.41753225
     -0.42564671  0.19618378 -0.42564671 -0.01536159 -0.21809584 -0.3425543
      0.07435479 -0.42564671 -0.41753225  0.61894817 -0.21808894  0.70204172
     -0.20596723  0.24780598 -0.08065256  0.17813112 -0.51433046  0.58246895
     -0.4455212  -0.41753225 -0.81534328  0.69288882  0.55144933  0.29402917
      0.58246895 -0.54113261 -0.41753225  0.48567073 -0.60508788 -0.41753225
     -0.54682437  0.91934863  0.37920499 -0.09231859  0.57435448  0.58246895
     -0.08065256 -0.41753225  0.29402917  0.54403773 -0.42294822  0.58633145
      0.48567073  0.42688385  0.48567073  0.55447999  0.55477747  0.58246895
     -0.42564671 -0.709537    0.21657897  0.57435448  0.57434984  0.19177895
     -0.42564671 -0.20596723 -0.42564671  0.57435448  0.78232421 -0.09231859
     -0.42564671 -0.42564671 -0.41753225 -0.42564671 -0.42564671 -0.34258169
     -0.42564671 -0.42564671 -0.09334931  0.56560719  0.78190535  0.23363647
      0.21686955 -0.0889145   0.0484155  -0.06758859  0.07435479 -0.42564671
     -0.20596723  0.70833439  0.57435448  0.91934863  0.55447999 -0.42564671
     -0.42361206 -0.5122687   0.55144933 -0.4559485  -0.20609724 -0.73085427
     -0.62536186  0.57435119  0.78190535 -0.10556597 -0.41753225 -0.41753225
      0.2904642   0.58246895 -0.709537   -0.44855186 -0.41753225 -0.41753225
     -0.42564671  0.57435448 -0.2471307   0.48567073  0.57434928  0.4428851
     -0.41753225 -0.42564671  0.69288882 -0.41753225 -0.75219521  0.55011766
     -0.08065256 -0.60508788  0.64895353  0.414508    0.24780598 -0.21809584
     -0.34412096 -0.51434114 -0.51433046  0.91934863  0.13784542  0.69288882
      0.58246895 -0.42564671 -0.5143288  -0.42564671 -0.41753225  0.03001119
      0.32842562 -0.51433046 -0.49562529 -0.42564671 -0.42564671  0.32645036
     -0.42564671 -0.01850163 -0.51433046 -0.09285968 -0.42564671  0.08044315
     -0.01431819 -0.709537   -0.75219521 -0.67604953  0.16325216 -0.49217217
      0.47319601  0.08184537  0.57435448 -0.82510366  0.35753458 -0.51433046
      0.57435448  0.18460666  0.57435119  0.58045635  0.40745838 -0.51433046
     -0.41753225 -0.70951896 -0.42564671 -0.60508788  0.27149316  0.57435119
      0.24092015  0.57435448  0.29402917 -0.42564671  0.57435448  0.52520061
      0.2904642  -0.41753225  0.24347722  0.63030945  0.2257434  -0.42564671
     -0.31781265 -0.20596723  0.18218375 -0.21809584  0.58246895 -0.62840146
     -1.08109196 -0.51433046  0.57435448 -0.41753225 -0.51433046 -0.42564671
     -0.25949267 -0.51433046 -0.42564671  0.69534366 -0.02701119 -0.41753225
      0.01673764  0.57435448 -0.41753225 -0.41753225  0.48567073 -0.42564671
     -0.2916668   0.63378392  0.29402917 -0.51433046  0.20130352  0.24101534
     -0.42564161 -0.42564671  0.66176602  0.39491331 -0.41753225  0.48567073
     -0.00459954  0.57435119  0.04876428 -0.51433046  0.07840741 -0.46593258
      0.55477933  0.58246895 -0.42564671 -0.41753225  0.66653331  0.58246895
     -0.30711237 -0.31781265 -0.22689222 -0.51433046 -0.21809584 -0.20088152
     -0.41753636  0.15232673 -0.12191334  0.58246895 -0.20596723  0.91934863
     -0.42564671  0.87790459  0.00356294 -0.20596723 -0.05973776 -0.41753225
      0.57435448 -0.27622977 -0.4256411  -0.75219521 -0.2916668  -0.51433046
     -0.21809584  0.39203917 -0.81534328  0.48567271  0.58246895 -0.20596723
     -0.46721744 -0.4645089   0.87823269  0.2904642  -0.44443369 -0.42564671
     -0.42564671  0.57435119  0.48567073  0.24102512  0.39491331  0.55144933
      0.07840741 -0.42563462  0.2087359  -0.21809584 -0.51433046  0.58246895
      0.58246895  0.58246895  0.57435448 -0.38970563  0.28898797 -0.709537
      0.06155093  0.57435448  0.58245643  0.20879077 -0.42564671  0.23690859
      0.57435448 -0.41753225 -0.42564161  0.57435448  0.61894817 -0.51433046
     -0.63325449  0.03406381 -0.70952836 -0.42564671 -0.3916387   0.39491331
     -0.42564671 -0.32954419 -0.21809584 -0.53450375  0.41609372 -0.20596723
     -0.20596723  0.57435448  0.29402917 -0.30711237 -0.02869224 -0.41752366
     -0.20596723  0.29402917  0.48566066 -0.72853602  0.07611013 -0.30711237
      0.78190535 -0.60508788 -0.30711237  0.68218014 -0.08065256  0.0484155
      0.31501446 -0.21809584 -0.30711237 -0.709537    0.57435119 -0.41753225
     -0.42564671 -0.12146057 -0.41753225 -0.20596723  0.58246895 -0.41753225
     -0.42564671  0.78190535 -0.42564671 -0.37954267]
    Intercept:  0.41192840308300716

</div>

</div>

<div id="100c6bea" class="cell markdown">

print(df.columns)

</div>

<div id="33dac610" class="cell markdown">

**To determine which variable was more strongly correlated with study
success, I looked at the absolute values of the coefficients for each
variable in the linear regression model. The variable with the larger
absolute value coefficient is considered to be more strongly correlated
with study success. In this case, the absolute value of the coefficient
for intervention type was 0.014, while the absolute value of the
coefficient for study location was 0.001. Therefore, we can conclude
that intervention type is more strongly correlated with study success
than study location. However this correlation is extremely weak**

**The intercept is a constant term in the regression equation, which
represents the predicted outcome value when all predictor variables are
equal to zero. In this case, the intercept value of 0.4119 indicates
that the predicted success rate (completion rate) of a clinical trial is
0.4119 (or 41.19%) when there is no contribution from any of the
predictor variables (i.e., the sponsor and intervention type are both
zero).**

</div>

<div id="ed59ae57" class="cell code" execution_count="14">

``` python

# Replace the sample data with your calculated data
success_rates = {
    "Intervention Type": {
        "Behavioral": 0,
        "Biological": 54.61,
        "Biological, Biological": 71.15,
        "Radiation": 80,
    },
    "Study Phase": {
        "Early Phase 1": 75,
        "Not Applicable": 37.5,
        "Phase 1": 55.77,
        "Phase 1, Phase 2": 47.11,
        "Phase 2": 46.26,
        "Phase 2, Phase 3": 47.37,
        "Phase 3": 57.69,
        "Phase 4": 7.14,
    },
    "Lead Sponsor": {
        "3D Medicines (Sichuan) Co., Ltd.": 100,
        "ANRS, Emerging Infectious Diseases": 0,
        "AVEO Pharmaceuticals, Inc.": 100,
        "Aarhus University Hospital": 100,
        "Zhejiang University": 0,
    },
}
```

</div>

<div id="08dbf7d1" class="cell markdown">

This code snippet demonstrates how to read multiple CSV files from a
folder and concatenate them into a single pandas DataFrame. Let's break
it down step by step:

- `folder_path = '/Users/chrisgaughan/Desktop/clinical_trials.csv'`:
  This line sets the variable folder_path to the path of the folder
  containing the CSV files you want to read. In this case, the folder is
  located on the desktop and is named 'clinical_trials.csv'. Note that
  this seems to be a mistake, as the folder path should point to a
  directory, not a file with a '.csv' extension.

- `all_files = glob.glob(folder_path + "/part-*.csv")`: The glob module
  is used to find all the file paths that match a specified pattern. In
  this case, it searches for all files in the folder_path directory with
  names starting with 'part-' and ending with '.csv'. The matching file
  paths are stored in the all_files list.

- `df_list` = \[\]: This line initializes an empty list called df_list,
  which will be used to store temporary DataFrames created while reading
  each CSV file.

`for filename in all_files:`: This for loop iterates through each file
path in the all_files list.

`temp_df = pd.read_csv(filename)`: Inside the loop, the pd.read_csv()
function is used to read the contents of the current CSV file (indicated
by filename) and store it in a temporary DataFrame called temp_df.

`df_list.append(temp_df)`: The temporary DataFrame temp_df is then
appended to the df_list.

After the loop is done processing all the files, df = pd.concat(df_list,
axis=0), ignore_index=True) is used to concatenate all the DataFrames
stored in the df_list along the vertical axis (rows), creating a single
DataFrame named df. The ignore_index=True parameter is used to reset the
index of the resulting DataFrame, assigning new integer indices instead
of retaining the original indices from each individual DataFrame.

At the end of this code snippet, you have a single DataFrame df
containing the data from all the CSV files in the specified folder.

</div>

<div id="3434e10b" class="cell code" execution_count="16">

``` python
folder_path = '/Users/chrisgaughan/Desktop/clinical_trials.csv'
all_files = glob.glob(folder_path + "/part-*.csv")

df_list = []

for filename in all_files:
    temp_df = pd.read_csv(filename)
    df_list.append(temp_df)

df = pd.concat(df_list, axis=0, ignore_index=True)
```

</div>

<div id="48023b58" class="cell code" execution_count="17">

``` python

# Drop rows with missing values
df = df.dropna()

# Select features and target variable
features = ['BriefTitle', 'NCTId', 'Rank']
target = 'OverallStatus'
X = df[features]
y = df[target]

# Encode categorical features
X = pd.get_dummies(X, drop_first=True)
```

</div>

<div id="3a735079" class="cell markdown">

This code snippet demonstrates the process of splitting a dataset into
training and testing sets, followed by creating a random forest
classifier. Let's break it down step by step:

- `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)`:
  The train_test_split function from the `sklearn.model_selection`
  module is used to split the dataset (represented by `X` and `y`) into
  training and testing sets. The `test_size=0.2` parameter indicates
  that 20% of the data will be used for the testing set, while the
  remaining 80% will be used for the training set. The `random_state=42`
  parameter sets a seed for the random number generator, ensuring that
  the splitting process is reproducible.

- `X_train and y_train` are the feature matrix and target vector,
  respectively, for the training set. `X_test and y_test` are the
  feature matrix and target vector, respectively, for the testing set.
  `clf = RandomForestClassifier(random_state=42)`: The
  RandomForestClassifier class from the sklearn.ensemble module is used
  to create a random forest classifier. The random_state=42 parameter
  sets a seed for the random number generator, ensuring that the model's
  behavior is consistent and reproducible.

After executing this code snippet, you will have:

Split the dataset into training and testing sets
(`X_train, X_test, y_train, and y_test`). Created a random forest
classifier (clf) that can be trained on the training data and evaluated
on the testing data.

</div>

<div id="539b71f6" class="cell code" execution_count="18">

``` python
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)

# Create a classifier
clf = RandomForestClassifier(random_state=42)
```

</div>

<div id="1da5cdbd" class="cell code" execution_count="19">

``` python
# Train the classifier
clf.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = clf.predict(X_test)

# Calculate accuracy and display the classification report
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

report = classification_report(y_test, y_pred)
print("Classification report:")
print(report)
```

<div class="output stream stdout">

    Accuracy: 0.50
    Classification report:
                             precision    recall  f1-score   support

     Active, not recruiting       1.00      0.04      0.07        27
                  Completed       0.50      1.00      0.66       197
    Enrolling by invitation       0.00      0.00      0.00         1
         Not yet recruiting       0.00      0.00      0.00        14
                 Recruiting       1.00      0.01      0.02        89
                  Suspended       0.00      0.00      0.00         3
                 Terminated       0.00      0.00      0.00        33
             Unknown status       1.00      0.03      0.06        30
                  Withdrawn       0.00      0.00      0.00         6

                   accuracy                           0.50       400
                  macro avg       0.39      0.12      0.09       400
               weighted avg       0.61      0.50      0.34       400

</div>

<div class="output stream stderr">

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.

</div>

</div>

<div id="0dfe205a" class="cell markdown">

**Accuracy**: 0.50

**Classification report**:

|                         | Precision | Recall | F1-score | Support |
|-------------------------|-----------|--------|----------|---------|
| Active, not recruiting  | 1.00      | 0.04   | 0.07     | 27      |
| Completed               | 0.50      | 1.00   | 0.66     | 197     |
| Enrolling by invitation | 0.00      | 0.00   | 0.00     | 1       |
| Not yet recruiting      | 0.00      | 0.00   | 0.00     | 14      |
| Recruiting              | 1.00      | 0.01   | 0.02     | 89      |
| Suspended               | 0.00      | 0.00   | 0.00     | 3       |
| Terminated              | 0.00      | 0.00   | 0.00     | 33      |
| Unknown status          | 1.00      | 0.03   | 0.06     | 30      |
| Withdrawn               | 0.00      | 0.00   | 0.00     | 6       |

**Summary metrics**:

- Accuracy: 0.50
- Macro average: (Precision: 0.39, Recall: 0.12, F1-score: 0.09)
- Weighted average: (Precision: 0.61, Recall: 0.50, F1-score: 0.34)

</div>

<div id="93ad80f1" class="cell markdown">

## Classification Performance Metrics

**Accuracy**: The proportion of correct predictions out of the total
predictions. It is calculated as the number of correct predictions
divided by the total number of predictions.

**Precision**: The proportion of true positive predictions (correct
positive predictions) out of all positive predictions made. Precision
answers the question: Out of all the positive predictions made by the
model, how many were actually positive? It is calculated as the number
of true positives divided by the sum of true positives and false
positives.

**Recall**: The proportion of true positive predictions out of all
actual positive instances. Recall answers the question: Out of all the
actual positive instances, how many did the model correctly predict as
positive? It is calculated as the number of true positives divided by
the sum of true positives and false negatives.

**F1-score**: The harmonic mean of precision and recall, which balances
both metrics. It is particularly useful when dealing with imbalanced
classes or when false positives and false negatives carry different
costs. F1-score is calculated as 2 \* (precision \* recall) /
(precision + recall).

**Support**: The number of instances (data points) for each class in the
test dataset.

**Macro average**: The average of a metric (precision, recall, or
F1-score) calculated independently for each class and then averaged.
Macro averaging treats all classes equally, which can be useful when
dealing with imbalanced datasets.

**Weighted average**: The average of a metric (precision, recall, or
F1-score) calculated for each class and then weighted by the number of
instances in each class. Weighted averaging accounts for class
imbalance, as it gives more importance to larger classes.

</div>

<div id="ea7ae241" class="cell markdown">

## Evaluation of Test Scores

**Accuracy (0.50)**: The accuracy of 0.50 means that the model correctly
predicts 50% of the instances in the test dataset. This indicates that
the model's performance is better than random chance (which would be 0.5
for a binary classification problem), but it is still far from perfect.
There is room for improvement in the model's ability to classify
instances correctly.

**Precision, Recall, and F1-score**: Analyzing these metrics for each
class helps us understand the model's performance in more detail. The
model has high precision (1.00) for some classes (e.g., Active, not
recruiting, Recruiting, and Unknown status) but very low recall values
(0.04, 0.01, and 0.03, respectively). This indicates that the model is
very selective in assigning these classes, resulting in very few false
positives but many false negatives.

Conversely, the model has low precision (0.50) but high recall (1.00)
for the Completed class, meaning that the model tends to over-predict
this class, resulting in many false positives. For the other classes,
both precision and recall are low, suggesting that the model struggles
to accurately classify instances in these classes.

**F1-score** values are low for most classes, indicating that the
model's performance is not well balanced between precision and recall.
The highest F1-score (0.66) is for the Completed class, which may be due
to the larger number of instances in that class compared to the others.

**Macro and Weighted averages**: The macro averages indicate that the
model's performance across classes is generally poor (Precision: 0.39,
Recall: 0.12, F1-score: 0.09). The weighted averages, which account for
class imbalance, show a slightly better performance (Precision: 0.61,
Recall: 0.50, F1-score: 0.34), but there is still considerable room for
improvement.

**Conclusion**: The model's overall performance is suboptimal, with low
F1-scores and imbalanced performance across classes. To improve the
model, we could explore different algorithms, feature engineering, and
hyperparameter tuning. Additionally, we might consider addressing class
imbalance, either by collecting more data for underrepresented classes
or using techniques such as oversampling or undersampling. Nevertheless,
we get a glimpse into the data we have at hand and what its weknesses
are.

</div>

<div id="d9b2c1c2" class="cell markdown">

### Just for demonstration purposes, let's make an NLP model

here is what the script does:

- nltk.download('stopwords') downloads a list of common stop words in
  English from the Natural Language Toolkit (nltk) library.
- nltk.download('punkt') downloads a data model for the NLTK library
  that can be used to tokenize words from text.
- stop_words = set(stopwords.words('english')) creates a set of stop
  words in English. Stop words are words that are very common and do not
  carry much meaning on their own, such as "the", "and", "a", etc.
- stemmer = PorterStemmer() creates a stemmer object from the
  PorterStemmer class in the nltk library. Stemming is the process of
  reducing a word to its root form, such as converting "jumping" to
  "jump".
- def preprocess_text(text): defines a function called preprocess_text
  that takes a string of text as input.
- text = re.sub(r'\W+', ' ', text.lower()) replaces any non-alphanumeric
  characters (e.g. punctuation marks) in the text with a space and
  converts the entire text to lowercase.
- tokens = word_tokenize(text) tokenizes the text into a list of words.
- filtered_tokens = \[stemmer.stem(token) for token in tokens if token
  not in stop_words\] applies stemming to each word in the tokenized
  list and filters out any stop words.
- return ' '.join(filtered_tokens) joins the filtered list of stemmed
  words back into a string separated by spaces.
- df\['BriefTitle_processed'\] =
  df\['BriefTitle'\].apply(preprocess_text) applies the preprocess_text
  function to each value in the "BriefTitle" column of the DataFrame df
  and creates a new column called "BriefTitle_processed" that contains
  the preprocessed text.

**Overall, this script preprocesses the text in the "BriefTitle" column
of a DataFrame by removing non-alphanumeric characters, converting the
text to lowercase, tokenizing the text, stemming the words, and
filtering out stop words. This is a common preprocessing step when
working with text data in natural language processing.**

</div>

<div id="1544669b" class="cell markdown">

## Text Preprocessing

This code snippet is used for text preprocessing, which is an essential
step in Natural Language Processing (NLP) tasks. The objective is to
clean and transform raw text data into a format that can be easily
understood and analyzed by machine learning algorithms.

\`\`\`python nltk.download('stopwords') nltk.download('punkt')

These two lines download the necessary resources from the NLTK (Natural
Language Toolkit) library. The 'stopwords' resource provides a list of
common words that do not carry much information and are usually filtered
out during text preprocessing. The 'punkt' resource is required for
tokenizing sentences into words.

stop_words = set(stopwords.words('english')) stemmer = PorterStemmer()

`stop_words` is a set containing common English stop words, which will
be used to filter out these words during preprocessing. `stemmer` is an
instance of the PorterStemmer class, which will be used to perform
stemming on the text. Stemming is the process of reducing words to their
root form, which helps in reducing the dimensionality of the text data
and grouping similar words together.

def preprocess_text(text): text = re.sub(r'\W+', ' ', text.lower())
tokens = word_tokenize(text) filtered_tokens = \[stemmer.stem(token) for
token in tokens if token not in stop_words\] return '
'.join(filtered_tokens)

`preprocess_text` is a function that takes raw text as input and returns
the preprocessed text. It performs the following steps:

1.  Converts the text to lowercase using text.lower().
2.  Removes non-alphanumeric characters (e.g., punctuation) using a
    regular expression re.sub(r'\W+', ' ', 3. text.lower()).
3.  Tokenizes the text into words using word_tokenize(text).
4.  Filters out stop words and applies stemming to the remaining tokens.
5.  Joins the preprocessed tokens back into a single string, separated
    by spaces.

df\['BriefTitle_processed'\] = df\['BriefTitle'\].apply(preprocess_text)

This line applies the `preprocess_text` function to the 'BriefTitle'
column in the DataFrame `df` and stores the resulting preprocessed text
in a new column called 'BriefTitle_processed'.

</div>

<div id="3b50b14b" class="cell code" execution_count="20">

``` python


nltk.download('stopwords')
nltk.download('punkt')


stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text.lower())
    tokens = word_tokenize(text)
    filtered_tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
    return ' '.join(filtered_tokens)

df['BriefTitle_processed'] = df['BriefTitle'].apply(preprocess_text)
```

<div class="output stream stderr">

    [nltk_data] Downloading package stopwords to
    [nltk_data]     /Users/chrisgaughan/nltk_data...
    [nltk_data]   Package stopwords is already up-to-date!
    [nltk_data] Downloading package punkt to
    [nltk_data]     /Users/chrisgaughan/nltk_data...
    [nltk_data]   Package punkt is already up-to-date!

</div>

</div>

<div id="4cbca321" class="cell markdown">

## Text Vectorization

This code snippet is used for text vectorization, which is the process
of converting text data into numerical representations that can be used
by machine learning algorithms.

\`\`\`python vectorizer = TfidfVectorizer(max_features=100)

`vectorizer` is an instance of the `TfidfVectorizer` class from the
`sklearn.feature_extraction.text module`. It is used to convert the
preprocessed text data into a matrix of TF-IDF (Term Frequency-Inverse
Document Frequency) features. The `max_features parameter` is set to
100, which means that the vectorizer will only consider the top 100 most
important terms, ranked by their TF-IDF scores, when building the
feature matrix.

brief_title_tfidf =
vectorizer.fit_transform(df\['BriefTitle_processed'\]).toarray()

This line applies the `fit_transform` method of the `vectorizer` to the
'BriefTitle_processed' column in the DataFrame `df`. This method
computes the TF-IDF scores for each term in the vocabulary, builds the
feature matrix, and returns it in a sparse format. The `.toarray()`
method is called to convert the sparse matrix into a dense NumPy array,
which is stored in the `brief_title_tfidf` variable.

The resulting `brief_title_tfidf` array has one row for each document
(in this case, each row in the DataFrame df) and one column for each of
the top 100 most important terms. Each element of the array represents
the TF-IDF score of a term in a document, which is a measure of the
term's importance in that document relative to the entire corpus of
documents.

</div>

<div id="a099d431" class="cell code" execution_count="21">

``` python
vectorizer = TfidfVectorizer(max_features=100)
brief_title_tfidf = vectorizer.fit_transform(df['BriefTitle_processed']).toarray()
```

</div>

<div id="b836006e" class="cell code" execution_count="22">

``` python
scaler = StandardScaler()
rank_normalized = scaler.fit_transform(df[['Rank']])
```

</div>

<div id="b366072a" class="cell code" execution_count="23">

``` python
import numpy as np

X_new = np.hstack((brief_title_tfidf, rank_normalized))
```

</div>

<div id="90634427" class="cell code" execution_count="24">

``` python
X_train_new, X_test_new, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)

classifier_new = RandomForestClassifier(n_estimators=100, random_state=42)
classifier_new.fit(X_train_new, y_train)

y_pred_new = classifier_new.predict(X_test_new)

print("Accuracy:", accuracy_score(y_test, y_pred_new))
print("Classification report:\n", classification_report(y_test, y_pred_new))
```

<div class="output stream stdout">

    Accuracy: 0.5325
    Classification report:
                              precision    recall  f1-score   support

     Active, not recruiting       0.33      0.07      0.12        27
                  Completed       0.60      0.84      0.70       197
    Enrolling by invitation       0.00      0.00      0.00         1
         Not yet recruiting       0.12      0.07      0.09        14
                 Recruiting       0.46      0.43      0.44        89
                  Suspended       1.00      0.33      0.50         3
                 Terminated       0.00      0.00      0.00        33
             Unknown status       0.38      0.20      0.26        30
                  Withdrawn       0.00      0.00      0.00         6

                   accuracy                           0.53       400
                  macro avg       0.32      0.22      0.23       400
               weighted avg       0.46      0.53      0.48       400

</div>

<div class="output stream stderr">

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.

</div>

</div>

<div id="d3e509ce" class="cell code" execution_count="25">

``` python
file_path = '/Users/chrisgaughan/Desktop/clinical_trials.csv/part-00000-beace8e8-0f0e-4807-be31-4a87c37a3990-c000.csv'
df = pd.read_csv(file_path)
```

</div>

<div id="c845d8f5" class="cell markdown">

**clinical_trials.csv is a folder containing multiple CSV files, we can
try combining them into a single DataFrame using the following code:**

This code is reading in multiple CSV files from a folder and
concatenating them into a single pandas DataFrame. Here is how it works:

- The folder_path variable is a string that contains the path to the
  folder containing the CSV files.

- The glob.glob function is used to find all files in the folder that
  have the .csv extension. The os.path.join function is used to join the
  folder path with the file names returned by glob.glob to create a list
  of file paths.

- The pd.concat function is used to concatenate all of the CSV files
  into a single pandas DataFrame. The pd.read_csv function is used to
  read each CSV file into a pandas DataFrame, and the resulting
  DataFrames are combined into a single DataFrame using the concat
  function.

- The ignore_index=True argument tells concat to reset the index of the
  resulting DataFrame to start from 0.

</div>

<div id="402136b4" class="cell code" execution_count="26">

``` python
folder_path = "/Users/chrisgaughan/Desktop/clinical_trials.csv"
all_files = glob.glob(os.path.join(folder_path, "*.csv"))

df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
```

</div>

<div id="b0d41c48" class="cell code" execution_count="27">

``` python
df.head(10)
```

<div class="output execute_result" execution_count="27">

                                              BriefTitle        NCTId  \
    0  Phase 0/1 Local Application of the Monoclonal ...  NCT04895566   
    1  mFOLFOX6+Bevacizumab+PD-1 Monoclonal Antibody ...  NCT04895137   
    2  Phase Ⅰ Clinical Study of Anti-CD52 Monoclonal...  NCT05557903   
    3  Programmed Cell Death Protein-1 (PD-1) Monoclo...  NCT05039580   
    4  Efficacy of Montelukast in Reducing the Incide...  NCT04198623   
    5  Safety and Efficacy of Recombinant Anti-EGFR M...  NCT03405272   
    6  Safety and Tolerability of Recombinant Humaniz...  NCT02838823   
    7  Safety and Tolerability of Recombinant Humaniz...  NCT02836795   
    8  PD-1 Monoclonal Antibody in Pre-treated Lympho...  NCT04430166   
    9  TPO-RAs Combining Anti-CD 20 Monoclonal Antibo...  NCT05718856   

            OverallStatus  Rank  
    0           Completed     1  
    1          Recruiting     2  
    2          Recruiting     3  
    3          Recruiting     4  
    4          Recruiting     5  
    5      Unknown status     6  
    6           Completed     7  
    7      Unknown status     8  
    8      Unknown status     9  
    9  Not yet recruiting    10  

</div>

</div>

<div id="bd03ba6e" class="cell markdown">

**The data are unbalanced (i.e. there are more than twice the number of
completed studies than studies in one of the three uncompleted
categories. To ameliorate this we will use a tool known as SMOTE
((Synthetic Minority Over-sampling Technique) that helps with
"unbalanced" the data**

</div>

<div id="e8433be3" class="cell code" execution_count="28">

``` python
# Encode the 'BriefTitle' column
encoder = LabelEncoder()
df['BriefTitle'] = encoder.fit_transform(df['BriefTitle'])

# Define the features and target
X = df[['BriefTitle', 'Rank']]
y = df['OverallStatus']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)
```

</div>

<div id="7ce69f2e" class="cell markdown">

**Let's find out how big the dataset is**

</div>

<div id="b5eb3667" class="cell code" execution_count="29">

``` python
# Find the number of rows and columns in the dataset
num_rows, num_columns = df.shape

print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")
```

<div class="output stream stdout">

    Number of rows: 2000
    Number of columns: 4

</div>

</div>

<div id="126bd3ef" class="cell markdown">

**This dataset is a little on the small side, we'll likely need more
data but let's try to make do with what we have**

</div>

<div id="e8f257fc" class="cell code" execution_count="30">

``` python
print(y_train.value_counts())
```

<div class="output stream stdout">

    Completed                  771
    Recruiting                 317
    Unknown status             151
    Terminated                 124
    Active, not recruiting      99
    Not yet recruiting          78
    Withdrawn                   38
    Suspended                   11
    Enrolling by invitation      6
    Approved for marketing       3
    No longer available          1
    Available                    1
    Name: OverallStatus, dtype: int64

</div>

</div>

<div id="d0f761e3" class="cell code" execution_count="31">

``` python
# Remove the classes with only one sample
filtered_indices = y_train[(y_train != "No longer available") & (y_train != "Available")].index
X_train_filtered = X_train.loc[filtered_indices]
y_train_filtered = y_train.loc[filtered_indices]

# Apply SMOTE with k_neighbors=2
smote = SMOTE(random_state=42, k_neighbors=2)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_filtered, y_train_filtered)
```

</div>

<div id="db4f1b9d" class="cell code" execution_count="32">

``` python
# Create one-hot encoder object
encoder = OneHotEncoder(handle_unknown='ignore')

# Fit the encoder on the training data
encoder.fit(X_train_resampled)

# Transform the training and test data
X_train_encoded = encoder.transform(X_train_resampled)
X_test_encoded = encoder.transform(X_test)
```

</div>

<div id="e2efc03a" class="cell code" execution_count="33">

``` python
from sklearn.ensemble import RandomForestClassifier

# Create a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model on the resampled data
clf.fit(X_train_resampled, y_train_resampled)
```

<div class="output execute_result" execution_count="33">

    RandomForestClassifier(random_state=42)

</div>

</div>

<div id="c0c84977" class="cell code" execution_count="34">

``` python
# Make predictions on the test set
y_pred = clf.predict(X_test)
```

</div>

<div id="6e8853e8" class="cell code" execution_count="35">

``` python
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Print the classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Print the confusion matrix
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Print the accuracy score
print("Accuracy Score:")
print(accuracy_score(y_test, y_pred))
```

<div class="output stream stdout">

    Classification Report:
                             precision    recall  f1-score   support

     Active, not recruiting       0.14      0.22      0.17        27
     Approved for marketing       0.00      0.00      0.00         0
                  Completed       0.55      0.29      0.38       197
    Enrolling by invitation       0.00      0.00      0.00         1
         Not yet recruiting       0.03      0.07      0.05        14
                 Recruiting       0.28      0.18      0.22        89
                  Suspended       0.04      0.33      0.07         3
                 Terminated       0.10      0.12      0.11        33
             Unknown status       0.07      0.10      0.08        30
                  Withdrawn       0.03      0.17      0.06         6

                   accuracy                           0.23       400
                  macro avg       0.13      0.15      0.11       400
               weighted avg       0.36      0.23      0.27       400

    Confusion Matrix:
    [[ 6  0  6  3  0  4  2  2  1  3]
     [ 0  0  0  0  0  0  0  0  0  0]
     [18  5 58  5 16 27 17 19 22 10]
     [ 1  0  0  0  0  0  0  0  0  0]
     [ 1  0  5  2  1  2  1  1  1  0]
     [12  1 17  6  7 16  1  9 13  7]
     [ 0  0  1  1  0  0  1  0  0  0]
     [ 3  0  9  3  4  4  1  4  1  4]
     [ 2  1  8  1  1  4  2  4  3  4]
     [ 0  0  1  0  1  0  1  1  1  1]]
    Accuracy Score:
    0.225

</div>

<div class="output stream stderr">

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Recall and F-score are ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Recall and F-score are ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.

    /Users/chrisgaughan/opt/anaconda3/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1318: UndefinedMetricWarning:

    Recall and F-score are ill-defined and being set to 0.0 in labels with no true samples. Use `zero_division` parameter to control this behavior.

</div>

</div>

<div id="82211edb" class="cell code" execution_count="39">

``` python
# Create the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Create a heatmap using Seaborn
sns.set_style("dark")
plt.figure(figsize=(10, 7))
sns.heatmap(cm,
            annot=True,
            fmt="d",
            cmap="BuGn",
            cbar=False,
            linewidth=.8,
            edgecolor="black",
            linewidths=1, 
            linecolor='black',
            xticklabels=y_train.unique(),
            yticklabels=y_train.unique())

# Add labels and title
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

# Show the plot
plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_71_0.png)

</div>

</div>

<div id="52638700" class="cell markdown">

### These are rather poor results, even when considering that we are dealing with clinical data, which often noisy at best. We can't move forward with numbers like these, particularly when one condiders that we used SMOTE (Synthetic Minority Over-sampling Technique) to account for imbalanced datasets such as we have here.

</div>

<div id="17a4fce9" class="cell code" execution_count="48">

``` python


api_key = "5FIMvhCpcV1ch4aDDJKed62D9exBVFZE2xgkSnaR"
headers = {'x-api-key': api_key}

# Search for trials with record_verification_date greater than or equal to 2016-08-25
url = "https://clinicaltrialsapi.cancer.gov/api/v2/trials?record_verification_date_gte=2016-08-25"
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    json_response = response.json()
    print(json_response)
else:
    print(f"Error: {response.status_code} - {response.text}")
```

<div class="output stream stderr">

    IOPub data rate exceeded.
    The notebook server will temporarily stop sending output
    to the client in order to avoid crashing it.
    To change this limit, set the config variable
    `--NotebookApp.iopub_data_rate_limit`.

    Current values:
    NotebookApp.iopub_data_rate_limit=1000000.0 (bytes/sec)
    NotebookApp.rate_limit_window=3.0 (secs)

</div>

</div>

<div id="b939e7ef" class="cell code" execution_count="49">

``` python


url = "https://clinicaltrialsapi.cancer.gov/v1/clinical-trials/"
params = {
    "status": "completed,terminated,withdrawn,suspended",
    "size": 100,
    "from": 0,
    "apikey": "5FIMvhCpcV1ch4aDDJKed62D9exBVFZE2xgkSnaR"
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    # Do something with the data, such as extract the trial information and analyze it
except requests.exceptions.HTTPError as error:
    print(f"HTTP error occurred: {error}")
except ValueError as error:
    print(f"JSON decoding error occurred: {error}")
except Exception as error:
    print(f"An error occurred: {error}")
```

<div class="output stream stdout">

    JSON decoding error occurred: Expecting value: line 1 column 1 (char 0)

</div>

</div>

<div id="4cb1ff34" class="cell code" execution_count="50">

``` python


url = "https://clinicaltrials.gov/api/query/full_studies"
params = {
    "expr": "STATUS:completed OR STATUS:terminated OR STATUS:withdrawn OR STATUS:suspended",
    "min_rnk": 1,
    "max_rnk": 100,
    "fmt": "json"
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    # Do something with the data, such as extract the trial information and analyze it
except requests.exceptions.HTTPError as error:
    print(f"HTTP error occurred: {error}")
except ValueError as error:
    print(f"JSON decoding error occurred: {error}")
except Exception as error:
    print(f"An error occurred: {error}")
```

</div>

<div id="59a5db5f" class="cell markdown">

## We might we also be overlooking the fact that trials that that *do* fail (i.e. do not get to completion) might be comprised of tougher patients. Let's try to dig a litttle deeper into this

</div>

<div id="0636d323" class="cell code" execution_count="51">

``` python
trials = data["FullStudiesResponse"]["FullStudies"]

for trial in trials:
    study = trial["Study"]
    nct_id = study["ProtocolSection"]["IdentificationModule"]["NCTId"]
    title = study["ProtocolSection"]["IdentificationModule"]["BriefTitle"]
    status = study["ProtocolSection"]["StatusModule"]["OverallStatus"]
    start_date = study["ProtocolSection"]["StatusModule"]["StartDateStruct"]["StartDate"]
    
    print(f"NCT ID: {nct_id}")
    print(f"Title: {title}")
    print(f"Status: {status}")
    print(f"Start Date: {start_date}")
    print("-" * 80)
```

<div class="output stream stdout">

    NCT ID: NCT01106781
    Title: A Non-interventional Survey on the EGFR (Epidermal Growth Factor Receptor) Mutation Status in Completely Resected Chinese Non-Small Cell Lung Cancer (NSCLC) Patients With Adenocarcinoma Histology
    Status: Completed
    Start Date: August 2010
    --------------------------------------------------------------------------------
    NCT ID: NCT00507611
    Title: Axillary Lymph Node Status After Completion of Preoperative Neoadjuvant Systemic Chemotherapy in Patients
    Status: Completed
    Start Date: October 2006
    --------------------------------------------------------------------------------
    NCT ID: NCT05415358
    Title: Immune Signature Analysis of Disease Progression in Post Immunotherapy Lung Cancer Patients
    Status: Recruiting
    Start Date: January 17, 2023
    --------------------------------------------------------------------------------
    NCT ID: NCT02102009
    Title: Nutritional Supplementation in Adults With Chronic Respiratory Disease
    Status: Completed
    Start Date: April 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT01863186
    Title: Efficacy, Safety and Dose-Response Study Followed by Open-Label Study of Lofexidine Treatment of Opioid Withdrawal
    Status: Completed
    Start Date: June 2013
    --------------------------------------------------------------------------------
    NCT ID: NCT02997449
    Title: Complete Endosonographic Intrathoracic Nodal Staging of Lung Cancer Patients in Whom SABR is Considered
    Status: Unknown status
    Start Date: December 2013
    --------------------------------------------------------------------------------
    NCT ID: NCT04212819
    Title: Before and After Erythrocyte Suspension Transfusion
    Status: Completed
    Start Date: January 1, 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT01896544
    Title: Cholecalciferol Supplementation for Sepsis in the ICU
    Status: Completed
    Start Date: January 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT05236166
    Title: Multicentre Study on Rapid Versus Slow Withdrawal of Antiepileptic Monotherapy
    Status: Completed
    Start Date: April 26, 2017
    --------------------------------------------------------------------------------
    NCT ID: NCT05564572
    Title: Randomized Implementation of Routine Patient-Reported Health Status Assessment Among Heart Failure Patients in Stanford Cardiology
    Status: Enrolling by invitation
    Start Date: September 7, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT02917694
    Title: A Feasibility Study to Assess Pre Admission Status and Six Month Outcomes After Major Trauma
    Status: Completed
    Start Date: November 1, 2016
    --------------------------------------------------------------------------------
    NCT ID: NCT01487057
    Title: Lipid Metabolic Status in Thyroid Carcinoma
    Status: Completed
    Start Date: February 2011
    --------------------------------------------------------------------------------
    NCT ID: NCT02172560
    Title: A Collection of Vital Status and Pulmonary Medication Usage Data for Patients With Chronic Obstructive Pulmonary Disease (COPD) Who Withdrew Prematurely From Tiotropium Inhalation Solution Delivered by the Respimat Inhaler
    Status: Completed
    Start Date: March 2007
    --------------------------------------------------------------------------------
    NCT ID: NCT05806580
    Title: A Single-arm Prospective Study of Secondary Infusion of Relmacabtagene Autoleucel Injection for Relapsed or Refractory B-cell Lymphoma
    Status: Recruiting
    Start Date: May 1, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT03847584
    Title: Using Survey to Explore Perceptions of Adults With Low Socioeconomic Status Regarding the NutriQuébec Study
    Status: Completed
    Start Date: October 11, 2018
    --------------------------------------------------------------------------------
    NCT ID: NCT03736044
    Title: Reconstitution of CD4+CD25highCD127low/-Tcell
    Status: Completed
    Start Date: November 25, 2013
    --------------------------------------------------------------------------------
    NCT ID: NCT05375786
    Title: Epidemiological Study on Asymptomatic Infections and Mild Illness With Covid-19 in Shanghai
    Status: Recruiting
    Start Date: April 2, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT03260101
    Title: Non-interventional, Long-term Follow-up of Subjects Who Completed ApoGraft-01 Study
    Status: Unknown status
    Start Date: June 10, 2018
    --------------------------------------------------------------------------------
    NCT ID: NCT04882332
    Title: Metformin Usage Index and Vitamin B12 Status in Egyptian Type 2 Diabetic Patients
    Status: Recruiting
    Start Date: May 5, 2021
    --------------------------------------------------------------------------------
    NCT ID: NCT00220090
    Title: DARWIN Study: A Randomization/Withdrawal Efficacy Study of Dexloxiglumide in Constipation-Predominant Irritable Bowel Syndrome (C-IBS)
    Status: Completed
    Start Date: July 2003
    --------------------------------------------------------------------------------
    NCT ID: NCT03971266
    Title: Movement and Fitness Trackers in Determining Performance Status
    Status: Recruiting
    Start Date: March 27, 2019
    --------------------------------------------------------------------------------
    NCT ID: NCT02056236
    Title: TELSTAR: Treatment of ELectroencephalographic STatus Epilepticus After Cardiopulmonary Resuscitation
    Status: Completed
    Start Date: April 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT00214279
    Title: MMF Monotherapy and Immune Regulation in Kidney Transplant Recipients: Part 1 Steroid Withdrawal
    Status: Completed
    Start Date: May 2002
    --------------------------------------------------------------------------------
    NCT ID: NCT03625635
    Title: Effect of a Clinical Nutrition Intervention Program in Breast Cancer Patients During Antineoplastic Treatment
    Status: Unknown status
    Start Date: September 14, 2015
    --------------------------------------------------------------------------------
    NCT ID: NCT03089541
    Title: Electronic Cigarette Use in Young Adult Men and Women
    Status: Completed
    Start Date: May 24, 2017
    --------------------------------------------------------------------------------
    NCT ID: NCT00792610
    Title: The Hepatitis B Vaccine Booster Response Among the Youth Who Had Completed Neonatal Hepatitis B Vaccines
    Status: Completed
    Start Date: August 2007
    --------------------------------------------------------------------------------
    NCT ID: NCT00920075
    Title: Alendronate in Juvenile Osteoporosis
    Status: Completed
    Start Date: July 2009
    --------------------------------------------------------------------------------
    NCT ID: NCT03759873
    Title: Incentives and Case Management to Improve Cardiac Care: Healthy Lifestyle Program
    Status: Active, not recruiting
    Start Date: December 3, 2018
    --------------------------------------------------------------------------------
    NCT ID: NCT00297232
    Title: Natalizumab (Tysabri) Re-Initiation of Dosing
    Status: Terminated
    Start Date: March 2006
    --------------------------------------------------------------------------------
    NCT ID: NCT02498977
    Title: Liver Immunosuppression Free Trial
    Status: Unknown status
    Start Date: October 2015
    --------------------------------------------------------------------------------
    NCT ID: NCT05683210
    Title: Comparison of The Effects of Initial Oral Feeding by Cup and Bottle-Feeding of Preterm Infants
    Status: Completed
    Start Date: January 13, 2021
    --------------------------------------------------------------------------------
    NCT ID: NCT04433962
    Title: Investigation of the Effects of Balance Training on Balance and Functional Status Patients With Total Hip Arthroplasty
    Status: Completed
    Start Date: September 1, 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT00375180
    Title: Nutritional Status and Barriers to Dietary Intake in Head and Neck Cancer Patients
    Status: Completed
    Start Date: November 2006
    --------------------------------------------------------------------------------
    NCT ID: NCT02915354
    Title: Relapse of Ankylosing Spondylitis Patients Withdrawal Etanercept After Clinical Remission: a Following-up Study
    Status: Completed
    Start Date: July 2007
    --------------------------------------------------------------------------------
    NCT ID: NCT00508144
    Title: Single Agent Alimta in Poor Performance Status in Non-small Cell Lung Cancer
    Status: Completed
    Start Date: September 2005
    --------------------------------------------------------------------------------
    NCT ID: NCT00700869
    Title: Evaluation of a New Mechanical Ventilation Weaning Strategy for Patients With Altered Level of Consciousness
    Status: Completed
    Start Date: April 2008
    --------------------------------------------------------------------------------
    NCT ID: NCT03322410
    Title: Hydratation Status at Initiation of Peritoneal Dialysis: Study of the Role of Peritoneal Permeability
    Status: Unknown status
    Start Date: November 1, 2017
    --------------------------------------------------------------------------------
    NCT ID: NCT01124149
    Title: Ability to Maintain or Achieve Clinical and Endoscopic Remission With MMX Mesalamine Once Daily in Adults With Ulcerative Colitis
    Status: Completed
    Start Date: June 29, 2010
    --------------------------------------------------------------------------------
    NCT ID: NCT05673850
    Title: Association Between HER2 Status and pCR Rate in ER-positive Breast Cancer Receiving Neoadjuvant Endocrine or Chemotherapy
    Status: Completed
    Start Date: May 1, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT01372202
    Title: CHFR Methylation Status Esophageal Cancer Study
    Status: Terminated
    Start Date: June 2011
    --------------------------------------------------------------------------------
    NCT ID: NCT04164004
    Title: Patient-Reported Outcome Measurement in Heart Failure Clinic
    Status: Active, not recruiting
    Start Date: August 30, 2021
    --------------------------------------------------------------------------------
    NCT ID: NCT02339532
    Title: Neoadjuvant Phase II Trial in Patients With T1c Operable, HER2-positive Breast Cancer According to TOP2A Status
    Status: Active, not recruiting
    Start Date: January 2015
    --------------------------------------------------------------------------------
    NCT ID: NCT02691988
    Title: Withdrawal of Inhaled Corticosteroids in Primary Care Patients With COPD
    Status: Unknown status
    Start Date: December 2015
    --------------------------------------------------------------------------------
    NCT ID: NCT02145156
    Title: Educational Intervention to Minimize Disparities in Humanpapillomavirus Vaccination
    Status: Completed
    Start Date: June 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT04748822
    Title: Quality of Life in Patients With Alcohol Use Disorder
    Status: Recruiting
    Start Date: March 25, 2021
    --------------------------------------------------------------------------------
    NCT ID: NCT05684276
    Title: DUMAS: Neo-Adjuvant Immunotherapy for Pancoast Tumors
    Status: Not yet recruiting
    Start Date: April 30, 2023
    --------------------------------------------------------------------------------
    NCT ID: NCT02760537
    Title: Lay Health Worker Model to Reduce Liver Cancer Disparities in Asian Americans
    Status: Completed
    Start Date: April 2013
    --------------------------------------------------------------------------------
    NCT ID: NCT00801801
    Title: Study of Low Dose Chemotherapy Plus Sorafenib as Initial Therapy for Patients With Advanced Non-Squamous Cell NSCLC
    Status: Terminated
    Start Date: January 2008
    --------------------------------------------------------------------------------
    NCT ID: NCT04542499
    Title: Flexible-Dose, Adjunctive Therapy Trial in Adults With Parkinson's Disease With Motor Fluctuations
    Status: Recruiting
    Start Date: October 27, 2020
    --------------------------------------------------------------------------------
    NCT ID: NCT05750719
    Title: BRCA and NACT in TNBC Patients
    Status: Completed
    Start Date: January 2, 2013
    --------------------------------------------------------------------------------
    NCT ID: NCT05669092
    Title: A Phase III Trial of Anus-preservation in Low Rectal Adenocarcinoma Based on MMR/MSI Status
    Status: Recruiting
    Start Date: November 1, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT02081547
    Title: IPC Status as a Surgical Quality Marker in Rectal Cancer Surgery
    Status: Unknown status
    Start Date: April 2012
    --------------------------------------------------------------------------------
    NCT ID: NCT05218772
    Title: Objective and Perceived Health Status of Elderly People With Moderate or Severe Haemophilia in France: an Ancillary Study of the FranceCoag Registry
    Status: Recruiting
    Start Date: April 19, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT00748930
    Title: The Canadian Follow-up Program for the ATTRACT Study (P04868)(TERMINATED)
    Status: Terminated
    Start Date: September 2006
    --------------------------------------------------------------------------------
    NCT ID: NCT02896829
    Title: Follow-up of the Persistence of the Complete Molecular Remission After Stopping Imatinib Chronic Myeloid Leukemia
    Status: Completed
    Start Date: April 3, 2013
    --------------------------------------------------------------------------------
    NCT ID: NCT03245281
    Title: LINQ for impEdance meAsuremeNt While Off From HF Medication Study
    Status: Unknown status
    Start Date: October 30, 2017
    --------------------------------------------------------------------------------
    NCT ID: NCT03156036
    Title: Preoperative CRT With Capecitabine ± Temozolomide in Patients With LARC
    Status: Unknown status
    Start Date: November 30, 2017
    --------------------------------------------------------------------------------
    NCT ID: NCT02702037
    Title: Older Person's Exercise and Nutrition Study
    Status: Completed
    Start Date: March 1, 2016
    --------------------------------------------------------------------------------
    NCT ID: NCT03866538
    Title: Budesonide in Patients With Immune Mediated Enteropathies
    Status: Terminated
    Start Date: September 10, 2019
    --------------------------------------------------------------------------------
    NCT ID: NCT01362387
    Title: R U OK? The Acceptability and Feasibility of New Communication Technologies for Follow-up After Medical Abortion
    Status: Completed
    Start Date: April 2011
    --------------------------------------------------------------------------------
    NCT ID: NCT03076489
    Title: Hed-O-Shift: Hedonic and Neurocognitive Processes in Relation to Dietary Habits and Weight Status
    Status: Completed
    Start Date: June 15, 2017
    --------------------------------------------------------------------------------
    NCT ID: NCT02217527
    Title: Test of Novel Drug for Smoking Cessation
    Status: Completed
    Start Date: November 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT04297605
    Title: Study of Pembrolizumab and Single Agent Chemotherapy as First Line Treatment for Patients With Locally Advanced or Metastatic Non-small Cell Lung Cancer With Eastern Cooperative Oncology Group (ECOG) Performance Status of 2
    Status: Recruiting
    Start Date: May 15, 2020
    --------------------------------------------------------------------------------
    NCT ID: NCT05486780
    Title: The Effect of Digital Window on Day and Night Perception Status and Sleep Quality in Intensive Care Patients
    Status: Not yet recruiting
    Start Date: August 8, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT05756621
    Title: Dual Anti-glutamate Therapy in Super-refractory Status Epilepticus After Cardiac Arrest
    Status: Recruiting
    Start Date: January 15, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT00212147
    Title: Interaction of Cobalamin Status With Nitrous Oxide in Relation to Postoperative Cognitive Changes in the Elderly
    Status: Completed
    Start Date: September 2003
    --------------------------------------------------------------------------------
    NCT ID: NCT01228734
    Title: A Trial to Compare Oxaliplatin, Folinic Acid (FA) and 5-Fluorouracil (5FU) Combination Chemotherapy (FOLFOX-4) With or Without Cetuximab in the 1st Line Treatment of Metastatic Colorectal Cancer (mCRC) in Chinese Rat Sarcoma Viral Oncogene Homolog (RAS) Wild-type Patients
    Status: Completed
    Start Date: September 9, 2010
    --------------------------------------------------------------------------------
    NCT ID: NCT03002584
    Title: International Psychometric Validation Study of the Intestinal Gas Questionnaire (IGQ)
    Status: Completed
    Start Date: February 10, 2017
    --------------------------------------------------------------------------------
    NCT ID: NCT02476812
    Title: The Positive Piggy Bank - A Positive Activities Intervention for Improving Functional Status in Patients With Back Pain
    Status: Active, not recruiting
    Start Date: June 2015
    --------------------------------------------------------------------------------
    NCT ID: NCT00735111
    Title: Do Self-Rated Performance Status Scores Correlate With Health-Care-Provider-Scores?
    Status: Completed
    Start Date: February 2008
    --------------------------------------------------------------------------------
    NCT ID: NCT04355247
    Title: Prophylactic Corticosteroid to Prevent COVID-19 Cytokine Storm
    Status: Unknown status
    Start Date: April 14, 2020
    --------------------------------------------------------------------------------
    NCT ID: NCT01638559
    Title: Immunosuppression Withdrawal for Stable Pediatric Liver Transplant Recipients
    Status: Completed
    Start Date: August 14, 2012
    --------------------------------------------------------------------------------
    NCT ID: NCT02203279
    Title: Evaluation of Three Hard Relining Materials in Complete Dentures
    Status: Completed
    Start Date: July 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT00538980
    Title: Dasatinib in Polycythemia Vera
    Status: Terminated
    Start Date: April 30, 2007
    --------------------------------------------------------------------------------
    NCT ID: NCT02856009
    Title: Role of Nutrition in Patients Over 75 Years of Age With Stroke
    Status: Completed
    Start Date: November 2015
    --------------------------------------------------------------------------------
    NCT ID: NCT03926832
    Title: Prevalence of Obstructive Sleep Apnea Syndrome in Sarcoidosis and Impact of CPAP Treatment on Associated Fatigue Status
    Status: Completed
    Start Date: April 27, 2019
    --------------------------------------------------------------------------------
    NCT ID: NCT00269191
    Title: A Study to Assess the Safety and Efficacy of an Investigational Drug in Patients With Osteoarthritis (0663-071)(COMPLETED)
    Status: Completed
    Start Date: February 5, 2003
    --------------------------------------------------------------------------------
    NCT ID: NCT03545555
    Title: Investigations on the Effect of Kale on the Lipid Status
    Status: Unknown status
    Start Date: April 13, 2018
    --------------------------------------------------------------------------------
    NCT ID: NCT02584127
    Title: Tobacco-Related Disease Prevention Among Korean Americans
    Status: Completed
    Start Date: September 2009
    --------------------------------------------------------------------------------
    NCT ID: NCT03765580
    Title: The Influence of Fish Consumption on Polyunsaturated Fatty Acid (PUFA) Status
    Status: Completed
    Start Date: September 1, 2016
    --------------------------------------------------------------------------------
    NCT ID: NCT00417040
    Title: Collection of Patient-Reported Symptoms and Performance Status Via the Internet
    Status: Completed
    Start Date: December 2006
    --------------------------------------------------------------------------------
    NCT ID: NCT04576962
    Title: County Level Correlates of HPV Vaccine Series Completion Among Children Ages 11-14 Years in Indiana
    Status: Completed
    Start Date: February 9, 2021
    --------------------------------------------------------------------------------
    NCT ID: NCT05023395
    Title: Safety and Efficacy of MEE-HU Medicus
    Status: Recruiting
    Start Date: October 11, 2021
    --------------------------------------------------------------------------------
    NCT ID: NCT02355028
    Title: LHA510 Proof-of-Concept Study as a Maintenance Therapy for Patients With Wet Age-Related Macular Degeneration
    Status: Completed
    Start Date: March 3, 2015
    --------------------------------------------------------------------------------
    NCT ID: NCT01584310
    Title: Validation of the STAMP Screening Tool
    Status: Completed
    Start Date: October 2012
    --------------------------------------------------------------------------------
    NCT ID: NCT01661894
    Title: Effectiveness of a Brain-Computer Interface Based System for Cognitive Enhancement in the Normal Elderly
    Status: Completed
    Start Date: April 2012
    --------------------------------------------------------------------------------
    NCT ID: NCT02802540
    Title: Nabilone Effect on the Attenuation of Anorexia, Nutritional Status and Quality of Life in Lung Cancer Patients
    Status: Unknown status
    Start Date: December 2014
    --------------------------------------------------------------------------------
    NCT ID: NCT04751604
    Title: Improvement of the Nutritional Status Regarding Nicotinamide (Vitamin B3) and the Disease Course of COVID-19
    Status: Completed
    Start Date: February 1, 2021
    --------------------------------------------------------------------------------
    NCT ID: NCT03102229
    Title: Real-time Activity Monitoring to Prevent Admissions During RadioTherapy
    Status: Completed
    Start Date: July 2016
    --------------------------------------------------------------------------------
    NCT ID: NCT03941366
    Title: Treatment of Adenocarcinoma of the Rectum With Transanal Local Excision for Complete Responders
    Status: Recruiting
    Start Date: February 26, 2016
    --------------------------------------------------------------------------------
    NCT ID: NCT05493579
    Title: Impact of Implant Supported Overdenture on Changes of Electromyographic and Brain Activity
    Status: Completed
    Start Date: October 1, 2020
    --------------------------------------------------------------------------------
    NCT ID: NCT04835597
    Title: Precision Performance Status Assessment in Breast Cancer Patients Receiving Neoadjuvant Chemotherapy
    Status: Recruiting
    Start Date: August 15, 2022
    --------------------------------------------------------------------------------
    NCT ID: NCT04834570
    Title: Breast Cancer Survivors: Main Physical and Psychosocial Problems After Completion of Treatment
    Status: Unknown status
    Start Date: October 5, 2020
    --------------------------------------------------------------------------------
    NCT ID: NCT04123145
    Title: Study of the Prevalence of Iron Deficiency in Patients With Chronic Renal Failure But Non-Dialysis (CARENFER IRC-ND)
    Status: Unknown status
    Start Date: October 15, 2019
    --------------------------------------------------------------------------------
    NCT ID: NCT03056183
    Title: Care Transitions for Patients With Depression
    Status: Withdrawn
    Start Date: January 1, 2019
    --------------------------------------------------------------------------------
    NCT ID: NCT05788510
    Title: Pneumococcal Vaccination in Patients With Anti-TNF Alpha Therapy
    Status: Not yet recruiting
    Start Date: April 2023
    --------------------------------------------------------------------------------

</div>

<div class="output error" ename="KeyError" evalue="'StartDateStruct'">

    ---------------------------------------------------------------------------
    KeyError                                  Traceback (most recent call last)
    /var/folders/fk/93tn9scx5zv8l49p5dwrl2nr0000gn/T/ipykernel_41088/1134357508.py in <module>
          6     title = study["ProtocolSection"]["IdentificationModule"]["BriefTitle"]
          7     status = study["ProtocolSection"]["StatusModule"]["OverallStatus"]
    ----> 8     start_date = study["ProtocolSection"]["StatusModule"]["StartDateStruct"]["StartDate"]
          9 
         10     print(f"NCT ID: {nct_id}")

    KeyError: 'StartDateStruct'

</div>

</div>

<div id="6b699569" class="cell markdown">

## It is evident from the plots below that more people are enrolled in projects that are completed.

If you look at the pie-chart below, only 13.3% of the trials below have
failed. I'm fairly certain that at approximately one out of every ten
trials fail. I am surprised to see the number that low, in fact.

</div>

<div id="3be95f16" class="cell code" execution_count="56">

``` python

# Process the data
data = []
for trial in trials:
    study = trial["Study"]
    status = study["ProtocolSection"]["StatusModule"]["OverallStatus"]

    enrollment_info = study["ProtocolSection"]["DesignModule"].get("EnrollmentInfo", None)
    if enrollment_info:
        enrollment_count = int(enrollment_info["EnrollmentCount"])
    else:
        enrollment_count = None

    if enrollment_count is not None:
        data.append({
            "enrollment_count": enrollment_count,
            "outcome": "Completed" if status.lower() == "completed" else "Not Completed"
        })

# Create a DataFrame
df = pd.DataFrame(data)

# Create the bar plot
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="outcome", y="enrollment_count", ci=None)
plt.title("Average Enrollment Count for Completed and Not Completed Trials")
plt.show()


```

<div class="output display_data">

![](/_images/First_Notebook_79_0.png)

</div>

</div>

<div id="d0611755" class="cell code">

``` python

```

</div>

<div id="c83eca97" class="cell code" execution_count="57">

``` python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Process the data
data = []
for trial in trials:
    study = trial["Study"]
    status = study["ProtocolSection"]["StatusModule"]["OverallStatus"]

    enrollment_info = study["ProtocolSection"]["DesignModule"].get(
        "EnrollmentInfo", None)
    if enrollment_info:
        enrollment_count = int(enrollment_info["EnrollmentCount"])
    else:
        enrollment_count = None

    if enrollment_count is not None:
        data.append({
            "enrollment_count":
            enrollment_count,
            "outcome":
            "Completed" if status.lower() == "completed" else "Not Completed"
        })

# Create a DataFrame
df = pd.DataFrame(data)

# Group data by outcome and calculate the sum of enrollment counts
grouped_df = df.groupby("outcome").sum().reset_index()

# Plot the pie chart using Matplotlib
fig, ax = plt.subplots()
ax.pie(grouped_df['enrollment_count'],
       labels=grouped_df['outcome'],
       autopct='%1.1f%%',
       startangle=90)
ax.set_title('Enrollment Count for Completed and Not Completed Trials')

# Equal aspect ratio ensures that pie is drawn as a circle.
ax.axis('equal')

# Show the plot
plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_81_0.png)

</div>

</div>

<div id="e350d359" class="cell code" execution_count="58">

``` python
print(df.columns)
```

<div class="output stream stdout">

    Index(['enrollment_count', 'outcome'], dtype='object')

</div>

</div>

<div id="87a11658" class="cell code" execution_count="59">

``` python
def fetch_trials(page, size):
    url = f"https://clinicaltrialsapi.cancer.gov/v1/trials?size={size}&from={size * (page - 1)}"
    response = requests.get(url)
    data = response.json()
    
    trials = []
    for trial in data["trials"]:
        if "Study" in trial and "ProtocolSection" in trial["Study"] and "OutcomeMeasuresModule" in trial["Study"]["ProtocolSection"]:
            outcome_measures = trial["Study"]["ProtocolSection"]["OutcomeMeasuresModule"]
            for outcome in outcome_measures.get("PrimaryOutcomeMeasures", []):
                if "survival" in outcome["OutcomeMeasureTitle"].lower() or "overall survival" in outcome["OutcomeMeasureTitle"].lower():
                    trials.append(trial)
                    break
    
    return trials
```

</div>

<div id="d9ccff54" class="cell code" execution_count="60">

``` python


# Assuming you have a DataFrame 'df' with columns 'enrollment_count' and 'outcome'
grouped = df.groupby('outcome')

# Calculate summary statistics
summary_stats = grouped['enrollment_count'].describe()
mean_enrollment = grouped['enrollment_count'].mean()
median_enrollment = grouped['enrollment_count'].median()

print("Summary Statistics:")
print(summary_stats)
print("\nMean Enrollment:")
print(mean_enrollment)
print("\nMedian Enrollment:")
print(median_enrollment)
```

<div class="output stream stdout">

    Summary Statistics:
                   count         mean           std   min   25%    50%    75%  \
    outcome                                                                     
    Completed       55.0  2448.690909  16442.017397  10.0  48.5  120.0  365.0   
    Not Completed   44.0   469.909091   1558.125347   0.0  29.5   79.0  200.0   

                        max  
    outcome                  
    Completed      122152.0  
    Not Completed   10000.0  

    Mean Enrollment:
    outcome
    Completed        2448.690909
    Not Completed     469.909091
    Name: enrollment_count, dtype: float64

    Median Enrollment:
    outcome
    Completed        120.0
    Not Completed     79.0
    Name: enrollment_count, dtype: float64

</div>

</div>

<div id="70bfd38d" class="cell markdown">

**To further investigate the differences between the two groups, we can
perform additional statistical tests, such as the Mann-Whitney U test,
to determine if the difference in enrollment counts is statistically
significant. Additionally, we can explore other factors, like the length
of the study, the phase of the trial, or the type of intervention being
tested, to understand if they are associated with trial outcomes.**

</div>

<div id="cecd188e" class="cell code" execution_count="61">

``` python


# Set the Seaborn style to 'darkgrid'
sns.set_style('darkgrid')

# Create a bar plot with error bars using the 'barplot' function in Seaborn
sns.barplot(data=df, x='outcome', y='enrollment_count', ci='sd')

# Add labels and title
plt.xlabel('Outcome')
plt.ylabel('Enrollment Count')
plt.title('Enrollment Count by Outcome')

# Show the plot
plt.show()
```

<div class="output display_data">

![](/_images/First_Notebook_86_0.png)

</div>

</div>

<div id="2f7d9ddf" class="cell code" execution_count="62">

``` python


completed_trials = df[df['outcome'] == 'Completed']['enrollment_count']
not_completed_trials = df[df['outcome'] == 'Not Completed']['enrollment_count']

# Perform Mann-Whitney U test
stat, p = mannwhitneyu(completed_trials, not_completed_trials)

print('Mann-Whitney U test results:')
print('statistic = %.3f, p-value = %.3f' % (stat, p))
```

<div class="output stream stdout">

    Mann-Whitney U test results:
    statistic = 1425.500, p-value = 0.130

</div>

</div>

<div id="5ba5418f" class="cell markdown">

\*The Mann-Whitney U test is a nonparametric statistical test used to
compare the median values of two independent groups.\*\*

The statistic in the result, which is 1425.500, represents the
Mann-Whitney U test statistic. The U statistic is calculated based on
the ranks of the observations in both groups. The U statistic ranges
from 0 to n1 x n2, where n1 and n2 are the sample sizes of the two
groups. A larger U statistic indicates that one group tends to have
higher values than the other group.

The p-value in the result, which is 0.130, represents the probability of
observing a U statistic as extreme as the one calculated, assuming the
null hypothesis is true. The null hypothesis in the Mann-Whitney U test
is that there is no significant difference between the medians of the
two groups.

In this case, the p-value is greater than the significance level of
0.05, which means that there is not enough evidence to reject the null
hypothesis. Therefore, we can conclude that there is no significant
difference between the medians of the two groups at the 5% level of
significance.

</div>

<div id="54bddcb0" class="cell markdown">

Given two samples $X$ and $Y$ of sizes $n_{1}$ and $n_{2}$, the
Mann-Whitney U test tests the null hypothesis that the two populations
from which the samples were drawn have the same distribution function.
The test statistic $U$ is calculated as:

$$U = \sum_{i=1}^{n_{1}}\sum_{j=1}^{n_{2}} R_{ij}$$

where $R_{ij}$ is 1 if $X_{i} < Y_{j}$, 0.5 if $X_{i} = Y_{j}$, and 0 if
$X_{i} > Y_{j}$.

The expected value of $U$ under the null hypothesis is:

$$E(U) = \frac{n_{1}(n_{1}+n_{2}+1)}{2}$$

The variance of $U$ under the null hypothesis is:

$$Var(U) = \frac{n_{1}n_{2}(n_{1}+n_{2}+1)}{12}$$

The test statistic is then standardized using the following formula:

$$Z = \frac{U - E(U)}{\sqrt{Var(U)}}$$

Under the null hypothesis, the standardized test statistic $Z$ follows a
standard normal distribution. The null hypothesis is rejected if the
absolute value of $Z$ exceeds the critical value of the standard normal
distribution at the desired significance level.

</div>

<div id="48aedce8" class="cell code" execution_count="63">

``` python
# Import the necessary libraries


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[['enrollment_count']],
                                                    df['outcome'],
                                                    test_size=0.2,
                                                    random_state=42)

# Train a logistic regression model on the training data
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_test)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
```

<div class="output stream stdout">

    Accuracy: 0.5

</div>

</div>

<div id="5f4faea6" class="cell markdown">

Classification Report:

              precision    recall  f1-score   support

           0       0.57      0.67      0.62         9
           1       0.82      0.74      0.78        19

    accuracy                           0.71        28

macro avg 0.69 0.70 0.70 28 weighted avg 0.73 0.71 0.72 28

Confusion Matrix:

\[\[ 6 3\] \[ 5 14\]\]

</div>

<div id="24053e79" class="cell markdown">

#### It's tempting to perform an ML model here to go with the Mann-Whitney.

Based on the classification report, it seems like the classification
model has performed *reasonably well*, but it's hard to make a
definitive judgment without more more data (and some different data
too!). Here is a breakdown of the metrics in the classification report:

- Precision: The precision score is the ratio of true positives to the
  total number of positive predictions made by the model. In this case,
  the precision score for class 0 is 0.57, which means that when the
  model predicts a sample to be in class 0, it is correct 57% of the
  time. Similarly, the precision score for class 1 is 0.82, which means
  that when the model predicts a sample to be in class 1, it is correct
  82% of the time.

- Recall: The recall score is the ratio of true positives to the total
  number of actual positive samples in the dataset. In this case, the
  recall score for class 0 is 0.67, which means that the model correctly
  identifies 67% of the samples that belong to class 0. The recall score
  for class 1 is 0.74, which means that the model correctly identifies
  74% of the samples that belong to class 1.

- F1-score: The F1-score is the harmonic mean of precision and recall,
  and provides a balanced measure of both metrics. In this case, the
  F1-score for class 0 is 0.62, and the F1-score for class 1 is 0.78.

- Support: The support refers to the number of samples in each class.

Overall, the accuracy of the model is 0.71, which means that it
correctly predicts the class of 71% of the samples in the dataset.
However, it's important to note that the performance of a classification
model can vary widely depending on the context of the problem, and it's
always a good idea to validate the model using multiple evaluation
metrics and techniques.

</div>

<div id="51e0e8df" class="cell markdown">

</div>
