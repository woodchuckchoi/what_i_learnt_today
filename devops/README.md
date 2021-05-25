# 무중단 배포
* Rolling Deployment - 기존 서비스나 인스턴스를 하나씩 다음 Release로 변경\
장점: 현재 사용 가능한 자원을 그대로 사용하여 무중단 배포를 할 수 있다.\
단점: 가용 서버(Capacity)가 적어지며, 롤백을 해야하는 경우 같은 방식으로 롤백을 할 때도 같은 방식으로 작동하므로 시간이 오래 소요된다. Sticky Session과 같은 방법을 사용하지 않는다면 UX에 문제가 있을 수 있다.
* Blue/Green Deployment - 기존 서비스나 인스턴스(Blue)와 같은 수의 리소스에 다음 Release(Green)를 배포한 후 Load Balancer, Proxy 등을 사용하여 Traffic을 Green으로변경. Downtime이 없고 Capacity가 줄어들지 않는다는 장점이 있지만, 순간적으로 리소스가 2배로 필요하다는 단점이 있다.\
장점: Capacity가 그대로 유지되며, 그린 배포에 문제가 있다면 다시 블루에 연결만 해주면 된다.
단점: 클라우드나 K8S같은 가상환경이 아니라면 리소스를 두 배로 늘리는데 부담이 있다.
* Canary Deployment - A/B 테스트 같이 일부 리소스에만 다음 Release를 배포한 후 Traffic의 일부만 새로운 Release로 Forward하여 문제가 있는지 테스트 후, 전체에 새로운 Release를 배포

---

# Docker
컨테이너와 VM은 애플리케이션과 필요한 Dependency를 가상화하여 어디에서나 동작할 수 있도록 만든다는 공통점이 있다. 하지만 VM은 하이퍼바이저라는 '실제 컴퓨터의 리소스를 배정받은 가상의 컴퓨터' 위에서 동작하는 반면, 컨테이너는 Linux OS Level에서 지원하는 Namespace 기능을 통해서 동작한다. 따라서 부가적인 OS라는 Overhead가 없기 때문에 좀 더 가볍고, 사용하기 편리하다.

---

# Makefile
	Target: Prerequisite
		Recipe
의 형태를 띄는 파일로, 프로그램을 Source로부터 Compile하는데 사용된다.

---

# Ambiguous Commands in Git
```
	git reset --soft // index (commit status)와 working directory를 유지한 상태로 HEAD만 이전 commit으로 돌린다.
	git reset [--mixed] // working directory를 유지하고 HEAD와 index를 이전 commit으로 돌린다. git reset의 default behaviour.
	git reset --hard // HEAD, index, working directory 모두를 이전 commit으로 돌린다.

	git rebase <branch> // HEAD가 가리키는 Branch를 <branch>의 마지막 commit을 parent로 옮긴다.
	
	git cherry-pick <commit> // <commit>을 현재 HEAD의 child로 가져온다.
```

---

# Dockerfile & Docker-compose Miscellaneous Knowledge
1. ARG는 Dockerfile을 통해서 image를 구성할 때 사용한다.
2. Docker와 Docker-compose 모두 ENV를 구성할 수 있지만, 같은 Key가 존재하면 Docker-compose의 ENV가 priority를 가진다. (overrides dockerfile env)

---

