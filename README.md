# ML API-SERVICES

This is the source code to run api-services server

## **Structure of project**
1. api-services
2. celery-worker
3. flower

## Detail each component

### api-services
1. FastAPI: web framework for developing RESTfullAPIs 
2. Uvicorn: ASGI web server
3. Background Tasks: it is a function (or services of fastapi) used for the task that has consumer long time
4. AsyncIO function (Task producer)

````
Some document:
 - https://fastapi.tiangolo.com/tutorial/background-tasks/
 - https://leimao.github.io/blog/Python-Concurrency-High-Level/
````

### celery-worker
1. Celery: The framework that support asynchronous task queue or job queue
2. Pool-config
3. Logger in celery
4. Task consumer

### flower
1. Flower: web tools which monitoring Celery Tasks / Events (Manage Tasks or Events)

### Other knowledge
1. Redis broker 
2. Redis database
3. Logging file

## How to run 

Run to follow the code 

> docker compose up -d --build

## How to use 

1. **API docs**

> xxxx.xxxx.xxxx.xxxx:8081/api/docs

2. **Tasks Management**

> xxxx.xxxx.xxxx.xxxx:5555

## How to see the log 

1. APIs logs: See at folder ***system_logs/api-services-logs/*** 
2. Worker logs: See at folder ***system_logs/celery-logs/***

## How to see the storages

Please see at: /system_storages/

## To do in future
- [ ] Replace Redis_broker to RabbitMQ
- [ ] Display CPU consumer with task or event 
- [ ] Deloy OCR model 
- [ ] Combine Flower with Prometheus metrics 
- [ ] Combine Prometheus metrics to Grafana monitoring

<hr>

License
Copyright (c) [2022] [Nguyễn Thái Học <nguyenthaihoc1996@outllok.com>]

