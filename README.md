# Laboratory work #3
## Варіант
Мамчур Василь ІО-12
12%3=0

Варіант:
Облік доходів - потрібно зробити сутність “рахунок” куди можна додавати гроші по мірі їх надходження(для кожного користувача свій) і звідти списуються кошти атоматично при створенні нової витрати. Логіка щодо заходу в мінус лишається на розсуд студентів(можете або дозволити це, або заборонити).

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