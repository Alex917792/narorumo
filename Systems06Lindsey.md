This page archives ten questions I answered when I was studying for the Indiana University computer science Ph.D. qualifying exam in Systems during summer 2010.  I passed the exam in August 2010.  I leave this stuff here in case someone benefits from it. -- Lindsey

# One: Threads #

## Which of the following items are typically considered to be unique to a process, but not unique to a thread? ##
  * CPU registers
  * page table pointer
  * stack pointer
  * open files
  * segment table
  * child processes
  * program counter

## Answer ##

CPU registers: These are unique to a thread; they're part of the
context that gets saved when we swap a thread out.

Page table pointer: There is only one, OS-wide page table, so it
wouldn't make sense for each thread to have a pointer into the page
table; this would be a process-level notion if not an OS-level notion.

Stack pointer and program counter: These would have to be unique to a
thread; threads have to keep track of where they are in execution.

Open files: Unique to a process, not a thread; two threads in a
process might both access a file, even though only one of them opened
it.

Segment table: This keeps track of allocated and available memory in a
process' address space (for instance, the information in
/proc/pid/maps for a particular pid on Linux), so it's
process-specific, not thread-specific.

Child processes: An individual thread can't fork a child process; it
has to be done at the process level.  So, unique to a process, not a
thread.

So, in all, we've got:

  * CPU registers -- thread
  * page table pointer -- OS
  * stack pointer -- thread
  * open files -- process
  * segment table -- process
  * child processes -- process
  * program counter -- thread

In Tanenbaum (p. 102), we have:

| **Per process items**         | **Per thread items** |
|:------------------------------|:---------------------|
| Address space                 | Program counter      |
| Global variables              | Registers            |
| Open files                    | Stack                |
| Child processes               | State                |
| Pending alarms                |                      |
| Signals and signal handlers   |                      |
| Accounting information        |                      |

I'm right about open files, child processes, program counter, CPU
registers, stack pointer (I assume that is part of "stack").  "Address
space" could possibly count as "segment table", so that's OK too.  No
word about "page table pointer" -- I still think that that's OS-wide.

## Which of the following are true statements about user-level threads versus kernel-level threads? ##

  * Invoking any system call that might block poses an extra problem for user-level threads
  * User level threads are more vulnerable to priority inversion than kernel-level threads
  * There is less overall scheduling overhead in a user-level thread system
  * User level threads retain advantages on symmetric multiprocessors
  * Upcalls are necessary to implement user-level threads. (An upcall is a notification, provided by the kernel to the user-level thread run-time system, that a thread has blocked.)

## Answer ##

From Tanenbaum (p. 108 and thereabouts):

"Invoking any system call that might block poses an extra problem for
user-level threads" -- true.  If there are several user-level threads
in a process and one blocks on a system call, none of them can run
because as far as the kernel is concerned, the entire process is
blocking.  If the kernel is aware of threads it might be able to allow
those threads not blocking on the system call to run.

"User level threads are more vulnerable to priority inversion than
kernel-level threads" -- false.  I don't see any particular reason why
this would be the case.

"There is less overall scheduling overhead in a user-level thread
system" -- true, because there is no need to go into the kernel when a
thread is finished running in order to pick another thread to run;
thread scheduling and context switching can happen without calling int
the kernel.

"User level threads retain advantages on symmetric multiprocessors" --
false; I don't see any particular reason why this would be the case,
either.

"Upcalls are necessary to implement user-level threads." -- I would
say false, that upcalls are not _required_, although they might help
with scheduling.

# Two: CPU Efficiency #

Measurements of a certain system have shown that the average process
runs for a time T before blocking on I/O. A process switch requires
time S, which is effectively wasted (over-head). For round-robin
scheduling with quantum Q, give a formula for the CPU efficiency for
each of the following.

  * Q = infinity
  * Q > T
  * S < Q < T
  * Q = S
  * Q nearly 0

## Answer ##

Is the "CPU efficiency" the percentage of time spent actually
computing something?  Let's assume that that's the case.

