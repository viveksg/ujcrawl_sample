import urllib2
import json
from HTMLParser import HTMLParser;

class HTMLParserA(HTMLParser):
	
	currentString = ""
	dtbool=0
	dataString = ""
	selectors = []
	values = {'ID':'','Type':'','Mame':'','Description':'','URL':'','Parent':'','Parent_URL':''}
	json_data = ""
	href_count = 0
        op_file_descriptor = ""

	def handle_starttag(self,tag,attrs):
		if (tag != "dt" and self.dtbool==0): #only parse dt tag or tags inside dt tag 
			return
		if(self.dtbool==0):
			self.href_count = 0
			self.init_dictonary()
                 
	        self.dtbool=1
		dataString = ""
		for attr in attrs:
			if(attr[0]=='href'):
			       if(self.href_count == 0): # first URL 	
			        	self.values['URL'] = attr[1]
			       else: 
			                self.values['Parent_URL'] = attr[1] # second URL, For parent of Index item
			       self.href_count = self.href_count + 1		
		

        def handle_data(self,data):
		if self.dtbool == 1:
		   self.dataString = self.dataString+" "+data.strip()

	def handle_endtag(self,tag):
		if (tag=="dt"):
		        self.appendSelector(self.dataString)
			self.complete_dictonary();
			self.writeOutput(json.dumps(self.values))
		   	self.dataString = "";
			self.dtbool = 0

	def init_dictonary(self):
                self.values  = {'ID':'','Type':'','Mame':'','Description':'','URL':'','Parent':'','Parent_URL':''};

	def complete_dictonary(self):# process whole plain text to get type and name of index item
		i = 0;
		pasteInTypeString = 0;
		currString = "";
		typeString = "";
		for i in range(0,len(self.dataString)):
			if(self.dataString[i]=="-"):
				 self.values['Name'] = currString.strip(' ')
				 pasteInTypeString = 1;
				 currString = ""
				 continue

			if(pasteInTypeString and pasteInTypeString <3): 
				if(self.dataString[i] == " " and not(typeString.lower() == 'static')):	
					pasteInTypeString = pasteInTypeString + 1; 
			        else:
					typeString = typeString + self.dataString[i];
			    
			currString = currString + self.dataString[i]

		self.values['Type'] = typeString;
		self.values['Description'] = currString.strip(' ')
			    



	def appendSelector(self,dataString):
		i=0;
		space_encountered=0
		eString=""
		for i in range(dataString.index("- ")+2,len(dataString)):
			if (dataString[i]==" "):
				space_encountered = space_encountered + 1
			eString = eString+dataString[i]
			if (space_encountered==2):
				break
		eString = eString.strip(' ')	
		if eString not in self.selectors:
		 	self.selectors.append(eString)

	def getSelector(self):
		return self.selectors

	

	def openFile(self):
		self.op_file_descriptor =  open("output_JSON.txt","w+")
	
	def writeOutput(self,data):
                self.op_file_descriptor.write(data)

	def closeFile(self):
                self.op_file_descriptor.close()

