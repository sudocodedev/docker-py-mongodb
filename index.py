import os
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime

choice = 0

schema = """
{
    "task": "",
    "tags": ["", "",],
    "status": "Done or Doing or Todo",
    "author": "",
    "task_created_at": "",
    "task_updated_at": "",
}
"""

question = """
*** TODO Manager ***

# Please select below options:

1) create a task
2) view particular tasks
3) view all tasks
4) view latest task
5) update task
6) delete task
7) delete all task
8) help
9) exit
10) task counts
11) clear screen
"""

def updateTask(collection):
    count = collection.count_documents({})
    if count == 0:
        print("No tasks found...")
        return

    option = input("do you want to update single or multiple records? (s/m, default will be s)").strip().lower()
    print()
    print("query:")
    search = input("Enter on which field, you want to update the tasks (options ==> task/ author/ status/ tags) >> ")

    if search not in ('task', 'author', 'status', 'tags'):
        print()
        print("not a valid search param, should be ==> task/ author/ status/ tags")
        return
    search_value = input("Enter the value for the above field >> ").strip().lower()
    print()

    query = {search: {'$regex': search_value, '$options': 'i'}}
    counts = collection.count_documents(query)

    if counts == 0:
        print()
        print("No tasks found based on the provided query...")
        return
    
    print("Enter field details:")
    field = input("Enter on which field, you want to delete the tasks (options ==> task/ author/ status/ tags) >> ")

    if field not in ('task', 'author', 'status', 'tags'):
        print("not a valid field param, should be ==> task/ author/ status/ tags")
        return
    
    field_value = input("Enter the value for the above field >> ").strip()

    update_task = {'$set': {field: field_value}}
    
    if option == 'm':
        collection.update_many(query, update_task)
        print(f"{counts} tasks updated successfully...")
    else:
        collection.update_one(query, update_task)
        print("task updated successfully...")

    print()
    

def deleteTask(collection):
    count = collection.count_documents({})
    if count > 0:
        search = input("Enter on which field, you want to delete the tasks (options ==> task/ author/ status/ tags) >> ")
        

        if search in ('task', 'author', 'status', 'tags'):
            value = input("Enter the value for the above field >> ").strip().lower()
            print()
            
            query = {search: {'$regex': value, '$options': 'i'}}
            
            counts = collection.count_documents(query)
            if counts > 0:
                collection.delete_many(query)
                print(f"{counts} tasks deleted successfully...")
            else:
                print("No tasks deleted")
        else:
            print("Please enter only below options for the search: ","task (part of task name)", "status", "author", "tags", end="\n")
            print()
            deleteTask(collection)
    else:
        print("No tasks found")
    print()

def deleteAllTask(collection):
    action=input("Are you sure to delete all tasks? (y/n) >> ")

    if action in 'yn':
        count = collection.count_documents({})
        if action == 'y' and count > 0:
            collection.delete_many({})
            print(f"All {count} tasks deleted successfully...")
        else:
            print("No tasks deleted...")
    else:
        print("Please a valid option either 'y' or 'n' in the prompt.")
    print()

def taskCounts(collection):
    print("Tasks count ==> ", collection.count_documents({}))

def viewLatestTask(collection):
    if collection.count_documents({}) != 0:
        cursor = collection.find({}).sort({"_id": -1}).limit(1)
        pprint(cursor.next(), indent=4, depth=2)
    print()

def viewParticularTasks(collection):
    search = input("Enter on which search criteria you want to view the tasks (options ==> task/ author/ status/ tags) >> ")
    
    if search in ('task', 'author', 'status', 'tags'):
        value = input("Enter the value for the above field >> ").strip().lower()
        print()
        
        query = {search: {'$regex': value, '$options': 'i'}}
        
        if collection.count_documents(query) > 0:
            cursor = collection.find(query)
            for task in cursor:
                pprint(task, indent=4, depth=2)
        else:
            print("No task(s) found for this search criteria...")
    else:
        print("Please enter only below options for the search: task (part of task name)/ status/ author/ tags", end="\n")
    print()

def viewAllTask(collection):
    count = collection.count_documents({})
    if count>0:
        for task in collection.find().sort({"_id": -1}):
            pprint(task, indent=4, depth=2)
    else:
        print("No tasks found...")
    print()

def createTask(name, collection):
    print()
    repeat = True
    tasks = []
    while repeat:
        task = input("Enter task to be added >> ")
        tags = input("Enter tags for your task (should be comma separated) eg. a,b,c... >> ").strip().split(',')
        _ = {
            "task": task,
            "tags": tags,
            "status": "Todo",
            "author": name,
            "task_created_at": datetime.now().strftime("%I:%M%p on %B %d, %Y"),
            "task_updated_at": datetime.now().strftime("%I:%M%p on %B %d, %Y")
        }
        
        tasks.append(_)

        print()
        holder = input("wanna add another task? (y/n, Default will be 'n') >> ")
        print()
        repeat = True if holder == 'y' else False

    collection.insert_many(tasks, ordered=False)
    print(f"{len(tasks)} tasks added successfully...")
    print()

def help():
    print("Here is the schema,","", schema, end="\n")

def start(choice: int, name: str, collection) -> None:
    while choice != 9:
        print("⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺")
        print(question)
        choice = int(input("Enter choice >>> "))
        print("👀")
        print()
        if choice==1:
            createTask(name, collection)
        if choice==3:
            viewAllTask(collection)
        if choice==8:
            help()
        if choice==10:
            taskCounts(collection)
        if choice==4:
            viewLatestTask(collection)
        if choice==11:
            clearScreen()
        if choice==2:
            viewParticularTasks(collection)
        if choice==6:
            deleteTask(collection)
        if choice==7:
            deleteAllTask(collection)
        if choice==5:
            updateTask(collection)

def sampleTask(name, collection):
    if collection.count_documents({}) == 0:
        print("creating a sample task...")

        task1 = {
        "task": "create your first task completed 🦾",
        "tags": ['first-task', 'great'],
        "status": "Done",
        "task_created_at": datetime.now().strftime("%I:%M%p on %B %d, %Y"),
        "task_updated_at": datetime.now().strftime("%I:%M%p on %B %d, %Y"),
        "author": name
        }

        collection.insert_one(task1)

        for task in collection.find():
            pprint(task, indent=4, depth=2)

        print()
        print("You are good to go!")
    else:
        print(f"Welcome back {name}!!")
    print()

def clearScreen():
    os.system('clear')

def main():
    clearScreen()
    print("connecting to DB...")

    try:
        username = os.environ.get('MONGO_ROOT')
        password = os.environ.get('MONGO_PASSWORD')
        port = os.environ.get('MONGO_PORT')
        print("retrived credentials...")
    except KeyError:
        print("username & password not found...","Exting the program...", end="\n")

    url=f"mongodb://{username}:{password}@db:{port}/"
    client = MongoClient(url)
    print("connected successfully!!")

    db = client.todo
    if db.list_collection_names() != []:
        print("using this collection ==>", db.list_collection_names())
    todo = db.todo

    name = input("provide your name >>> ")

    sampleTask(name, todo)
    start(choice, name, todo)
    print("Done for the day, Bye!")
    client.close()
    
if __name__ == "__main__":
    main()