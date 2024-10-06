from caches import *
import m5
from m5.objects import *

from m5.objects import StridePrefetcher

#path for the binary
binary = "tests/test-progs/hello/bin/x86/linux/hello"

system = System()
# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range
# Create a simple CPU
system.cpu = X86TimingSimpleCPU()

# system.cache_line_size = 128 # Set block size to 128 bytes
# Create an L1 instruction and data cache
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

system.cpu.dcache.prefetcher = StridePrefetcher(degree=4, latency=1)

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create a memory bus, a coherent crossbar, in this case
system.l2bus = L2XBar()
# Hook the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
# Create an L2 cache and connect it to the l2bus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)
# Create a memory bus
system.membus = SystemXBar()
# Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)
# create the interrupt controller for the CPU
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports
# Create a DDR3 memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.workload = SEWorkload.init_compatible(binary)
# Create a process for a simple "Hello World" application
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()
root = Root(full_system=False, system=system)
m5.instantiate()
print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")



