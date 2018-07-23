import time
from TaskList import *
import os
import pickle

SAVE_LOC = 'tasky_save.txt'

#Tasky

def load():
	file_obj = open(SAVE_LOC, 'rb')
	task_list = pickle.load(file_obj)
	return task_list

def main_screen():
	task_list = load()
	current_task = task_list.get_current_task()
	next_task = task_list.get_next_task()
	task_list = task_list.get_tasks()
	
	print('The current time is: ', end='')
	print('{0}'.format(time.strftime('%X')))
	print('Current Task: {0}'.format(current_task))
	#print('Next Task: {0}'.format(next_task))
	#print('Tasks: {0}'.format(task_list))
	
def add_task():
	task_list = load()
	task = str(input('Next Task (x to e(X)it):\n'))
	# Exit code
	if (task.lower() == 'x'):
	
		save(task_list)
		return False
	# Reset Tasky
	elif (task.lower() == 'reset'):
		new()
		return True
	# Correct current task
	elif (task.lower() == 'correct'):
		change = False
		task_change = str(input("Enter the corrected task:\n"))
		print('{0} will be replaced with {1}'.format(task_list.get_current_task(), task_change))
		if (confirm()):
			task_list.correct_task(task_change)
			save(task_list)
		return True
	elif (task.lower() == 'next'):
		task_list.inc_count()
		save(task_list)
		return True
	# Replace task and deliver new task
	else:
		task_list.add_task(task)
		
		save(task_list)
		return True

def confirm():
	confirm = str(input('Are you sure (y/n)?\n')).lower()
	while (confirm != 'y' and confirm != 'n'):
		confirm = str(input('Invalid Answer\nAre you sure? (y/n)?')).lower()
	if (confirm == 'y'):
		return True
	else:
		return False
		
def save(task_list):
	with open(SAVE_LOC, 'wb') as handle:
		pickle.dump(task_list, handle, -1)
	#print('Tasky Saved!')
	
def new():
	can_continue = False
	while (not(can_continue)):
		try:
			int_input = int(input('Number of tasks in the new list? (default is 3): '))
			if (int_input > 0):
				can_continue = True
		except:
			print("Must be an integer >0!")
	task_list = TaskList(int_input)
	task_list.populate_list()
	save(task_list)
	
def new_or_load():
	type_input = str(input('(N)ew List or (L)oad List?\n'))
	while (type_input[0] != 'n' and type_input[0] != 'l'):
		type_input = str(input('(N)ew List or (L)oad List?')).lower()
	if (type_input[0] == 'n'):
		new()
	else:
		task_list = load()
		save(task_list)

def main():
	print('Welcome to Tasky')
	task_list = new_or_load()
	main_screen()
	
	while (add_task()):
		print('\nTasky')
		main_screen()
	
main()