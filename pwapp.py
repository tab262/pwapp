from Tkinter import * 
from datetime import datetime
import tkMessageBox
import encrypt


def getSites(sitesTextFile):
    return sitesTextFile.read().split()

def getPWs(pwTextFile):
	return pwTextFile.read().split()

def setWindowSettings(window):
    window.title("PW Manager")
    window.geometry("470x500") 

def addSite(siteName, pw, sitesList,sites,pws,key,newUser):
	if siteName.get() != '' and pw.get() != '' and key.get() != '':
		#writes new site to list of sites
		#sitesTextFile.write(siteName.get() + '\n')
		
		#encrypts the password returns encrypted pw
		encryptedPassword = encrypt.encrypt2((pw.get()+'-'+newUser.get()), key.get())
		
		#writes password in encrypted format
		#pwTextFile.write(encryptedPassword)
		#pwTextFile.write('\n')
		
		print siteName.get()
		print encryptedPassword
		#print sites 
		
		#adds site and password to list to call from
		sites.append(siteName.get())
		pws.append(encryptedPassword)
		
		print sites
		print pws
		print len(sites)
		print len(pws)
		#add site to listbox
		sitesList.insert(END, siteName.get())
		
		#empties out entry fields
		pw.set('')
		siteName.set('')
		key.set('')
		newUser.set('')

def getSiteInfo(obj, siteText, sites,pwText,pws, decryptkey, logText,userText):
	try:
		index = int(obj.curselection()[0])
		current = "Site: "
		current2 = "PW: "
		current3 = "User: "
		siteText.set(current + sites[index])
		print "Encrypted PW: ",pws[index]
		try:
			decPass = encrypt.encrypt2(pws[index], decryptkey.get(),2)
		except:
			time = str(datetime.time(datetime.now()))
			time = time[:8]
			string =  "\n" + time + "# Incorrect Key Format"
			logText.insert(INSERT, string)
			tkMessageBox.showerror(message="Invalid Key")
		else:
			detailsList = decPass.split('-')
			pwString = detailsList[0]
			userString = detailsList[1]
			pwText.set(current2 + pwString)
			userText.set(current3 + userString)
			decryptkey.set('')
			print "Index: ",index
	except IndexError, e:
	    print 'Tuple empty or site not selected'
    
def populateList(sitesList, sites):
	for i in range(len(sites)):
		sitesList.insert(i,sites[i])   

def deleteSiteInfo(sites, pws, sitesList):
	#sitesList is gui object to modify
	#sites contains list of sites
	#siteToDelete is the string of the selected site to delete
    index = int(sitesList.curselection()[0])
    siteName = sites[index]
    response = tkMessageBox.askquestion(message="Are you sure you want to delete this site profile? It cannot be recovered")
    if response == 'yes':
		del sites[index]
		del pws[index]
		sitesList.delete(0, END)
		populateList(sitesList, sites)
    


def myQuit(sitesTextFile, pwTextFile, sites, pws,window):
    sitesTextFile.close()
    pwTextFile.close()
    sitesTextFile = open('sites','w')
    pwTextFile = open('pw','w')
    for i in range(len(sites)):
        sitesTextFile.write(sites[i] + '\n')
        pwTextFile.write(pws[i])
        pwTextFile.write('\n')
    window.quit()
