#!/usr/bin/env python3
#encoding=UTF-8

import os
import json

class TMS:
    quit_called = False

    def __init__(self, directory):
        os.chdir(directory)
        self.mode = 'tasks'
    
    def load(self):
        with open("tasks", encoding='UTF-8') as f:
            inp = json.load(f)
            self.tasks = inp['Tasks']
            self.info = inp['Info']

        with open("info", encoding='UTF-8') as f:
            inp = json.load(f)
            self.task_counter = inp['TaskCounter']
            self.info_counter = inp['InfoCounter']

    def save(self):
        if self.tasks == None:
            print("Tasks were not loaded")
            print("Exiting app to prevent data corruption")
            exit(1)
        with open('tasks', 'w', encoding='UTF-8') as f:
            json.dump({"Tasks": self.tasks, "Info": self.info}, 
                    f, ensure_ascii = False, indent=4)    
        with open('info', 'w', encoding='UTF-8') as f:
            json.dump({"TaskCounter": self.task_counter, 
                "InfoCounter": self.info_counter}, 
                    f, ensure_ascii = False, indent=4)    
        print('Progress has been saved.')

    def add_task(self, task):
        tags = input('Add |-separated tags:\n\t').strip().split('|')
        if tags == ['']:
            tags = []
        imm = input('Urgent? [0/1/y/n/д/н]\n\t')
        try:
            imm = {"0": False, "1": True ,"n": False, "y": True, "н": False, "д": True}[imm]
        except KeyError:
            print("Wrong key, operation aborted.")
            return 
        self.task_counter += 1
        self.tasks['Next'].append([self.task_counter, task, tags, imm])
        print('Task "{0}" was added to Next with tags {1} and with id {2}'.format(task, tags, self.task_counter))

    def add_info(self, info):
        tags = input('Add |-separated tags:\n\t').strip().split('|')
        if tags == ['']:
            tags = []
        self.info_counter += 1
        self.info['Noted'].append([self.info_counter, info, tags])
        print(f'Information {info} was noted with tags {tags} and with id {self.info_counter}')

    def switch_task_category(self, category, task_id):
        location, task_entry = self.find_task_by_id(task_id)
        if location is None:
            return
        self.tasks[category].append(task_entry)
        self.tasks[location].remove(task_entry)
        if category == 'Done' and location in ['Next', 'Current']:
            print(f'You did it!:) Task {task_entry[1]} with id {task_id} was completed!')
        elif category == 'Current' and location in ['Done', 'Failed']:
            print(f'Task {task_entry[1]} with id {task_id} was returned to Current!')
        elif category == 'Current' and location == 'Next':
            print(f'Moved task {task_entry[1]} with id {task_id} to Current!')  
        elif category == 'Next' and location == 'Current':
            print(f'Task {task_entry[1]} with id {task_id} was returned to Next!')     
        elif category == 'Failed' and location in ['Current', 'Next']:
            print(f'Task {task_entry[1]} was marked as Failed! Very sad :(')

    def delete_task(self, task_id):
        location, task_entry = self.find_task_by_id(task_id)
        if location is None:
            return
        self.tasks[location].remove(task_entry)
        print(f'Task {task_entry[1]} with id {task_id} was deleted from {location}!')    
        if task_id == self.task_counter:
            self.task_counter -= 1
            print('Counter has been reduced')
            
    def find_task_by_id(self, task_id):
        for i in self.tasks["Current"]:
            if i[0] == task_id:
                return ["Current", i]
        for i in self.tasks["Next"]:
            if i[0] == task_id:
                return ["Next", i]
        for i in self.tasks["Done"]:
            if i[0] == task_id:
                return ["Done", i]
        for i in self.tasks["Failed"]:
            if i[0] == task_id:
                return ["Failed", i]
        print(f'Could not find task with id {task_id}')
        return [None, None]


    def edit_task(self, task_id):
        location, task_entry = self.find_task_by_id(task_id)
        if location is None:
            return
        print(f'Task found in {location}')
        command = input('Enter new name:\n\t')
        if command == '_':
            command = task_entry[1]
        tags = input('Add |-separated tags:\n\t').split('|')
        if tags == ['']:    
            tags = []
        elif tags == ['_']:
            tags = task_entry[2]
        imm = input('Urgent? [0/1/y/n/д/н]\n\t')
        if imm == '_':
            imm = task_entry[3]
        else:
            try:
                imm = {"0": False, "1": True ,"n": False, "y": True, "н": False, "д": True}[imm]
            except KeyError:
                print("Wrong key, operation aborted.")
                return 
        
        print(f'Task {task_entry[1]} was renamed to {command}')        
        task_entry[1] = command
        task_entry[2] = tags
        task_entry[3] = imm
    
    def print_tasks(self, categories, list_of_tags):
        def print_category(self, category, tags_to_print):
            print_list = {True: [], False: []} # Urgent/Non-urgent
            for i in self.tasks[category]:
                if len(tags_to_print) == 0 or set(i[2]).intersection(tags_to_print).__len__():
                    print_list[i[3]].append(i)
            
            if len(print_list[True]) + len(print_list[False]):
                print(f'{category}: ')
                print('\tUrgent: ')
                for i in print_list[True]:
                    print(f'\t\t{i[0]}: {i[1]}', end = '')
                    if i[2] == []:
                        print()
                    else:
                        print(' ({0})'.format(', '.join(i[2])))
                print('\t{0}: '.format('Non-urgent'))
                for i in print_list[False]:
                    print('\t\t{0}: {1}'.format(i[0],i[1]),end = '')
                    if i[2] == []:
                        print()
                    else:
                        print(' ({0})'.format(', '.join(i[2])))
            else:
                print(f'{category} is empty!')
            
        print_category(self, "Current", list_of_tags)
        for param in categories:
            if param == 'n':
                print_category(self, "Next", list_of_tags)
            elif param == 'f':
                print_category(self, "Failed", list_of_tags)
            elif param == 'd':
                print_category(self, "Done", list_of_tags)
            else:
                print(f'Unknown parameter {param}')

    def print_info(self, categories, list_of_tags):
        def print_category(self, category, tags_to_print):
            print_list = []
            for i in self.info[category]:
                if len(tags_to_print) == 0 or set(i[2]).intersection(tags_to_print).__len__():
                    print_list.append(i)
            
            if len(print_list):
                print(f'{category}: ')
                for i in print_list:
                    print(f'\t{i[0]}: {i[1]}', end = '')
                    if i[2] == []:
                        print()
                    else:
                        print(' ({0})'.format(', '.join(i[2])))
            else:
                print(f'{category} is empty!')
            
        print_category(self, "Noted", list_of_tags)
        for param in categories:
            if param == 'a':
                print_category(self, "Acknowledged", list_of_tags)
            else:
                print(f'Unknown parameter {param}')

    def extract_tags(self, list_of_words):
        list_of_tags = []
        i = 0
        while i != len(list_of_words):
            if list_of_words[i] == '-t':
                list_of_words.pop(i)
                if i != len(list_of_words):
                    list_of_tags.append(list_of_words[i])
                    list_of_words.pop(i)
                else:
                    print('No tag followed')
            else:
                i += 1
        return list_of_tags

    def extract_params(self, list_of_words):
        i = 0
        list_of_params = []
        while i != len(list_of_words):
            if list_of_words[i][0] == '-':
                for letter in list_of_words[i][1:]:
                    list_of_params.append(letter)
                list_of_words.pop(i)
            else:
                i += 1
        return list_of_params

    def run(self):
        while not self.quit_called:
            command = input('Enter command: \n\t')
            command_splitted = command.split(' ')
            
            if command_splitted[0] in ['Q', 'q', 'й', 'Й']:
                self.save()
                print('Goodbye! :)')
                #os.system("clear")
                self.quit_called=True
            elif command_splitted[0] in ['S', 's', 'ы', 'Ы']:
                self.save()       
            elif command_splitted[0] == 'info':
                self.mode = 'info'
                print('Switched to Info')
            elif command_splitted[0] == 'tasks':
                self.mode = 'tasks'
                print('Switched to Tasks')
            elif command_splitted[0] == 'p':
                list_of_tags = self.extract_tags(command_splitted)
                list_of_params = self.extract_params(command_splitted)
                if self.mode == 'tasks':
                    self.print_tasks(list_of_params, list_of_tags)       
                else:
                    self.print_info(list_of_params, list_of_tags)       
            elif self.mode == 'tasks':
                if command_splitted[0] in ['D', 'd', 'в', 'В']:
                    self.switch_task_category('Done', int(command[2:]))
                elif command_splitted[0] in ['T', 't', 'е', 'Е']:
                    self.switch_task_category('Current', int(command[2:]))  
                elif command_splitted[0] in ['F', 'f', 'а', 'А']:
                    self.switch_task_category('Failed', int(command[2:]))       
                elif command_splitted[0].lower() in ['undone']:
                    self.switch_task_category('Current', int(command[7:]))  
                elif command_splitted[0].lower() in ['untake']:
                    self.switch_task_category('Next', int(command[7:]))  
                elif command_splitted[0] in ['R', 'r', 'к', 'К']:
                    self.edit_task(int(command[2:]))    
                elif command_splitted[0].lower() in ['del']:
                    self.delete_task(int(command[4:]))    
                else:
                    if input('Do you want to add this as a task? [Y/n, Д/н]:\n\t') in ['Y', 'y', 'Д', 'д']:
                        self.add_task(command)
            elif self.mode == 'info':
                if input('Do you want to add this as an info? [Y/n, Д/н]:\n\t') in ['Y', 'y', 'Д', 'д']:
                    self.add_info(command)



if __name__ == '__main__':
    tms = TMS('/home/er/PROJECTS/TMS')
    tms.load()
    tms.run()

