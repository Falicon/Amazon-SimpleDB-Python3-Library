import simpledb

####
#### ENTER YOUR AMAZON PROVIDED KEY & SECERET BELOW ####
####

aws_access_key = "YOUR ACCESS KEY ASSIGNED BY AMAZON"
aws_access_seceret = "YOUR ACCESS SECRET ASSIGNED BY AMAZON"

####
#### CREATE AN INSTANCE OF OUR PYTHON SIMPLEDB CLASS USING YOUR AMAZON KEY & SECERET ####
####

mydb = simpledb.SimpleDB(aws_access_seceret, aws_access_key)

####
#### DOMAIN ACTIONS (confirmed working 3/20/2009) ####
####

# createdomain - required params (domain name as string), optional params (none)
result = mydb.createdomain("likefeature")
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

# listdomains - require params (none), optional params (max number of domains as string, next token as string)
result = mydb.listdomains()
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

# domainmetadata - require params (domain name as string), optional params (none)
result = mydb.domainmetadata("falicon")
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

# deletedomain - require params (domain name as string), optional params (none)
result = mydb.deletedomain("likefeature")
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

####
#### ITEM & ATTRIBUTE ACTIONS (confirmed working 3/30/2009) ####
####

# getattributes - require params (item name as string, domain name as string), optional params (attribute name as string)
result = mydb.getattributes("account", "", "accounts")
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

# batchputattributes  - require params (items as array of dictionaries), optional params (domain name as string)
domainname = "accounts"
items = []
attributes = []
record = {'name':'username','value':'kevin','replace':'true'}
attributes.append(record)
record = {'name':'password','value':'another_secert'}
attributes.append(record)
item = {'itemname':'account1','attributes':attributes}
items.append(item)
attributes = []
record = {'name':'username','value':'tyler'}
attributes.append(record)
item = {'itemname':'account2','attributes':attributes}
items.append(item)
result = mydb.batchputattributes(items, domainname)
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

# putattributes - require params (item name as string, items as array of dictionaries), optional params (domain name as string)
domainname = "accounts"
itemname = "account"
items = []
record = {'name':'username','value':'falicon','replace':'true'}
items.append(record)
record = {'name':'username','value':'timothy','replace':'true'}
items.append(record)
record = {'name':'password','value':'super_seceret_password'}
items.append(record)
result = mydb.putattributes(itemname, items, domainname)
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

# deleteattributes - require params (item name as string, domain name as string), optional params (items as array of dictionary)
domainname = "likefeature"
itemname = "falicon_twitter_http://draftwizard.com/test.php"
items = []
record = {'name':'username'}
items.append(record)
result = mydb.deleteattributes(itemname, items, domainname)
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

####
#### SEARCH ACTIONS (confirmed working 3/30/2009)  ####
####

# select - require params (select expression as string), optional params (next token as string)
result = mydb.select("select * from likefeature")
#### DUMP THE RESULTS TO THE SCREEN FOR TESTING/DEBUGGING ####
mydb.debug(result)

####
#### DEPRECATED ####
####

# query - require params (domain name as string), optional params (query expression as string, max number of items as string, next token as string)
# result = mydb.query("accounts", "['username' = 'kevin']")

# querywithattributes - require params (domain name as string), optional params (query expression as string, attribute name as string, max number of items as string, next token as string)
# result = mydb.querywithattributes("accounts","['username' = 'kevin']")

