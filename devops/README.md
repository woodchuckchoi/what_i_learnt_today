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


