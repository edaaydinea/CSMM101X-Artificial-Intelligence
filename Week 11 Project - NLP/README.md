Week 11 Project: NLP
====================
**INSTRUCTIONS**

Congratulations on making it to the last programming project. By coming this far, we assume that you have accumulated formidable knowledge in both traditional Artificial Intelligence (AI) and modern Machine Learning (ML), and from now on we will treat you as such. This assignment intends to give you a flavor of a real world AI/ML application, which often require to gather the raw data, do preprocessing, design suitable ML algorithms and implement the solution. Today, we touch on an active research area in Natural Language Processing (NLP), sentiment analysis.

Given the exponentially growing of online review data (Amazon, IMDB and etc), sentiment analysis becomes increasingly important. We are going to build a sentiment classifier, i.e., evaluating a piece of text being either positive or negative.

The "Large Movie Review Dataset"(*) shall be used for this project. The dataset is compiled from a collection of 50,000 reviews from IMDB on the condition there are no more than 30 reviews each movie. Number of positive and negative reviews are equal. Negative reviews have scores lesser or equal 4 out of 10 while a positive review greater or equal 7 out of 10. Neutral reviews are not included on the other hand. Then, 50,000 reviews are divided evenly into the training and test set.

**Dataset is credited to Prof. Andrew Mass in the paper, Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. (2011). [Learning Word Vectors for Sentiment Analysis.](http://ai.stanford.edu/~amaas/papers/wvSent_acl2011.pdf) The 49th Annual Meeting of the Association for Computational Linguistics (ACL 2011).*

**Due date:**

**The assignment's final due date is 12/13/2020, 23:30 UTC. **

### **I. Instruction**

Up until now, most of the course projects have been requiring you to implement algorithms discussed in lectures. This assignment is going to introduce a few advanced concepts of which implementations demand a non-trivial programming expertise. As such, before reinventing the wheel, we would advise you to first explore the incredibly powerful existing Python libraries. The following two are highly recommended:

-   <http://scikit-learn.org/stable/>
-   <http://pandas.pydata.org/>

#### Stochastic Gradient Descent Classifier

In this project, we will train a Stochastic Gradient Descent Classifier. Recalled from the Machine Learning project, you were asked to implement a gradient descend update algorithm for linear regression. While gradient descend is powerful, it can be prohibitively expensive when the dataset is extremely large because every single data point  needs to be processed.

However, it turns out when the data is large, rather than the entire dataset, SGD algorithm performs just as good with a small random subset of the original data. This is the central idea of Stochastic SGD and particarly handy for the text data since corpus are often humongous.

You should read sklearn document and learn how to use a SGD classifier. For adventurers, you are welcome to manually implement SGD yourself. Wikipedia provides a good first reference, <https://en.wikipedia.org/wiki/Stochastic_gradient_descent>.

#### ***Data Preprocessing***

The training data is provided in the directory "../resource/lib/publicdata/aclImdb/train/" of Vocareum. If you wish to download the data to your local machine for inspections, use the following link: <http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz>[.](http://ai.%20stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz.)  

Your first task is explore this directory. There are two sub-directories **pos/** for positive texts and **neg/ **for negative ones. **You do not need to worry about unsup/, and you do not ned them.** 

Now **combine the raw database into a single csv**** files,** "**imdb_****tr.csv**". The csv file should have three columns, **"row_number"** and **"text" and "polarity"**. The column **"text"** contains review texts from the aclImdb database and the column **"polarity"** consists of sentiment labels, 1 for positive and 0 for negative. An example of "imdb.tr.csv" is provided in the workspace.

In addition, common English stopwords should be removed**. **An English stopwords reference are provided in your Vocareum work space for your reference. Your driver.py (as explained below) **will have access to it during run time**.

#### ***Unigram Data Representation***

The very first step in solving any NLP problem is finding a way to represent the text data so that machines can understand. A common approach is using a document-term vector where each document is encoded as a discrete vector that counts occurrences of each word in the vocabulary it contains. For example, consider two one-sentence documents:  

-   d2: "Artificial Intelligence is awesome"

The vocabulary V = {artificial, awesome, Columbia, course, I, intelligence, is, love} and two documents can be encoded as v1 and v2 as follow:

![](https://courses.edx.org/assets/courseware/v1/5118ee126880ea7b89d93fa6a625f6de/asset-v1:ColumbiaX+CSMM.101x+3T2020+type@asset+block/table1.png)

Hint: When building our model you should assume no access to the test data. Then what if there are words that appear only in test data but not in training data? The features will mismatch if you include those. Therefore, when extracting features in the test set, you should only **use the vocabulary that was used in the training set.**

If you wish to know more, start from here [https://en.wikipedia.org/wiki/Document-term_ matrix](https://en.wikipedia.org/wiki/Document-term_%20matrix). This data representation is also called **a unigram model**.

Now, write a python function to transform text column in **imdb_tr.csv** into a term-document matrices using uni- gram model then train a **Stochastic Gradient Descent (SGD) classifier** whose loss="hinge" and penalty="l1" on this data.

On the other hand, in the driver.py, you will also find the link to ***"../resource/lib/publicdata/imdb_te.csv"*** which is our benchmark file for the performance of the trained classifier. "***imdb_te.csv"** *has two columns: **"row_number"** and **"text". **The column** "polarity"** is excluded and your job is to use the trained SGD classifier to predict this information. You should transform **imdb_te.csv** using unigram data model as well and use the trained SGD to predict the converted test set. Predictions must be formatted line by line and stored in "**unigram.output.txt" **in your Vocareum workspace. An example of the output file is provided for your benefits.

**If you wish to run the test in your local machine, download the following [test file](https://courses.edx.org/assets/courseware/v1/9dbe589c9a231b5174729e059a17e8eb/asset-v1:ColumbiaX+CSMM.101x+3T2020+type@asset+block/imdb_te.csv.zip).**

#### ***Bigram Representation***

A more sophisticated data representation model is the bigram model where occurrences depend on a sequence of two words rather than an individual one. Taking the same example like before, v1 and v2 are now encoded as follow:

![](https://courses.edx.org/assets/courseware/v1/a9f26850f894230a0cb47c6c026bd436/asset-v1:ColumbiaX+CSMM.101x+3T2020+type@asset+block/table2.png)

Instead of enumerating every individual words, bigram counts the number of instance a word following after another one. In both d1 and d2 "intelligence" follows "artificial" so v1(intelligence | artificial) = v2(intelligence | artificial) = 1. In contrast, "artificial" does not follow "awesome" so v1(artificial | awesome) = v2(artificial | awesome) = 0.\
Since the Unigram model doesn't take into account the context of the words in a document, in this part you will extend your previous solution by creating a model that also counts Bigrams to introduce some context in your vocabulary. This should  produce the test prediction file "**bi****gram.output.txt" .**

#### ***Tf-idf:***

Sometimes, a very high word counting may not be meaningful. For example, a common word like "say" may appear 10 times more frequent than a less-common word such as "machine" but it does not mean "say" is 10 times more relevant to our sentiment classifier. To alleviate this issue, we can instead use **term** **frequency**** tf[t]**** = 1 + log(f[t,d] ) **where** f[t,d]** is the count of term t in document d. The log function dampens the unwanted influence of common English words.

Inverse document frequency (idf) is a similar concept. To take an example, it is likely that all of our training documents belong to a same category which has specific jargons. For example, Computer Science documents often have words such as computers, CPU, programming and etc  appearing over and over. While they are not common English words, because of the document domain, their occurrences are very high. To rectify, we can adjust using **inverse term frequency *****idf[t] = log( N / df[t] ) ***where **df[t]** is the number of documents containing the term t and N is the total number of document in the dataset.

Therefore, instead of just word frequency, tf-idf for each term t can be used,** tf-idf[t] = tf[t] ∗idf[t].**  

Repeat the same exercise as in the Unigram and Bigram data model but apply tf-idf this time to produce test prediction files, "**uni****gramtfidf.output.txt" **and "**bi****gramtfidf.output.txt"**

### **II. What you need to submit:**

Your task in this assignment is to write driver.py to produce sentiment predictions over the **imdb_te.csv** by various text data representation (unigram, unigram with tf-idf, bigram and bigram with tf-idf). Please ensure your driver.py write the predictions to the following files **during the run time** (one-time outputs are not accepted):

-   unigram.output.txt
-   unigramtfidf.output.txt
-   bigram.output.txt
-   bigramtfidf.output.txt

Be very ***precise*** with these file names because the auto-grader will rerun your driver.py and look for them for evaluation. As usual, your program will be run as follows:

$python3 driver.py

It is highly recommended that before submission you should perform some sanity check so you will not waste your time and opportunity to submit. Below are something you want to keep in mind:

- The name of your program file correspond with the expected, exactly

- The name of the output file generated by your program

- The libraries that you are using in your program be allowed (only standards lib)

- The way you read the training and testing data is correct (Be aware of **headers**! Do not get off-by-one error!)

- You have performed cross validation on your model

Note:  Our grade will **not **call imdb_data_preprocess() ourselves. You will need to do data processing under *if __name__ == "__main__": *by yourself in the driver.
