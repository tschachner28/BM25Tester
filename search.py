from rank_bm25 import BM25Okapi
import datetime

start_time = datetime.datetime.now()
corpus = {
    "use/enable privileged BPF operations, bpf, perform/run/execute a command/operation on an extended BPF map or program, bpf-helpers, (e)BPF helpers, print debugging messages, get the time since the system was booted, to interact with eBPF maps, or manipulate network packets, eBPF firewall, tc-bpf": "CAP_BPF",
    "change/modify/edit (file) UIDs and GIDs, enable changing file ownership, change the /etc/shadow file associated with the userID": "CAP_CHOWN",
    "Bypass file (read, write, execute, r, w, x) permission checks, allows a non-root user full file-system access, rename a root owned file, ignore permission bits of files, full access to filesystem": "CAP_DAC_OVERRIDE",
    "Bypass file read permission checks, bypass directory read and execute permission checks, invoke open_by_handle_at, obtain handle for a pathname and open file via a handle returned by a previous call to name_to_handle_at(), use the linkat AT_EMPTY_PATH flag, allows to ignore the read permission bits and  execute open_by_handle_at to read outside a container chroot, read/write/execute credentials": "CAP_DAC_READ_SEARCH",
    "Lock memory, mlock, lock virtual address space into RAM to prevent that memory from being paged to the swap area, blocks process memory from being swapped to disk, mlockall,  locks all of the calling process's virtual address space into RAM, mmap, map files or devices into memory, create new mapping in the virtual address space of the calling process, shmctl, System V shared memory control, perform control operation, allocate memory using huge pages, memfd_create, create an anonymous file, create file that lives in RAM and has a voltaile backing storage, mmap, shmctl": "CAP_IPC_LOCK",
    "Bypass permission checks for operations on System V IPC objects, use the shmctl function": "CAP_IPC_OWNER",
    "Establish (new) (file) lease (on arbitrary file), F_SETLEASE, fcntl, obtain an exclusive lease on the file, block other processes from opening the file for up to /proc/sys/fs/lease-break-time seconds": "CAP_LEASE",
    "Bind a socket to/listen to privileged ports (port numbers less than 1024), bind low ports as non-root user": "CAP_NET_BIND_SERVICE",
    "Make socket broadcasts, listen to multicasts, send/receive broadcasts": "CAP_NET_BROADCAST",
    "Use RAW sockets, use PACKET sockets, bind to any address for transparent proxying, SO_BINDTODEVICE": "CAP_NET_RAW",
    "Set file capabilities, execute the file, have write access to the file, deploy as non-root user, grant full capabilities to a file, write to file capability sets which are stored in an extended attribute": "CAP_SETFCAP",
    "Manipulate process GIDs and supplementary GID list, forge GID when passing socket credentials via UNIX domain sockets, write a group ID mapping in a user namespace, gid_map, allow non-root user to set GID, setgroups(), setgid(), setegid(), setregid(), setresgid(), set supplementary group IDs of a user, drop supplementary groups": "CAP_SETGID",
    "Lower the process nice value - nice setpriority - and change the nice value for arbitrary processes; set real-time scheduling policies for calling process, and set scheduling policies and priorities for arbitrary processes - sched_setscheduler, sched_setparam, sched_setattr; set CPU affinity for arbitrary processes - sched_setaffinity; set I/O scheduling class and priority for arbitrary processes ioprio_set; apply migrate_pages to arbitrary processes and allow processes to be migrated to arbitrary nodes; apply move_pages to arbitrary processes; use the MPOL_MF_MOVE_ALL flag with mbind and move_pages; set priorities": "CAP_SYS_NICE",
    "ptrace, trace arbitrary processes, get_robust_list, process_vm_readv, process_vm_writev, transfer data to or from the memory of arbitrary processes, kcmp, compare two processes to determine if they share a kernel resource: virtual memory, open file description, open file descriptors, filesystem information, working directory, filesystem root, I/O context, table of signal dispositions, list of System V semaphore undo operations, address space, attach GDB to a process, attach debugger to process, trace processes you can't send signals to": "CAP_SYS_PTRACE",
    "Use reserved space on ext2 filesystems; make ioctl calls controlling ext3 journaling; override disk quota limits; increase resource limits; override RLIMIT_NPROC resource limit; override maximum number of consoles on console allocation; override maximum number of keymaps; allow more than 64hz interrupts from the real-time clock; raise msg_qbytes limit for a System V message queue above the limit in /proc/sys/kernel/msgmnb; allow the RLIMIT_NOFILE resource limit on the number of in-flight file descriptors to be bypassed when passing file descriptors to another process via a UNIX domain socket; override the /proc/sys/fs/pipe-size-max limit when setting the capacity of a pipe using the F_SETPIPE_SZ fcntl command; use F_SETPIPE_SZ to increase the capacity of a pipe above the limit specified by /proc/sys/fs/pipe-max-size; override /proc/sys/fs/mqueue/queues_max, /proc/sys/fs/mqueue/msg_max, and /proc/sys/fs/mqueue/msgsize_max limits when creating POSIX message queues (see mq_overview(7)); employ the prctl PR_SET_MM operation; set /proc/[pid]/oom_score_adj to a value lower than the value last set by a process with CAP_SYS_RESOURCE, change hard/soft limit": "CAP_SYS_RESOURCE"
}

tokenized_corpus = [doc.split(" ") for doc in list(corpus.keys())]
bm25 = BM25Okapi(tokenized_corpus)

queries = ["manipulate network packets", "enable changing file ownership", "rename root owned file", "read credentials",
           "lock memory", "bypass permission checks", "lease", "bind low ports", "receive broadcasts",
           "SO_BINDTODEVICE", "write to file capability sets", "drop supplementary groups", "set priorities",
           "trace processes", "change hard limit", "shmctl"]
answers = ["CAP_BPF", "CAP_CHOWN", "CAP_DAC_OVERRIDE", "CAP_DAC_READ_SEARCH", "CAP_IPC_LOCK", "CAP_IPC_OWNER",
           "CAP_LEASE", "CAP_NET_BIND_SERVICE", "CAP_NET_BROADCAST", "CAP_NET_RAW", "CAP_SETFCAP", "CAP_SETGID",
           "CAP_SYS_NICE", "CAP_SYS_PTRACE", "CAP_SYS_RESOURCE", "CAP_IPC_OWNER"]

pass_count = 0
num_results = 0
for i, query in enumerate(queries):
    tokenized_query = query.split(" ")
    scores = bm25.get_scores(tokenized_query)
    print(scores)
    num_results = len([score for score in scores if score > 1.0]) # count number of matches
    matching_descriptions = bm25.get_top_n(tokenized_query, list(corpus.keys()), n=num_results) # return matches
    capabilities = [corpus[description] for description in matching_descriptions]

    #test_result = "PASS" if capabilities[0] == answers[i] else "FAIL" # checks whether result is as expected
    #pass_count += 1 if test_result == "PASS" else 0
    #print(query + ": " + str(capabilities) + " - " + str(test_result))
    print(query + ": " + str(capabilities))

end_time = datetime.datetime.now()
time_elapsed = end_time - start_time
#print(str(pass_count) + "/" + str(len(queries)) + " tests passed")
print("Time elapsed: " + str(time_elapsed) + " for " + str(len(queries)) + " searches on " + str(len(corpus)) + " records")

