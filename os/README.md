# Introduction
프로그램 내장형 모델의 컴퓨터에서 메모리에 Instruction(Program)을 탑재하는 OS가 없다면 메모리에 arbitrary 데이터가 있으므로 프로세스를 실행할 수 없다.\
즉 멀티프로세싱, IO, 네트워크, 하드웨어 관리 모두 OS가 제어하므로 OS없이는 컴퓨터를 사용할 수 없다.

컴퓨터는 프로세서와 메인 메모리(RAM, ROM), 하드디스크로 구성된다.\
RAM은 수 Gb인데 비해, ROM은 수 Kb를 차지한다. RAM은 휘발성이므로 내용이 유지되지 않지만, ROM과 하드디스크는 비휘발성이므로 전원이 없어도 내용이 유지된다.\
따라서 컴퓨터를 부팅할 때, 컴퓨터는 ROM의 내용을 읽고 실행한다.\
ROM은 POST(Power-On Self-Test, 컴퓨터 자체 진단), Boot Loader(하드디스크의 OS를 메인 메모리(RAM)에 탑재)을 순서대로 실행하고, 이외에 컴퓨터 동작에는 관여하지 않는다.\
이렇게 로드된 OS는 컴퓨터의 전원이 연결된 동안 메모리에 유지된다.(Resident) 하지만 OS를 제외한 프로그램은 사용 시에 메모리에 탑재되고, 사용을 종료하면 메모리 해제된다.

하드웨어를 관리하는 Kernel과 이에 대한 API 역할을 하는 System Call, 사용자가 입력하는 명령어를 인식하고 실행하는 Shell 모두 OS에 속한다.\
Application은 OS 위에서 OS의 기능을 빌려 동작한다.

OS의 주된 기능은 Processor Management, Memory Management, I/O Management, File Management, Network Management, Security Management 등이 있다.

---

# 고등 운영체제
Time Sharing 운영체제는 하나의 CPU(프로세서)와 메모리를 사용하여 여러 사용자의 Task를 짧은 시간동안 Switch하며 처리한다. 하지만 더 효율적인 연산을 위해서 고등 운영체제가 생겼다.

* 멀티프로세서 - 한 시스템이 다수의 프로세서를 사용하여 더 높은 컴퓨팅 파워를 낸다. 다수의 CPU가 한 메모리를 공유한다.
* 분산처리 - 여러 시스템이 통신을 통해서 어떠한 작업을 분산 처리한다. 다수의 CPU와 다수의 메모리.
* 실시간 시스템 - 어떠한 작업이 완료되는 데드라인을 지정하여 이후의 응답은 사용하지 않는 시스템. Navigator에서 특정 시점까지 데이터가 필요함, 이후의 응답은 필요하지 않음. 공장자동화, 군사목적 등에 사용.

---

# 인터럽트 기반 시스템
현대의 운영체제는 인터럽트 기반 시스템이다.\
부팅이 끝나면 운영체제는 메모리에 상주(resident)하며, event를 기다리며 대기한다.\
마우스, 키보드 등의 하드웨어 혹은 소프트웨어에서 event를 발생하여 프로세서에게 신호를 보내고, 프로세서는 이 신호에 해당하는 ISR(Interrupt Service Routine)을 실행한다.\
하드웨어, 소프트웨어 뿐만 아니라 내부 인터럽트 또한 ISR을 trigger한다.\
내부 인터럽트는 division by 0와 같은 err가 발생할 때의 signal과 같다.\
만약 division by 0 인터럽트가 발생하면, 해당 프로세스를 종료시키는 ISR이 실행된다.

ISR이 종료되면 원래의 대기상태 또는 사용자 프로그램으로 복귀한다.

---

# 이중 모드
단일 시스템에서는 한 컴퓨터를 여러 유저가 사용하거나, 한 유저가 여러 프로그램을 실행하는 상황에서 한 사람이 고의로 혹은 실수로 STOP, HALT, RESET등의 명령을 사용하여 전체 시스템에 영향을 줄 수 있다.\
따라서 사용자 프로그램은 STOP등 치명적인 명령을 사용할 수 없도록 사용자(user) 모드와 관리자(supervisor/previleged) 모드를 분리한 것이 이중 모드이다.

CPU의 구성요소인 Register, ALU, CU 중에 Register는 Carry, Negative, Zero, Overflow 등의 flag를 가진다. 여기에 하나의 flag를 더 추가하여 previleged mode / user mode를 구분한다.\
운영체제의 서비스를 실행할 때는 privileged mode에서, 사용자 프로세스를 실행할 때는user mode에서 동작한다. 사용자 프로세스가 OS에 Software Interrupt를 g혹은 하드웨어가 Interrupt를 보내면, OS가 프로세스의 주도권을 가져오고, CPU의 user mode flag는 true값을 가진다. OS가 작업을 수행한 후, 다시 사용자 프로세스를 실행할때는 user mode flag가 false가 된다.\
이와 같이 운영체제는 각 리소스를 보호한다.

## 입출력장치 보호, 메모리 보호, CPU 보호

