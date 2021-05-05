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
운영체제의 서비스를 실행할 때는 privileged mode에서, 사용자 프로세스를 실행할 때는 user mode에서 동작한다. 사용자 프로세스가 OS에 Software Interrupt를, 혹은 하드웨어가 Interrupt를 보내면, OS가 프로세스의 주도권을 가져오고 CPU의 user mode flag는 true값을 가진다.\
OS가 작업을 수행한 후, 다시 사용자 프로세스를 실행할때는 user mode flag가 false가 된다.\
이와 같이 운영체제는 각 리소스를 보호한다.

## 입출력장치 보호, 메모리 보호, CPU 보호

* 입출력장치 보호
입출력 장치를 제어하는 명령을 Privileged Mode에서만 사용할 수 있도록 한다.\
사용자 프로그램이 입출력을 하려면 OS에 요청하여 privileged mode로 전환하여 OS가 입출력을 대행한다. 이후 user mode로 복귀한다. 만약 사용자 프로그램이 올바른 요청을 보내지 않았을 경우 OS는 해당 요청을 거부한다.

* 메모리 보호
Modern 컴퓨터에서는 메인 메모리에 하나의 프로그램이 아닌 OS, 여러 프로그램, 다른 유저의 프로그램이 탑재되어 있으므로, OS와 다른 유저의 프로그램이 사용하는 메모리에 접근할 수 없도록 CPU-\>Memory의 Memory Bus에 User에 따라 접근을 허용, 불허하는 로직(MMU)을 적용하여 메모리를 보호한다.


```
	CPU	-> Address Bus ->	Memory
		<- Data Bus <-
```

다른 메모리 영역을 침범할 때 Segmentation Error를 나타낸다.

* CPU 보호

한 사용자가 실수 또는 고의로 CPU 시간을 독점하는 경우 다른 사용자의 프로그램을 실행 할 수 없는 상태가 된다.\
따라서 OS에 Timer를 두어서 일정 시간 경과 시 Timer가 Interrupt 하도록 한다.\
Interrupt된 운영체제는 CPU 작업을 다른 프로그램으로 강제로 전환한다.

---

# 운영체제 서비스
OS는 Application이 요구하는 HW 리소스를 효율적으로 나눌 수 있게 해준다.
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
인터럽트는 CPU(프로세서)와 OS Kernel 사이에서 전달되며, 시스템 콜은 프로세스와 OS Kernel 사이에서 전달된다.

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

## Context Switch
* Scheduler - 어떤 Process를 실행할지 결정하는 OS의 프로그램
* Dispatcher - Scheduler가 선택한 Process를 실행하기 위해서 현재 프로세스의 상태(register, MMU)를 저장하고, 실행할 프로세스의 상태를 불러오는 프로그램
* Context Switching Overhead - 위의 프로세스들이 실행되기 때문에 context switch가 일어날 때는 overhead가 발생한다. 이를 막기위해서 scheduler, dispatcher는 보통 C같은 high-level programming language가 아닌, low-level로 만들어진다.

---

# CPU 스케쥴링 알고리즘
*Preemptive(선점) VS Non-preemptive(비선점)*
선점 방식은 CPU에서 프로세스가 동작 중이어도 다음 프로세스가 프로세서를 선점하고, 이전 프로세스를 쫓아낼 수 있다.\
이와 반대로 비선점 방식은 CPU에서 프로세스가 동작 중이면 다른 프로세스가 해당 리소스를 점유할 수 없다.

eg) 병원에서 응급환자가 도착하면 Preemptive 방식으로 기존 환자가 아닌 응급환자를 보살핀다. 반면 은행에서는 (대체로) Non-preemptive 방식으로 순서대로 고객을 응대한다.

Scheduling Criteria(Scheduling 방식 비교를 위한 척도)의 예시는 아래와 같다.
* CPU Utilisation(%)
* Throughput(jobs/time)
* Turnaround Time(time) - 작업이 Process Ready Queue에 들어가고, 완료되어 나오기 까지 걸린 시간
* Waiting Time(time) - Process Ready Queue에서 CPU에서 처리되기까지 대기하는 시간
* Response Time(time) - Input 후, Output까지 걸리는 시간

