# url-shortener
This is a URL shortener service for UvA project. There are three microservices in the system, which is *api-service*, *authenticator-service*, and *database*. The users need to provide a valid access token in the HTTP Authorization header when requesting every API in *api-service*, which the access token can be obtained through the *authenticator-service*. Both *api-service* and *authenticator-service* would access *database* to store and load the user information and the short and full URL mapping.

# Project Layout

We provide two deployments methods for the URL shortener project. The first one is on **Docker**. The second one is on **Kubernetes**. The source code of url-shortener project is under `url-shortener/url-shortener/` directory. The deployment script for Docker (assignment 3.1) is under `url-shortener/deployment/docker` directory, and the deployment script for Kubernetes (assignment 3.2) is under `url-shortener/deployment/kubernetes` directory. Below is the rough directory layout of our project.

```
url-shortener/
  README.md
  .github/                # The github workflow action. Build and push the docker image when commit.
  
  deployment/
    docker/               # Contain the script to deploy url-shortener on Docker (assignment 3.1).
    kubernetes/           # Contain the Ansible script to deploy Kubernetes cluster and
                          # depoly url-shortener on Kubernetes. (assignment 3.2).
                          
  url-shortener/          # Contain the common source that would be used in both docker and kubernetes. 
    api/                  # The source code of api-service, including Dockerfile.
    authenenticator/      # The source code of authenticator-service, including Dockerfile.
    db/                   # The Dockerfile of database.
    
```

# Getting Started

## Docker

>Get started with URL Shortener on Docker

### Prerequisite

- **Install Docker engine and Docker compose**

  The easiest way is to install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/), which includes Docker Compose along with Docker Engine and Docker CLI.

### Install

To install url-shortener service, follow the below steps:

1. **Clone the url-shortener repository**

   ```
   git clone https://github.com/Vishwamitra/url-shortner.git
   ```

2. **Deploy and run url-shortener service on Docker**

   ```bash
   bash url-shortener/deployment/docker/run.sh
   ```

### Usage

See and interact with RESTful APIs on **http://127.0.0.1:5001/apidocs/** for *api-service* and **http://127.0.0.1:5002/users/apidocs/** for *authenticator-service*.

## Kubernetes

>Get started with URL Shortener on Kuberentes

### Prerequisite

- **Prepare target machines for Kubernetes Cluster**

  Prepare at least two target machines with **Debian 11** operating system **X86_64** architecutre. The target machines need to have at least 2 CPU and 4 Gi memory.

  >The deployment of Kubernetes cluster might fail under other environments.

- **Prepare one host as Ansible node**

  Please follow the step in [Ansible documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) to install Ansible on the node that is able to connect with target machines. Choose one of the targe machines as the Ansible node is also acceptable.

- **Enable SSH connection on target machines**

  The ansible node communicate with target machines through SSH connection. Therefore, the target machines need to enable SSH connection.

### Install

To install url-shortener service, follow the below steps:

1. **Clone the url-shortener repository**

   Clone the project on the Ansible node.

   ```bash
   git clone https://github.com/Vishwamitra/url-shortner.git
   ```

2. **Configure inventory file**

   Modify the target machines information in `url-shortener/deployment/kubernetes/ansible/hosts`. This allow Ansible node to connect with the target machines.

   ```ini
   [master]
   k8s-master ansible_host=145.100.135.169 ansible_user=student169 ansible_password=passwd
   
   [worker]
   k8s-worker1 ansible_host=145.100.135.170 ansible_user=student170 ansible_password=passwd
   k8s-worker2 ansible_host=145.100.135.171 ansible_user=student171 ansible_password=passwd
   ```

   You only have to modify **ansible_host**, **ansible_user**, and **ansible_password** these three field. Do not change other parts. To note that the provided ansible_user must be sudo user.

3. **Deploy and run url-shortener service on Kubernetes**

   ```bash
   bash url-shortener/deployment/kubernetes/run.sh
   ```

### Usage

Before access our service, add the mapping of **snv.io** to one of your target machines IP address in `/etc/hosts` files.

```bash
# The example record of /etc/hosts file #
145.100.135.169 snv.io
```

After adding the mapping, see and interact with RESTful APIs on **http://snv.io:32080/apidocs/** for *api-service* and **http://snv.io:32080/users/apidocs/** for *authenticator-service*.



# Development

## Docker

- **Environment variable configuration**

If you want your url-shortener service run on different port, configure the environment variable in `url-shortener/url-shortener/.env` file. Also, you can modify the database password, the base URL, and the lifespan of access token in this file. The default configuration is shown as below.