Off the top of my head, I thought that round-robin scheduling with
quantum Q meant that each process got time Q, whether it needed it or
not; if it finished during its quantum, the CPU would be idle until
the end of the quantum.  Some googling (this question shows up
[all over](http://www.google.com/search?q=Measurement+of+a+certain+system+have+shown+that+the+average+process+runs+for+a+time+T+before+blocking+on+IO.)) suggests that that's not the case, and Tanenbaum (p. 154)
confirms it: "Each process is assigned a time interval, called its
quantum, during which it is allowed to run.  If the process is still
running at the end of the quantum, the CPU is preempted and given to
another process.  If the process has blocked or finished before the
quantum has elapsed, the CPU switching is done when the process
blocks, of course."

I don't know if we should include the context switch time S in Q, or
if it's in addition to Q, but let's assume that it's in addition to Q.

Q = infinity: The process will have the CPU until it blocks.  So, the
process will run for T; then the next process will run for T (plus the
S needed for the switch), and so on.  Each process will need T+S of
processor time to get T worth of work done, so the efficiency is
T/(T+S).  (Pretty good for CPU efficiency, but CPU efficiency may not
be the only thing we want to maximize!)

Q > T: If the quantum is large enough that processes always block on
I/O before it is over, the efficiency will be the same as in the
"infinity" example: T/(T+S).

S < Q < T: Here, processes don't finish running during their quantum.
We don't know how big of a difference there is between Q and T, but we
know that the process will require T/Q process switches during its
lifetime, and each of those will take time S, so, S `*` (T/Q) time
will be needed for context switching.  In all, we will need T + (S `*`
(T/Q)) time to get work done that should take time T if it were
allowed to happen all at once, so the efficiency is: T / (T + (ST/Q)).

Some clever people have simplified this as follows:

```
T            T              T              T              1          Q
--------  =  ----------- =  ----------- =  ----------- =  ------- =  ---
T + ST/Q     TQ/Q + ST/Q    (TQ + ST)/Q    T * (Q+S)/Q    (Q+S)/Q    Q+S
```

So, Q/(Q+S).

Q = S: Again, a process will need to do T/Q context switches in its
lifetime, and if Q is S, that's equal to T/S.  It'll need to do that S
times.  So, a total of T time spent context switching.  In all, we'll
need T time to do work plus T time spent context switching, so, T
/(T+T), or 50% efficiency.

Q = nearly 0: We won't even have time to do the context switching --
efficiency will go to 0 as Q goes to 0.

# Three: Semaphores #

Suppose we have two threads Ta and Tb that we would like to wait for
each other at a certain point in their execution

### Thread Ta ###

```
statement a1
rendezvous_a()
statement a2
```

### Thread Tb ###

```
statement b1
rendezvous_b()
statement b2
```

Here, we want Ta not to execute a2 until Tb has executed b1 and we
want Tb not to execute b2 until Ta has executed a1. That is, we want
the threads to "rendezvous" by calling rendezvous\_a() and
rendezvous\_b().

Give a semaphore-based solution for rendezvous\_a() and
rendezvous\_b(). Declare any variables you might need, along with their
initial values. Make sure that deadlock is not possible in your
solution.

## Answer ##

So, just to be clear, these orders of statements are OK:

a1, b1, a2, b2

b1, a1, a2, b2

a1, b1, b2, a2

b1, a1, b2, a2

But these aren't:

a1, a2, b1, b2

a1, a2, b2, b1

b1, b2, a1, a2

b1, b2, a2, a1

a1 and b1 both have to finish before either a2 or b2 may run.  I think
we should be able to do this:

```
semaphore sem = 2;

void rendezvous_a() {
down(sem);
while(sem > 0) { yield(); }
}

void rendezvous_b() {
down(sem);
while(sem > 0) { yield(); }
}
```

where yield() is a function that causes this thread to yield in favor
of some other thread (possibly running the scheduler).

Off the top of my head, I don't see deadlock in this.  Neither
`rendezvous` function can finish unless the other one is called, and
that can't happen unless we're past the statement we cared about
having happen.  One concern might be that the `wait()`ing doesn't
allow enough time for the other thread to run, so we'd have to make
sure to have the waiting period be long enough.

# Four: Deadlock #

Consider the following program with two concurrent processes foo and bar:

```
int x = 0, y = 0, z = 0;
sem lock1 = 1, lock2 = 1;

process foo {
  z = z + 2;
  P(lock1);
  x = x + 2;
  P(lock2);
  V(lock1);
  y = y + 2;
  V(lock2);
}

process bar {
  P(lock2);
  y = y + 1;
  P(lock1);
  x = x + 1;
  V(lock1);
  V(lock2);
  z = z + 1;
}
```

Here the variables lock1 and lock2 are semaphores and the P() and V()
functions are the associated "down" and "up" operations, respectively.

  * How might this program deadlock? You should demonstrate that the conditions you list specifically meet all of the conditions required for deadlock to occur.
  * Can the program deadlock in more than one state?
  * What are the possible final values of x, y, and z in the deadlock state? If the program can deadlock in more than one state, please specify which state results in the final values you give.
  * What are the possible final values of x, y, and z if the program terminates?

## Answer ##

"How might this program deadlock? You should demonstrate that the
conditions you list specifically meet all of the conditions required
for deadlock to occur."

For a deadlock to happen, each process has to be waiting for the other
one to release some resource before it can proceed, causing both to be
stuck forever.  As one example of deadlock, suppose that foo gets this
far:

> z = z + 2;
> P(lock1);
> x = x + 2;

Meanwhile, bar gets this far:

> P(lock2);
> y = y + 1;

Now bar tries to run

> P(lock1);

but can't because foo has the lock on lock1.  Meanwhile, foo tries to
run

> P(lock2);

but can't because bar has the lock on lock2.

To be a little more formal about it, let's show that this situation
meets the four conditions that must hold for there to be a deadlock
(Tanenbaum, p. 438):

Mutual exclusion: Is each resource either currently assigned to
exactly one process or available?  Yes.  There are two resources,
lock1 and lock2; lock1 is assigned to one process, foo; lock2 is
assigned to one process, bar.

Hold and wait: Can foo and bar request new resources?  Yes.  They're
each trying to request the lock that the other has.

No preemption: Can resources not be forcibly taken away from a
process?  Yes.  The only way to release the locks is for the processes
holding them to release them.

Circular wait: Is there a chain of two or more processes, each waiting
for a resource held by the next?  Yes.  foo is waiting for lock2,
which is held by bar; bar is waiting for lock1, which is held by foo.

Mnemonic: "MeRaNoPreC"

"Me" = mutual exclusion = each resource is either held by exactly one
process or available

"Ra" = requests allowed = processes can request more resources even if
they already have some

"NoPre" = no preemption = there's no way to get a resource away from a
process aside from that process explicitly releasing it

"C" = circularity = there's a chain of processes waiting for each
other

"Can the program deadlock in more than one state?"

I can only see the one state that would cause deadlock, although that
state could have been arrived at by more than one path (e.g., either
foo or bar could have started running first).

"What are the possible final values of x, y, and z if the program
terminates?"

If the program runs without deadlocking (say, if it behaves just as it
would have if foo ran to completion, followed by bar), we'd have:

x, y, and z are initialized: {x = 0, y = 0, z = 0}
z is incremented by 2: {x = 0, y = 0, z = 2}
x is incremented by 2: {x = 2, y = 0, z = 2}
y is incremented by 2: {x = 2, y = 2, z = 2}
y is decremented by 1: {x = 2, y = 1, z = 2}
x is decremented by 1: {x = 1, y = 1, z = 2}
z is decremented by 1: {x = 1, y = 1, z = 1}

So the final values of x, y, and z are all 1.

# Five: Virtual Memory #

Consider a system that uses 32-bit address and 3-level page
table. Among the 32-bit virtual addresses, 4 bits are used to index
into the first-level page table, 8 bits for the second-level, and
another 8 bits for the third-level.

  * What is the page size of this system?
  * If a page table entry is 2 bytes long, what is the size of the second-level page table?
  * Give reasons why the page size in a virtual memory system should neither be too large or too small.
  * What is a translation lookaside buffer (TLB) and what does it do?

## Answer ##

First, "what is the page size of this system?"  First let's talk about
how the 3-level page table works.  We have 32-bit addresses.  In a
given address, we're told that 4 of those bits index into the
first-level page table, which means that there can be 16 distinct
values, so the first-level page table has 16 rows, each of which point
us into one of 16 second-level tables.

Then, each address has 8 bits that index into a second-level page
table, so that's 256 values.  So the second-level table has 256 rows,
each of which points us into one of 256 third-level tables.  Finally,
each address has 8 bits that index into a third-level page table with
256 rows, each of which points us to a particular page.  Subtracting
the 4, 8, and 8, there are 12 bits left in the virtual address, so 12
bits left to determine location on that page.  2^12 = 4096, so there
are 4096 locations on the page.  If each location is a byte (that is,
if memory is byte-addressable in this system), then the page size is
4KB.  If memory is word-addressable with, say, 32-bit words (aka
4-byte words), then the page size is 4 times that, 16KB.

Second, "If a page table entry is 2 bytes long, what is the size of
the second-level page table?"

Well, we decided that there are really 16 separate second-level
tables, so let's figure out what the size of one is and then multiply
it by 16.  The table has 256 rows, so 256 `*` 2 bytes = 512 bytes.
Then, multiplying 512 bytes by 16, we get 8192 bytes or 8KB.  Each of
the 16 will probably have some constant amount of header information,
though, so in reality it will be a little larger.

Third, "Give reasons why the page size in a virtual memory system
should neither be too large or too small."

The appropriate page size depends on the nature and locality of the
data that needs to be brought into memory.  We can only bring data
into memory in increments of a page, so if we have large pages and we
only need a few bytes of data from each page we bring into memory,
then all of the other space that those pages take up in memory will be
wasted as far as we're concerned.  On the other hand, if we have small
pages and we need lots of data that's consecutive in memory, then it
would be more efficient to bring it in on large pages together and
avoid the per-page overhead of having to page in lots of small pages.

Fourth, "What is a translation lookaside buffer (TLB) and what does it do?"

(With some help from Wikipedia:) A TLB is typically a hardware cache
adjacent to the CPU that speeds the process of translating virtual
addresses to physical addresses.  When an address needs to be
translated, the TLB's mapping of virtual to physical addresses is
searched first.  If the TLB doesn't have a mapping for a particular
virtual address, we have to do a page table lookup, or page walk, of
that address, which is expensive, especially in the case of a
multi-level page table like this one, since we have to read several
memory locations in order to compute the physical address.  After the
address has been computed, it's saved in the TLB so it will be
available next time it's needed.

# Six: Caches #
Consider a program that accesses pages in the following order:

```
1,3,4,1,2,6,1,1,3,2,4,5,4,2,3,2,4
```

Assuming no pages are in memory when the program starts, show how many
page faults will occur when using the following replacement algorithms
and number of frames.

  * LRU, one frame
  * FIFO, one frame
  * LRU, three frames
  * FIFO, three frames

## Answer ##

From what I can tell on
[the Wikipedia page for "page replacement algorithm"](http://en.wikipedia.org/wiki/Page_replacement_algorithm), a frame is simply a slot in
memory that can hold a page.  Working on that assumption:

LRU, one frame: There's only room for one page in memory.  We'll
initially get a page fault when trying to access page 1, and we'll
page in page 1.  Then we'll get a page fault trying to access page 3,
and page it in, and so on.  We'll get a page fault every time we try
to access any page, unless it was the same as the previous one
accessed.  So, for the 17 page accesses, we'll get 16 page faults (all
except the repeated access of page 1).

FIFO, one frame: It will be the same as above; there's never a choice
of what to page out since there's only one frame, so the choice of
page replacement algorithm doesn't matter.

LRU, three frames: Now the choice of page replacement algorithm starts
to matter.  The accesses will go like this:

```
1 -- page fault; page in 1.
3 -- page fault; page in 3.
4 -- page fault; page in 4.
4 -- already there.
1 -- already there.
2 -- page fault; page out 3 since it's least recently accessed of {1, 3, 4} and page in 2.  Now memory contains {1, 4, 2}.
6 -- page fault; page out 4 and page in 6.  Now memory contains {1, 2, 6}.
1 -- already there.
1 -- already there.
3 -- page fault; page out 2 and page in 3.  Now memory contains {1, 6, 3}.
2 -- page fault; page out 6 and page in 2.  Now memory contains {1, 3, 2}.
4 -- page fault; page out 1 and page in 4.  Now memory contains {3, 2, 4}.
5 -- page fault; page out 3 and page in 5.  Now memory contains {2, 4, 5}.
4 -- already there.
2 -- already there.
3 -- page fault; page out 5 and page in 3.  Now memory contains {2, 4, 3}.
2 -- already there.
4 -- already there.
```

Whew.  still pretty bad, but this time we only had 10 page faults for
17 accesses.

FIFO, three frames:

```
1 -- page fault; page in 1.
3 -- page fault; page in 3.
4 -- page fault; page in 4.
4 -- already there.
1 -- already there.
2 -- page fault; page out 1 since it was first in and page in 2.  Memory: {3, 4, 2}.
6 -- page fault; page out 3 and page in 6.  Memory: {4, 2, 6}.
1 -- page fault; page out 4 and page in 1.  Memory: {2, 6, 1}.
1 -- already there.
3 -- page fault; page out 2 and page in 3.  Memory: {6, 1, 3}.
2 -- page fault; page out 6 and page in 2.  Memory: {1, 3, 2}.
4 -- page fault; page out 1 and page in 4.  Memory: {3, 2, 4}. 
5 -- page fault; page out 3 and page in 5.  Memory: {2, 4, 5}.
4 -- already there.
2 -- already there.
3 -- page fault; page out 2 and page in 3.  Memory: {4, 5, 3}.
2 -- page fault; page out 4 and page in 2.  Memory: {5, 3, 2}.
4 -- already there.
```

That time we got twelve page faults out of 17 page accesses, so, not
quite as good as LRU.

# Seven: Where's the Bottleneck? #

While running a job, the CPU utilization ratio is 15%, the paging-disk
utilization is 90%, and the network is used at 40% of its
capacity. Please identify which of the following may improve the
overall throughput of the program and explain why.

  * Install a faster CPU
  * Double the size of the memory
  * Double the network bandwidth
  * Double the size of the disk
  * Upgrade the paging algorithm to include pre-fetching
  * Increase the page size

## Answer ##

I'm going to assume that "paging-disk utilization" is the amount of
swap space that's being used.  It looks like this system is spending
most of its time swapping pages in and out.  Of the suggested ideas,
doubling the memory is most likely to help, because we'd have to swap
less often.  Increasing the page size and upgrading the paging
algorithm to use pre-fetching of pages could either hurt or help,
depending on the locality of the data.

Installing a faster CPU, increasing the network bandwidth, and
doubling the size of the disk are not likely to help: a faster CPU
might help if the CPU were pegged, but since CPU utilization is only
15%, it won't improve throughput.  Similarly, increasing the network
bandwidth won't improve throughput since network utilization is only
40%.  Doubling the size of the disk might actually hurt if it makes
the disk slower.

# Eight: Filesystems #

Consider a "standard" UNIX filesystem (with i-nodes, indirect blocks,
etc). Assume that the file block cache is initially empty, and that
the i-node cache initially contains the current working
directory. Assume "bar" exists in the current working directory.

Suppose a program executes the following sequence of instructions.
```
fd = Open("bar"); // open the file
Seek(fd,0); // seek to beginning of file
Write(fd, "A", 1); // write one byte
Close(fd); // close the file
```

Reading or writing one block or i-node requires 1 disk access.

  * What is the minimum number of disk accesses that this sequence of instructions could possibly require? If it is not possible to give an exact value, explain why and indicate what additional information is needed.
  * What is the maximum number of disk accesses that this sequence of instructions could possibly require? If it is not possible to give an exact value, explain why and indicate what additional information is needed.

## Answer ##

In this "standard" Unix filesystem, we'll assume that we need one
inode for every file, regardless of whether that file is a directory
or a leaf file.  For a leaf file, the inode contains information about
the file and a list of addresses for its data blocks.  For a
directory, the inode contains its children's names and inode numbers.
Let's also assume that the library containing the Open(), Seek(), and
Write() system calls is already loaded into memory.

When we call `fd = Open("bar");`, the inode cache contains the inode
for the current working directory, and that inode contains "bar" and
its inode number, so we don't need to access the disk to find "bar"s
inode number.  But then we need to read "bar"'s inode, requiring 1
disk access, so that we can find out what its first block is.
"bar"'s inode goes into the inode cache.

For the `Seek(fd,0);` call, we probably don't have to do another disk
access.

For `Write(fd, "A", 1);`, we have to bring the first block of "bar"
into the file block cache, requiring 1 disk access; then, after
writing, we have to write that block back to the disk, requiring 1
disk access.  (Depending on the implementation, the write might not
happen eagerly; it might not happen until we close the file, for
instance, but either way, one disk access is necessary for the write.

No disk accesses are necessary for `Close(fd);`.

So, there are a minimum of 2 disk accesses required by this sequence
of instructions.  What could cause the number to increase?  One
possibility is that accessing the file block cache or the inode cache
actually requires a disk access.  Another possibility is that the
Write() call is writing across a block boundary (unlikely in this
case, since we're only writing one byte), in which case we'd have to
bring in every block that's being written to.  Another, perhaps more
plausible reason, is that we can only do writes to the device in block
increments, so we actually have to read from the device into a buffer,
write our byte to the buffer, and then write back to the device,
increasing the number of necessary disk accesses by 1.

# Nine: System  Calls #

To access an operating system service, a user process must make a
system call. In a user program, the interface presented by a system
call is a library procedure with the same name as the system call, eg,
read(), which is prototyped as follows:

```
ssize_t read(int fd, void *buf, size_t count);
```

  * An operating system exists to provide a number of services and functions to users. What needs are met by having system calls?
  * What are the functional differences between a system call and a normal (non-system) function call? IE, what things must you do with a system call (and why) that you can't do with a normal function call?
  * What are the operational differences between a system call and a normal (non-system) function call? IE, what are some differences in how they are implemented?
  * What are the precise series of steps performed when a system call is invoked? If you like, you may illustrate your answer using the read() system call shown above (or you can use a system call of your choice).

## Answer ##

"What needs are met by having system calls?"

When programming at the user level, we don't have the power to
directly do things like read from the disk, write to the disk, write
to the screen, get input from the keyboard, and so on.  Instead, the
OS has to do these things for us, and we have to ask nicely by means
of system calls.  System calls provide a well-defined and safe
interface by which user programs can interact with the hardware.

"What are the functional differences between a system call and a
normal (non-system) function call? IE, what things must you do with a
system call (and why) that you can't do with a normal function call?"

(With some help from [the Wikipedia page for "system call"](http://en.wikipedia.org/wiki/System_call):) We usually need system calls to:
do device I/O (e.g., as in the above examples, or as in remote
devices); manage processes (e.g., create them, terminate them, send
signals to each other, have processes wait for signals, allocate
memory to a process, free memory belonging to a process); manage files
(e.g., create, delete, open, close); and to get information about the
OS (e.g., time, date).

"What are the operational differences between a system call and a
normal (non-system) function call?  IE, what are some differences in
how they are implemented?"

A normal function call can run in user space.  A system call requires
control to be transferred to the kernel, typically by means of an
interrupt or trap.  The details of how the transfer of control is
implemented vary depending on the platform and architecture.

"What are the precise series of steps performed when a system call is
invoked? If you like, you may illustrate your answer using the read()
system call shown above (or you can use a system call of your
choice)."

It varies depending on the platform and architecture, but for this
question, let's assume Linux and on an x86 architecture.  When read()
is invoked, its arguments fd, buf, and count are saved in registers,
and the system call number is saved in another register.  Control
passes to the kernel by means of an interrupt instruction.  The kernel
saves the contenst of all the registers, then looks at the register in
which the syscallno was saved and executes the code that is associated
with that system call number.  In the case of our read() system call,
it will have to read from disk, which may take some time, so the
scheduler runs and may schedule another process to run while this
process is blocking on disk I/O.  When the system call is finished
executing, it restores the contents of registers and returns control
to user space.

#summary Lindsey studies for the systems qual some more.

# Ten: Synchronization #

A doctor's office consists of a waiting room with n chairs and the
examination room containing the examination table.  If there are no
customers to be served, the doctor goes to sleep.  If a patient enters
the doctor's office and all waiting room chairs are occupied, then the
patient leaves the office.  If the doctor is busy but chairs are
available, then the patient sits in one of the free chairs.  If the
doctor is asleep, the patient wakes up the doctor.  Write an algorithm
that uses either POSIX threads or semaphores to coordinate the doctor
and the patients.

## Answer ##

Here's something inspired by the semaphore solution to the
producer/consumer problem in Tanenbaum p. 130.  The wrinkle here is
that if a patient comes in and all the chairs are full, the patient
process doesn't just wait; that patient just goes away.  That's why
the patient process needs the queue\_not\_full() check.

```
semaphore empty_chairs = n;
semaphore full_chairs = 0;
semaphore mutex = 1; /* for controlling access to the queue */

/* Doctor process -- runs forever */
void doctor() {
  patient p;

  while(1) {
    /* If full_chairs is already 0, then this down() call will just
       wait -- the equivalent of the doctor sleeping.  */
    down(&full_chairs);
    
    /* Critical region */
    down(&mutex);
    p = remove_patient_from_queue();
    up(&mutex);
    up(&empty_chairs);

    treat_patient(p);
  }
}

/* Patient process -- we'll have several of these */
void patient() {
  /* Critical region */
  down(&mutex);
  /* If the queue is full, don't do anything */
  if (queue_not_full()) {
    add_patient_to_queue();
    
    /* This call should never have to wait, since if we got this far,
    we know the queue isn't full. */
    down(&empty_chairs);

    /* This will wake up the doctor if he's sleeping. */
    up(&full_chairs);
  }
  up(&mutex);
}
```