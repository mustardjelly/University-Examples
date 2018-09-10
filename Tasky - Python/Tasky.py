import time
from TaskList import *
import os
import pickle

SAVE_LOC = 'tasky_save.txt'

#Tasky
def print_commands():
	comm_dict = {}
	comm_dict['x'] = "Exit"
	comm_dict['reset'] = "Reset tasky"
	comm_dict['correct'] = "Edit the current task"
	comm_dict['next'] = "Skip to the next task but do not change it"
	
	print("{0:^30}".format("COMMANDS"))
	for key in comm_dict:
		print("{0:>10} : {1}".format(key, comm_dict[key]))

def load():
	file_obj = open(SAVE_LOC, 'rb')
	task_list = pickle.load(file_obj)
	return task_list

def main_screen():
	task_list = load()
	current_task = task_list.get_current_task()
	task_list = task_list.get_tasks()
	print_main(current_task)
	
def print_main(current_task):	
	print('The current time is: ', end='')
	print('{0}'.format(time.strftime('%X')))
	print('Current Task: {0}'.format(current_task))
	
def exit(task_list):
	save(task_list)
	return False
	
def add_task():
	task_list = load()
	task = str(input('Task to add? {0} will be over-written: '.format(task_list.get_current_task())))
	comm = task.lower()
	
	# Exit code
	if (comm == 'x'):
		return exit(task_list)
	if (comm == '?'):
		print_commands()
		return True
	# Reset Tasky
	elif (comm == 'reset'):
		task_list = new()
	# Correct current task
	elif (comm == 'correct'):
		task_change = str(input("Enter the corrected task:\n"))
		print('{0} will be replaced with {1}'.format(task_list.get_current_task(), task_change))
		if (confirm()):
			task_list.correct_task(task_change)
	elif (comm == 'next'):
		task_list.inc_count()
	# Replace task and deliver new task
	else:
		task_list.add_task(task)
	
	save(task_list)
	return True

def confirm(task_list, task_change):
	while True:
		confirm = str(input('Are you sure (y/n)?\n')).lower()
		if (confirm == 'y'):
			return True
		elif (confirm == 'n'):
			return False
		
def save(task_list):
	with open(SAVE_LOC, 'wb') as handle:
		pickle.dump(task_list, handle, -1)
	
def new():
	while (True):
		try:
			int_input = int(input('Number of tasks in the new list? (default is 3): '))
			if (int_input > 0):
				break
			else:
				print("Must be greater than 0!") 
		except (ValueError):
			int_input = 3
			break
			
	task_list = TaskList(int_input)
	task_list.populate_list()
	return task_list
	
def init():
	while True:
		type_input = str(input('(N)ew List or (L)oad List?\n')).lower()
		if (type_input == 'n'):
			task_list = new()
			save(task_list)
			break
		elif (type_input == 'l'):
			return load()

def main():
	print('Welcome to Tasky')
	task_list = init()
	
	while (True):
		if (add_task()):
			print('\nTasky')
			main_screen()
		else:
			break
	
main()