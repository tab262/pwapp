from Tkinter import * 
from datetime import datetime
import tkMessageBox
import encrypt

sitesTextFile 	= open('sites', 'ab+')
pwTextFile 		= open('pw', 'ab+')
logIntro		= open('logIntro', 'r')
def getSites():
    return sitesTextFile.read().split()

def getPWs():
	return pwTextFile.read().split()

def addSite(siteName, pw, sitesList,sites,pws,key):
	if siteName.get() != '' and pw.get() != '' and key.get() != '':
		#writes new site to list of sites
		sitesTextFile.write(siteName.get() + '\n')
		
		#encrypts the password returns encrypted pw
		encryptedPassword = encrypt.encrypt2(pw.get(), key.get())
		
		#writes password in encrypted format
		pwTextFile.write(encryptedPassword)
		pwTextFile.write('\n')
		
		print siteName.get()
		print encryptedPassword
		print sites 
		
		#adds site and password to list to call from
		sites.append(siteName.get())
		pws.append(encryptedPassword)
		
		print sites
		#add site to listbox
		sitesList.insert(END, siteName.get())
		
		#empties out entry fields
		pw.set('')
		siteName.set('')
		key.set('')
	
def setWindowSettings(window):
    window.title("PW Manager")
    window.geometry("470x500")      

def getSiteInfo(obj, index, siteText, sites,pwText,pws, decryptkey, logText):
	try:
		index = int(obj.curselection()[0])
		current = "Site: "
		current2 = "PW: "
		siteText.set(current + sites[index])
		print "Encrypted PW: ",pws[index]
		try:
			decPass = encrypt.encrypt2(pws[index], decryptkey,2)
		except:
			time = str(datetime.time(datetime.now()))
			time = time[:8]
			string =  "\n" + time + "# Incorrect Key Format"
			logText.insert(INSERT, string)
			tkMessageBox.showerror(message="Incorrect Key Format")
		else:
			pwText.set(current2 + decPass)
			print "Index: ",index
	except IndexError, e:
	    print 'Tuple empty or site not selected'
    
def populateList(sitesList, sites):
	for i in range(len(sites)):
		sitesList.insert(i,sites[i])   
    
#################################################################    
def main():
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
    label3.place(x=10,y=450)
    
    #pw text
    pwText = StringVar()
    pwText.set("PW: ")
    label4 = Label(window, textvariable=pwText)
    label4.place(x=13,y=470)
    
  
    ####LISTBOX####
    #sitesScrollbar = Scrollbar(window)
    #sitesScrollbar.place(x=20,y=35)
    
    #get sites, pws and populate
    sites = getSites()
    pws = getPWs()
    sitesList = Listbox(window, height=20, width=25)
    populateList(sitesList, sites)
    sitesList.place(x=10,y=55) 
    index = 0
    ####BUTTON####
    button1 = Button(window, text='Get Site Info', width = 10, command=lambda : getSiteInfo (sitesList,index,siteText,sites,pwText,pws, decryptKey.get(), text))
    button1.place(x=10,y=415)    
    
    decryptLabel = Label(window, text="Decrypt Key:")
    decryptLabel.place(x=10,y=390)
    
    decryptKey = StringVar()
    decryptEntry = Entry(window, textvariable=decryptKey, width=14, show="*")
    decryptEntry.place(x=95,y=390)
    
    
    ####ADDING NEW SITE####
    setHeight = 35
    addSiteLabel = Label(window, text="Add new site:")
    addSiteLabel.place(x=300,y=setHeight+5)
    
    newSiteLabel = Label(window, text="Site Name:")
    newSiteLabel.place(x=231,y=setHeight+40)
    newSiteName = StringVar()
    entryBoxSite = Entry(window, textvariable=newSiteName)
    entryBoxSite.place(x=300,y=setHeight+40)
    
    newPWLabel = Label(window, text="Password:")
    newPWLabel.place(x=237,y=setHeight+60)
    newPw = StringVar()
    pwBoxSite = Entry(window, textvariable=newPw, show="*")
    pwBoxSite.place(x=300,y=setHeight+60)
    
    addButton = Button(window, text="ADD", command=lambda : addSite(newSiteName,newPw,sitesList, sites,pws, encryptKey))
    addButton.place(x=412,y=setHeight+90)
    
    ####MASTER PW####
    encryptLabel = Label(window, text="Encrypt Key:")
    encryptLabel.place(x=220,y=setHeight+20)
    
    encryptKey = StringVar()
    encryptEntry = Entry(window, textvariable=encryptKey)
    encryptEntry.place(x=300,y=setHeight+20)
    
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
    quitButton = Button(window, text="QUIT", command=lambda : quit(window))
    quitButton.place(x=410,y=450)
    #run gui
    window.mainloop()
    print 'Closing files'
    sitesTextFile.close()
    pwTextFile.close()
    
def quit(window):
	window.destroy()    

if __name__=="__main__":main()

