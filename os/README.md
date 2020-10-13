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