## CPU Scheduling Algorithms
* First-Come, First-Serve(FCFS) : 시간이 오래 걸리는 프로세스가 먼저 실행될 경우, 평균 대기시간이 늘어나게 된다.
* Shortest-Job-First(SJF) : 작업 시간이 적게 걸리는 프로세스를 먼저 실행하여 대기시간을 줄인다. 평균 대기시간을 줄이는데 최적이지만, 작업 시간을 예측하는 것은 사실상 불가능하다. Preemptive와 Non-preemprive 모두 구현가능하다.(Shortest-remaining-time 기법)
* Priority : 우선순위(int)가 낮은 값을 먼저 처리한다. internal한 요인(time limit, memory requirement 등), external한 요인(amount of funds, political factors 등)에 따라 우선순위를 정하며, preemptive, non-preemptive 모두 구현가능하다. Starvation(우선순위에 계속 밀려서 CPU에 처리되지 않음)이 생길 수 있다.Aging을 통해서 우선순위에 보정값을 줘서 Starvation을 해결한다.
* Round-Robin : Time-sharing 방식으로 각 프로세스에 같은 양의 CPU Time(일반적으로 10~100msec)을 할당한다. CPU Time을 0으로 수렴시키면 다수의 Process가 Parallel하게 동작하는 Process Sharing을 경험할 수 있지만, context switching에 따른 overhead가 과다해진다.
* Multilevel Queue : Process를 System Process Group, Interactive Process Group, Batch Process Group 등으로 나누고 각각의 Queue에 절대적인 우선순위 설정하거나 CPU Time을 차등배분한다. 각 Queue는 독립된 Scheduling 정책을 가진다. * Multilevel Feedback Queue : Group으로 분리된 Process가 특정 조건 내에 작업을 완료하지 못하면, 다른 우선순위, CPU 할당을 받은 다른 Group으로 옮겨서 작업을 이어간다.

---

# Process Creation
## Process Creation
프로세스는 프로세스에 의해 만들어진다.\
Parent Process -> Child Process 형식을 띄는 Process Tree로 나타내진다.\
각각의 Process는 Unique한 PID를 가지며, Parent Process ID(PPID) 역시 Process 정보에 포함된다.\
프로세스의 생성은 fork() System Call을 통해서 부모 프로세스를 복사하고 exec()를 통해서 복사된 프로세스를 대체할 프로세스를 메모리에 로드한다.

## Process Termination
exit()을 통해서 Memory와 열린 File과 같은 모든 자원을 반납한다.

---

# Thread
## Multithread
한 프로세스에 2개 이상의 Thread가 존재하는 경우\
다중 Thread가 빠르게 Context Switch되면서 동시에 실행되는 것처럼 보인다.(Concurrency)\
Thread는 Process의 메모리 공간을 공유한다. 하지만 지역변수가 저장되는 Stack은 공유하지 않는다.

---

# Process Synchronisation
Independent VS Cooperative로 나뉜다.\
Cooperative의 경우 시스템의 다른 Process에 영향을 받는 Process를 뜻한다.\
Concurrent Access to Shared Data는 Inconsistency를 유발할 수 있다. -> BankAccount Problem

High-level language에서는 한 줄의 코드라도, 실제 컴퓨터가 동작하는 코드는 여러 줄로 구성되어 시간지연이 생기기 때문에 BA Problem(Critical Section Problem)이 발생한다.\
다중 스레드로 구성된 시스템이 공통의 변수에 접근하면서 변수가 inconsistent해지는 범위를 Critical Section이라고 한다.\
이에 대한 Solution은 아래와 같다.

* Mutual Exclusion 상호 배제 - 한번에 한 Process/Thread만 Critical Section에 접근할 수 있다.
* Progress 진행 - 어떤 Process/Thread가 진입할 지는 유한 시간 내에 결정되야한다.
* Bounded Waiting 유한 대기 - 어떤 Process/Thread라도 유한 시간 내에 Critical Section에 진입할 수 있다.

## Synchronisation Tools
* Semaphore - Sync 문제를 해결하기 위한 소프트웨어 도구이며 정수형 변수와 두 개의 동작(P, V)을 가진 구조이다.

```
	//Go
	queue := make(chan chan struct{})
	type Semaphore struct {
		value int // 사용 가능한 Resource의 양
	}
	
	func (s *Semaphore) acquire() {
		receiver := make(chan struct {})
		s.value -= 1
		if s.value < 0 {
			queue <- receiver
			// add this process/thread to list
			// block
			select {
				case <- receiver:
					break
			}
		}
	}
	
	func (s *Semaphore) release() {
		s.value += 1
		if s.value <= 0 {
			// remove a process P from list
			// wakeup P
			receiver := <- queue
			receiver <- struct{} {}
		}
	}
```

대기시키는 Queue를 다른 형태의 Data Structure로 변환하거나 value가 0인 다른 Semaphore를 사용하여 Ordering을 바꿀 수 있다.

## 전통적 동기화 예시
* Producer, Consumer
Producer가 데이터를 생성하고 Consumer가 소비\
eg) Compiler -> Assembler, Server -> Client\
Producer와 Consumer의 속도 차이로 Buffer를 사용한다. 하지만 Buffer의 크기가 유한하다.(Bounded Buffer)\
Buffer가 가득 찼을 때 Producer는 데이터를 더 생성할 수 없고, Consumer는 Buffer가 비었을 때 데이터를 소비할 수 없다.

Buffer의 in과 out index, Producer와 Consumer가 Critical Section에 동시에 접근하지 못하도록 하여 문제 해결, 또한 Semaphore를 사용하여 busy-wait(무한 루프를 돌면서 CPU 소모)

