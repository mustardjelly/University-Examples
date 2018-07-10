/*
	The threads.
*/

void thread1() {
	int i;
	for (i = 0; i < 4; i++)
		puts("hi");
}

void thread2() { 
	int i;
	for (i = 0; i < 5; i++)
		puts("bye");
}

const int NUMTHREADS = 3;

// An array of the functions which should be called for each thread
// threadFuncs[0] = thread1
typedef void (*threadPtr)();
threadPtr threadFuncs[] = {thread1, thread2, thread1};
