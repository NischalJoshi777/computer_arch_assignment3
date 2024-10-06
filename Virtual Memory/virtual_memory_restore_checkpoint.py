from pathlib import Path
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import (
    obtain_resource,
)
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.X86, num_cores=1)

memory = SingleChannelDDR3_1600(size="1GB")


cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="32kB", l1i_size="32kB", l2_size="512kB"
)

# Setup the board.
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Create the shell script to write, compile, and run the C++ Hello World program
readfile_contents = """
cd tests/test-progs/hello/bin/x86/linux/hello;  # Navigate to the directory containing hello
./hello;                      # Execute the hello program
m5 exit;                      # Exit the simulation after running hello
"""

# Set the Full System workload.
board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-5.4.49"),
    disk_image=obtain_resource("x86-ubuntu-18.04-img"),
    checkpoint=  Path("/Users/nischaljsh/Documents/gem5/virutal"),
)

board.readfile = Path("tests/test-progs/hello/bin/x86/linux/hello")

#modifying table buffer
def modify_tlb_after_init():
    for cpu in board.processor.get_cores():
        # Access the MMU of the core and modify ITLB and DTLB
        mmu = cpu.core.mmu
        mmu.itb.size = 128  
        mmu.dtb.size = 128 

modify_tlb_after_init()


sim = Simulator(board=board, full_system=True)
print("Restoring from checkpoint and beginning simulation!")
sim.run()
print(
    "Exiting @ tick {} because {}.".format(
        sim.get_current_tick(), 
        sim.get_last_exit_event_cause()
    )
)