* Readers, Writers
읽기만 하는 Reader는 다수가 동시에 DB에 접근 가능해도된다. 하지만 Writer가 DB에 접근했을 때, Reader와 다른 Writer는 Block 되어야 한다.

* Dining Philosopher
```
	// Go
	lstick.Acquire()
	rstick.Acquire()
	
	// Eating
	
	rstick.Release()
	lstick.Release()
```
하지만 모든 철학자가 Deadlock에 걸릴 수도 있다.

---

## Deadlock
Process가 어떤 자원을 가진 상태로 다른 자원을 필요로 할 때 Deadlock이 발생할 수 있다.
* Mutual Exclusion (상호 배타)
* Hold and Wait (점유 대기)
* No Preemption (비선점)
* Circular Wait (환형 대기)

## Resource
동일 형식의 자원이 여러 개 있을 수 있다.\
자원을 사용할 때는 요청, 사용, 반납의 과정을 거친다.\
Deadlock 발생을 막기위해서 위의 필요 조건 중 1개 이상을 제거하면 Deadlock은 발생하지 않는다.

---

# Deadlock 처리
* 방지 - Deadlock 필요조건 중 한 가지 이상을 방지
	* 자원을 공유할 수 있도록 한다. (일반적으로 불가능하다.)
	* 모든 자원을 Process 시작 시에 가져오거나, 다른 자원을 기다릴 때 가지고 있는 자원을 Release한다. (자원 활용률 저하)
	* 자원을 선점 가능(뺏을 수 있도록) 한다. (자원에 따라 불가능할 수 있다.)
	* 자원에 번호를 부여해서 우선 순위를 둔다. (자원 활용률 저하)
* 회피 - Process가 자원을 요청할 때 요청된 자원이 Deadlock을 유발하지 않도록 계산해서 할당한다.
* 복구 - Deadlock이 발생하면 Process 종료 등의 방법으로 Deadlock을 해결한다. (검사에 대한 Overhead 발생)
* 무시 - Deadlock은 실제로 잘 일어나지 않는다. 따라서 Deadlock이 발생해도 아무 조치를 하지 않는다. 사용자가 컴퓨터를 재시작한다.

---

# Monitor
Semaphore와 같이 sync를 해결해주는 Data Structure, 하지만 High-Level에서 구현된 Process 동기화 방식\
Process는 Critical Section 앞의 Queue에서 wait하며 Critical Section을 지난 후 release를 통해서 Queue의 대기 중인 Process를 notify로 깨워줘서 Critical Section으로 진입시킨다.

---

# Main Memory Management
기계어/어셈블리어 프로그램에서 Object-oriented programming/high level programming으로 패러다임이 변하면서 메모리에 대한 수요가 높아짐\
메모리를 효과적으로 사용하기 위해서 메모리의 낭비를 없애고, 가상 메모리를 적용한다.

## Memory Structure
CPU가 Memory의 address를 전달하면 Memory는 해당 address에 있는 data를 CPU에 전달한다.\
Memory는 위의 예와 같이 주소와 데이터로 이루어져있다.

* 프로그램 개발

Source - High Level Programming Language / Assembly (test.c)\
Object - Compile/Assemble 결과물 (test.o)\
Executable - Object File을 Link한 결과물 (test.o + Libraries)\

프로그램이 실행되기 위해서는 code, data(literal, static/global var), stack(local var)이 메모리에 올려져야한다.\
또한 이것을 메모리의 어떤 위치에 올려야 하는지, Multi Process 환경에서 위치를 어떻게 바꿔야하는지를 정해야 한다.\
이 문제를 돕는 것이 CPU와 메모리 사이에서 동작하는 MMU(Memory Management Unit)이다.

MMU는 base register(하한 주소값), limit register(상한 주소값), relocation register가 탑재되어있다.

	//main executable이 메모리 0x0000 위치에 항상 로드된다고 가정한다.
	//하지만 해당 위치에 이미 다른 프로세스가 동작 중이어서 다른 위치에 main process를 올려야한다. 편의를 위해 0x500에 올린다고 가정한다.
	//이때 MMU의 relocation register는 500이라는 값을 가짐으로써, CPU가 0에 접근해도 500 위치로 보내준다. (Logical Location VS Physical Location)
	//CPU -> Memory[base register + relocation register:limit register + relocation register]