# AWS IAM & Bucket Policy
AWS IAM Permission S3 Full Access는 S3 Bucket Policy에 자신의 계정이 등록되어 있지 않아도 접근 가능하다.\
S3 ACL에 Root 계정이 등록되어 있기 때문이다.\
AWS IAM의 Policy는 명시적으로 연결 가능하지 않으면 모두 DENY하는 정책을 사용한다.\
따라서 특정 S3 Bucket에만, 특정 Action을 할 때만 접근 가능하게 한다면 'Resource'는 해당 bucket에만, action을 특정해서 사용할 수 있다.\
단 Root 계정은 ACL에서 기본적으로 Read, Write가 가능하게 되어있으므로 만약 Root 계정도 통제하고 싶다면 이를 deactivate 한 후 Bucket Policy에 Role의 ARN을 추가하는 방식으로 사용한다.\
위의 방법을 통해서 Cross Account에도 접근 가능 권한을 줄 수 있다.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::AccountB:user/AccountBUserName"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::AccountABucketName/*"
            ]
        }
    ]
}
```

---

# Git stash and reset
1. git reset branch를 통해서 특정 commit으로 돌아갈 수 있다.
2. working directory에 local change가 있다면 git stash push "description"을 통해서 change를 저장하고, git stash apply (or pop)을 통해서 저장된 change를 현재의 commit에 반영한다.

---

# Building a container from scratches
Container is basically the combination of a namespace (what you can see) and a control group (what you can use).

```
	package main
	
	import (
		"fmt"
		"io/ioutil"
		"os"
		"os/exec"
		"path/filepath"
		"strconv"
		"syscall"
	)
	
	// go run main.go run <cmd> <args>
	func main() {
		switch os.Args[1] {
		case "run":
			run()
		case "child":
			child()
		default:
			panic("help")
		}
	}
	
	func run() {
		fmt.Printf("Running %v \n", os.Args[2:])
	
		cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
		cmd.Stdin = os.Stdin
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		cmd.SysProcAttr = &syscall.SysProcAttr{
			Cloneflags:   syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID | syscall.CLONE_NEWNS,
			Unshareflags: syscall.CLONE_NEWNS,
		}
	
		must(cmd.Run())
	}
	
	func child() {
		fmt.Printf("Running %v \n", os.Args[2:])
	
		cg()
	
		cmd := exec.Command(os.Args[2], os.Args[3:]...)
		cmd.Stdin = os.Stdin
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
	
		must(syscall.Sethostname([]byte("container")))
		must(syscall.Chroot("/home/liz/ubuntufs"))
		must(os.Chdir("/"))
		must(syscall.Mount("proc", "proc", "proc", 0, ""))
		must(syscall.Mount("thing", "mytemp", "tmpfs", 0, ""))
	
		must(cmd.Run())
	
		must(syscall.Unmount("proc", 0))
		must(syscall.Unmount("thing", 0))
	}
	
	func cg() {
		cgroups := "/sys/fs/cgroup/"
		pids := filepath.Join(cgroups, "pids")
		os.Mkdir(filepath.Join(pids, "liz"), 0755)
		must(ioutil.WriteFile(filepath.Join(pids, "liz/pids.max"), []byte("20"), 0700))
		// Removes the new cgroup in place after the container exits
		must(ioutil.WriteFile(filepath.Join(pids, "liz/notify_on_release"), []byte("1"), 0700))
		must(ioutil.WriteFile(filepath.Join(pids, "liz/cgroup.procs"), []byte(strconv.Itoa(os.Getpid())), 0700))
	}
	
	func must(err error) {
		if err != nil {
			panic(err)
		}
	}
```

# Docker's resource management
```
Containers and the host use the same kernel. Although the programs running in Docker can't see the host filesystem, only their own filesystem.

Unused files will sit on disk, only the used files will be loaded into memory.

Multiple containers using the same base image are capable of sharing resources. However they don't share files, hence each will have to load its own copy of the files they need. 

Docker uses AUFS, Union File System, which uses "copy on write". What it means is that, When you have multiple base images, those images take disk space, but when you run N containers from those images, there is no actual disk used. As it is copy-on-write, only modified files will take space on the host.
```

# Docker O'Reily
Docker는 UFS(union file system)을 이용한다. 여러 파일 시스템이 계층 구조로 마운트되어 하나의 파일 시스템처럼 사용할 수 있게 해준다.\
이미지의 파일 시스템은 읽기 전용 계층에 마운트되고, 실행 중인 컨테이너가 변경한 내용은 읽기-쓰기 계층에 쓰여진다.\
따라서 실행 중인 시스템에서 변경된 내용을 찾으려면 최상위 읽기-쓰기 계층만 참고하면 된다.

```
$ docker diff [container] # image와 비교해서 바뀐 파일 리스트 반환

