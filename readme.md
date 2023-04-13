# paper DOI finder
## Using Semantic Scholar Paper Data

Have you ever downloaded a lot of papers on to your computer, but need a DOI ID to easily insert it into Mendeley, Zotero or any other reference manager? This should able to help you.
This script retrieves paper data(DOI or other IDs) from the Semantic Scholar API using paper titles found in a specified directory.

## Usage

1. Set the `top` parameter in the `get_papers` function call to the desired directory path.
2. Run the script to generate a CSV file containing the paper data.

## Dependencies

Basically python's standard library

- `urllib.parse`
- `requests`
- `os`
- `json`