## 메모리 낭비 방지
* Dynamic Loading
프로그램 실행에 반드시 필요한 데이터만 Memory에 적재한다. (에러 처리와 같이 불필요한 부분을 skip한다.)\
실행 시 필요한 데이터가 로드되지 않았다면, 그 부분만 메모리에 동적으로 탑재한다.
* Dynamic Linking
여러 프로그램이 공통적으로 사용하는 Library를 Memory에 중복해서 올리는 낭비를 줄인다.\
하나의 Library Routine만 Memory에 load하고 다른 App 실행 시 이 Routine과 연결한다. (Linux - Shared Library)
* Swapping
Memory에 load되었으나 현재 사용하지 않는 process의 이미지를 swap device에 저장한다. Process의 크기가 크면 backing store의 입출력에 따른 overhead가 크다.\
backing store(swap area)의 크기는 main memory의 크기와 비슷하게 정하는것이 이 이유다.

## Contiguous Memory Allocation
Multi Process 환경에서 하나의 Memory에 여러 Process가 load/unload되며 사용할 수 있는 연속적인 메모리가 scattered되어 process를 할당할 수 없는 상황(external fragmentation)이 발생한다.\
위의 문제를 해결하기 위한 Contiguous Memory Allocation은 아래의 3가지 방법이 있다.
* First-fit - Memory를 순차적으로 탐색하여 가장 먼저 발견한 Process의 필요 Memory에 Load
* Best-fit - 가장 Process의 필요 Memory에 가까운 Memory의 위치에 load
* Worst-fit - 가장 차이가 큰 (가장 큰) Memory의 위치에 load (남는 공간이 가장 커지기 때문에 다른 Process가 Hole에 끼어들어갈 여지가 가장 크다.)

Memory 할당 속도면에서 first-fit이, 이용률면에서는 first-fit, best-fit이 최적이다.\
하지만 어떠한 최적화 알고리즘으로도 1/3 수준의 Memory는 사용 불가능하다.\
Process를 옮겨서 Memory의 Hole의 수를 줄이는 Compaction은 Overhead가 너무 크다.

## Paging
Process를 Page 단위로 잘라서 Memory에 끼워넣는다.\
Process는 Page의 집합으로, Memory는 Frame의 집합으로 구성된다.\
MMU의 Relocation Register를 여러 개 설정해서 Process가 연속된 메모리에 load된 것처럼 나타낸다.

* Address Translation(주소 변환)

CPU가 내는 주소는 2진수로 표현된다(전체 m비트)\
하위의 n비트는 offset 또는 displacement이다\
상위 m-n비트는 Page의 번호

```
	//page size = 16bytes = 2 ** 4
	//logical address 50 = 0b110010
	// 0b11 = physical address, 0b0010 = displacement
```

---

# Paging
	# Q1
	PageSize = 4 Bytes
	Page Table : 5 6 1 2
	Logical Address 13, Physical Address?
	
	Page Table Index		Page Table Value
	0						5
	1						6
	2						1
	3						2
	
	Logical Address = (Page Number) ++ (Displacement)
	
	13 = 0b1101 
	PageSize = 4 = 2 ** 2
	
	0b11 = Page Table Index 0b01 = Displacement
	Physical Address = 0b1001 (9)
	
	# Q2
	PageSize = 1 KB
	Page Table : 1 2 5 4 8 3 0 6
	Logical Address 3000, Physical Address?
	
	PageSize = 1KB = 2 ** 10
	
	3000 = 0b101110111000
	
	0b10 = Page Table Index 0b1110111000 = Displacement
	Physical Address = 0b1011110111000
	
	Physical Address = 0x1A53 = 0b000110(1001010011)
	Logical Address = 0b111001010011

## 외부 단편화(External Fragmentation)
Process의 크기가 각자 다르므로, 할당되던 공간을 반환했을 때, 다른 프로세스가 차지할 수 없을만큼 작은 공간이 생길 수도 있다. 이러한 공간 낭비를 외부 단편화라 부르며, 프로세스를 잘게 쪼개서 연속된 메모리를 차지하고 있는 것처럼 Paging Table을 만들어 사용하는 Paging 방식으로 해결 가능하다.

## 내부 단편화(Internal Fragmentation)
Process의 크기가 Page Size의 배수가 아니면 마지막 페이지는 한 Frame을 채울 수 없어서 남는 Memory 공간이 생기게 된다.\
External Fragmentation에 비해 낭비되는 메모리가 미미하므로 일반적으로 skip한다.

## Page Table 만들기
CPU Register 혹은 Main Memory에 생성할 수 있다.\
CPU Register로 구성할 경우 Address 변환 속도가 빠르지만, CPU Register의 공간이 한정되어 있어 Table의 크기가 제한된다.\
Main Memory에 Page Table을 구성할 경우 크기 제한이 적지만, Address 변환 속도가 느리다.\
혹은 TLB라는 별도의 Buffer 저장 장치를 사용하여 구성할 수도 있다.

*Protection & Sharing*
* Protection - 모든 주소는 PageTable을 경유하므로 PageTable Entry마다 rwx 비트를 두어서 해당 Page에 대한 접근 제어
* Sharing - 같은 Code를 사용하는 다수의 Process가 있다면 Code에 사용되는 Memory를 공유할 수 있다. (Re-enterant code)

