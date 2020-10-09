# MigratoryData config
## H/W
* 2 x Intel Xeon X5650 CPU at 2.66 GHz (6 cores per CPU, totaling 12 cores)
* 96 GB RAM (DDR3 at 1333 MHz)
* Network adapter Intel X520-DA2 (10 Gbps)
* CentOS / RHEL 7.1 with the default kernel 3.10.0-229 (without kernel recompilation)

## Kernel

	sysctl -w fs.file-max=12000500 // Kernel에서 open 할 수 있는 최대 파일의 개수
	sysctl -w fs.nr_open=20000500 // Process에서 open 할 수 있는 최대 파일의 개수
	ulimit -n 20000000 // shell과 shell에서 생성한 프로세스에 할당할 리소스 지정, n flag는 최대 file descriptor를 설정
	sysctl -w net.ipv4.tcp_mem='10000000 10000000 10000000' // 커널에서 tcp에 사용할 메모리의 크기 설정(unit = page = 4096 bytes) pressure를 가하는 최소값, pressure를 가하기 시작할 값, 최대 가질 수 있는 메모리
	sysctl -w net.ipv4.tcp_rmem='1024 4096 16384' // TCP socket의 read에 사용되는 버퍼의 크기, min, default, max
	sysctl -w net.ipv4.tcp_wmem='1024 4096 16384' // TCP socket의 write에 사용되는 버퍼의 크기, min, default, max
	sysctl -w net.core.rmem_max=16384 // TCP를 포함한 모든 socket의 read에 사용되는 버퍼의 크기 
	sysctl -w net.core.wmem_max=16384 // TCP를 포함한 모든 socket의 write에 사용되는 버퍼의 크기 
	
	//proc/irq에서 찾을 수 있는 network adapter의 smp_affinity 수정
	sysctl -w vm.nr_hugepages=30720 // 가장 최근에 사용한 page의 virtual-physical 주소 테이블을 저장하는 TLB를 효과적으로 사용하기 위해 JVM에서 normal page가 아닌 huge table을 사용하게 한다.

---
