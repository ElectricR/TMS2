#encoding=UTF-8

import os
import json

os.chdir('/home/er')

with open("tasks", encoding='UTF-8') as f:
    info = json.load(f)
    #info = {'Counter': 0, "Tasks": {'Done': [], 'Current': [], 'Next': []}}
    tasks = info['Tasks']
    global_counter = info['Counter']
    binds = info['Binds']

quit_called = False

def save_tasks(tasks, global_counter, binds):
    with open('tasks', 'w', encoding='UTF-8') as f:
        info['Tasks'] = tasks
        info['Counter'] = global_counter
        info['Binds'] = binds
        json.dump(info, f, ensure_ascii = False, indent=4)    
        print('Progress has been saved.')

def add_task(tasks, task):
    global global_counter
    tags = input('Add |-separated tags:\n\t').split('|')
    if tags == ['']:
        tags = []
    imm = input('Urgent? [0/1/y/n/д/н]\n\t')
    try:
        imm = {"0": False, "1": True ,"n": False, "y": True, "н": False, "д": True}[imm]
    except KeyError:
        print("Wrong key, operation aborted.")
        return 
    global_counter += 1
    tasks['Next'].append([global_counter, task, tags, imm])
    print('Task "{0}" was added to Next with tags {1} and with id {2}'.format(task, tags, global_counter))

def complete_task(tasks, task_id):
    for i in tasks['Current']:
        if i[0] == task_id:
            tasks['Done'].append(i)
            tasks['Current'].remove(i)
            print('You did it!:) Task "' + i[1]+'" with id '+str(i[0]) + ' was completed!')
            return
    for i in tasks['Next']:
        if i[0] == task_id:
            tasks['Done'].append(i)
            tasks['Next'].remove(i)
            print('You did it!:) Task "' + i[1]+'" with id '+str(i[0]) + ' was completed!')
            return
    print(f'Could not find task with id {task_id}')
    
            
def undone_task(tasks, task_id):
    for i in tasks['Done']:
        if i[0] == task_id:
            tasks['Current'].append(i)
            tasks['Done'].remove(i)
            print('Task "{0}" with id {1} was returned to Current!'.format(i[1], str(i[0])))
  
            
def untake_task(tasks, task_id):
    for i in tasks['Current']:
        if i[0] == task_id:
            tasks['Next'].append(i)
            tasks['Current'].remove(i)
            print('Task "{0}" with id {1} was returned to Next!'.format(i[1], str(i[0])))     
            
def fail_task(tasks, task_id):
    for i in tasks['Current']:
        if i[0] == task_id:
            tasks['Failed'].append(i)
            tasks['Current'].remove(i)
            print('Task "{0}" was marked as Failed! Very sad :('.format(i[1]))
    for i in tasks['Next']:
        if i[0] == task_id:
            tasks['Failed'].append(i)
            tasks['Next'].remove(i)
            print('Task "{0}" was marked as Failed! Very sad :('.format(i[1]))
            
def take_task(tasks, task_id):
    for i in tasks['Next']:
        if i[0] == task_id:
            tasks['Current'].append(i)
            tasks['Next'].remove(i)
            print('Moved task "'+ i[1] + '" with id ' + str(i[0])+' to current tasks!')  

def delete_task(tasks, task_id, global_counter):
    dest = None
    while 1: #WTF
        for i in tasks['Done']:
            if i[0] == task_id:
                dest = 'Done'
                break
        if dest != None:
            break
        for i in tasks['Current']:
            if i[0] == task_id:
                dest = 'Current'
                break
        if dest != None:
            break
        for i in tasks['Next']:
            if i[0] == task_id:
                dest = 'Next'
                break
        if dest != None:
            break
        for i in tasks['Failed']:
            if i[0] == task_id:
                dest = 'Failed'
                break
        break
    if dest == None:
        print('Couldn\'t find task with this id!')
        return global_counter
    else:
        tasks[dest].remove(i)
        print('Task "{0}" with id {1} was deleted from {2}!'.format(i[1],str(task_id),dest))    
        if task_id == global_counter:
            global_counter -= 1
            print('Counter has been reduced')
        return global_counter

