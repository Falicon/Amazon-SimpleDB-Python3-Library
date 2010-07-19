# Basic Python 3 Library
import base64
import datetime
import hashlib
import hmac
import http.client
import urllib.parse

class SimpleDB:
  """Python Wrapper class for Amazon's SimpleDB Service"""
  def __init__(self, aws_access_seceret, aws_access_key):
    self.aws_access_seceret = aws_access_seceret
    self.aws_access_key = aws_access_key
    self.params = []
    self.signature = ""
    self.request = ""

  def debug(self, detail):
    print()
    print(detail)
    print()

  def buildparams(self, action_command):
    # define the basic request string details (encoding where needed)
    self.params = []
    current_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    self.params.append('Action=' + urllib.parse.quote(action_command))
    self.params.append('SignatureMethod=HmacSHA256')
    self.params.append('SignatureVersion=2')
    self.params.append('Timestamp=' + urllib.parse.quote(current_time))
    self.params.append('Version=2009-04-15')

  def createsignature(self):
    # create the signature
    # set up the required format of the request string for generating our signature
    self.params.sort()
    sigreq = "GET\nsdb.amazonaws.com\n/\n"
    sigreq += "AWSAccessKeyId=" + urllib.parse.quote(self.aws_access_key) + "&"
    sigreq += '&'.join(self.params)
    sha256 = hmac.new(self.aws_access_seceret.encode(), sigreq.encode(), hashlib.sha256)
    digest = sha256.digest()
    self.signature = base64.encodestring(digest).decode().strip()

  def createrequest(self):
    # set up the actual request string we'll pass to the service
    self.params.sort()
    # http://sdb.amazonaws.com/
    self.request = "/?AWSAccessKeyId=" + urllib.parse.quote(self.aws_access_key) + "&"
    self.request += "&".join(self.params)
    self.request += "&Signature=" + urllib.parse.quote(self.signature)

  def makerequest(self):
    # create the signature (using your key and seceret)
    self.createsignature()
    self.createrequest()
    # finally build the request
    conn = http.client.HTTPConnection('sdb.amazonaws.com')
    conn.request('GET', self.request)
    res = conn.getresponse()
    return res.read().decode()

  def createdomain(self, domainname):
    # call the CreateDomain method
    self.buildparams("CreateDomain")
    self.params.append("DomainName=" + urllib.parse.quote(domainname))
    return self.makerequest()

  def listdomains(self, maxnumberofdomains = "", nexttoken = ""):
    # call the ListDomains method
    self.buildparams("ListDomains")
    if maxnumberofdomains != "":
      self.params.append("MaxNumberOfDomains=" + urllib.parse.quote(maxnumberofdomains))

    if nexttoken != "":
      self.params.append("NextToken=" + urllib.parse.quote(nexttoken))

    return self.makerequest()

  def deletedomain(self, domainname):
    # call the DeleteDomain method
    self.buildparams("DeleteDomain")
    self.params.append("DomainName=" + urllib.parse.quote(domainname))
    return self.makerequest()

  def domainmetadata(self, domainname):
    # call the DomainMetadata method
    self.buildparams("DomainMetadata")
    self.params.append("DomainName=" + urllib.parse.quote(domainname))
    return self.makerequest()

  def getattributes(self, itemname, attributename = "", domainname = ""):
    # call the GetAttributes method
    self.buildparams("GetAttributes")
    self.params.append("ItemName=" + urllib.parse.quote(itemname))
    if attributename != "":
      self.params.append("AttributeName=" + urllib.parse.quote(attributename))

    if domainname != "":
      self.params.append("DomainName=" + urllib.parse.quote(domainname))

    return self.makerequest()

  def query(self, domainname, queryexpression = "", maxnumberofitems = "", nexttoken = ""):
    # call the Query method
    self.buildparams("Query")
    self.params.append("DomainName=" + urllib.parse.quote(domainname))
    if maxnumberofitems != "":
      self.params.append("MaxNumberOfItems=" + urllib.parse.quote(maxnumberofitems))

    if nexttoken != "":
      self.params.append("NextToken=" + urllib.parse.quote(nexttoken))

    if queryexpression != "":
      self.params.append("QueryExpression=" + urllib.parse.quote(queryexpression))

    return self.makerequest()

  def querywithattributes(self, domainname, queryexpression = "", attributename = "", maxnumberofitems = "", nexttoken = ""):
    # call the QueryWithAttributes method
    self.buildparams("QueryWithAttributes")
    self.params.append("DomainName=" + urllib.parse.quote(domainname))
    if queryexpression != "":
      self.params.append("QueryExpression=" + urllib.parse.quote(queryexpression))

    if attributename != "":
      self.params.append("AttributeName=" + urllib.parse.quote(attributename))

    if maxnumberofitems != "":
      self.params.append("MaxNumberOfItems=" + urllib.parse.quote(maxnumberofitems))

    if nexttoken != "":
      self.params.append("NextToken=" + urllib.parse.quote(nexttoken))

    return self.makerequest()

  def select(self, selectexpression, nexttoken = ""):
    # call the Select method
    self.buildparams("Select")
    self.params.append("SelectExpression=" + urllib.parse.quote(selectexpression))
    if nexttoken != "":
      self.params.append("NextToken=" + urllib.parse.quote(nexttoken))

    return self.makerequest()

  def putattributes(self, itemname, items, domainname = ""):
    # call the PutAttributes method
    self.buildparams("PutAttributes")
    self.params.append("ItemName=" + urllib.parse.quote(itemname))
    counter = 0
    for i in items:
      try:
        self.params.append("Attribute." + str(counter) + ".Name=" + urllib.parse.quote(i['name']))
        self.params.append("Attribute." + str(counter) + ".Value=" + urllib.parse.quote(i['value']))
      except KeyError:
        # no value key, but it's required so throw an error
        print("Attributes require a name and a value")
        return

      try:
        if i['replace'].lower() == "true":
          self.params.append("Attribute." + str(counter) + ".Replace=true")

      except KeyError:
        # no replace key, OK to ingore this
        pass

      counter += 1

    if domainname != "":
      self.params.append("DomainName=" + urllib.parse.quote(domainname))


    return self.makerequest()

  def batchputattributes(self, items, domainname = ""):
    # call the BatchPutAttributes method
    self.buildparams("BatchPutAttributes")
    counter = 0
    for i in items:
      try:
        self.params.append("Item." + str(counter) + ".ItemName=" + urllib.parse.quote(i['itemname']))
      except KeyError:
        # no name key, but it's required so throw an error
        print('Items require an item name')

      acounter = 0
      for attrib in i['attributes']:
        try:
          self.params.append("Item." + str(counter) + ".Attribute." + str(acounter) + ".Name=" + urllib.parse.quote(attrib['name']))
          self.params.append("Item." + str(counter) + ".Attribute." + str(acounter) + ".Value=" + urllib.parse.quote(attrib['value']))
        except KeyError:
          # no name key, but it's required so throw an error
          print("Items require a Name and a Value")

        try:
          if attrib['replace'].lower() == "true":
            self.params.append("Item." + str(counter) + ".Attribute." + str(acounter) + ".Replace=true")
        except KeyError:
          # no replace key, OK to ingore this
          pass

        acounter += 1

      counter += 1

    if domainname != "":
      self.params.append("DomainName=" + urllib.parse.quote(domainname))

    return self.makerequest()

  def deleteattributes(self, itemname, items, domainname = ""):
    # call the DeleteAttributes method
    self.buildparams("DeleteAttributes")
    self.params.append("ItemName=" + urllib.parse.quote(itemname))
    counter = 0
    for i in items:
      counter += 1
      try:
        self.params.append("Attribute." + str(counter) + ".Name=" + urllib.parse.quote(i['name']))
        self.params.append("Attribute." + str(counter) + ".Value=" + urllib.parse.quote(i['value']))
      except KeyError:
        # no name key, but it's required so throw an error
        pass

    if domainname != "":
      self.params.append("DomainName=" + urllib.parse.quote(domainname))

    return self.makerequest()

