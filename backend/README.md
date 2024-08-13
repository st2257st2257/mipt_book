# Naletay backend

Python

To launch python project in docker:
```
cd djangoproject
docker run --rm -v ./:/usr/src/app -p 8000:8000 -it $(docker build -q .)
```