def edit_task(tasks, task_id):
    dest = None
    task_pos = -1
    for _ in range(1): #lmao
        for i in range(len(tasks['Done'])):
            if tasks['Done'][i][0] == task_id:
                dest = 'Done'
                task_pos = i
                break
        for i in range(len(tasks['Current'])):
            if tasks['Current'][i][0] == task_id:
                dest = 'Current'
                task_pos = i
                break
        for i in range(len(tasks['Next'])):
            if tasks['Next'][i][0] == task_id:
                dest = 'Next'
                task_pos = i
                break
    if dest == None:
        print('Couldn\'t find task with this id!')
    else:
        print('Task found in {0}'.format(dest))
        command = input('Enter new name:\n\t')
        if command == '_':
            command = tasks[dest][task_pos][1]
        tags = input('Add |-separated tags:\n\t').split('|')
        if tags == ['']:    
            tags = []
        elif tags == ['_']:
            tags = tasks[dest][task_pos][2]
        imm = input('Urgent? [0/1/y/n/д/н]\n\t')
        if imm == '_':
            imm = tasks[dest][task_pos][3]
        else:
            try:
                imm = {"0": False, "1": True ,"n": False, "y": True, "н": False, "д": True}[imm]
            except KeyError:
                print("Wrong key, operation aborted.")
                return 
        
        print('Task {0} was renamed to {1}'.format(tasks[dest][task_pos][1],command))        
        tasks[dest][task_pos][1] = command
        tasks[dest][task_pos][2] = tags
        tasks[dest][task_pos][3] = imm
    
def print_tasks(tasks, list_of_params, list_of_tags):
    def print_category(tasks, category, tags_to_print):
        print_list = {True:[],False:[]}
        for i in tasks[category]:
            if len(tags_to_print) != 0:
                if set(i[2]).intersection(tags_to_print) != set():
                    print_list[i[3]].append(i)
            else:
                print_list[i[3]].append(i)
        
        if len(print_list[True]) + len(print_list[False]) == 0:
            print('{0} is empty!'.format(category))
        else:
            print('{0}: '.format(category))
            print('\t{0}: '.format('Urgent'))
            for i in print_list[True]:
                print('\t\t{0}: {1}'.format(i[0],i[1]),end = '')
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
        
    categories = ['Current']
    for param in list_of_params:
        if param == 'n':
            categories.append('Next')
        elif param == 'f':
            categories.append('Failed')
        elif param == 'd':
            categories.append('Done')
        else:
            print(f'Unknown parameter {param}')
    for category in categories:
        print_category(tasks, category, list_of_tags)

def extract_tags(list_of_words):
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

def extract_params(list_of_words):
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


def bind(binds, bind_c, command):
    binds[bind_c] = command

while not quit_called:
    command = input('Enter command: \n\t')
    if command in binds.keys():
        command = binds[command]
    command_splitted = command.split(' ')
    
    list_of_tags = extract_tags(command_splitted)
    list_of_params = extract_params(command_splitted)

    if command_splitted[0] in ['Q', 'q', 'й', 'Й']:
        save_tasks(tasks, global_counter, binds)
        print('Goodbye! :)')
        os.system("clear")
        quit_called=True
    elif command_splitted[0] in ['D', 'd', 'в', 'В']:
        complete_task(tasks, int(command[2:]))
    elif command_splitted[0].lower() in ['del']:
        global_counter = delete_task(tasks, int(command[4:]), global_counter)    
    elif command_splitted[0].lower() in ['undone']:
        undone_task(tasks, int(command[7:]))  
    elif command_splitted[0].lower() in ['untake']:
        untake_task(tasks, int(command[7:]))  
    elif command_splitted[0].lower() in ['bind']:
        bind(binds, command_splitted[1], ' '.join(command_splitted[2:]))  
    elif command_splitted[0] in ['T', 't', 'е', 'Е']:
        take_task(tasks, int(command[2:]))  
    elif command_splitted[0] in ['R', 'r', 'к', 'К']:
        edit_task(tasks, int(command[2:]))    
    elif command_splitted[0] in ['S', 's', 'ы', 'Ы']:
        save_tasks(tasks, global_counter, binds)       
    elif command_splitted[0] in ['F', 'f', 'а', 'А']:
        fail_task(tasks, int(command[2:]))       
    elif command_splitted[0] in ['P', 'p', 'з', 'З']:
        print_tasks(tasks, list_of_params, list_of_tags)
    else:
        if input('Do you want to add this as a task? [Y/n, Д/н]:\n\t') in ['Y', 'y', 'Д', 'д']:
            add_task(tasks, command)
    
    

