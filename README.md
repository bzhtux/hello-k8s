```
 _   _      _ _             _  _____ ____  
| | | | ___| | | ___       | |/ ( _ ) ___| 
| |_| |/ _ \ | |/ _ \ _____| ' // _ \___ \ 
|  _  |  __/ | | (_) |_____| . \ (_) |__) |
|_| |_|\___|_|_|\___/      |_|\_\___/____/ 
                                           
```

Hello-k8s is a simple 3 tiers Python app to help learning how kubernetes works and to understand kubernetes key objects. 

# Python app

Hello-k8s is a 3 tiers application with a frontend an API for core actions and REDIS to store messages.

```shell
+--------------------+
| hello-k8s-frontend |
+--------------------+
	|
	|
  +---------------+
  | hello-k8s-api |
  +---------------+
	|
	|
     +-------+
     | redis |
     +-------+
```

To run, the application need to grab some environment variables for its configuration otherwise it use default values.

```python
import os

######################
### HELLO-K8S-FRONTEND  # noqa
######################
try:
    HKF_DEBUG = os.environ['HKF_DEBUG']
except KeyError:
    HKF_DEBUG = False

try:
    HKF_HOST = os.environ['HKF_HOST']
except KeyError:
    HKF_HOST = "0.0.0.0"

try:
    HKF_PORT = os.environ['HKF_PORT']
except KeyError:
    HKF_PORT = 8080
MAX_MSG_GET = 10


#######
### API  # noqa
#######
try:
    API_HOST = os.environ['API_HOST']
except KeyError:
    API_HOST = "0.0.0.0"

try:
    API_PORT = int(os.environ['API_PORT'])
except KeyError:
    API_PORT = 5000
```

`API_HOST` and `API_PORT` will be defined in k8s manifest as environment variables and hello-k8s-frontend will be able to use them to connect to API.

# k8s

## cluster deployment with GKE

First set your project with `gcloud` :

```shell
$ gcloud config set project [PROJECT_ID]
```

Set a region for your cluster:

```shell
$ gcloud config set compute/zone europe-west1-c
```

Then create a kubernetes cluster:

```shell
$ gcloud container clusters create hello-k8s --num-nodes=3
```

To authenticate for the new cluster:

```shell
$ gcloud container clusters get-credentials hello-k8s
```

You can verify you are logged in with to new cluster:

```shell
$ kubectl config current-context
gke_xxx-yyy-zzz-bzhtux_europe-west1-c_hello-k8s
```

Now create a namespace for this demo:

```shell
$ kubectl delete namespace demo
```

Now you can define a new context using this namespace. To do so, you need some informations that can be retrieved with this command:

```shell
$ kubectl config view
```

or 

```shell
$ kubectl config current-context
```

Define a new context named demo:

```shell
$ kubectl config set-context demo --namespace=demo --cluster=<YOUR CURRENT CLUSTER NAME> --user=<YOUR CURRENT CLUSTER NAME>
```

Now your context is set to demo:

```shell
$ kubectl config current-context
demo
```


## Services

Each app will be exposed to others using a service. A service is a abstraction wich define  a logical set of pods using selectors (mainly). A best practice is to start deploying services before deployments.

You can have a look at the frontend service file:

```yaml
$ cat 06-frontend-service.yml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  labels:
    app: hello-k8s
    tier: frontend
spec:
  # if your cluster supports it, uncomment the following to automatically create
  # an external load-balanced IP for the frontend service.
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: hello-k8s
    tier: frontend
```

 * `kind`: This k8s object is a `Service`
 * `type`:  LoadBalancer to use a GCP load balancer or other Iaas specific LBs
 * `selector.app` is the given name for the deployment app (here frontend as mentioned in the k8s/03-frontend-deployment.yml file)
 * `ports.port` is the exposed port
 * `port.targetPort` is the istening port of the deployment (HKF_PORT)

Create all the services (redis, api and frontend): 

```shell
$ kubectl create -f k8s/02-redis-service.yml
$ kubectl create -f k8s/04-api-service.yml
$ kubectl create -f k8s/06-frontend-service.yml
```

You can verify your servies with:

```shell
$ kubectl get services
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)        AGE
api        ClusterIP      10.51.252.49    <none>           5000/TCP       48m
frontend   LoadBalancer   10.51.243.159   <pending>        80:30580/TCP   48m
redis      ClusterIP      10.51.241.45    <none>           6379/TCP       49m
```