#################################################################    
def main():
    #I/O and populating lists
    try:
        sitesTextFile = open('sites','r')
        pwTextFile = open('pw','r')
    except:
        sitesTextFile = open('sites','w')
        pwTextFile = open('pw','w')
        sitesTextFile.close()
        pwTextFile.close()
        sitesTextFile = open('sites','r')
        pwTextFile = open('pw','r')
        
        
    logIntro =open('logIntro', 'r')
    sites = getSites(sitesTextFile)
    pws = getPWs(pwTextFile)
    
    
    #####GUI CREATION COMMENCE#####
    window = Tk()
    setWindowSettings(window)
    
    #title text
    mainText = StringVar()
    mainText.set("PW Manager")
    label1 = Label(window, textvariable=mainText, width=9)
    label1.place(x=200,y=1)
    
    #scroll text
    scrollText = StringVar()
    scrollText.set("Scrollable")
    label2 = Label(window,textvariable=scrollText)
    label2.place(x=9,y=40)
    
    #site text
    siteText = StringVar()
    siteText.set("Site: ")
    label3 = Label(window, textvariable=siteText)
    label3.place(x=10,y=440)
    
    #user text
    userText = StringVar()
    userText.set("User: ")
    userTextLabel = Label(window, textvariable=userText)
    userTextLabel.place(x=5.5, y=460)
    
    #pw text
    pwText = StringVar()
    pwText.set("PW: ")
    label4 = Label(window, textvariable=pwText)
    label4.place(x=13,y=480)
    
  
    ####LISTBOX####   
    #Populate list
    sitesList = Listbox(window, height=20, width=25)
    populateList(sitesList, sites)
    sitesList.place(x=10,y=55) 
    index = 0
    ####BUTTON####
    decryptLabel = Label(window, text="Decrypt Key:")
    decryptLabel.place(x=8,y=390)
    
    button1 = Button(window, text='Get Site Info', width = 8, command=lambda : getSiteInfo (sitesList,siteText,sites,pwText,pws, decryptKey, text,userText))
    button1.place(x=7,y=412)
    
    deleteButton = Button(window, text='Delete Site Info', width = 10, command=lambda : deleteSiteInfo(sites, pws, sitesList))
    deleteButton.place(x=106, y=412)    
    
    
    decryptKey = StringVar()
    decryptEntry = Entry(window, textvariable=decryptKey, width=14, show="*")
    decryptEntry.place(x=95,y=390)
    
    
    ####ADDING NEW SITE####
    addSiteFrame = Frame(window)
    setHeight = 35
    addSiteLabel = Label(window, text="Add new site:")
    addSiteLabel.place(x=300,y=setHeight+5)
    
    encryptLabel = Label(window, text="Encrypt Key:")
    encryptLabel.place(x=220,y=setHeight+20)
    encryptKey = StringVar()
    encryptEntry = Entry(window, textvariable=encryptKey, show='*')
    encryptEntry.place(x=300,y=setHeight+20)
    
    newSiteLabel = Label(window, text="Site Name:")
    newSiteLabel.place(x=231,y=setHeight+40)
    newSiteName = StringVar()
    entryBoxSite = Entry(window, textvariable=newSiteName)
    entryBoxSite.place(x=300,y=setHeight+40)
    
    newUserLabel = Label(window, text="Username: ")
    newUserLabel.place(x=237,y=setHeight+60)
    newUser = StringVar()
    useBoxSite = Entry(window, textvariable=newUser)
    useBoxSite.place(x=300,y=setHeight+60)
    
    newPWLabel = Label(window, text="Password:")
    newPWLabel.place(x=237,y=setHeight+80)
    newPw = StringVar()
    pwBoxSite = Entry(window, textvariable=newPw, show="*")
    pwBoxSite.place(x=300,y=setHeight+80)
    
    addButton = Button(window, text="ADD", command=lambda : addSite(newSiteName,newPw,sitesList, sites,pws, encryptKey,newUser))
    addButton.place(x=412,y=setHeight+105)
    
    
    
    ####LOG BOX####
    w = Frame(window)
    w.place(x=225,y=192)
    scrollbar = Scrollbar(w)
    scrollbar.pack(side=RIGHT,fill=Y)
    log = StringVar()
    log.set(logIntro.read())
    text = Text(w, wrap=WORD, yscrollcommand=scrollbar.set, height=12, width=32)
    text.insert(INSERT,log.get())
    text.pack()
    scrollbar.config(command=text.yview)
    
    ###QUIT BUTTON###
    quitButton = Button(window, text="QUIT", command=lambda : myQuit(sitesTextFile, pwTextFile, sites, pws,window))
    quitButton.place(x=410,y=450)
    #run gui
    window.mainloop()
    print 'Closing files'
    sitesTextFile.close()
    pwTextFile.close()
    
def quit(window):
	window.destroy()    

if __name__=="__main__":main()

