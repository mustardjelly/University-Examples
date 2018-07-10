/*
 ============================================================================
 Name        : OSA1.2.c
 Author      : Sam Powell
 UPI         : mgu011
 Version     : 1.0
 Description : Thread yield implementation. (P2)
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

#include "littleThread.h"
#include "threads2.c" // rename this for different threads

Thread newThread; // the thread currently being set up
Thread mainThread; // the main thread
Thread head;
Thread executing; // the currently executing thread
struct sigaction setUpAction; // group of information about a signal handler called SetUpAction

// remove Thread and all links from linked list
void threadRemoval(Thread aThread) {
	// if thread is the only job in the list
	if (aThread->next->tid == aThread->tid) {
		// clear significant thread pointers
		head = NULL;
		executing = NULL;
	} else {
		head = aThread->next; //head moves to the next item in the list
		// delete regerences to this thread
		aThread->prev->next = aThread->next;
		aThread->next->prev = aThread->prev;
		executing = aThread->next; // executing switches to the next thread
	}
	// delete references on this thread, may not need to be done?
	aThread->next = NULL;
	aThread->prev = NULL;
	free(aThread->stackAddr); // Wow!
}


// convert state integers to names
const char* getStateName(int state) 
{
	switch (state) 
	{
		case 0: return "setup";
		case 1: return "running";
		case 2: return "ready";
		case 3: return "finished";
	}
}

// print the state of all threads
void printThreadStates() {
	Thread currentThread = head;
	printf("\nThread States\n=============\n");
	for (int i = 0; i < NUMTHREADS; i++) {
		printf("threadID: %d ", i);
		// if thread exists in linked list
		if (currentThread != NULL && currentThread->tid == i){
			printf("state:%s\n", getStateName(currentThread->state));
			currentThread = currentThread->next;
		} else { // else we know the thread has finished
			printf("state:finished\n");
		}
		
	}
	puts("");
}

/*
 * Switches execution from prevThread to nextThread.
 */
void switcher(Thread prevThread, Thread nextThread) {
	if (prevThread->state == FINISHED) { // it has finished
		printf("disposing %d\n", prevThread->tid);
		threadRemoval(prevThread);
		if (executing){
			nextThread->state = RUNNING;
			printThreadStates();
			longjmp(nextThread->environment, 1);//move to nextThread
		} else {
			longjmp(mainThread->environment, 1);//go back to main
		}
	// freeze where I am
	} else if (setjmp(prevThread->environment) == 0) { // so we can come back here
		// if the previous thread is not finished
		prevThread->state = READY;
		nextThread->state = RUNNING;
		printThreadStates();
		//printf("scheduling %d\n\n", nextThread->tid);
		// return to associateStack and carry out the code we were up to (if statement of associateStack)
		longjmp(nextThread->environment, 1); //
	}
}

// runs all threads, can be modified to determine which thread to run next
void scheduler() {
	// if nothing is executing; (first call)
	if (executing == NULL) {
		executing = head; // set executing thread
		// switching from mainThread to the thread declared as executing
		switcher(mainThread, executing);
	} else {
		executing = executing->next; // change executing thread to next thread
		switcher(executing->prev, executing);
	}
}

void threadYield() {
	scheduler(); // logic for switching occurs in scheduler
}

/*
 * Associates the signal stack with the newThread.
 * Also sets up the newThread to start running after it is long jumped to.
 * This is called when SIGUSR1 is received.
 */
void associateStack(int signum) {
	Thread localThread = newThread; // what if we don't use this local variable?
	localThread->state = READY; // now it has its stack
				    // thread is "ready" to run now
	// setjmp like an exception handler
	// remembers where you are (saves registers of your process)
	// variables on the stack will be the same
	// if setjmp returns 0, you have callled setjmp
	if (setjmp(localThread->environment) != 0) { // will be zero if called directly
		// call the start routine of our thread
		// runs to completion
		(localThread->start)();
		localThread->state = FINISHED;
		// start up a new one
		// if all jobs are done back to main thread
		if (head == NULL){
			switcher(localThread, mainThread); // back to the main thread
		} else { // otherwise switch to the next job in the list
			switcher(localThread, localThread->next); // to the next thread
		}
	}
}
/*
 * Sets up the user signal handler so that when SIGUSR1 is received
 * it will use a separate stack. This stack is then associated with
 * the newThread when the signal handler associateStack is executed.
 */