* 입출력장치 보호
입출력 장치를 제어하는 명령을 Privileged Mode에서만 사용할 수 있도록 한다.\
사용자 프로그램이 입출력을 하려면 OS에 요청하여 privileged mode로 전환하여 OS가 입출력을 대행한다. 이후 user mode로 복귀한다. 만약 사용자 프로그램이 올바른 요청을 보내지 않았을 경우 OS는 해당 요청을 거부한다.\

* 메모리 보호
Modern 컴퓨터에서는 메인 메모리에 하나의 프로그램이 아닌 OS, 여러 프로그램, 다른 유저의 프로그램이 탑재되어 있으므로, OS와 다른 유저의 프로그램이 사용하는 메모리에 접근할 수 없도록 CPU-\>Memory의 Memory Bus에 User에 따라 접근을 허용, 불허하는 로직(MMU)을 적용하여 메모리를 보호한다.

	CPU	-> Address Bus ->	Memory
		<- Data Bus <-

다른 메모리 영역을 침범할 때 Segmentation Error를 나타낸다.

* CPU 보호
한 사용자가 실수 또는 고의로 CPU 시간을 독점하는 경우 다른 사용자의 프로그램을 실행 할 수 없는 상태가 된다.\
따라서 OS에 Timer를 두어서 일정 시간 경과 시 Timer가 Interrupt 하도록 한다.\
Interrupt된 운영체제는 CPU 작업을 다른 프로그램으로 강제로 전환한다.

---

# 운영체제 서비스
OS는 Application이 요구하는 HW 리소스를 효율적으로 나눌 수 있게 해준다.\
* Process Management - CPU 자원을 관리
* Main Memory Management - 메인 메모리를 관리
* File Management - 하드디스크 내의 파일을 관리
* IO Management - IO 장치를 관리
* Networking - 네트워크 관리
* Protection - IO, 메모리, 프로세서 보호를 관리
등의 여러 서비스를 제공한다.

## Process Management
프로세스는 메모리에서 실행 중인 프로그램을 가리킨다.\
주요 기능은 아래와 같다.

1. 프로세스의 생성, 소멸
2. 프로세스 활동 일시 중단, 재개
3. 프로세스간 통신(IPC)
4. 프로세스간 동기화
5. 교착상태 처리

## Main Memory Management
1. 프로세스에 메모리 할당
2. 메모리 추적 및 감시
3. 메모리 회수
4. 메모리 효과적 사용
5. 가상 메모리 관리

## File Management
Track과 Sector로 구성된 디스크를 파일로 추상화
1. 파일의 생성과 삭제
2. 디렉토리 생성과 삭제
3. open, close, read, write 등 기본 동작 지원
4. Track, Sector와 File의 매핑
5. 백업

## Secondary Storage Management
하드디스크, 플래시 메모리등 보조기억장치를 관리
1. 빈 공관 관리
2. 저장공간 할당
3. 디스크 스케쥴링

## IO Device Management
1. Device Driver 관리
2. IO Device 성능 향상: buffering, caching, spooling

---

## System Call
운영체제 서비스를 받기 위한 호출\
인터럽트는 CPU(프로세서)와 OS Kernel 사이에서 전달되며, 시스템 콜은 프로세스와 OS Kernel 사이에서 전달된다.\

---

# Process
Process는 Program in Execution, 하드디스크에 저장되어있는 프로그램을 메모리에 탑재해서 실행되는 상태를 뜻한다.\
프로세스의 상태는 아래와 같다.

* New - 하드디스크의 프로그램이 메모리에 적재된 상태
* Ready - CPU에서 실행할 준비 완료, New 혹은 Waiting을 거쳐 Ready 된다. Time Sharing 시스템일 경우 Running에서 Ready가 될 수도 있다.
* Running - CPU가 실행 중인 프로세스의 상태
* Waiting - CPU가 IO 혹은 다른 프로세스를 실행하는 동안 기다리는 프로세스의 상태
* Terminated - 프로세스 종료

## PCB(Process Control Block)
하나의 프로세스에는 한 개의 PCB가 할당되어 프로세스에 대한 모든 정보를 저장한다.\
저장되는 정보는 아래와 같다.

* 프로세스의 상태
* 프로세스 카운터 - CPU가 프로세스를 실행하는 순서를 저장
* MMU - CPU가 접근 가능한 메모리의 범위를 명시
* PID - Process의 ID
* Open Files - 프로세스가 open한 파일들의 집합을 저장

프로세스가 동작하는 거의 모든 행동은 Queue를 통해서 순서에 따라 처리된다.\
Queue를 통해서 순서를 지정하는 Job Scheduler는 OS의 Process Management에서 돌아간다.\
Job Scheduler가 지정한 Queue를 항상 순서대로 실행하지는 않는다.(Long-term Scheduler) CPU Scheduler가 어떤 프로세스를 CPU가 먼저 실행할지를 정한다.(Short-term Scheduler)\
 Medium-term Scheduler는 Swapping을 통해서 현재 메모리에 탑재된 프로세스 중 사용되지 않는 프로세스를 리소스를 효과적으로 사용하기 위해 디스크에 보관한다.




















