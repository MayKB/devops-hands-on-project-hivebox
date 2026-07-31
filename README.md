[![Dynamic DevOps Roadmap](https://img.shields.io/badge/Dynamic_DevOps_Roadmap-559e11?style=for-the-badge&logo=Vercel&logoColor=white)](https://devopsroadmap.io/getting-started/)
[![Community](https://img.shields.io/badge/Join_Community-%23FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://newsletter.devopsroadmap.io/subscribe)
[![Telegram Group](https://img.shields.io/badge/Telegram_Group-%232ca5e0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/DevOpsHive/985)
[![Fork on GitHub](https://img.shields.io/badge/Fork_On_GitHub-%2336465D?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox/fork)

# HiveBox - DevOps End-to-End Hands-On Project

<p align="center">
  <a href="https://devopsroadmap.io/projects/hivebox" style="display: block; padding: .5em 0; text-align: center;">
    <img alt="HiveBox - DevOps End-to-End Hands-On Project" border="0" width="90%" src="https://devopsroadmap.io/img/projects/hivebox-devops-end-to-end-project.png" />
  </a>
</p>

> [!CAUTION]
> **[Fork](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox/fork)** this repo, and create PRs in your fork, **NOT** in this repo!

> [!TIP]
> If you are looking for the full roadmap, including this project, go back to the [getting started](https://devopsroadmap.io/getting-started) page.

This repository is the starting point for [HiveBox](https://devopsroadmap.io/projects/hivebox/), the end-to-end hands-on project.

You can fork this repository and start implementing the [HiveBox](https://devopsroadmap.io/projects/hivebox/) project. HiveBox project follows the same Dynamic MVP-style mindset used in the [roadmap](https://devopsroadmap.io/).

The project aims to cover the whole Software Development Life Cycle (SDLC). That means each phase will cover all aspects of DevOps, such as planning, coding, containers, testing, continuous integration, continuous delivery, infrastructure, etc.

Happy DevOpsing ♾️

## Before you start

Here is a pre-start checklist:

- ⭐ <a target="_blank" href="https://github.com/DevOpsHiveHQ/dynamic-devops-roadmap">Star the **roadmap** repo</a> on GitHub for better visibility.
- ✉️ <a target="_blank" href="https://newsletter.devopsroadmap.io/subscribe">Join the community</a> for the project community activities, which include mentorship, job posting, online meetings, workshops, career tips and tricks, and more.
- 🌐 <a target="_blank" href="https://t.me/DevOpsHive/985">Join the Telegram group</a> for interactive communication.

## Preparation

- [Create GitHub account](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) (if you don't have one), then [fork this repository](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox/fork) and start from there.
- [Create GitHub project board](https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project) for this repository (use `Kanban` template).
- Each phase should be presented as a pull request against the `main` branch. Don’t push directly to the main branch!
- Document as you go. Always assume that someone else will read your project at any phase.
- You can get senseBox IDs by checking the [openSenseMap](https://opensensemap.org/) website. Use 3 senseBox IDs close to each other (you can use the following [5eba5fbad46fb8001b799786](https://opensensemap.org/explore/5eba5fbad46fb8001b799786), [5c21ff8f919bf8001adf2488](https://opensensemap.org/explore/5c21ff8f919bf8001adf2488), and [5ade1acf223bd80019a1011c](https://opensensemap.org/explore/5ade1acf223bd80019a1011c)). Just copy the IDs, you will need them in the next steps.

<br/>
<p align="center">
  <a href="https://devopsroadmap.io/projects/hivebox/" imageanchor="1">
    <img src="https://img.shields.io/badge/Get_Started_Now-559e11?style=for-the-badge&logo=Vercel&logoColor=white" />
  </a><br/>
</p>

---

## Implementation

### Description

This is a simple app that will be built upon as the HiveBox project is completed over time.
In its current state, three endpoints can be accessed using Flask.
- **/temperature:** Gets the average temperature of three SenseBoxes
- **/version:** Gets the current version of the project on GitHub
- **/metrics:** Gets Prometheus metrics about the app

### Prerequisites

- Docker
- kind
- kubectl
- GitHub Container Registry
- curl

### Preparation

- Clone the repository by opening a terminal and running `git clone https://github.com/MayKB/devops-hands-on-project-hivebox.git`
- Make sure Docker is running and has Kubernetes enabled
  - If using WSL, make sure `Enable integration with my default WSL distro` is set in Settings > Resources > WSL integration
- Create a file called `.env` in the project root, and input three SenseBox IDs using the following format:
````
SENSEBOX_ID_1=5eba5fbad46fb8001b799786
SENSEBOX_ID_2=5c21ff8f919bf8001adf2488
SENSEBOX_ID_3=5ade1acf223bd80019a1011c
````

### Local Execution

- To create a kind cluster, run `kind create cluster`
- Make sure you are using the correct context by running `kubectl config use-context kind-kind`.
- Install cloud-provider-kind, which will emulate a cloud connection, start by running `VERSION="$(basename $(curl -s -L -o /dev/null -w '%{url_effective}' https://github.com/kubernetes-sigs/cloud-provider-kind/releases/latest))"`
  - If you are using a proper Linux distribution, run `docker run -d --name cloud-provider-kind --rm --network host -v /var/run/docker.sock:/var/run/docker.sock registry.k8s.io/cloud-provider-kind/cloud-controller-manager:${VERSION}`
  - If you are on a Mac or using WSL 2, run `sudo docker run -d --name cloud-provider-kind --privileged --rm --network host -v /var/run/docker.sock:/var/run/docker.sock registry.k8s.io/cloud-provider-kind/cloud-controller-manager:${VERSION} --enable-lb-port-mapping` and enter your password if prompted
- Verify that cloud-provider-kind is running with `docker ps --filter name=cloud-provider-kind`. You can also check the logs with `docker logs cloud-provider-kind`
- Apply the cloud-provider-kind manifest file with `kubectl apply -f .k8s/base/deploy-cloud.yaml`
- Verify the gateway was created properly by running `kubectl get gateway -n gateway-infra gateway`. Look for `PROGRAMMED: True` to confirm.
- To build the image, navigate to the project folder and run `docker build -t <image name> .`
- Tag the image using `docker tag <image name> ghcr.io/<lowercase github username/org name>/<image name>:local-test`
- Push to GitHub Container Registry using `docker push ghcr.io/<lowercase github username/org name>/<image name>:local-test`
- Update `.k8s/base/deploy-app.yaml` to use `image: ghcr.io/<lowercase github username/org name>/<image name>:placeholder`
- Update `.k8s/overlays/dev/kustomization.yaml` to use `name: ghcr.io/<lowercase github username/org name>/<image name>`
- Apply the app deploy manifest file with `kubectl apply -k .k8s/overlays/dev/`
- Apply your env variables as a configmap using `kubectl create configmap hivebox-config --from-env-file=.env -n hivebox-namespace`
- Create a secret to allow you to pull from the registry by running
````
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<username> \
  --docker-password=<token> \
  -n hivebox-namespace
````
- Apply the http routing manifest file with `kubectl apply -f .k8s/base/http-route.yaml`
- Test the application with `curl`
  - If using a proper linux distribution, run `GW_ADDR=$(kubectl get gateway -n gateway-infra gateway -o jsonpath='{.status.addresses[0].value}')` to set the IP address, then run `curl --resolve some.exampledomain.example:80:${GW_ADDR}/metrics http://some.exampledomain.example` to test the `/metrics` endpoint. The same can be done for `/version` and `/temperature`.
  - If using WSL2, first find the ephemeral port by running `docker ps` then finding the `0.0.0.0:<ephemeral port>->80/tcp` address that belongs to the `envoyproxy/envoy` image. Then test the `metrics` endpoint with `curl -v --max-time 15 -H "Host: some.exampledomain.example" http://localhost:<port>/metrics`. The same can be done for `/version` and `/temperature`. It may take up to a minute for it to start connecting properly, so if you get an error give it some time before trying again.

### Cleanup

- Start by deleting the namespaces and their resources with
````
kubectl delete namespace gateway-infra
kubectl delete namespace hivebox-namespace
````
- Stop and remove cloud-provider-kind with `docker stop cloud-provider-kind`
- Delete the kind cluster with `kind delete cluster`

### Troubleshooting

- If you get the error `Unable to find image 'registry.k8s.io/cloud-provider-kind/cloud-controller-manager:latest'` after running the `sudo docker run [...]` command, there may be an issue with the GitHub API. Run `curl -s -L -o /dev/null -w '%{http_code} %{url_effective}\n' https://github.com/kubernetes-sigs/cloud-provider-kind/releases/latest` until you get a `200` status response, then rerun the `sudo docker run [...]` command.
- If you get the error `error from registry: unauthorized` after running the `docker tag [...]` or `docker push [...]` commands, run `docker login ghcr.io` and log in to the GitHub Container Registry with your GitHub username and the same personal access token you will use in the `kubectl create secret [...]` command. This is a classic Personal Access Token that requires `delete:packages`, `repo` and `write:packages` permissions.