$ docker logs [container] # container에서 실행한 모든 작업 내용 반환
```

Docker는 default로 unix domain socket을 사용하지만 tcp socket도 지원한다.

---

# Secret in Docker
당연하게도 Dockerfile 내에 (layer 안에) secret을 저장하는 건 최악의 방법이다. 누구든 컨테이너에 접근 권한만 있다면 secret을 가져갈 수 있으니까.\
이를 막기위해서 컨테이너의 시작 시점에 환경 변수로 secret을 전달하거나, secret이 포함된 volume을 컨테이너에 붙여서 secret을 전달하는게 일반적이다.\
하지만 가장 좋은 방법은 컨테이너가 다른 신뢰할 수 있는 웹 서버, vault 같은 key-value storage에서 필요한 secret을 가져오는 것이다.\
aws 같은 경우에는 ec2 instance의 특정 ip에는 built-in metadata server가 동작하고 있고, metadata를 통해서 role을 assume해서 secret을 받아 사용할 수 있다.

---

# EFK Stack
(Micro Service) -> Fluentd -> ElasticSearch -> Kibana
Fluentd는 Log를 수집해서 목적지로 전달하는 역할을 한다.\
ElasticSearch는 Kibana의 backend를 맡으며 String 검색 엔진 기능으로 log의 처리를 담당한다.\
Kibana는 ES에서 처리된 log를 시각화하는 Front의 역할을 한다.

일반적으로 각 (Micro) Service는 K8S, Docker-Compose 등의 logging 기능을 통해서 FluentD에게 Log를 전달하고, FluentD는 전달받은 log의 전처리, 다음 system으로 전달, 여러 fluentd의 요청 aggregation 등을 처리한다.\
Fluentd를 통해서 Service와 Domain에 대해서 tagging을 하고 이를 (S3에 전달하거나) 또 다른 Fluentd를 통해서 통합하여 ES (cluster)로 전달한다.\
Kibana는 config을 통해서 ES cluster에 접근하며, ES cluster는 구성되면 cluster에 전달되는 데이터를 distribute-process한다.

ElasticSearch는 기본적으로 distributed-system이므로 clusterName.nodeName으로 구성된 identifier에서 clusterName이 같다면 자동으로 cluster를 구성하고 request, data를 cluster내에서 분산 처리한다.\
/etc/elasticsearch/elasticsearch.yml 파일을 수정하여 cluster를 구성한다.

```
cluster.name: logging-cluster

node.name: "node-1"

# master node
node.master: true

# worker(data) nodes:
node.data: true

# node network information
network.host: IP addr like 192.168.14.25 or smthing like it

# REST port
http.port: 9200

# details of the nodes in the cluster
discovery.zen.ping.unicast.hosts: ["172.11.11.11", "192.168.14.25"]