## Segmentation
Process를 논리적인 내용(Paging은 무조건 같은 크기로)으로 잘라서 Memory에 배치한다.\
Segment의 크기는 일반적으로 같지 않다.

MMU의 Segment Table은 Paging Table과 비슷하다.

	Segment Table Base			Limit
	1400						1000
	6300						400
	4300						400
	3200						1100
	4700						1000
	
	// Logical Address(2, 100) = Physical Address 4400
	// Logical Address(1, 500) = Physical Address Segmentation Fault Error!

*Protection & Sharing*
* Protection - Segment Table Entry마다 r, w, x 비트를 둬서 각 Segment에 대한 접근을 제어한다. 
* Sharing - 같은 Code를 사용하는 다수의 Process가 있다면 Code에 사용되는 Memory를 공유할 수 있다. (Re-enterant code)

*같은 방식으로 Protection, Sharing이 동작하지만 논리적으로 나누는 편이 더 나은 수준의 관리가 가능하다.*

*하지만 Segmentation은 External Segmentation 문제에 취약할 수 있다. 따라서 Segment를 Paging한다! Paged Segmentation!!*

---

# Virtual Memory
Physical Memory보다 더 큰 Process를 실행할 수 있을까?\
Process의 이미지를 모두 Memory에 올릴 필요는 없다. 현재 필요한 기능 / 부분의Demand Page만 Memory에 load함으로서 Memory의 총량보다 더 큰 크기의 Process를 실행할 수 있다.\
Page Table에 Valid Bit Field를 추가해서 현재 Memory에 load된 Page와 그렇지 않은 Page를 나타낸다.\
Invalid (0) Process가 필요할 때, 해당 Process를 보조기억장치에서 Memory로 동적으로 load한다.\
Process의 Image는 Backing Store(SWAP device)에 저장해서 Page가 unload되고 다시 load 되었을 때까지 status를 저장한다.

* Page Fault - Invalid Page 발생 시, CPU에 Interrupt 발생, CPU는 OS에 Page Fault Routine을 trigger해서 OS가 Memory Load를 하도록 한다.

* Pure Demand Paging - Process 시작부터 아무 Page를 Load하지 않아서 Page Fault Routine을 통한 Overhead가 발생하는 대신에 Memory를 아낄 수 있다.
* PrePaging - Process 시작 시에 최대한의 Page를 Load해서 Overhead를 줄이지만, Memory가 낭비될 수 있다.

*Swapping과 Demand Paging은 SWAP device와 Memory사이에 전달되는 단위의 차이가 Process, Page로 다르다*

---

## Effective Access Time

	p = page fault rate
	
	T(eff) = (1-p)*Tm + p*Tp
	// Tm = Memory 접근 시간
	// Tp = Disk 접근 시간(seek time + rotational delay + transfer time)

## Locality
메모리 접근은 시간적, 공간적 지역성을 가진다.(반복문이 많고, 대부분의 코드는순차적으로 실행되기 때문에)\
따라서 한번 PageFault가 발생하면 한 Page가 아닌 연속된 다수의 page를 Memory에 Load한다.

## Page Replacement
Demand Paging의 경우 요구되는 Page를 backing store에서 가져온다. 하지만 프로그램을 계속 실행함에 따라서 demand page가 늘어나고 언젠가 Memory는 가득 차게 된다.\
Memory가 가득 차면 추가로 Page를 가져오기 위해서 어떤 Page를 backing store로 보내고(page-out) 그 빈 공간으로 필요한 Page를 가져온다.(page-in)\
이렇게 쫓겨난 Page를 Victim Page라고 한다.

I/O시간 절약을 위해서 modified되지 않은 페이지를 (변수의 경우 modify되는 경우가 많을 것이다.) victim page로 선택한다.\
여러 Page 중에서 Victim Page를 선택하는 방법은 아래 등이 있다.

* Random - 무작위로 Victim Page를 선택
* FIFO - 먼저 Load된 Page를 먼저 Victim Page로 선택
* OPT - 앞으로 가장 오래 사용되지 않을 Page와 교체 // 미래에 어떤 Page를 사용하지 않을지 모르므로 비현실적이다. 
* LRU - Least-Recently-Used

## Page Reference String

	CPU가 전달하는 주소 = 100 101 102 432 612 103 104 611 612
	Page Size가 100 Bytes라면
	페이지 번호는 1 1 1 4 6 1 1 6 6
	Page Reference String은 1 4 6 1 6 (Page Fault가 일어나지 않는 상황을 제외한다.)


## Global / Local Replacement
* Global Replacement - Memory 상의 모든 Process에 대해 교체
* Local Replacement - Memory 상의 자기 Process에 대해 교체
*Global Replacement가 더 효과적일 수 있다.*

---

