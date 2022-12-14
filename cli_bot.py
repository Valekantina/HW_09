from contact_list import contacts
import time
#creating parser function that will take user input and convert it to the known operation
def parser(user_input: str):
    comm = None #commands
    param = [] # parameters

#dict of all known to the bot operations
    operations = {
        "hello": hello,
        "hi": hello,
        "hey":hello,
        "help": help,
        "add": add,
        "change": change,
        "show all": show_all,
        "good bye": exit,
        "bye": exit,
        "close": exit,
        "exit": exit,
        "phone": phone,
    }
    for k in operations:
        if user_input.lower().startswith(k):
            comm = operations[k]
            user_input = user_input.lstrip(k)
            for i in filter(lambda x: x!= "", user_input.split(" ")):
                param.append(i)
            return comm, param
    return comm, param
# creating simple functions for help, hello and exit, as they do not require error handler
def help(*args) -> str:
    return f"I know these commands: hello, help, add, change, phone, show all, good bye, bye, close, exit"

def hello() -> str:
    return f"How can I help you?"

def exit():
    print(f"Good bye!")
    time.sleep(1.5) # added delay on quit() so the message "Good bye!" is visible
    quit()

# creating main function thar will interact with the user
def main():
    print(hello())
    while True:
        user_input = input("Input command: ")
        comm, param = parser(user_input)
        if comm:
            print(comm(*param))
        else:
            print (f"Sorry, I do not know this command, please try again. Or type'help' for help")
# creating error wrapper
def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError:
            return f"Please provide me with a name and a phone number"
        except IndexError:
            return f"Sorry, you have not provided enough arguments"
        except KeyError:
            return f"This name does not exist in contacts"
    return wrapper

# creating function to add new contacts
@input_error
def add(*args) -> str:
    name, number, *_ = args
    if name in contacts:
        return f"This contact already exists, if you want to update it please choose 'change'"
    contacts.update({name:number})
    return f"Contact was added successfully"

# creating function to change existing contact
@input_error
def change(*args) -> str:
    name, number, *_ = args
    if name in contacts:
        contacts.update({name:number})
    else:
        return f"There is no contact under name '{name}'. If you wish to add the contact, please choose 'add'"
    return f"Contact was changed successfully"

# creating function to display contacts_list
@input_error
def show_all() -> str:
    result = []
    for name, number in contacts.items():
        result.append("\t{:>20} : {:<12} ".format(name, number))
    if len(result) <1:
        return f"You have not added any contacts yet"
    return "\n".join(result)

# creating function to view phone number of a chosen person from contact_list
@input_error
def phone(*args) -> str:
    name = args[0]
    if contacts.get(name):
        return "\t{:>20} : {:<12} ".format(name, contacts.get(name))
    else:
        return f"There is no contact under name '{name}'. If you wish to add the contact, please choose 'add'"

# making sure the code will only run when get_bd.py file is executed as a script
if __name__ == "__main__":
    main()
