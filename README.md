# ML API-SERVICES

This is the source code to run api-services server

## **Structure of project**
| Services           | Description                                         | branch deploy |       Status       |
|:-------------------|:----------------------------------------------------|---------------|:------------------:|
| api-services       | manage router and coordinator to celery             | main          | :heavy_check_mark: |
| celery             | is a open source which support asynchronous         | main          | :heavy_check_mark: |
| flower             | task manager from Queue which create from API's     | main          | :heavy_check_mark: |
| nginx              | Load balancer that support serving model            | v2            | :heavy_check_mark: |
| tensorflow-serving | Serving model to host server                        | v2            | :heavy_check_mark: |
| System logs        | Logs anything happend under system which make error | v2            | :heavy_check_mark: |
| Storage logs       | Logs anything which people upload to server         | v2            | :heavy_check_mark: |



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

### Load balancer
1. Nginx: Supporting when many requests sent to web server, it helps consume and balancing that helps system not crash (over memory/CPU)
   1. Protocol can we using 
      1. HTTP/HTTPs
      2. gRPCs
   
2. Haproxy: a frame work support reverse proxy and load balancer 

### Serving machine learning model 
1. Tensorflow serving apis: This is the framework of google which support serve model with "saved_model format" you need convert model to standard format when we use

*Note*: 
- you can use "saved_model_cli" to check your model is a good format when you serve to production  
- Tensorflow-serving-apis support 2 protocol to communicate such "HTTP:8501" and "gRPCs:8501"
- ***In this project I create 2 replicas (from tf_serve services) to serve model that why i need nginx to loadbalancer to process model***

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

3. **Nginx**

> xx.xx.xx.xx:4000

4. **TF-serving**

> HTTP: xx.xx.xx.xx: 8501

> gRPCs: xx.xx.xx.xx: 8500

*Note* 
- You can access from your area to tf-serving server beacause i'm not public port of container which contain serving servies to your local area

## How to see the log 

1. APIs logs: See at folder ***system_logs/api-services-logs/*** 
2. Worker logs: See at folder ***system_logs/celery-logs/***

## How to see the storages

Please see at: /system_storages/

## To do in future
- [ ] Replace Redis_broker to RabbitMQ
- [x] Display CPU consumer with task or event 
- [ ] Deloy OCR model 
- [ ] Combine Flower with Prometheus metrics 
- [ ] Combine Prometheus metrics to Grafana monitoring

<hr>

License
Copyright (c) [2022] [Nguyễn Thái Học <nguyenthaihoc1996@outllok.com>]

