from tkinter import *
import requests
from urllib.request import urlopen, Request
from PIL import ImageTk,Image
import io
import webbrowser

class news_GUI : 

    def __init__(self):

        try:
            self.data = requests.get("https://newsdata.io/api/1/latest?country=in&language=en&apikey=pub_c0f3643f166144ce908b709535b2a6c4").json()
        except:
            print("Abhi thikh kerke deta hu(API ki dikkat h)")    
        self.loadgui()
        self.load_news_item(0)
        self.root.mainloop()
        
    def loadgui(self): 
        self.root = Tk()
        self.root.title("NEWS APP")
        self.root.iconbitmap(r"resources\favicon.ico")
        self.root.geometry('500x600')
        self.root.resizable(0,0)
        self.root.config(bg="#1e1e1e")
        
        self.canvas = Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame = Frame(self.canvas, bg="#1e1e1e")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


    def clear(self): 
        for i in self.frame.winfo_children(): 
            i.destroy()

    def load_news_item(self,index): 

        if index < 0 or index >= len(self.data["results"]):
            return
        self.clear()

        img_url = self.data["results"][index]["image_url"]

        try:
            if img_url:
                req = Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                rawdata = urlopen(req).read()
                im = Image.open(io.BytesIO(rawdata)).resize((350,250))
            else:
                raise Exception("No image")
        except:
            im = Image.open("fallback.png").resize((490,250))

        photo = ImageTk.PhotoImage(im)

        lable = Label(self.frame, image=photo)
        lable.image = photo 
        lable.pack()

        heading = Label(self.frame,text= self.data["results"][index]["title"], bg='black',fg= 'white',wraplength=500,justify='center')
        heading.pack(pady=(5,5),padx=(5,0))
        heading.config(font=('verdana',15))

        details = Label(self.frame,text= self.data["results"][index]["description"], bg='black',fg= 'white',wraplength=500,justify='center')
        details.pack(pady=(5,5),padx=(5,0))
        details.config(font=('verdana',10))
        

        frame = Frame(self.frame,bg = "#1D1D1D")
        frame.pack(expand=True,fill=BOTH)

        if index !=  0:
            prev = Button(frame,text="prev",width=20,height=3,command=lambda: self.load_news_item(index-1))
            prev.pack(side=LEFT,padx=(10,5))

        read = Button(frame,text="Read more",width=20,height=3,command=lambda: self.open_link(self.data["results"][index]["link"]) )
        read.pack(side=LEFT,padx=5)

        if index != len(self.data["results"])-1: 
            next= Button(frame,text="next",width=20,height=3,command=lambda: self.load_news_item(index+1))
            next.pack(side=LEFT,padx=5)

    def open_link(self,url): 
        if url:
            webbrowser.open(url)


obj = news_GUI()