service elasticsearch restart
```

---

# CICD tools
MSA 혹은 MSA가 아니더라도 Container를 사용해서 서비스를 구현하고, CICD를 적용하기위해서는 어떤 기술을 적용해야 하는지 고민하는 경우가 많다.\
AWS 같은 경우에는 AWS CodePipeline(CodeCommit, CodeBuild, CodeDeploy), AWS ECS(AWS 표준의 Container Service)와 기타 등등을 제공하는데 테스트해본 결과 (특히) ECS가 사용하기 힘들다.\
설정 포맷이 널리 사용되는 k8s, docker-compose 형식과 차이가 클뿐만 아니라, cluster를 구성하는 Console 설정마저도 복잡하다. (튜토리얼 따라서 console에서 설정하는 것도 실패해서 cli는 건들지도 않았지만)\
문제는 CodePipeline의 배포 부분에서 container의 버젼을 바꾸는 것과 같은 서비스를 제공하는 건 ECS가 전부라는 것.\
ECS가 아니라면 직접 container image의 버젼을 수정하고 적용하는 부분을 만들어야되는데, 사실 그렇게하려면 Jenkins를 쓰는게 훨씬 간단하다.\
그렇지만 AWS에서 container orchestration tool 중 가장 널리 사용되는 K8S도 지원하므로 (EKS) 이에 대한 CICD reference도 찾아봤다.\
간단하게, repository에 k8s config file을 두고, code build 환경에서 aws cli를 사용해서 kubectl에게 EKS cluster에 대한 권한을 준다.\
sed 등의 툴로 이미지 버젼이 변경된 k8s config을 kubectl로 apply해서 이미지 버젼 업데이트를 한다. (deploy 방식은 k8s에서 기본 제공하는 rolling, 따로 설정한다면 bluegreen도 된다)\
k8s를 사용한다는데서 이미 훨씬 더 개발자가 사용하기 편리하다고 생각하지만 (kubectl과 k8s config 포맷은 정말 간단하다.) 위 방식의 단점도 생각해보자면 일단 EKS cluster를 유지하는 고정비용이 ap-northeast-2기준 cluster당 월 72$가 필요하고, 적용 중인 terraform에서 한 눈에 보기 좀 어려울 것 같다고 생각한다.\
위의 단점에 재반박을 하자면, CodePipeline을 사용하는 것보다는 비싸지만 그 이상으로 k8s가 제공하는 기능(service discovery, deployment 등)이 많다는 점, CodePipeline을 사용하더라도 한 곳에서 Terraform으로 모든 리소스를 관리하기 어렵다는 의견을 낼 수 있을 것 같다.\
더 리서치를 하고, 더 생각해봐야겠지만 Google Tech 매니아라 그런지 K8S를 사용하는 위의 방식이 신뢰가 가고, 다른 방법보다 편리하다고 생각한다.

---

# Docker Network
* bridge - Default network driver. Standalone 컨테이너가 다른 컨테이너와 통신을 가능하게 한다.
* host - Standalone 컨테이너가 Host의 network를 직접적으로 사용할 수 있게 한다.

---

# Dynamic Port Mapping
한 Host에서 하나의 Port는 한 번에 한 대상에 대해서만 Listen이 가능하다.\
그렇다면 동일한 Instance에서 Blue Green Deployment는 불가능한걸까?\
이에 대한 답은 Dynamic Port Mapping이다.\
App이 사용하는 Host의 Port를 static하게 설정하지 않는다.\
Dynamic하게 설정된 Port는 Instance 외부의 Load Balancer에게 Port에 대한 정보를 제공하고 Load Balancer는 Health Check, Listener를 사용하여 Dynamic Port Mapping을 구현한다.

---

# Service Mesh
1. MSA를 적용한 시스템의 내부 통신이 Mesh 형태를 띄는 것을 Service Mesh라고 한다.
2. Service Mesh는 서비스간 통신을 추상화하여 안전하고, 빠르게 만드는 infra layer이다. 추상화를 통해서 네트워크를 제어, 추적한다.
3. Service Mesh는 URL 경로, 호스트 헤더, API 버젼 등의 규칙을 기반으로 하는 Application Layer의 서비스이다.

## Why Service Mesh
MSA와 Cloud 환경이 Norm이 되면서 시스템의 런타임 복잡성이라는 다른 문제점이 발생했다.\
MSA/Cloud 환경에서는 많은 수의 service와 instance가 동시에 동작하면서 로깅을 처리하고, 인스턴스를 관리하거나, 한정된 Bandwidth 내에서 서비스 간의 통신을 제어해야하는 요구 사항이 있다.\
이와 같은 문제를 해결하기 위해서 Service Mesh는 아래와 같은 기능을 제공한다.

* Service Discovery
* Load Balancing
* Dynamic Request Routing
* Circuit Breaking
* Retry and Timeout
* TLS
* Distributed Tracing
* metrics 수집

## How Service Mesh
Service Mesh Architecture의 구현은 보통 서비스의 앞단에 경량화 프록시를 사이드카 패턴으로 배치하여 서비스 간의 통신을 제어하는 방법으로 구현한다.\
서비스 간의 통신은 사이트카로 배치된 경량화 Proxy를 통해서 동작한다. 이 경량화 Proxy에 Routing Rules, Retry, Timeout 등을 설정하고 Logic을 작성하여 공통 기능을 Service에서 분리한다.

```
사이드카 패턴은 클라우드 디자인 패턴의 일종입니다.
기본 Application 외 필요한 추가 기능을 별도의 Application으로 구현하고 이를 동일한 프로세스 또는 컨테이너 내부에 배치하는 것입니다.
동일한 프로세스 또는 컨테이너에 배치된 사이드카 Application은 저장 공간, 네트워크 등의 리소스를 공유하며 모니터링, 로깅, 프록시 등의 동작을 합니다.
사이드카 패턴에는 몇가지 장점이 있습니다.
사이드카 Application은 기본 Application과 별도의 Application입니다.
기본 Application의 로직을 수정하지 않고도 추가 기능을 수행할 수 있습니다.
기본 Application을 polyglot 프로그래밍을 적용해 요구 사항에 최적화된 환경에서 개발을 진행할 수 있습니다.
사이드카 Application은 기본 Application과 리소스를 공유할 수 있습니다. 이를 통해 모니터링에 필요한 Metrics 수집, 프록시 동작 등을 수행할 수 있습니다.
```

대표적인 Service Mesh의 구현체는 istio가 있다.

## Service Mesh Pros and Cons

### Pros
* 기능을 어플리케이션 외부에 구현하며 재사용 가능하다.
* MicroService Architecture를 도입하면서 발생한 런타임 복잡성 이슈를 해결한다.
* 어플리케이션 개발시 언어와 미들웨어 등에 종속성을 제거한다.

### Cons
* 시스템의 런타임 인스턴스 수가 크게 증가한다. (최소 2배수)
* 서비스 간 통신에 네트워크 레이어가 추가된다.
* 신기술이다. 구현체가 Release 될 때까지 시간이 필요하다.

---

# Nat GW VS Instance

NAT (Network Address Translation) Gateway / Instance는 private subnet의 instance가 public internet에 접근할 수 있도록한다.\
Private subnet의 instance의 source IPV4를 NAT GW/Instance의 public ip로 교체함으로써 외부와 통신할 수 있도록 하는 것이다.\
하지만 public으로부터 NAT을 통해 내부의 Instance에 접근 (Ingress)는 허용하지 않는다. (Internet Gateway와의 차이)

AWS에서 관리하는 NAT Gateway와는 달리 NAT Instance는 public subnet에 instance를 생성하고, 이를 Gateway로 사용하는 방식이다.

둘의 차이는 아래와 같다.

| Attribute | NAT gateway |	NAT instance |
| --------- | ----------- | ------------ |
| Availability | Highly available. NAT gateways in each Availability Zone are implemented with redundancy. Create a NAT gateway in each Availability Zone to ensure zone-independent architecture. | Use a script to manage failover between instances.|
| Bandwidth | Can scale up to 45 Gbps. | Depends on the bandwidth of the instance type.|
| Maintenance	| Managed by AWS. You do not need to perform any maintenance.	| Managed by you, for example, by installing software updates or operating system patches on the instance. |
| Performance	| Software is optimized for handling NAT traffic.	| A generic Amazon Linux AMI that's configured to perform NAT. |
| Cost | Charged depending on the number of NAT gateways you use, duration of usage, and amount of data that you send through the NAT gateways. | Charged depending on the number of NAT instances that you use, duration of usage, and instance type and size. |
| Type and size	| Uniform offering; you don’t need to decide on the type or size.	| Choose a suitable instance type and size, according to your predicted workload. |
| Public IP addresses	| Choose the Elastic IP address to associate with a NAT gateway at creation. | Use an Elastic IP address or a public IP address with a NAT instance. You can change the public IP address at any time by associating a new Elastic IP address with the instance. |
| Private IP addresses | Automatically selected from the subnet's IP address range when you create the gateway.	| Assign a specific private IP address from the subnet's IP address range when you launch the instance. |
| Security groups	| Cannot be associated with a NAT gateway. You can associate security groups with your resources behind the NAT gateway to control inbound and outbound traffic. | Associate with your NAT instance and the resources behind your NAT instance to control inbound and outbound traffic. |
| Network ACLs | Use a network ACL to control the traffic to and from the subnet in which your NAT gateway resides. | Use a network ACL to control the traffic to and from the subnet in which your NAT instance resides. |
| Flow logs	| Use flow logs to capture the traffic.	| Use flow logs to capture the traffic. |
| Port forwarding	| Not supported. | Manually customize the configuration to support port forwarding. |
| Bastion servers	| Not supported. | Use as a bastion server. |
| Traffic metrics	| View CloudWatch metrics for the NAT gateway. | View CloudWatch metrics for the instance. |
| Timeout behavior | When a connection times out, a NAT gateway returns an RST packet to any resources behind the NAT gateway that attempt to continue the connection (it does not send a FIN packet). | When a connection times out, a NAT instance sends a FIN packet to resources behind the NAT instance to close the connection. |
| IP fragmentation | Supports forwarding of IP fragmented packets for the UDP protocol. Does not support fragmentation for the TCP and ICMP protocols. Fragmented packets for these protocols will get dropped. | Supports reassembly of IP fragmented packets for the UDP, TCP, and ICMP protocols. |


---

# Docker Multi-Stage Builds
## Before Multi-Stage Build
```
One of the most challenging things about building images is keeping the image size down. Each instruction in the Dockerfile adds a layer to the image, and you need to remember to clean up any artifacts you don’t need before moving on to the next layer. To write a really efficient Dockerfile, you have traditionally needed to employ shell tricks and other logic to keep the layers as small as possible and to ensure that each layer has the artifacts it needs from the previous layer and nothing else.

