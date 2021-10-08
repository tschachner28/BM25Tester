from rank_bm25 import BM25L
import datetime

start_time = datetime.datetime.now()
corpus = {
    "use/enable privileged BPF operations, bpf, perform/run/execute a command/operation on an extended BPF map or program, bpf-helpers, (e)BPF helpers, print debugging messages, get the time since the system was booted, to interact with eBPF maps, or manipulate network packets, eBPF firewall, tc-bpf": "CAP_BPF",
    "change/modify/edit (file) UIDs and GIDs, enable changing file ownership, change the /etc/shadow file associated with the userID": "CAP_CHOWN",
    "Bypass file (read, write, execute, r, w, x) permission checks, allows a non-root user full file-system access, rename a root owned file, ignore permission bits of files, full access to filesystem": "CAP_DAC_OVERRIDE",
    "Bypass file read permission checks, bypass directory read and execute permission checks, invoke open_by_handle_at, obtain handle for a pathname and open file via a handle returned by a previous call to name_to_handle_at(), use the linkat AT_EMPTY_PATH flag, allows to ignore the read permission bits and  execute open_by_handle_at to read outside a container chroot, read/write/execute credentials": "CAP_DAC_READ_SEARCH",
    "Lock memory, mlock, lock virtual address space into RAM to prevent that memory from being paged to the swap area, blocks process memory from being swapped to disk, mlockall,  locks all of the calling process's virtual address space into RAM, mmap, map files or devices into memory, create new mapping in the virtual address space of the calling process, shmctl, System V shared memory control, perform control operation, allocate memory using huge pages, memfd_create, create an anonymous file, create file that lives in RAM and has a voltatile backing storage, mmap, shmctl": "CAP_IPC_LOCK",
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

preprocessed_corpus = {
    "use enable privileged bpf operations run execute command operation extended  map program bpf-helpers interact with eBPF helpers firewall print debugging messages get time since system booted manipulate network packets packet tc-bpf": "CAP_BPF",
    "change modify edit uid uids gid gids user group id ids file ownership /etc/shadow file userid chown": "CAP_CHOWN",
    "bypass read write execute r w x checks allow full filesystem access rename root owned file ignore permission bits": "CAP_DAC_OVERRIDE",
    "bypass file directory read execute permission checks credentials invoke open_by_handle_at obtain pathname handle open file via handle returned by previous call to name_to_handle_at linkat_empty_path flag outside container chroot": "CAP_DAC_READ_SEARCH",
    "lock memory mlock calling process virtual address space into ram prevent paged to swap area block process memory from swapped to disk mlockall mmap map files file devices device create new mapping shmctl System v shared control control operation allocate huge pages memfd_anonymous file volatile backing storage": "CAP_IPC_LOCK",
    "bypass permission checks check operations operation system v ipc objects object shmctl": "CAP_IPC_OWNER",
    "establish obtain new exclusive file lease arbitrary file f_setlease fcntl block other processes from opening /proc/sys/fs/lease-break-time seconds": "CAP_LEASE",
    "bind socket listen privileged low ports port numbers less than 1024": "CAP_NET_BIND_SERVICE",
    "make send receive socket sockets broadcast broadcasts listen multicast multicasts": "CAP_NET_BROADCAST",
    "use raw socket packet sockets bind any address transparent proxying so_bindtodevice": "CAP_NET_RAW",
    "set grant full file capabilities execute write access deploy capability sets": "CAP_SETFCAP",
    "manipulate process set gids supplementary gid list forge socket credentials unix domain sockets write group id groups ids mapping user namespace map setgroups setgid setegid setregid setresgid drop supplementary": "CAP_SETGID",
    "lower change process nice value setpriority set priority arbitrary processes real-time real time scheduling policies calling process priorities sched_setscheduler sched_setparam sched_setattr cpu affinity sched_setaffinity I/O input output class ioprio_set apply migrate_pages migrated to nodes move_pages mpol_mf_move_all flag mbind": "CAP_SYS_NICE",
    "ptrace trace arbitrary processes get_robust_list process_vm_readv process_vm_writev transfer data memory kcmp compare two processes determine share kernel resource virtual memory open file description descriptors filesystem information root working directory I/O context table signal dispositions list system v semaphore undo operations address space attach gdb debugger": "CAP_SYS_PTRACE",
    "reserved space ext2 filesystems ioctl controlling ext3 journaling override increase raise disk quota resource resources limits limits rlimit_nproc maximum max number consoles console allocation keymaps keymap more greater 64hz interrupts real-time clock msg_qbytes system v message queue above /proc/sys/kernel/msgmnb rlimit_nofile in-flight file descriptors bypassed process unix domain socket /proc/sys/fs/pipe-size-max set capacity pipe f_setpipe_sz fcntl pipe /proc/sys/fs/mqueue/queues_max /proc/sys/fs/mqueue/msg_max and /proc/sys/fs/mqueue/msgsize_max limits posix message queues prctl pr_set_mm operation oom_score_adj lower below cap_sys_resource change modify edit hard soft limit": "CAP_SYS_RESOURCE"
}

essential_keywords = {
    "CAP_BPF": ["bpf", "packet", "packets"],
    "CAP_IPC_LOCK": ["lock", "mlock", "mlockall", "mmap", "shmctl"],
    #"CAP_IPC_LOCK": ["lock"],
    "CAP_LEASE": ["lease", "leases"],
    "CAP_NET_BIND_SERVICE": ["bind", "ports", "port"],
    "CAP_NET_BROADCAST": ["broadcast", "broadcasts", "multicast", "multicasts"],
    "CAP_NET_RAW": ["raw", "packet"],
    "CAP_SETFCAP": ["fcap", "capabilities", "capability"],
    "CAP_SETGID": ["gid", "gids"],
    "CAP_SYS_PTRACE": ["trace", "ptrace"]
}

capabilities_ordering = {
    "CAP_BPF": 0, "CAP_CHOWN": 1, "CAP_DAC_OVERRIDE": 2, "CAP_DAC_READ_SEARCH": 3, "CAP_IPC_LOCK": 4, "CAP_IPC_OWNER": 5,
    "CAP_LEASE": 6, "CAP_NET_BIND_SERVICE": 7, "CAP_NET_BROADCAST": 8, "CAP_NET_RAW": 9, "CAP_SETFCAP": 10,
    "CAP_SETGID": 11, "CAP_SYS_NICE": 12, "CAP_SYS_PTRACE": 13, "CAP_SYS_RESOURCE": 14
}

#tokenized_corpus = [doc.split(" ") for doc in list(corpus.keys())]
tokenized_corpus = [doc.split(" ") for doc in list(preprocessed_corpus.keys())]
#bm25 = BM25Okapi(tokenized_corpus)
bm25 = BM25L(tokenized_corpus)

queries = ["manipulate network packets", "enable changing file ownership", "rename root owned file", "read credentials",
           "lock memory", "bypass permission checks", "lease", "bind low ports", "receive broadcasts",
           "so_bindtodevice", "write to file capability sets", "drop supplementary groups", "set priorities",
           "trace processes", "change hard limit", "shmctl",
           "bind ports less than 1024", "listen to multicast", "privileged bpf operations",
           "grant or remove capability in capability set", "manipulate process gids", "raise process nice value",
           "use raw and packet sockets", "mlock", "override write permisson checks", "change file uid"] # lowercase, no punctuation
answers = ["CAP_BPF", "CAP_CHOWN", "CAP_DAC_OVERRIDE", "CAP_DAC_READ_SEARCH", "CAP_IPC_LOCK", "CAP_IPC_OWNER",
           "CAP_LEASE", "CAP_NET_BIND_SERVICE", "CAP_NET_BROADCAST", "CAP_NET_RAW", "CAP_SETFCAP", "CAP_SETGID",
           "CAP_SYS_NICE", "CAP_SYS_PTRACE", "CAP_SYS_RESOURCE", "CAP_IPC_OWNER",
           "CAP_NET_BIND_SERVICE", "CAP_NET_BROADCAST", "CAP_BPF", "CAP_SETFCAP", "CAP_SETGID", "CAP_SYS_NICE",
           "CAP_NET_RAW", "CAP_IPC_LOCK", "CAP_DAC_OVERRIDE", "CAP_CHOWN"]

pass_count = 0
num_results = 0
for i, query in enumerate(queries):
    tokenized_query = query.split(" ")
    scores = bm25.get_scores(tokenized_query)
    print(scores)
    num_results = len([score for score in scores if score > 2.0]) # count number of matches
    matching_descriptions = bm25.get_top_n(tokenized_query, list(corpus.keys()), n=num_results) # return matches
    matching_capabilities = [corpus[description] for description in matching_descriptions]
    capabilities = []

    # choose capabilities whose scores indicate that they are the best match
    max_scores_capabilities = [matching_capabilities[0]]
    max_score = scores[capabilities_ordering[matching_capabilities[0]]]
    for i in range(1, len(matching_capabilities)):
        if scores[capabilities_ordering[matching_capabilities[i]]] >= max_score / 2:
            max_scores_capabilities.append(matching_capabilities[i])
    # capabilities = max_scores_capabilities if len(max_scores_capabilities) > 0 else capabilities
    matching_capabilities = max_scores_capabilities

    for cap in matching_capabilities: # Check if query contains the necessary keywords for given capability to be returned
        cap_contains_essential_keywords = False
        if cap in essential_keywords.keys():
            for word in tokenized_query:
                if word in essential_keywords[cap]:
                    cap_contains_essential_keywords = True
                    #query_contains_essential_keywords = True
                    break

        if cap_contains_essential_keywords:
            capabilities.append(cap)

    if len(capabilities) < 1: # if no essential keywords in query, disregard capabilities filtered using essential keywords
        capabilities = [c for c in matching_capabilities if c not in essential_keywords.keys()]
        if len(capabilities) < 1:
            capabilities = matching_capabilities

    print(query + ": " + str(capabilities))

end_time = datetime.datetime.now()
time_elapsed = end_time - start_time
print("Time elapsed: " + str(time_elapsed) + " for " + str(len(queries)) + " searches on " + str(len(corpus)) + " records")

