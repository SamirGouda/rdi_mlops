# SERVER

## ABOUT PROJECT
### API server for COVID19 detection
* server is found on [flask_api.py](flask_api.py)
* deploy to cloud was done on [https://www.heroku.com/](https://www.heroku.com/) since it supports CD 
* CI is achieved using some github actions in [./github/workflows](./github/workflows)

## SERVER ENDPOINTS
server has 2 endpoints
* alive
used to verifiy server is up or down
* predict
used to predict images, returns json file with COVID19 and NORMAL as keys and their probabilities as values

## REQUESTS
curl
* alive
```sh
curl -X 'GET' ''
```
* predict
```sh
curl -X POST -F file=@"$$file" /predict
```