It was actually very common to have one Dockerfile to use for development (which contained everything needed to build your application), and a slimmed-down one to use for production, which only contained your application and exactly what was needed to run it. This has been referred to as the “builder pattern”. Maintaining two Dockerfiles is not ideal.

---

build.sh:

#!/bin/sh
echo Building alexellis2/href-counter:build

docker build --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy \  
    -t alexellis2/href-counter:build . -f Dockerfile.build

docker container create --name extract alexellis2/href-counter:build  
docker container cp extract:/go/src/github.com/alexellis/href-counter/app ./app  
docker container rm -f extract

echo Building alexellis2/href-counter:latest

docker build --no-cache -t alexellis2/href-counter:latest .
rm ./app

---

Above build script first creates an image to extract the compiled application from, then copy and use the artifact to run a slim image.
```

## Multi-Stage Build
```
Dockerfile:

# syntax=docker/dockerfile:1
FROM golang:1.16
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v golang.org/x/net/html
COPY app.go .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=0 /go/src/github.com/alexellis/href-counter/app .
CMD ["./app"]

---
each stage can be named for convenience
---

# syntax=docker/dockerfile:1
FROM golang:1.16 AS builder
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v golang.org/x/net/html
COPY app.go    .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/github.com/alexellis/href-counter/app .
CMD ["./app"]

