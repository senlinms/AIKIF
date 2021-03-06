====================
 AIKIF Requirements
====================

This document describes the goals and requirements of AIKIF. 
Note that these are fluid and still very much a work in progress.

.. contents::




Overall Goals
=============
There are 4 main goals:

- Framework to collect and map information to knowledge

- Process Automation

- Control of Personal data

- AI Management 


Intentions
----------
The intention of AIKIF is to allow **all** of your information to be locally accessible, searchable and managed by yourself.

This includes the general high level information, processes and metadata around it, as well as the content of the data.


If everything is specified in a machine readable format, then rather than manually perform computer related tasks, the methods can be catalogued and structured so they can be automated.


Requirements
============
Goal 1 - Framework to collect and map information to knowledge
-----

map data to knowledge using your own rules
``````````````
The business rules engine is the primary method of adding conditional logic to the AIKIF and is a fairly generic table.
User clicks on Business Rules > Add and can add business rules as follows:
what table is this for [tblName] | Any Table | Any Table in [schema]

A generic business rules engine which defines many parts of the day to day operation. This is likely to be a core category used by mapper.py to get the appropriate rules list, eg RULES_DATA_COUNTRY, RULES_TOP_PROJECT, RULES_SYSTEM_FILE_BACKUP

The structure of the rules MUST be generic enough to handle any type of automated task, for example - 
- Data updates   - detailed data mappings (eg change China (excl Mongolia)  to China in country ref file
- PC Admin tasks - copy all source code to NAS each night at 10pm 
- Web scraping   - download funny pictures from Reddit at 5pm | check for online orders

aikif programs using rules
``````````````
Any program in AIKIF can add to the rules table and there is a column in rules to show which program added it. So that program can then read all its own rules, eg Tax.py reads the finance rules and doesn't care about engineering tolerance rules.
In addition there are numerous categories that can optionally be applied to each rule - may not be a table format, possibly json or dictionary.

Each program registers it's functions as follows 

.. code:: python

    t = aikif.Toolbox()
    t.add({'file':'knapsack.py', 'function':'solve_greedy_trivial', 'args':['int', 'dict'], 'return':['int', 'list']})

    t.add({'file':'knapsack.py', 'function':'solve_smallest_items_first', 'args':['int', 'dict'], 'return':['int', 'list']})
    t.add({'file':'knapsack.py', 'function':'solve_expensive_items_first', 'args':['int', 'dict'], 'return':['int', 'list']})
    t.add({'file':'knapsack.py', 'function':'solve_value_density', 'args':['int', 'dict'], 'return':['int', 'list']})
 

store disparate data locally linked to common ontology
``````````````
Agents (internal to aikif or external) are used to collect information from various sources.

The will be stored in a local data store (text, database, XML - users choice), and indexed to allow full searching.

Agents include:

- Email
- Browser favourites
- File metadata
- datasets


Initially, a small self contained ontology will be used to handle AIKIF processes and data, but  may later be linked to a standard upper ontology, (not sure which one or how) See - http://www.acutesoftware.com.au/aikif/ontology.html


understanding of bias to monitor data inputs and sources
``````````````
Bias will give a rough weighting to a piece of information based on source, time, context, etc.
This is used when automatically parsing data to ensure that a random comment on a forum does not get equal weighting to a peer reviewed academic paper.

There can be multiple biases, and each user can modify the weights to what they deem accurate for their situation


Goal 2 - Process Automation
-----
automatic documentation of program development
``````````````

Use the AIKIF to completely manage projects, as it stores not only details on programs (as objects having events such as created, ran, copied to prod), but also datasets (such as size, date loaded, etc) and simply have an overall ‘Task’ / Contact / Event template to manage the overall projects

.. code:: python

    from aikif import codeDocData as doc
    from aikif import businessRules as bus
    proj = doc.Project('Read Datafiles')
    proj.RegisterProgram('importTools.py', 'program to read in a datafile', 'T:\user')
    proj.Task('document columns')
    proj.Folder(‘WORKING’, 'T:\user')
    proj.Folder('BACKUP', 'E:\backup\user')
    proj.Contact(‘djmurray’)
    
    backups = bus.BackupRules()
    backups.Source(‘t:\\user’)
    backups.Dest(‘NAS’)
    backups.Schedule(‘DAILY’)


Option 2

.. code:: python

    csvProject = aikif.project.Project('csvProject', 'Download CSV file and load to database', 'T:\projects\csvProject')
    csvProject.add_requirement('dl', 'dl the file from the web')
    csvProject.add_requirement('sched', 'schedule refresh each day at 6am')
    csvProject.task.add('todo1', 'thing to do')
    csvProject.task.add('todo2', 'more stuff to do')
    csvProject.folder.add('master folder', 'T:\projects\csvProject')
    csvProject.folder.add('backup folder', 'z:\BK_projects\csvProject')
    csvProject.folder.add('deploy folder', 'T:\projects\csvProject\deploy')
    csvProject.link('task', 'requirement', 'dl' , 'todo1')





Log intent, progress and outcomes of all AI / Data processing tasks.
``````````````

This section shows actual usage of AIKIF to manage business processes - example for Acute Software
Document a business

.. code:: python

    import aikif.project
    my_biz = Project(name=‘Acute Software’, type=’business’, desc=‘Custom Software development’)
    my_biz.add_detail(‘website’, ‘http://www.acutesoftware.com.au’)
    my_biz.add_detail(email, ‘djmurray@acutesoftware.com.au ’)
    
    my_biz.add_type(type=‘Cash Sale’, category=’Taxable_income’, desc=’Manual sales over counter - no customer details recorded’)
    
    my_biz.add_type(type=‘Online Sale’, category=’Taxable_income’, desc=’Online sales orders from RegNow’)
    

    # Now setup some data structures to hold information
    import aikif.dataTools.cls_data_table
    import aikif.cls_log
    lg =Log('Acute Software', 'T:\user\docs\business')
    tbl_sales = DataTable(‘Sales’, cols=[‘Date’, ‘Amount’, ‘Cust’])
    tbl_expenses = DataTable(‘Expenses’, cols=[‘Date’, ‘Amount’, ‘Cust’])
    

Record Cash Sales
Record a single sale (no customer details available)

.. code:: python

    amount = input(‘Amount of Sale’)
    my_biz.record(tbl_sales, type=‘Cash Sale’, cols=[sysdate, amount, ‘cash sale’])
    
    #Record Expenses for tax purposes
    date    = input(‘Date of Purchase’)
    amount  = input(‘Amount’)
    details = input(‘Details’)
    my_biz.record(tbl_expenses, type=‘Purchases’, cols=[date, amount, details])
    
    Generate Profit and Loss Statement
    # simple summary
    print( ‘Total profit = ‘, sum(sales.amount) / sum(expenses.amount))
    
    # summary by day
    sales_by_day = tbl_sales.aggregate(’amount’, ’Date’)
    exp_by_date  = tbl_expenses.aggregate(’amount’, ’Date’)
    
    #profit = [[‘Day’, ‘Type’, ‘Amount’]]
    profit = DataType(‘Profit’, [‘Day’, ‘Type’, ‘Amount’])
    for row in sales_by_day:
        profit.append([row.date, ‘Sales’, row.amount])
    for row in exp_by_date :
    profit.append([row.date, ‘Expense’, row.amount])
    

automatic collection, validation and processing of data
``````````````

This section shows various examples of setting up emails, folder locations ready to help automate business tasks

.. code:: python
    import aikif.agent.gather.agent_emails
    account = GmailAccount(username, password, save_folder)
    agt = EmailAgent('email_agent', ‘.’, True, 1 , account)
    
Automatically Collect Sales from emails
The method shows a function to automatically sales from RegNow emails

.. code:: python

    sales_search_string = "(SUBJECT Order Item) AND (FROM RegNow)"
    sales_emails = account.get_all_emails_containing(100, sales_search_string)
    for sales_email in sales_emails:
    cust, date, amount = aikif.parse(sales.email)
    my_biz.record(tbl_sales, type=‘Online Sales’, cols=[date, amount, cust])
    

Context Monitor
``````````````
watches what you do, where you are and automatically provides ALL info for that thing.

eg.. fixing a fence, driving to shops, working on AIKIF, reading reddit

Methods of detection

- Mobile GPS coords
- Ip address lookup
- Pc name (user list of locations)
- what is running. Pc / phone / tablet
- Apps running (agent collect)
- Folders / files used
- Pc usage

Then use an automated project clustering process combined with optional user defined list of mapping usage to projects to figure out what user was working on.


Goal 3 - Control of Personal data
-----
get your data off the cloud and under your control
``````````````
Agents store data locally, so you will always have the information regardless of which online services disappear.



agents to download data from various cloud hosts and store locally
``````````````
The aikif toolbox can setup a daily agent to run tasks


index data locally for simple unified search across all sources (facebook, email, documents, photo metadata, web favourites)
``````````````
There are several levels of local indexing starting at the meta 'project level' based on tags and categories down to full text searching.

Goal 4 - AI Management
-----
Define methods an AI can use (aikif.toolbox)
``````````````
The Toolbox function maps programs (internal and external) to a standard format to all computers to identify tools and run them.

The benefit of an AI using methods via the framework to is log times and results to see the outcomes of various algorithms. This provides a central place to manage and track the success and types of results.

Simple interface to manage and control AI's
``````````````
Web service has API to control all aspects of AIKIF

Web app example shows how this can be used to manage AI applications run with different data sources and parameters
 

Log all results with useful milestones and checkpoints
``````````````

The log aggregates should show useful summaries