# Frame Allocation
* Thrashing
CPU utilisation VS Degree of Multiprogramming\
Process의 개수가 증가함에 따라 CPU 이용률은 증가한다.\
하지만 일정 수준을 넘어서면 page in/out에 사용되는 overhead 때문에 CPU의 이용률이 오히려 감소한다. (Thrashing)

Thrashing을 극복하기 위해서 Global Replacement보다는 Local Replacement를 사용하는 편이 좋다.\
Process당 적절한 수의 **Frame을 할당**하는 것이 CPU 이용률 향상에 유리하다.

* Static Allocationn
	* Equal Allocation
	* Proportional Allocation
* Dynamic Allocation
	* Working Set Model - N 시간에 얼마만큼의 Frame을 사용할지를 과거의 수치를 통해서 예측한다. (Working set과 window를 통해서 예측)
	* Page Fault Frequency - Page Fault 발생 비율의 상한/하한선을 정하고 초과시에 더 많은 Frame을 할당, 미만시에 Frame을 회수한다.

## Page Size
Page의 일반적인 크기는 4KB ~ 4MB 수준이며 점점 커지는 경향을 띈다.\
Page의 크기는 아래에 영향을 끼친다.
* Internal Fragmentation
* Page-in, Page-out 시간
* Page Table Size
* Memory Resolution(사용되는 Memory의 밀도)
* Page Fault 발생 확률

PageTable은 원래 별도의 chip(TLB 캐시)에 저장되었으나, 최근에는 Cache 메모리와 함께 CPU에 적재된다.

---

# FILE Allocation
컴퓨터 시스템 자원 관리
* CPU - Process Management(CPU Scheduling, Process Synchronisation)
* 주기억장치 - Memory Management(Paging, Virtual Memory)
* 보조기억장치 - File System

Hard Disk(보조기억장치)는 Track(동심원)과 Sector(동심원의 일정한 길이의  외변)로 이루어진다.\
Sector의 크기는 일반적으로 512Bytes이지만 Sector 자체의 크기가 너무 작기 때문에 Sector의 집합인 Block을 사용한다.\
그렇기 때문에 하드디스크를 Block Device라고 한다.\
한 글자 (Character Size == 1Byte)를 저장하더라도 Hard Disk의 Block Size만큼의 용량을 차지하게 된다. Block Size는 OS가 정하게 된다.

각각의 파일에 대해서 Free Block을 어떻게 할당할 것인가? == FILE Allocation은 아래와 같은 방법을 사용한다.
* Contiguous Allocation - 각 파일을 연속된 Block에 할당한다. Header의 이동을 최소화하여 I/O 성능이 뛰어나다. 동영상, 음악 등의 매체에 적합하다. 순서대로 접근할 수도 있으며, 특정 부분을 바로 읽을 수도 있다. 하지만 생성, 삭제를 반복하면 Hole이 생겨서 낭비되는 부분이 생기기 쉽다.(External Fragmentation) 또한 File을 생성했을 때, 크기가 얼마나 될 것인가를 알 수 없다.
* Linked Allocation - Linked List처럼 각 Block이 다음 Block을 가리키는 4Bytes~의 포인터를 저장한다. External Fragmentation이 발생하지 않는다. 하지만 Direct Access가 불가능하며, 포인터가 끊어질 경우 더 이상 File에 접근하지 못하는 점, 느린 속도가 단점으로 남는다. 개선 방법으로 Windows에서 사용하는 FAT 파일시스템이 있다. 포인터들만 모은 File Allocation Table을 별도의 Block에 이중 저장(손상 시 복구를 위해서)하여 Direct Access와 속도를 개선했다.
* Indexed Allocation - Unix/Linux에서 사용하는 방식으로 File당 한 개의 Index Block을 가진다. 이 Index Block은 File의 포인터의 집합이며, Directory는 해당 Index block들을 가리킨다. Direct Access가 가능하며, External Segmentation이 없다. Index block을 할당하기 위해서 저장공간의 손실이 있다는 단점이 있다. 또한 Index Block의 최대 크기에 따라서 File의 최대 크기가 정해진다는 단점을 극복하기 위해서 Linked, Multilevel Index, Combined 같은 방식을 차용한다.

## Disk Scheduling
Disk 접근 시간은 Seek time + Rotational time + Transfer time으로 결정된다.\
이중 Cylinder를 탐색하는 Seek Time이 가장 크다.

Multi Process 환경에서는 Disk Queue에 많은 Request가 쌓이게 된다.\
이 Request를 가장 빠르게 처리하는 방법은 == Disk Scheduling

Disk Scheduling 방법은 아래와 같다.
* First-Come First-Serve
* Shortest-Seek-Time-First - 그 순간의 Head 위치에서 가장 가까운 Cylinder부터를 탐색하는 방법, Optimal하지 않으며 혼자 멀리 떨어진 Disk Request의 경우 Starvation 문제가 발생한다.
* Scan Scheduling - Head가 계속 Inward-Outward로 움직이며 이에 해당하는 Disk Request를 처리한다. Disk Queue의 Request가 Uniform Distribution을 따른다는 가정 하에 유용한 방법이다.

