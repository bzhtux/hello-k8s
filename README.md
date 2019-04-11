```
 _   _      _ _             _  _____ ____  
| | | | ___| | | ___       | |/ ( _ ) ___| 
| |_| |/ _ \ | |/ _ \ _____| ' // _ \___ \ 
|  _  |  __/ | | (_) |_____| . \ (_) |__) |
|_| |_|\___|_|_|\___/      |_|\_\___/____/ 
                                           
```

Hello-k8s is a simple Python app using REDIS learn how kubernetes works and to understand kubernetes key objects.

# Python app

Hello-k8s is a 3 tiers application with a frontend to server webUI, and API to interact with REDIS and REDIS to store messages.

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

The most important thing for this application to run is to catch environment variables for its configuration:

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

`API_HOST` and `API_PORT` will be defined in k8s manifest as environment variables for hello-k8s-frontend to use them to connect to API.

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
gke_cso-pcfs-emea-bzhtux_europe-west1-c_hello-k8s
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

```shell
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
 * `selector.app` is the given name for the deployment app (here redis as mentioned in the k8s/01-redis-deployment.yml file)
 * `ports.port` is the exposed port
 * `port.targetPort` is the istening port of the deployment (pods)

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

Now services are deployed, you can create deployments for redis, api and frontend. But before just take a look at `k8s/05-frontend-deployment.yml` that create a deployment for the frontend application:

```shell
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

You can create deployments using `k8s/*deployment.yml`:

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
frontend   LoadBalancer   10.51.245.190   130.211.51.142   80:32521/TCP   37m
```

Open your browser to `http://130.211.51.142` and leave a kind message ;-)