---
or use an external image as a stage
---
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

---

# CKAD

---

## CORE

* Create a namespace called frontend.
```
kubectl create ns frontend
```

* Create a pod named nginx in frontend namespace. Use nginx image.
```
kubectl run nginx --image=nginx -n  frontend
```

* Get list of all pods in kube-system namespace and write the output to /root/kube-system-pods.txt file.
```
kubectl get pods -A > /root/kube-system-pods.txt
```

* Get the list of all services across all namespaces and write the output to /root/all-services.txt file.
```
kubectl get services -A > /root/all-services.txt
```

* Create a pod named hello with image busybox and command echo "Hello World". Make sure the pod do not restart automatically.
```
kubectl run busybox --image busybox --restart=Never -- echo "Hello World"
```

* Generate a pod manifest file at /root/mypodx.yaml. Pod name should be mypodx with image redis. Make sure you only generate the pod manifest file, you do not have to crete the pod.
```
kubectl run mypodx --image=redis --dry-run=client -o yaml > /root/mypodx.yaml
```

* Create a namespace called 'mynamespace' and a pod with image nginx called nginx on this namespace
```
kubectl create ns mynamespace

kubectl run nginx --image=nginx -n mynamespace
```

* Create the pod that was just described using YAML
```
kubectl run --image=nginx -n mynamespace --restart=Never --dry-run=client -o yaml > pod.yam
```

* Create a busybox pod (using kubectl command) that runs the command "env". Run it and see the output
```
kubectl run busybox --image=busybox --restart=Never -- env

kubectl logs busybox
```

