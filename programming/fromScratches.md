# Go 설치 및 환경 설정
1. Go 설치 - Golang 공식 Page에서 지원하는 Install Method 선택하여 설치
2. 환경 설정 - pkg 매니징, build output의 default path 역할, go tools path 역할을 할 path 설정 (기본값은 $HOME/go)
3. Go mod init [package URI]를 사용하여 module init 혹은 git 등으로부터 소스 import
	* Go module을 사용할 때는 go language server를 사용하는 편을 go dev team은 추천한다.
4. 기타 필요한 tool 설치

# Package 구성 Basics
```
.
├── README.md
├── go.mod
├── main.go
└── src
    ├── blueprint
    ├── controller
    └── core
        ├── module
        ├── service
        └── util
```
Go의 package구성은 base directory로부터 folder 이름으로 구분되는 package에 대한 service discovery로 이루어진다.\
예를 들어 main.go가 위치한 base directory로부터 import를 할 때는 github.com/woodchuckchoi/fromScratches를 import하고, 따로 설정하지 않는다면 fromScratches가 사용할 package 이름이 된다.\
util을 import 할 때는 github.com/woodchuckchoi/fromScratches/src/core/util을 import하고 util.Func()와 같은 방식으로 package를 사용하게 된다.\
github.com/woodchuckchoi 와 같은 URI는 Package Hosting 서비스의 종류와 사용자에 따라 달라진다. 원한다면 Self-Hosting Server도 가능하다.\
공개된 소스는 go get [package]를 통해서 다운로드 받을 수 있다.

go mod를 사용하지 않을 경우 go의 package discovery는 $GOPATH의 하위 directory에 한정되므로, go module을 사용하던가 매번 다른 package를 다룰 때마다 GOPATH를 바꿔가며 작업한다.


