from tkinter import *
import sqlite3
import tkinter.messagebox
from reportlab.pdfgen import canvas
win=Tk()
win.title("Bill Generator")
win.minsize(400,500)
win.maxsize(400,500)
price=[]
itms=[]
qn=[]
class dbase():
	def price(self,itm):
		con=sqlite3.connect('billgen.db')
		c=con.cursor()
		c.execute("SELECT price FROM bill WHERE item=?",(itm,))
		p=int(c.fetchone()[0])
		print(p)
		return p;
class ui(dbase):
	def __init__(self):
		lb1 = Label(text ="Item").place(x=10,y=10,width=100,height=25)
		lb2 = Label(text ="Quantity").place(x=150,y=10,width=50,height=25)
		items=['Pasta','Noodles','Fries','Fried Rice','Chicken Chili','Kefsa','Egg Roll','Manchurian','Chowmein','Manchow Soup'] 
		self.item = StringVar()
		self.item.set(items[0])
		L_item=OptionMenu(win,self.item,*items).place(x=10,y=40,width=130,height=25)
		self.qt=Entry(bd=2)
		self.qt.place(x=150,y=40,width=40,height=25)
		lb3=Label(text ="Product(s)").place(x=60,y=80)
		lb4=Label(text ="Quantity").place(x=210,y=80)
		lb5=Label(text ="Price").place(x=295,y=80)
		self.scrollbar = Scrollbar(orient=VERTICAL,command=self.scr)	
		self.l1=Listbox(win,yscrollcommand=self.scrollbar.set,bd=1,width=30,height=20)
		self.l2=Listbox(win,yscrollcommand=self.scrollbar.set,bd=1,width=20,height=20)
		self.l3=Listbox(win,yscrollcommand=self.scrollbar.set,bd=1,width=10,height=20)
		self.scrollbar.place(x=343,y=100,height=325)
		self.l1.place(x=10,y=100)
		self.l2.place(x=185,y=100)
		self.l3.place(x=280,y=100)	
		B = Button(text ="Add Item", command = self.cmnd).place(x=220,y=40)	
		prnt=Button(text="Print",command=self.prn).place(x=282,y=445)
	def cmnd(self):
		try:
			if int(self.qt.get())>0:
				self.price=super().price(self.item.get())
				self.price=self.price*int(self.qt.get())
				price.append(int(self.price))
				itms.append(str(self.item.get()))
				qn.append(str(self.qt.get()))
				self.tot=sum(price)*1.15
				self.l1.insert(END,"\t".expandtabs(15)+self.item.get())
				self.l2.insert(END,"\t".expandtabs(12)+self.qt.get())							
				self.l3.insert(END,"\t".expandtabs(6)+str(self.price))	
				self.lb6=Label(text="Total + 15% GST").place(x=15,y=423)
				self.lb7=Label(text=int(self.tot)).place(x=288,y=423)
		except ValueError: 
			tkinter.messagebox.showerror("Bill Generator", "Invalid Entry!!!")
	def prn(self):
			print("printing...")
			c=canvas.Canvas("Bill.pdf")
			x=40
			y=800
			x1=140
			x2=240
			z=20
			c.drawString(x,y,"Item")
			c.drawString(x1,y,"Quantity")
			c.drawString(x2,y,"Price")
			for i,j,k in zip(price,itms,qn):
				c.drawString(x,y-z,str(j))
				c.drawString(x+5,y-z,"")
				c.drawString(x2,y-z,str(i))
				c.drawString(x2+5,y-z,"")
				c.drawString(x1,y-z,str(k))
				c.drawString(x1+5,y-z,"")
				print(i,j,k,end="\t")
				z=z+20
			c.drawString(0,y-z+3,"")
			c.drawString(x,y-z,"Total + 15% GST")
			c.drawString(x2,y-z,str(int(self.tot)))
			c.save()
	def scr(self,*args):
		self.l1.yview(*args)
		self.l2.yview(*args)
		self.l3.yview(*args)
u=ui()
win.mainloop()
