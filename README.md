# BACK-END 
### To run project locally

**Firstly:** 
Clone the repository 

Command:
```
git clone https://github.com/VasyaMamchur/Back-end.git
```
Next, you need to go to the project folder.

**Secondly:** 
Build an image

Run Docker

Command:
```
docker build . -t <image_name>:latest
```

**Thirdly:**
You must check if the application works

Command:
```
docker run -it --rm --network=host <image_name>:latest
```

**Finally:**
Install docker-compose and try to build and run the container using commands:
```
docker-compose build
docker-compose up
```