* Get the YAML for a new namespace called 'myns' without creating it
```
kubectl create ns myns --dry-run=client -o yaml > myns.yaml
```

* Get the YAML for a new ResourceQuota called 'myrq' with hard limits of 1 CPU, 1G memory and 2 pods without creating it
```
kubectl create myrq --hard=cpu=1,memory=1G,pods=2 --dry-run=client -o yaml > myrq.yaml
```

* Create a pod with image nginx called nginx and expose traffic on port 80
```
kubectl run nginx --image=nginx --port=80
```

* Change pod's image to nginx:1.7.1. Observe that the container will be restarted as soon as the image gets pulled
```
kubectl set image po/nginx nginx=nginx:1.7.1
```

---

## Config

* Create a config map called my-config in namespace called datatab. Use value confa=exvalue You may need to create namespace if it does not exists.
```
kubectl create ns datatab

kubectl create configmap my-config -n datatab --from-literal=confa=exvalue
```

* A configmap al-conf has been created. Expose the value of al-user to a pod named al-pod as AL\_USER environment variable. Use redis image for the pod.
```
kubectl run al-pod --image=redis --dry-run=client -o yaml > al-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: al-pod
  name: al-pod
spec:
  containers:
  - image: redis
    name: al-pod
    resources: {}
    env:
      - name: AL_USER
        valueFrom:
          configMapKeyRef:
            name: al-conf
            key: al-user
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

kubectl apply -f al-pod.yaml
```

* Create a Pod named secure-pod. Use redis image. Run pod as user 1000 and group 2000.
```
kubectl run secure-pod --image=redis --dry-run=client -o yaml > secure-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secure-pod
  name: secure-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 2000
  containers:
  - image: redis
    name: secure-pod
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

kubectl apply -f secure-pod.yaml
```

* ### Create a pod manifest file at /root/limited-pod.yaml with name limited-pod and busybox image. Set memory request at 100Mi and limit at 200Mi. You do not need to create the pod.
```
kubectl run limited-pod --image=busybox --requests=memory=100Mi --limits=memory=200Mi --dry-run=client -o yaml > limited-pod.yaml
```

* Create a secret db-secret with value MYSQL\_ROOT\_PASSWORD=YoYoSecret and MYSQL\_PASSWORD=XoXoPassword.
```
kubectl create secret generic db-secret --from-literal=MYSQL_ROOT_PASSWORD=YoYoSecret --from-literal=MYSQL_PASSWORD=XoXoPassword
```

* Create a configmap db-config with value MYSQL\_USER=k8s and MYSQL\_DATABASE=newdb.
```
kubectl create configmap db-config --from-literal=MYSQL_USER=k8s --from-literal=MYSQL_DATABASE=newdb
```

* Create a pod named mydb with image mysql:5.7 and expose all values of db-secret and db-config as environment variable to pod.
```
kubectl run mydb --image=mysql:5.7 --dry-run=client -o yaml > mydb.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: mydb
  name: mydb
spec:
  containers:
  - image: mysql:5.7
    name: mydb
    resources: {}
    envFrom:
    - secretRef:
        name: db-secret
    - configMapRef:
        name: db-config
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

kubectl apply -f mydb.yaml
```

* Create a service account named namaste.
```
kubectl create serviceaccount namaste
```

* Use the service account to create a yo-namaste pod with nginx image.
```
kubectl run yo-namaste --image=nginx --serviceaccount=namaste
```

---

## Multi-Container Pods

* Create a pod mp-hello with image alpine,nginx and consul:1.8. Use command sleep infinity for alpine container.
```
kubectl run mp-hello --image=alpine --dry-run=client -o yaml -- sleep infinity > mp-hello.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: mp-hello
  name: mp-hello
spec:
  containers:
  - args:
    - sleep
    - infinity
    image: alpine
    name: alpine
    resources: {}
  - image: nginx
    name: nginx
  - image: consul:1.8
    name: consul
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

kubectl apply -f mp-hello.yaml
```

