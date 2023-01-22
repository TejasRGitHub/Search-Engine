# Project - CS 582 Information Retrieval 
## Tejas Dhananjay Rajopadhye (UIN - 675873639)

## About 

This project report outlines the specification of the Search Engine made as a final project for CS 582 - Information Retrieval. 
The goal of this project is to design a Web Search Engine that will consist of roughly three stages - web crawler, preprocessing and indexing results based on a weighing scheme. 
The web crawler will start from a UIC domain link and will crawl web pages. 
Once the webpage is captured it will be stored. This webpage will then be preprocessed by the processing system developed during Homework 1 and the results of this will be weighted according to TF-IDF weighing scheme. 
This TF-IDF data along with similarity measures like Cosine Similarity will then be used to provide results to the user about the query that the user provides.

## Setting up the project 

Note - This project was created and testing the Pycharm IDE

1. First Create Folder called "RetrievedDocs" inside the root directory
2. Install the dependencies required for this project. Please type in 'pip install requests', 'pip install BeautifulSoup', 'pip install numpy', 'pip install nltk'. If prompted while running the searchRetrivel to download the stemmer files please install and download them accordingly.
3. In order to start scraping, please run the crawler.py file by issuing command 'python crawler.py'.
4. For directly working on search queries please type 'python searchRetrival <path\_to\_RetrievedDocs Directory>'