# wcofun-dl
wcofun-dl is a python script wrapped in a docker container 
with all of the needed dependencies that can scrape and download 
videos from the website wcofun.net. It can be easily ran in
the provided Docker container by pulling the image:

`docker pull ghcr.io/gssparks/wcofun-dl:main`

and then running the following command:

`docker run -it -v "$(pwd)":/downloads wcofun-dl [script arguments]`

The accepted arguments are:
```
usage: wcofun-dl.py [-h] [-d] [--batch] URL

Downloads media from wcofun.net

positional arguments:
  URL         <Required> url link

optional arguments:
  -h, --help  show this help message and exit
  -d          Downloads videos
  --batch     Run using a batch of urls.
```
