/*
 ============================================================================
 Name        : littleThread.h
 Author      : Robert Sheehan
 Version     : 1.0
 Description : header file for OS assignment 1 2017
 ============================================================================
 */

#include <setjmp.h>

/* The thread states */
enum state_t { SETUP, RUNNING, READY, FINISHED };

typedef struct thread {
	int tid;		// thread identifier so you know which thread you are talking about
	void (*start)();	// the start function which is called when we start the thread running
	jmp_buf environment;	// saved registers 
	enum state_t state;	// the state of the thread
	void *stackAddr;	// the stack address for use when disposing of the thread
	struct thread *prev;	// pointer to the previous thread
	struct thread *next;	// pointer to the next thread
} *Thread;