* Create a Pod with two containers, both with image busybox and command "echo hello; sleep 3600". Connect to the second container and run 'ls'
```
kubectl run two-container --image=busybox --dry-run=client -o yaml -- /bin/sh -c "echo hello; sleep 3600" > two-container.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: two-container
  name: two-container
spec:
  containers:
  - args:
    - /bin/sh
    - -c
    - echo hello; sleep 3600
    image: busybox
    name: two-container1
    resources: {}
  - args:
    - /bin/sh
    - -c
    - echo hello; sleep 3600
    image: busybox
    name: two-container2
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

kubectl apply -f two-container.yaml

kubectl exec -it two-container -c two-container2 -- ls
```

---

## Observability

* Create a pod myredis with image redis. Define a liveness probe and readiness probe with an initial delay of 5 seconds and command redis-cli PING.
```
kubectl run myredis --image=redis --restart=Never --dry-run=client -o yaml > myredis.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: myredis
  name: myredis
spec:
  containers:
  - image: redis
    name: myredis
    resources: {}
    livenessProbe:
      exec:
        command:
        - redis-cli
        - PING
      initialDelaySeconds: 5
    readinessProbe:
      exec:
        command:
        - redis-cli
        - PING
      initialDelaySeconds: 5
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

kubectl apply -f myredis.yaml
```

* Create a pod httptest with image kennethreitz/httpbin. Define a readiness probe at path /status/200 on port 80 of the container.
```
kubectl run httptest --restart=Never --image=kennethreitz/httpbin --dry-run=client -o yaml > httptest.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: httptest
  name: httptest
spec:
  containers:
  - image: kennethreitz/httpbin
    name: httptest
    resources: {}
    readinessProbe:
      httpGet:
        path: /status/200
        port: 80
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

kubectl apply -f httptest.yaml
```

* Create a Pod named myenv with command sh -c "printenv && sleep 1h". Use alpine image.
```
kubectl run myenv --image=alpine --restart=Never -- sh -c "printenv && sleep 1h"
```

* Save the logs of the pod to /root/myenv.log file.
```
kubectl logs myenv > /root/myenv.log
```

---

## Pod Design

* Create a deployment named hoth with image httpd in planets namespace.
```
kubectl create ns planets

kubectl create deploy hoth --image=httpd -n planets
```

* Scale the deployment to 4 replicas.
```
kubectl scale --replica=4 -n plants deployment hoth
```

* Update the deployment to use httpd:2.4.46 image.
```
kubectl set image deployment hoth httpd=httpd:2.4.46 -n planets
```

* Deployment yavin is deployed but after an upgrade, new pods are not getting created. Rollback the deployment yavin so they are working again.
```
kubectl rollback undo deploy yavin
```

* Deployment naboo is created. Make sure the replicas autoscale with minimum 2 and maximum 5 when at 80% CPU. Use naboo as the name of HPA resource.
```
kubectl autoscale deploy naboo --min=2 --max=5 --cpu-percent=80 --name=naboo
```

* Create a Cron job bespin that runs every 5 minutes(*/5 * * * *) and runs command date. Use alpine image.
```
kubectl create cronjob bespin --image=alpine --schedule='*/5 * * * *' -- date
```

* Label node node01 with shuttle=true.
```
kubectl label node node01 shuttle=true
```

* Remove annotation flagship=finalizer form node01.
```
kubectl label node node01 flagship-
```

* Get the name and image of all pods in skywalker namespace having label jedi=true. Write the output to /root/jedi-true.txt.
```
kubectl get po -n skywalker -l jedi=true > jedi-true.txt
```

* Create 3 pods with names nginx1,nginx2,nginx3. All of them should have the label app=v1
```
kubectl run nginx1 --image=nginx --restart=Never --labels=app=v1
kubectl run nginx2 --image=nginx --restart=Never --labels=app=v1
kubectl run nginx3 --image=nginx --restart=Never --labels=app=v1
```

* Change the labels of pod 'nginx2' to be app=v2
```
kubectl label po nginx2 app=v2 --overwrite
```

* Create a deployment with image nginx:1.18.0, called nginx, having 2 replicas, defining port 80 as the port that this container exposes
```
kubectl create deploy nginx --image=nginx:1.18.0 --replicas=2 --port=80
```

---

## Services & Networking