Scan Variants
1. C-Scan - Disk Cylinder idx의 끝에 도달하면 처음으로 돌아간다.
2. Look - Request의 상한, 하한까지만 탐색한다.
3. C-Look - C-Scan + Look

---

# Assembly
A processor is comprised of registers, stack, 


## Register
Working memory with different purposes, fixed width (32bit machine has 32bit registers, 64bit machines, 64bit registers)

## Stack
Array-like LIFO data structure that has a stack pointer and random access feature

x32 assembly
```
global _start # to make identifier accessible to the linker

_start: # identifier followed by a colon will create a label, labels are used to name locations in the code

mov eax, 1 # mov integer 1 to eax register
mov ebx, 42 # mov integer 42 to ebx register
int 0x80 # interrupt handler for system calls (hex 80), the system call it makes is determined by eax register.
# eax being 1 indicates the system exit call(end of the programme), whilst ebx is used to indicate the status.
```

```
nasm -f elf32 ex1.asm -o ex1.o # build 32bit elf object file (ELF = executabl and linking file, executable format used by Linux)
ld -m elf_i386 ex1.o -o ex1 # ld command to build an executable from an object file
```

```
$ ./ex1

$ echo $?
42
```

```
sub ebx, 29 # ebs -= 29
add ebx, ecx # ebx += ecx
mul ebx # eax \*= ebx
div edx # eax /= edx
```

```
section .data
    msg db "Hello, World!", 0x0a # save the string in db and add a newline character
    len equ $ - msg # len is eqaul to the current cursor - the start of msg

section .text
_start:
    mov eax, 4      ; sys_write system call
    mov ebx, 1      ; stdout file descriptor 
    mov ecx, msg    ; bytes to write
    mov edx, len    ; number of bytes to write
    int 0x80        ; perform system call

    mov eax, 1
    mov ebx, 0
    int 0x80    ; return successfully
```

```
    cmp ecx, 100    ; compare ecx with 100, store the result internally
    je  ; jump if equal
    jne ; jump if not eqaul
    jg  ; jump if greater
    jge ; jump if greater or eqaul
    jl  ; jump if less
    jle ; jump if less or eqaul
```

---

# Unix Domain Socket
```
Unix sockets are used as any other socket types. This means, that socket system calls are used for them. The difference between FIFOs and Unix sockets, is that FIFO use file sys calls, while Unix sockets use socket calls.

Unix sockets are addressed as files. It allows to use file permissions for access control.

Unix sockets are created by socket sys call (while FIFO created by mkfifo). If you need client socket, you call connect, passing it server socket address. If you need server socket, you can bind to assign its address. While, for FIFO open call is used. IO operation is performed by read/write.

Unix socket can distinguish its clients, while FIFO cannot. Info about peer is provided by accept call, it returns address of peer.

Unix sockets are bidirectional. This means that every side can perform both read and write operations. While, FIFOs are unidirectional: it has a writer peer and a reader peer.

Unix sockets create less overhead and communication is faster, than by localhost IP sockets. Packets don't need to go through network stack as with localhost sockets. And as they exists only locally, there is no routing.
```

---

# PID 0
Main Process(init, responsible for starting/shutting down)는 PID 1이 할당된다. 그렇다면 0은?\
PID 0 is reserved for swapper(or sched) which is responsible for paging. It is actually part of the kernel rather than a user process.

---

# Endian
* Big - 최상위 바이트가 앞에 오는 경우, 사람이 사용하는 방식이지만, 수가 커지면 (차지하는 바이트의 수가 늘어나면) 저장된 메모리를 오른쪽으로 옮겨야한다.
* Littel - 최상위 바이트가 앞에오지만, 그 다음 바이트가 왼쪽에 오는 방식. 디버깅이 어렵지만 수가 커지더라도 재배치에 따른 오버헤드가 발생하지 않는다.
* Intel이 Little Endian 방식을 사용하며, Motorola가 Big Endian을 사용한다.

