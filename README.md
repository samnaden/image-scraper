# image-scraper

## instructions
- go to https://programmablesearchengine.google.com/controlpanel/create
- put in a search engine name
- click the radio button "Search the entire web"
- hit the slider "Image search"
- copy the value for cx shown in the code snippet
- go to https://developers.google.com/custom-search/v1/introduction
- click "Get a Key"
- create a project and get the API key
- Run the below code from a terminal, from this directory. Images will be saved in ./image_scraper/downloaded

```commandline
export IMAGE_API_KEY="{your_api_key}"
export IMAGE_API_CX="{your_cx}"

poetry install
poetry shell

# first arg is the search term, second arg is the number of images you want downloaded
python ./image_scraper "whale" "42"
```

## FYIs
It is difficult to test this at scale on a free google API account due to rate limiting.  
Sometimes websites block the programmatic download of images for security reasons. An enhancement to this program could be to check for that and fetch a new image in its place.
