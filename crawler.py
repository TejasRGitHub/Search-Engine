## Tejas Dhananjay Rajopadhye (UIN - 675873639)
## Used for Final Project in CS 582 Information retrieval
## Code to crawl uic.edu domain and parse content
## This code contains BFS logic to crawl the UIC domain and get the pages
## The retrieved pages are then store into the

## Import Statements
import json
import requests
from bs4 import BeautifulSoup

## Crawler Globals
# Page to Crawl
BASE_URL="https://cs.uic.edu"
PAGES_TO_CRAWL=3000

# List of URL Links to reject
IGNORE_LIST=[ ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".css", ".js", ".aspx", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".mp4", ".avi", ".tar", ".gz", ".tgz", ".zip",]
PATH_TO_STORE_PAGES="./RetrievedDocs"


def crawlBFS():
    # Initialize the count of unique pages crawled
    numOfPagesVisited = 0
    # Initialize the BFS Queue containing only links to the pages visited
    BFSQueue = []
    BFSQueue.append(BASE_URL)

    # Initialize list of BFS URLs which are visited by the BFS Crawler
    visitedPagesList = []

    # Initialize a map from document to the URL
    docToURL = dict()

    # pop the URL and then get the contents of the page only if it points to an HTML resource in the UIC domain
    # page data =Fetch the Web page and call the preposesing function to remove HTML Tags along with the CSS the HTML Tags carry with them
    # Store Page data into some json based file like a dictionary (URL_OF_PAGE) -> (Page Data )
    # Call another function with the same HTML Page Data to extract further links from the anchor tags
    # Add only those links which are not present in both the Queues and then iterate

    # Iterative Algorithm for BFS
    # while (Queue != empty && count < PAGES_TO_CRAWL)
    while(BFSQueue.__len__() != 0 and numOfPagesVisited < PAGES_TO_CRAWL):
        #Pop the item from the queue
        url = BFSQueue.pop(0)
        print("Visiting URL --> " + url)

        if (url in visitedPagesList):
            continue
        visitedPagesList.append(url)
        try:
            # Fetch the page
            webPage = requests.get(url)

            if (webPage.status_code >= 200 and webPage.status_code < 300):
                #Add to the visited links

                numOfPagesVisited = numOfPagesVisited + 1
                print("Number of Pages Visited -> " + str(numOfPagesVisited))

                #Link it in the map
                docToURL[numOfPagesVisited] = url

                # Extract the content of the webpage
                htmlContent = BeautifulSoup(webPage.content, "lxml")

                textContentFromPage = htmlContent.get_text()
                # Store this in a file Or In Memory If needed
                #print(textContentFromPage)
                fileObj = open(PATH_TO_STORE_PAGES + "/" + str(numOfPagesVisited), "w",  encoding="utf-8")
                fileObj.write(str(textContentFromPage))
                fileObj.close()

                visitedLinksFile = open("visitedLinks", "w", encoding="utf-8")
                visitedLinksFile.write(str(visitedPagesList))
                visitedLinksFile.close()


                # Extract the a links from the webpage
                listOfAnchors = htmlContent.find_all('a')

                for link in listOfAnchors:
                    # get the href from the anchor
                    hrefLink = link.get('href')
                    if (hrefLink is None):
                        continue
                    hrefLink = hrefLink.lower()

                    ## Condition when the link starts with a /
                    if (hrefLink.startswith('/')):
                        if (hrefLink.endswith('/')):
                            hrefLink = hrefLink[:-1]
                        if ((url + hrefLink) not in visitedPagesList and (url + hrefLink) not in BFSQueue):
                            hrefLink = url + hrefLink
                        else:
                            continue
                    if ("https" not in hrefLink):
                        continue
                    # Check if the link doesn't point to any of the ignore lists
                    if (hrefLink in IGNORE_LIST):
                        continue

                    # Clean up the url
                    if (hrefLink.endswith('/')):
                        hrefLink = hrefLink[:-1]

                    if ("uic.edu" in hrefLink and hrefLink not in visitedPagesList and hrefLink not in BFSQueue):
                        BFSQueue.append(hrefLink)
            else:
                visitedPagesList.append(url)
        except Exception as e:
            print(e)
            visitedLinksFile = open("visitedLinks", "w", encoding="utf-8")
            visitedLinksFile.write(str(visitedPagesList))
            visitedLinksFile.close()

            mapFile = open("mapDocToURL", "w", encoding="utf-8")
            json.dump(docToURL, mapFile)
            mapFile.close()


    mapFile = open("mapDocToURL", "w", encoding="utf-8")
    json.dump(docToURL, mapFile)
    mapFile.close()
    return


def main():
   print("Starting Crawler --->>>")
   crawlBFS()
   print("Crawling Finished")

if __name__ == "__main__":
    main()