```
	----------------------------
	|  |  |  |  |  |  |  |  |  |
	----------------------------

Big Endian의 경우 가장 앞의 바이트가 시작점을 차지하므로, 그 앞에 다른 바이트가 추가된다면 (수가 커진다면) 바이트의 배열 전체를 한 칸씩 옮겨야 한다는 단점이 있다.

eg) 123이 메모리에 |.....321|로 저장되었을 때, 1123으로 수정된다면 |....3211|으로 저장된 모든 바이트를 옮기는 방식이 Big Endian.
123이 메모리에 |321.....|로 저장되고, 1123으로 수정된다면 |3211....|로 수정되는 것이 Little Endian.

Big-endian is an order in which the "big end" (most significant value in the sequence) is stored first (at the lowest storage address). Little-endian is an order in which the "little end" (least significant value in the sequence) is stored first. For example, in a big-endian computer, the two bytes required for the hexadecimal number 4F52 would be stored as 4F52 in storage (if 4F is stored at storage address 1000, for example, 52 will be at address 1001). In a little-endian system, it would be stored as 524F (52 at address 1000, 4F at 1001).

For people who use languages that read left-to-right, big endian seems like the natural way to think of a storing a string of characters or numbers - in the same order you expect to see it presented to you. Many of us would thus think of big-endian as storing something in forward fashion, just as we read.

An argument for little-endian order is that as you increase a numeric value, you may need to add digits to the left (a higher non-exponential number has more digits). Thus, an addition of two numbers often requires moving all the digits of a big-endian ordered number in storage, moving everything to the right. In a number stored in little-endian fashion, the least significant bytes can stay where they are and new digits can be added to the right at a higher address. This means that some computer operations may be simpler and faster to perform.
```

---

# Atomicity
Single CPU machine일 경우에는 명령을 실행하는 sequence가 한 갈래를 가지며, 이 갈래가 interrupt 될 수 없다는 조건을 설정함으로써 Atomic Operation이 implement 된다.\
반면 Multi-core CPU machine에서는 한 CPU가 atomic operation이 발생한다는 신호를 다른 CPU들에게 전달한다. 신호를 전달받은 다른 CPU들은 해당하는 캐쉬를 Ram으로 flush함으로써 atomicity를 보장하게 된다.

---

# Coroutine

```
A coroutine is similar to a thread (in the sense of multithreading): it is a line of execution, with its own stack, its own local variables, and its own instruction pointer; but it shares global variables and mostly anything else with other coroutines. 
The main difference between threads and coroutines is that, conceptually (or literally, in a multiprocessor machine), a program with threads runs several threads in parallel. 
Coroutines, on the other hand, are collaborative: at any given time, a program with coroutines is running only one of its coroutines, and this running coroutine suspends its execution only when it explicitly requests to be suspended.
```

Coroutine은 multi-core 환경에서도 오직 하나의 coroutine만 동작할 수 있다. (병렬성 X, 다중 process에 속한 thread의 경우 multi-core에서 병렬하게 동작할 수 있음)\
즉 Coroutine은 독립적으로 실행되지 않고, 순서를 정하며 작동한다.

---

# Context Switching

```
Context Switching involves storing the context or state of a process so that it can be reloaded when required and execution can be resumed from the same point as earlier. This is a feature of a multitasking operating system and allows a single CPU to be shared by multiple processes.
```

## Context Switching Steps

The steps involved in context switching are as follows −

1. Save the context of the process that is currently running on the CPU. Update the process control block and other important fields.
2. Move the process control block of the above process into the relevant queue such as the ready queue, I/O queue etc.
3. Select a new process for execution.
4. Update the process control block of the selected process. This includes updating the process state to running.
5. Update the memory management data structures as required.
6. Restore the context of the process that was previously running when it is loaded again on the processor. This is done by loading the previous values of the process control block and registers.

## Context Switching Cost

Context Switching leads to an overhead cost because of TLB flushes, sharing the cache between multiple tasks, running the task scheduler etc.\
Context switching between two threads of the same process is faster than between two different processes as threads have the same virtual memory maps. Because of this TLB flushing is not required.

---

# File Storage vs Block Storage vs Object Storage

```
File storage organizes and represents data as a hierarchy of files in folders; block storage chunks data into arbitrarily organized, evenly sized volumes; and object storage manages data and links it to associated metadata.
```

## File Storage
* Data is stored as a single piece of information inside a folder.
* Computer needs to know the path to the file in order to access it.
* Data stored in files is organized and retrieved using a limited amount of metadata that tells the computer exactly where the file itself is kept.
* File storage has broad capabilities and can store just about anything. It’s great for storing an array of complex files and is fairly fast for users to navigate.
* File-based storage systems must scale out by adding more systems, rather than scale up by adding more capacity.

## Block Storage
* Block storage chops data into blocks and store them as separate pieces.
* Each block of data is given a unique identifier, which allows a storage system to place the smaller pieces of data wherever is most convenient.
* Block storage is often configured to decouple the data from the user’s environment and spread it across multiple environments that can better serve the data.
* Block storage doesn’t rely on a single path to data—like file storage does—it can be retrieved quickly.
* When data is requested, the underlying storage software reassembles the blocks of data from these environments and presents them back to the user.

## Object Storage
* Object storage is a flat structure in which files are broken into pieces and spread out among hardware.
* data is broken into discrete units called objects and is kept in a single repository, instead of being kept as files in folders or as blocks on servers.
* To retrieve the data, the storage operating system uses the metadata and identifiers, which distributes the load better and lets administrators apply policies that perform more robust searches.
* Object storage requires a simple HTTP API.
* Objects can’t be modified—you have to write the object completely at once.