void setUpStackTransfer() {
	/* Where I want to go to ((void *) associateStack) if SIGUSR1 arrives
	 * at this process
	 */
	setUpAction.sa_handler = (void *) associateStack; 
	setUpAction.sa_flags = SA_ONSTACK;
	/* man sigaction
	   set up a stack for each thread we create
	   SIGUSR1 signal
	   &setUpAction address of information
	 */
	sigaction(SIGUSR1, &setUpAction, NULL);
}

/*
 *  Sets up the new thread.
 *  The startFunc is the function called when the thread starts running.
 *  It also allocates space for the thread's stack.
 *  This stack will be the stack used by the SIGUSR1 signal handler.
 */
Thread createThread(void (startFunc)()) {
	static int nextTID = 0; // static must be stored in a different area of memory
	Thread thread;
	stack_t threadStack; 	// threadStack is a variable of type stack_t
				// structure which stores information about the stack
	// Allocating space for the information of the thread
	if ((thread = malloc(sizeof(struct thread))) == NULL) {
		perror("allocating thread");
		exit(EXIT_FAILURE);
	}
	thread->tid = nextTID++; // non-instance variable
	thread->state = SETUP;
	thread->start = startFunc;
	// Allocating space for the stack of the thread
	// amount of memory = SIGSTKSZ (16K?)
	// When you write a call in C which may return an error you must attempt to handle the area
	if ((threadStack.ss_sp = malloc(SIGSTKSZ)) == NULL) { // space for the stack
		perror("allocating stack");
		exit(EXIT_FAILURE);
	}
	// ss_sp = stack pointer
	thread->stackAddr = threadStack.ss_sp;
	threadStack.ss_size = SIGSTKSZ; // the size of the stack
	threadStack.ss_flags = 0;
	// man sigaltstack
	// the memory ive just allocated will become our stack. Initiated every time
	if (sigaltstack(&threadStack, NULL) < 0) { // signal handled on threadStack
		perror("sigaltstack");
		exit(EXIT_FAILURE);
	}
	newThread = thread; // So that the signal handler can find this thread
	// kill is the system call that sends signals
	// stacks set up but not associated with anything
	// getpid() kill is sending a signal to its first parameter. This is sending a signal
	// to yourself. 
	// SIGUSR1 is the signal which is being sent
	// Since it has a handler for that signal, jumps to associateStack
	kill(getpid(), SIGUSR1); // Send the signal. After this everything is set.
	return thread;
}

int main(void) {
	struct thread controller;
	Thread threads[NUMTHREADS];
	mainThread = &controller;
	mainThread->state = RUNNING;
	setUpStackTransfer();
	// create the threads
	for (int t = 0; t < NUMTHREADS; t++) {
		threads[t] = createThread(threadFuncs[t]);
	}
	// create doubly linked list with thread pointers
	for (int t = 0; t < NUMTHREADS; t++) {
		if (t == 0) { // first thread
			threads[t]->next = threads[0];
			threads[t]->prev = threads[0];
			head = threads[t];
		} // last thread
		else if (t == NUMTHREADS - 1) {	
			threads[t]->next = threads[0];
			threads[t]->prev = threads[(t-1)];
			threads[t-1]->next = threads[t];
			threads[0]->prev = threads[t];
		}
		else { // middle thread
			threads[t]->next = threads[0];
			threads[t]->prev = threads[(t-1)];
			threads[t-1]->next = threads[t];
			threads[0]->prev = threads[t];
		}
	}

	printThreadStates();
	puts("switching to first thread");
	scheduler();
	
	puts("\nback to the main thread");
	printThreadStates();
	
	return EXIT_SUCCESS;
}
