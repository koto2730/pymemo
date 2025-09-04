#! /usr/bin/env python
# -*- coding: utf-8 -*-


from tkinter import *
from os import listdir, stat, remove, environ
from os.path import exists
from time import time, strftime, localtime
from sys import platform

from src.pymemo.config import Config
import re
import pickle as cPickle

CONFIG = Config()

from src.pymemo.memogrep import memogrep

# --- strict configure ---
LTAG='GOTO_TAG'
WTAG='URL_TAG'
CTAG='COMEFROM_TAG'
KEY_FILE_NAME='keyword'
DATA_EXT='.txt'
try:
	if platform == 'win32':
		FILE_HEAD = environ['COMPUTERNAME']
	else:
		FILE_HEAD = environ['HOSTNAME']
except:
	FILE_HEAD = 'memo'

class PyMemo(Tk):

	work_dir = './'
	listData = []
	curFilename = ''
	curText = ''
	keyword = ['PyMemo']
	KEY = re.compile(r'(?P<comefrom>^<<<\S*)')
	infoText = ''


	def __init__(self):
		Tk.__init__(self)
		self.encode = CONFIG.get('Main', 'BASE_ENCODE')
		self.createWidgets()
		self.title("pymemo - 0.0.10")
		#root.maxsize(width=300, height=200)
		#root.minsize(width=150, height=100)
		self.resizable(width=YES, height=YES)
		self.transient()
		self.initData()


	def initData(self):
		self.work_dir = CONFIG.get('Main', 'WORK_DIR')
		self.__readKeywordFile()
		self.__addTimeSortList()


	def preEnd(self):
		self.__save()
		self.quit()


	def __readKeywordFile(self):
		fpathname = self.work_dir + KEY_FILE_NAME
		if exists(fpathname):
			fin = open(fpathname, 'rb')
			try:
				self.keyword = cPickle.load(fin)
			finally:
				fin.close()
		else:
			self.__writeKeywordFile()
		if not isinstance(self.keyword, list):
			self.keyword = ['PyMemo']


	def __writeKeywordFile(self):
		fpathname = self.work_dir + KEY_FILE_NAME
		fo = open(fpathname, 'wb')
		try:
			cPickle.dump(self.keyword, fo, True)
		finally:
			fo.close()


	def new(self):
		if self.__save():
				self.__clear()
				self.__updateList()


	def __save(self):
		text = self.textView.get("1.0", "end-1c")
		if text == '': return False
		#text = text.encode(self.encode)
		# keyword db 
		m = self.KEY.match(text)
		if m:
			uk = m.group('comefrom')[3:]
			if not self.keyword.count(uk) :
				self.keyword.append(uk)
				self.keyword.sort()
				self.keyword.reverse()
				self.__writeKeywordFile()
		if self.curFilename:
			fpathname = self.work_dir + self.curFilename 
			open(fpathname, 'w').write(text)
			return True
		else:
			num = 0
			fname = strftime('%Y%m%d', localtime())
			while True:
				fpathname = "%s%s%s%02d%s" %  (
							self.work_dir, FILE_HEAD, fname, num, DATA_EXT) 
				if not exists(fpathname) :
					open(fpathname, 'w').write(text)
					return True
				num += 1
		return False


	def __open(self, fname):
		fpathname = self.work_dir + fname
		text = open(fpathname, 'r').read()
		self.curFilename = fname
		self.curText = text
		self.__displayMemo()


	def __displayMemo(self):
		TAG = re.compile('(?P<link>(\[\S*\])|(>>>\S*))|(?P<url>(http://|file:///)\S*)|(?P<keyp>%s)' % ('|'.join(self.keyword)))
		rawdata = self.curText
		i = 0
		n = len(rawdata)
		while i < n:
			match = TAG.search(rawdata, i)
			if not match:
				self.textView.insert('end', rawdata[i:n])
				break
			else:
				j = match.start(match.lastgroup)
				if i < j: self.textView.insert('end', rawdata[i:j])
				k = match.end(match.lastgroup)
				if match.lastgroup == 'link':
					self.textView.insert('end', rawdata[j:k], LTAG)
				elif match.lastgroup == 'url':
					self.textView.insert('end', rawdata[j:k], WTAG)
				elif match.lastgroup == 'keyp':
					self.textView.insert('end', rawdata[j:k], CTAG)
				i = k

		linkcolor = CONFIG.get('Window','LCOLOR')
		linkcolor2 = CONFIG.get('Window','LCOLOR2')
		self.textView.tag_configure(LTAG, foreground=linkcolor)
		self.textView.tag_configure(WTAG, foreground=linkcolor, underline=True)
		self.textView.tag_configure(CTAG, foreground=linkcolor2, underline=True)
		self.textView.tag_bind(LTAG, '<ButtonPress>', self.__searchFile)
		self.textView.tag_bind(WTAG, '<ButtonPress>', self.__openUrl)
		self.textView.tag_bind(CTAG, '<ButtonPress>', self.__searchFile2)


	def __searchFile(self, event):
		currentPos = event.widget.index('@%d,%d' % (event.x, event.y))
		#currentTags = widget.tag_names(currentPos)
		ranges = self.textView.tag_ranges(LTAG)
		for i in range(0, len(ranges), 2):
			start = ranges[i]
			stop = ranges[i+1]
			if start <= currentPos <= stop:
				break
		text = self.textView.get(start, stop)
		self.SEARCH_BOX.delete(0,'end')
		if text[0:3] == '>>>':
			self.SEARCH_BOX.insert(INSERT, text[3:])
		else:
			self.SEARCH_BOX.insert(INSERT, text[1:-1])
		self.searchKeyword()


	def __searchFile2(self, event):
		currentPos = event.widget.index('@%d,%d' % (event.x, event.y))
		#currentTags = widget.tag_names(currentPos)
		ranges = self.textView.tag_ranges(CTAG)
		for i in range(0, len(ranges), 2):
			start = ranges[i]
			stop = ranges[i+1]
			if start <= currentPos <= stop:
				break
		text = self.textView.get(start, stop)
		self.SEARCH_BOX.delete(0,'end')
		self.SEARCH_BOX.insert(INSERT, text)
		self.searchKeyword()


	def __openUrl(self, event):
		import webbrowser
		currentPos = event.widget.index('@%d,%d' % (event.x, event.y))
		cur_l, cur_c = currentPos.split('.')
		# currentTags = widget.tag_names(currentPos)
		ranges = self.textView.tag_ranges(WTAG)
		for i in range(0, len(ranges), 2):
			start = ranges[i]
			stop = ranges[i+1]
			#start_l, start_c = start.split('.')
			#stop_l, stop_c = stop.split('.')
			#if (int(start_l) == int(cur_l) == int(stop_l)):
			#	if int(start_c) <= int(cur_c) <= int(stop_c):
			text = self.textView.get(start, stop)
			webbrowser.open_new(text)
			#		break


	def __openUrls(self):
		import webbrowser
		ranges = self.textView.tag_ranges(WTAG)
		for i in range(0, len(ranges), 2):
			start = ranges[i]
			stop = ranges[i+1]
			text = self.textView.get(start, stop)
			webbrowser.open(text, True)


	# def __checkUrls(self):
	# 	import pywebcheck, os
	# 	if not self.__checkFormat(self.curText): return
	# 	data = self.curText.split('\n')
	# 	l = pywebcheck.checkUpdateSite(data[1:])
	# 	self.curText = data[0] + '\n' + '\n'.join(l)
	# 	self.textView.delete("1.0", "end-1c")
	# 	self.__displayMemo()


	def __checkFormat(self, text):
		'''̤����'''
		return True


	def delete(self):
		if self.curFilename:
			fpathname = self.work_dir + self.curFilename 
			remove(fpathname)
		self.__clear()
		self.__updateList()


	def cut(self, event=None):
		self.textView.event_generate("<<Cut>>")
		return "break"


	def copy(self, event=None):
		self.textView.event_generate("<<Copy>>")
		return "break"


	def paste(self, event=None):
		self.textView.event_generate("<<Paste>>")
		return "break"


	def select_all(self, event=None):
		self.textView.tag_add("sel", "1.0", "end-1c")
		self.textView.mark_set("insert", "1.0")
		self.textView.see("insert")
		return "break"


	def remove_selection(self, event=None):
		self.textView.tag_remove("sel", "1.0", "end")
		self.textView.see("insert")


	def __clear(self):
		self.curFilename = ''
		self.textView.delete("1.0", "end-1c")


	def searchKeyword(self, event=None):
		pattern = self.SEARCH_BOX.get()
		self.__clearList()
		if pattern:
			#pattern = pattern.encode(self.encode)
			self.__addContentTimeSortList(pattern)
		else:
			self.__addTimeSortList()


	def __updateList(self):
		self.__clearList()
		self.__addTimeSortList()


	def __clearList(self):
		self.textList.delete(0, self.textList.size())
		#self.textList.delete(0, len(self.listData))
		self.listData = []


	def keyRebuild(self):
		self.keyword = ['PyMemo']
		flist = listdir(self.work_dir)
		for fname in flist:
			if fname == KEY_FILE_NAME: continue
			fpathname = self.work_dir + fname
			data = open(fpathname).readline()
			m = self.KEY.match(data)
			if m:
				uk = m.group('comefrom')[3:]
				if not self.keyword.count(uk):
					self.keyword.append(uk)
		self.__writeKeywordFile()


	def __addTimeSortList(self):
		flist = listdir(self.work_dir)
		for fname in flist:
			if fname == KEY_FILE_NAME: continue
			fpathname = self.work_dir + fname
			atime = (stat(fpathname))[7]
			data = open(fpathname, 'r').readline()
			data = data
			if self.curFilename == fname: atime = time()
			self.listData.append([atime, fname, data]) 
		self.listData.sort()
		self.listData.reverse()
		i = 0
		for data in self.listData:
			self.textList.insert(i, data[2])
			i+=1


	def __addContentTimeSortList(self, pattern):
		flist = listdir(self.work_dir)
		for fname in flist:
			if fname == KEY_FILE_NAME: continue
			fpathname = self.work_dir + fname
			atime = (stat(fpathname))[7]
			datalist = memogrep(fpathname, pattern)
			for data in datalist:
				data2 = data
				if self.curFilename == fname: atime = time()
				self.listData.append([atime, fname, data2]) 
		self.listData.sort()
		self.listData.reverse()
		i = 0
		for data in self.listData:
			self.textList.insert(i, data[2])
			i+=1


	def OnListButtonRelease(self,event):
		index = int((self.textList.curselection())[0])
		fname = (self.listData[index])[1]
		self.__save()
		self.__clear()
		self.__open(fname)
		self.__updateList()


	def showAbout(self):
		top = Toplevel(self)
		t = Text(top)
		t.pack()
		t.insert(INSERT, self.infoText)
		self.wait_window(top)

	def createWidgets(self):
		frameMain = Frame(self, relief=SUNKEN, height=700)
		frameButton = Frame(self)

		self.SEARCH_BOX = Entry(frameButton)
		self.SEARCH_BOX.bind("<Key-Return>", self.searchKeyword)
		self.SEARCH_BOX.pack(side=LEFT, fill=BOTH)
		#KeyPress, KeyRelease
		
		self.SEARCH = Button(frameButton)
		self.SEARCH["text"] = u"検索"
		self.SEARCH["command"] = self.searchKeyword
		self.SEARCH.pack(side=LEFT)

		self.NEW = Button(frameButton)
		self.NEW["text"] = u"新規作成"
		self.NEW["fg"] = "blue"
		self.NEW["command"] = self.new
		self.NEW.pack(side=LEFT)

		#self.CUT = Button(frameButton)
		#self.CUT["text"] = u"�ڼ�"
		#self.CUT["command"] = self.cut
		#self.CUT.pack(side=LEFT)

		#self.COPY = Button(frameButton)
		#self.COPY["text"] = u"ʣ��"
		#self.COPY["command"] = self.copy
		#self.COPY.pack(side=LEFT)

		#self.PASTE = Button(frameButton)
		#self.PASTE["text"] = u"Ž��"
		#self.PASTE["command"] = self.paste
		#self.PASTE.pack(side=LEFT)

		self.SELECT_ALL = Button(frameButton)
		self.SELECT_ALL["text"] = u"全選択"
		self.SELECT_ALL["command"] = self.select_all
		self.SELECT_ALL.pack(side=LEFT)

		self.REMOVE_SELECT = Button(frameButton)
		self.REMOVE_SELECT["text"] = u"選択解除"
		self.REMOVE_SELECT["command"] = self.remove_selection
		self.REMOVE_SELECT.pack(side=LEFT)

		self.CLEAR = Button(frameButton)
		self.CLEAR["text"] = u"クリア"
		self.CLEAR["command"] = self.__clear
		self.CLEAR.pack(side=LEFT)

		self.OPENURLS = Button(frameButton)
		self.OPENURLS["text"] = u"OpenURLs"
		self.OPENURLS["command"] = self.__openUrls
		self.OPENURLS.pack(side=LEFT)

		#self.CHKURLS = Button(frameButton)
		#self.CHKURLS["text"] = u"CheckURLs"
		#self.CHKURLS["command"] = self.__checkUrls
		#self.CHKURLS.pack(side=LEFT)

		self.DELETE = Button(frameButton)
		self.DELETE["text"] = u"削除"
		self.DELETE["fg"] = "purple"
		self.DELETE["command"] = self.delete
		self.DELETE.pack(side=LEFT)

		self.KEYDB_REBUILD = Button(frameButton)
		self.KEYDB_REBUILD["text"] = u"DB再構築"
		self.KEYDB_REBUILD["fg"] = "red"
		self.KEYDB_REBUILD["command"] = self.keyRebuild
		self.KEYDB_REBUILD.pack(side=LEFT)

		#self.ABOUT = Button(frameButton)
		#self.ABOUT["text"] = u"about"
		#self.ABOUT["command"] =  self.showAbout
		#self.ABOUT.pack(side=RIGHT)

		self.QUIT = Button(frameButton)
		self.QUIT["text"] = u"終了"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.preEnd
		self.QUIT.pack(side=RIGHT)

		frameButton.pack(side=TOP, fill=BOTH)

		frameList = Frame(self, relief=SUNKEN, height=200)
		self.scrollbarList = Scrollbar(frameList, orient=VERTICAL,
									   takefocus=FALSE, highlightthickness=0)
		self.textList = Listbox(frameList, setgrid=True)
		self.scrollbarList.config(command=self.textList.yview)
		self.textList.config(yscrollcommand=self.scrollbarList.set)
		self.scrollbarList.pack(side=RIGHT, fill=Y)
		self.textList.bind('<ButtonRelease-1>', self.OnListButtonRelease)
		self.textList.pack(side=LEFT, expand=TRUE, fill=BOTH)
		frameList.pack(side=LEFT, expand=TRUE, fill=BOTH)

		frameText = Frame(frameMain, relief=SUNKEN)
		self.scrollbarView = Scrollbar(frameText, orient=VERTICAL, 
									   takefocus=FALSE, highlightthickness=0)
		self.textView = Text(frameText, wrap=WORD, highlightthickness=0)
		self.scrollbarView.config(command=self.textView.yview)
		self.textView.config(yscrollcommand=self.scrollbarView.set)
		self.scrollbarView.pack(side=RIGHT, fill=Y)
		self.textView.pack(side=LEFT, expand=TRUE, fill=BOTH)
		frameText.pack(side=LEFT, expand=TRUE, fill=BOTH)

		frameMain.pack(side=TOP, expand=TRUE, fill=BOTH)


def main():
	pm = PyMemo()
	pm.mainloop()


if __name__=='__main__':
	main()
