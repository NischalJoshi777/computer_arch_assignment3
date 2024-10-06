import argparse
from importlib.metadata import requires
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import PrivateL1PrivateL2WalkCacheHierarchy
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import MESITwoLevelCacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator

parser = argparse.ArgumentParser()
#for command line arguments
parser.add_argument(
    "--checkpoint-path",
    type=str,
    required=False,
    default="virutal/",
    help="The directory to store the checkpoint.",
)
args = parser.parse_args()
# 1. Creating a simple processor
processor = SimpleProcessor(cpu_type= CPUTypes.TIMING,isa=ISA.X86,num_cores=1,)

# 2. Memory size
memory = SingleChannelDDR3_1600(size="1GB")

# Here we setup a MESI Two Level Cache Hierarchy.
cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="32kB", l1i_size="32kB", l2_size="512kB"
)

# Setup the board
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy
)

# Set the workloa
board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-5.4.49"),
    disk_image=obtain_resource("x86-ubuntu-18.04-img"),
    # readfile_contents=readfile_contents+ command
)

# Create and run the simulator
simulator = Simulator(
    board=board,
    full_system= True,
)

print("Beginning simulation!")
simulator.run()
print(
    "Exiting @ tick {} because {}.".format(
        simulator.get_current_tick(), 
        simulator.get_last_exit_event_cause()
    )
)
print("Taking checkpoint at", args.checkpoint_path)
simulator.save_checkpoint(args.checkpoint_path)
print("Done taking checkpoint")

# readfile_contents = """ echo "Setting boot arguments...";
# echo "console=ttyS0 root=/dev/sda1 rw" > /proc/cmdline;
# """
# command = """
# echo "Hello World"
# m5 exit;
# """

