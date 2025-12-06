from tkinter import *
import requests
from urllib.request import urlopen
from PIL import ImageTk,Image
import io


class news_GUI : 
    def __init__(self):
        self.data = requests.get("https://newsdata.io/api/1/latest?country=in&language=en&apikey=pub_c0f3643f166144ce908b709535b2a6c4").json()
        self.loadgui()
        self.load_news_item(0)
        
        self.root.mainloop()

    def loadgui(self): 
        self.root = Tk()
        self.root.title("NEWS APP")
        self.root.iconbitmap(r"resources\favicon.ico")
        self.root.geometry('350x600')
        self.root.resizable(0,0)
        self.root.config(bg="gray")
        

    def clear(self): 
        for i in self.root.pack_slaves(): 
            i.destroy()

    def load_news_item(self,index): 
        self.clear()

        img_url = self.data["results"][index]["image_url"]

        if img_url:
            rawdata = urlopen(img_url).read()
            im = Image.open(io.BytesIO(rawdata)).resize((350,250))
        else:
            im = Image.open("fallback.png").resize((350,250))

        photo = ImageTk.PhotoImage(im)

        lable = Label(self.root, image=photo)
        lable.pack()

        heading = Label(self.root,text= self.data["results"][index]["title"], bg='black',fg= 'white',wraplength=350,justify='center')
        heading.pack(pady=(10,20))
        heading.config(font=('verdana',15))

        details = Label(self.root,text= self.data["results"][index]["description"], bg='black',fg= 'white',wraplength=350,justify='center')
        details.pack(pady=(10,20))
        details.config(font=('verdana',15))
        

        frame = Frame(self.root,bg = 'black')
        frame.pack(expand=True,fill=BOTH)

        prev = Button(frame,text="prev",width=16,height=3)
        prev.pack(side=LEFT)

        read = Button(frame,text="Read more",width=16,height=3)
        read.pack(side=LEFT)

        next= Button(frame,text="next",width=16,height=3)
        next.pack(side=LEFT)



obj = news_GUI()