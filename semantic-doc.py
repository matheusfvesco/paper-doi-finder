from urllib.parse import urlparse, quote
import requests
import os
import json
from time import sleep

# Define the query and data endpoints for the Semantic Scholar API
query_endpoint = "https://api.semanticscholar.org/graph/v1/paper/search?query="
data_endpoint = "https://api.semanticscholar.org/graph/v1/paper/"
fields = "?fields=title,url,year,externalIds"

global_wait = 10

# function definition
def get_papers(top: str) -> list:
    """
    This function takes in a directory path and returns a list of paper titles found in that directory.
    """
    paper_list = []

    # Walk through the directory and its subdirectories
    for file in os.walk(top):
        # If there are no files in the current directory, continue to the next one
        if file[2] == []:
            continue
        # Add each paper title to the list (removing the file extension)
        for paper in file[2]:
            paper_list.append(paper[:-4])

    return paper_list


def find_same_paper(papers: list, target: str) -> int:
    """
    This function takes in a list of papers and a target paper title and returns the index of the target paper in the list.
    If the target paper is not found, it returns True.
    """

    # TODO: write function that compares strings and if string is 10% similar to another(Levenshtein distance)
    # return True if yes. Test every name and find the closest match.

    for index, paper in enumerate(papers):
        if paper["title"] == target:
            return index

    return True


def get_semantic_id(query: str) -> str:
    """
    This function takes in a query string and returns the Semantic Scholar ID of the first result from the Semantic Scholar API.
    """
    # Parse the query string to make it URL-friendly
    parsed = quote(query.lower())
    # Make a GET request to the Semantic Scholar API with the parsed query string
    r = requests.get(query_endpoint + parsed)
    sleep(global_wait)

    # Load the response content as JSON
    content = json.loads(r.content)
    data = content["data"]

    # Find the index of the target paper in the data
    index = find_same_paper(data, query)

    # If no matching paper is found, print paper name and return None
    if index:
        print()
        print(f"CHECK THE PAPER: {query}")
        print()
        return
    else:
        print(query)

    # Print the Semantic Scholar ID of the matching paper
    # print(data[index]['paperId'])

    return data[index]["paperId"]


def parse_semantic_id_list(papers: list) -> list:
    """
    This function takes in a list of paper titles and returns a list of their corresponding Semantic Scholar IDs.
    """
    ids = []

    # For each paper title, get its Semantic Scholar ID and add it to the list
    for paper in papers:
        _index = get_semantic_id(paper)
        if _index == None:
            continue
        ids.append(_index)

    return ids


def get_paper_data(semantic_id: str) -> tuple:
    """
    This function takes in a Semantic Scholar ID and returns a tuple containing the paper's title and DOI (if available).
    """
    # Make a GET request to the Semantic Scholar API with the specified ID and fields
    r = requests.get(data_endpoint + semantic_id + fields)
    # Load the response content as JSON
    content = json.loads(r.content)
    sleep(global_wait)

    try:
        # Try to return the paper's title and DOI
        return content["title"], content["externalIds"]["DOI"]
    except:
        # If the DOI is not available, return the paper's title and all external IDs
        return content["title"], content["externalIds"]


def get_data_list(papers: list) -> list:
    """
    This function takes in a list of Semantic Scholar IDs and returns a list of tuples containing each paper's title and DOI (if available).
    """
    data_list = []

    # For each Semantic Scholar ID, get its paper data and add it to the list
    for paper in papers:
        data_list.append(get_paper_data(paper))

    return data_list


# Get a list of papers from the specified directory
papers = get_papers("Artigos")

# Get a list of Semantic Scholar IDs for the papers
papers = parse_semantic_id_list(papers)

# Get a list of paper data for the papers
papers = get_data_list(papers)

# Print the list of paper data
print(papers)

# Write the paper data to a CSV file
with open("papers.csv", "w") as file:
    file.write(f"title;ID" + "\n")

    # For each paper, write its title and DOI (or external IDs) to the file
    for paper in papers:
        file.write(f"{paper[0]};{paper[1]}" + "\n")

    # Close the file
    file.close()