```ini
DATABASE_NAME=url_shortener
DATABASE_USER=postgresadmin
DATABASE_PASSWORD=admin123
DATABASE_PORT=5432

API_PORT=5001
API_DEBUG=True
BASE_URL_FOR_SHORT_URL=https://snv.io

AUTHENTICATOR_PORT=5002
AUTHENTICATOR_DEBUG=True
ACCESS_TOKEN_LIFESPAN=3600
```

## Kuberenetes

- **Deploy parital services**

  If you only want to deploy parital service instead of all services, you can control it by configure `url-shortener/deployment/kubernetes/ansible/taglist` file

  ```
  [v] k8s
  [v] monitor-service
  [v] infra-service
  [v] app-service
  ```

  - **k8s**: Deploy **Kubernetes cluster**.
  - **monitor-service**: Deploy **k9s** on master node.
  - **infra-service**: Deploy **Calico**, **Ingress NGINX Controller**, and **Longhorn**.
  - **app-service**: Deploy **URL Shortener**, which include *api-service*, *authenticator-service*, and *database*.

  The default configuration is to deploy everything. For example, if you only want to deploy **k8s** and **monitor-service**. Just tick these two and cross others as below shown.

  ```
  [v] k8s
  [v] monitor-service
  [x] infra-service
  [x] app-service
  ```

- **URL Shortener Environment variable configuration**

  If you want to change the database username and password or the service domain name. Configure the variable in `url-shortner/deployment/kubernetes/ansible/roles/deploy-k8s-service/files/app-service/url-shortener/config.ini`.

  ```ini
  [SERVICE-CONFIG]
    HELM_TEMPLATE_PATH="helm/url-shortener/"
    SERVICE_NAME="url-shortener"
    SERVICE_NAMESPACE="url-shortener"
    DOMAIN_NAME="snv.io"
  
  [POSTGRESQL-CONFIG]
    POSTGRESQL_USER="postgresadmin"
    POSTGRESQL_PASSWORD="admin123"
  ```

- **Other configuration**

  In fact, all of our the service deployment is managed through [Helm Charts](https://helm.sh). Therefore, more configurable value can be found in the `values.yaml` file in the helm charts of each services. For example, you can configure the number of replica of url-shortener pod in `url-shortner/deployment/kubernetes/ansible/roles/deploy-k8s-service/files/app-service/url-shortener/helm/url-shortener/values.yaml` file. The detail directory layout of our project is shown below.

  ```
  url-shortener/
    README.md
    .github/                               # The github workflow action. Build and push                                                                # The docker image when commit.
    
    url-shortener/                         # Contain the common source that would 
                                           # be used in both docker and kubernetes.
                                          
    deployment/                            
      docker/                              # Contain the script to deploy url-shortener 
                                           # on Docker (assignment 3.1).
      kubernetes/                          # Contain the Ansible script to deploy Kubernetes cluster and
                                           # depoly url-shortener on Kubernetes. (assignment 3.2).
        run.sh
        taglist                  
        ansible/
          hosts                            # The inventory file for target machine
          playbook.yaml
          roles/
            ansible-init/                  # Init connection between target machine and
                                           # ansible node.
            helm/                          # Install Helm on master node.
  
            docker/                        # Install Docker Engine on all machines.
  
            k8s-install/                   # Install kubeadm, kubelet, kubectl on all machines.
  
            k8s-master-init/               # Init master node.
  
            k8s-worker-init/               # Join k8s cluster.
  
            deploy-k8s-service/            # Deploy service on k8s.
              tasks/
              files/
                app-services/              # Contains the helm charts and deploy script of app-services.
                  url-shortener/
                    helm/                  # Helm chart of url-shortener.
                      url-shortener/      
                        charts/
                        templates/
                        Chart.yaml
                        values.yaml        # Configure more values in this file.
                    config.ini
                    deploy.sh
                    uninstall.sh
  
                infra-services/
                  calico/
                    helm/                  # Helm chart of calico.
                  ingress-nginx/
                    helm/                  # Helm chart of calico.
                  longhorn/
                    helm/                  # Helm chart of longhorn.
  
                monitor-service/
                  k9s/
  ```
  
  

# Reference

- Our application refer to [this structure](https://auth0.com/blog/best-practices-for-flask-api-development/), as we consider it as properly structure.

- The error handle of our application for 400 and 404 exceptions refer to [Blueprint Error Handlers](https://flask.palletsprojects.com/en/2.2.x/errorhandling/#blueprint-error-handlers) in Flask official document.

- The token signature refer to [rsa-sign-verify-example](https://cryptobook.nakov.com/digital-signatures/rsa-sign-verify-examples)