## Deployments

When services are successfully deployed, you can create deployments for redis, api and frontend. But before just take a look at `k8s/05-frontend-deployment.yml` that create a deployment for the frontend application:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: hello-k8s
        tier: frontend
    spec:
      containers:
      - name: hello-k8s-frontend
        image: bzhtux/hello-k8s-frontend:0.0.8
        imagePullPolicy: Always
        env:
          - name: GET_HOSTS_FROM
            value: env
          - name: FLASK_ENV
            value: dev
          - name: API_HOST
            value: api
          - name: API_PORT
            value: '5000'
          - name: HKF_PORT
            value: '8080'
        ports:
        - containerPort: 8080
```

 * `replicas` define the number of instances to run
 * `labels.app` define the application's name (used by selectors for example)
 * `env` all environment variables required by the application
 * `API_HOST` and `API_PORT` will be used by application to connect to API
 * `HKF_PORT` is used by the application and `containerPort` is use by kubernetes, but it must be the same value.

You can create deployments using `k8s/*deployment.yml` files:

```shell
$ kubectl create -f k8s/01-redis-deployment.yml
$ kubectl create -f k8s/03-api-deployment.yml
$ kubectl create -f k8s/05-frontend-deployment.yml
```

You can get pods informations:

```shell
$ kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
api-7f665ddd4f-kntnx        1/1     Running   0          9m
frontend-6bcd76b6df-2f8sw   1/1     Running   0          9m
redis-5c998bd8d8-tkhhs      1/1     Running   0          35m
```

Now to use hello-k8s get the LoadBalancer IP:

```shell
$ kubectl get services frontend
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)        AGE
frontend   LoadBalancer   10.51.245.190   130.211.52.149   80:32521/TCP   37m
```

Open your browser to `http://130.211.52.149` and leave a kind message ;-)

## Limits and Requests

Request is what a container is guarantee to get and limit ensure usage never go above its value. For example if your nodes provide a 3,4 G of memory you can't request for more otherwise container will never start.

Let's try to set requests and limits that shouldn't let the application to work correctly:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: hello-k8s
        tier: frontend
    spec:
      containers:
      - name: hello-k8s-frontend
        image: bzhtux/hello-k8s-frontend:0.0.12
        imagePullPolicy: Always
        resources:
          requests:
            cpu: 1m
            memory: 10Mi
          limits:
            cpu: 10m
            memory: 100Mi
        env:
          - name: GET_HOSTS_FROM
            value: env
          - name: FLASK_ENV
            value: dev
          - name: API_HOST
            value: api
          - name: API_PORT
            value: '5000'
          - name: HKF_PORT
            value: '8080'
        ports:
        - containerPort: 8080
```

This mean that you request 1 mili CPU and 100M of memory and you are limited by 10 milmi CPU and 100M of memory. Apply this new configuration:

```shell
$ kubectl apply k8s/07-fake-requests-limits.yml
```

Now see how the application works under load testing. Run siege to perform a load testing:

```shell
$ siege -d1S -c255 -t10S http://130.211.52.149/
[...]
Lifting the server siege...
Transactions:		          16 hits
Availability:		       35.56 %
Elapsed time:		        9.98 secs
Data transferred:	        0.19 MB
Response time:		        3.54 secs
Transaction rate:	        1.60 trans/sec
Throughput:		        0.02 MB/sec
Concurrency:		        5.67
Successful transactions:          16
Failed transactions:	          29
Longest transaction:	        9.80
Shortest transaction:	        0.00
```

Availability is 35% so that mean the application need more resources than it can have currently. Let set better requests and limits for this application:

```shell
$ kubectl apply -f k8s/08-limits-requests.yml
```

Re run the load testing and observe the application behavior:

```shell
$ siege -d1S -c255 -t10S http://130.211.52.149/
[...]
Lifting the server siege...
Transactions:		         552 hits
Availability:		      100.00 %
Elapsed time:		        9.93 secs
Data transferred:	        5.57 MB
Response time:		        3.25 secs
Transaction rate:	       55.59 trans/sec
Throughput:		        0.56 MB/sec
Concurrency:		      180.90
Successful transactions:         552
Failed transactions:	           0
Longest transaction:	        9.18
Shortest transaction:	        0.24
```

Now availability is 100%, the application can use enough resources as required.

## Persistent disks

Frontend and API are stateless applications but REDIS is not and require a persistent disk to keep its data if redis container dies. Add some message to hello-k8s and then delete the redis deployment and re create it:

```shell
$ kubectl delete -f k8s/01-redis-deployment.yml
$ kubectl create -f k8s/01-redis-deployment.yml
```

Go back to the web interface, all the mesages have disappeared ! If you want to avoid such a behavior you have to use persistent disk for the redis pod.

You can take a look at the `k8s/09-redis-with-pv.yml` :

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
spec:
  serviceName: redis
  selector:
    matchLabels:
      app: redis
  replicas: 1
  template:
    metadata:
      labels:
        app: redis
        tier: backend
    spec:
      containers:
      - name: redis
        image: redis
        ports:
        - containerPort: 6379
          name: redis
        volumeMounts:
        - mountPath: "/data"
          name: redis-pv-claim
  volumeClaimTemplates:
  - metadata:
      name: redis-pv-claim
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 3Gi
```

* `kind` define as a statefulset instead of deployment
* `volumeMounts` define mount point inside the container here redis store its data in `/data` directory
* `volumeMounts.name` should be the same as `volumeClaimTemplates.metadata.name`
* `accessModes` RW access from only one instance not a share volume.
* `requests.storage` define the volume size, here 3G

Now remove redis deployment and add redis statefulset:

```shell
$ kubectl delete -f k8s/01-redis-deployment.yml
$ kubectl create -f k8s/09-redis-with-pv.yml
$ kubectl get pods -w -l app=redis
NAME      READY   STATUS              RESTARTS   AGE
redis-0   0/1     ContainerCreating   0          10s
redis-0   1/1   Running   0     11s
```

Now go back to the web interface, add some messages and delete the redis pod:

```shell
$ kubectl delete pod -l app=redis
$ kubectl get pods -w -l app=redis
redis-0   1/1   Terminating   0     11m
redis-0   0/1   Terminating   0     11m
redis-0   0/1   Terminating   0     11m
redis-0   0/1   Terminating   0     11m
redis-0   0/1   Pending   0     0s
redis-0   0/1   Pending   0     0s
redis-0   0/1   ContainerCreating   0     0s
redis-0   1/1   Running   0     11s
```

Go back to the web interface, you can see your messages.

From the event view you can see that when the pod is deleted the volume is detached and then attached to the new pod:

```shell
Normal   SuccessfulAttachVolume   Pod   AttachVolume.Attach succeeded for volume "pvc-dd3fe58c-5ded-11e9-8cd1-42010a84001d"
```

## Liveness & readiness

### Liveness

At some point you may want high availability for your application and kubernetes can help with `liveness`. `LivenessProbe` with `httpGet` can perform a health check against your application. For example you may define a new route in your application `/healthz` and use this URI with `livenessProbe`:

```yaml
...
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 3
          periodSeconds: 15
...
```

 * `path` : define the URI to check
 * `port` : define the listening port of your application
 * `initialDelaySeconds` tells k8s to wait N sec before performing the first check
 * `periodSeconds` tells k8s to wait N sec before next check

 
### Readiness
 
 For any reasons your application may load a huge amount of data at startup, `readinessProbe` can help user experience. Kubernetes will route traffic to the new pods only when readiness is successful:
 
 ```yaml
 ...
         readinessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 3
          periodSeconds: 15
 ...
 ```
 
The key for readiness are the same as liveness.

As an example if `livenessProbe.httpGet.path` check result in another status code than 200, after 3 checks the pod will be killed because unhealthy.

To see a demo, run the following command:

```shell
$ kubectl apply -f k8s/12-api-liveness-404.yml
```

See now what is happening:

```shell
$ kubectl get events -w
...
0s    Warning   Unhealthy   Pod   Liveness probe failed: HTTP probe failed with statuscode: 404
0s    Warning   Unhealthy   Pod   Liveness probe failed: HTTP probe failed with statuscode: 404
0s    Warning   Unhealthy   Pod   Liveness probe failed: HTTP probe failed with statuscode: 404
0s    Normal   Killing   Pod   Container hello-k8s-api failed liveness probe, will be restarted
0s    Normal   Pulling   Pod   Pulling image "bzhtux/hello-k8s-api:0.0.9"
...
```

To restore a valid path for api, run the following command:

```shell
$ kubectl apply -f k8s/11-api-liveness.yml
```