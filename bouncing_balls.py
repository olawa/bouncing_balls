from tkinter import *
import random as r


class App(Tk):
    """ creates an app with a frame for balls and input boxes for gravity etc """
    def __init__(self):
        super().__init__()
        self.frame = Frame(self)
        self.canvas = Canvas(self, width=1200, height=1200, background='gray75') #,
        self.canvas.grid(row=0,column=1)
        self.frame.grid(row=0,column=0, sticky="n")
        self.gravity = StringVar()
        self.num_balls = StringVar()
        self.speed = StringVar()
        self.gravity.set("2")
        self.num_balls.set("25")
        self.speed.set("30")
        self.start_button = Button(self.frame, text="Add balls", width=10, height=4)
        self.start_button.grid(row=4,column=0)
        self.start_button.bind("<Button-1>", self.start)
        self.stop_button = Button(self.frame, text="Clear", width=10, height=4)
        self.stop_button.grid(row=6,column=0)
        self.stop_button.bind("<Button-1>", self.stop)
        self.update_button = Button( self.frame, text="Update", width=10,  height=4)
        self.update_button.grid(row=4,column=1)
        self.update_button.bind("<Button-1>", lambda event: self.update_vars(event, delay, current_gravity))
        self.num_balls_info = Label(self.frame, text = "Balls: ")
        self.num_balls_info.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nw")
        self.gravity_info = Label(self.frame, text = "Gravity: ")
        self.gravity_info.grid(row=1, column=0, columnspan=4, padx=5, pady=5,sticky="w")
        self.speed_info  = Label(self.frame, text = "Delay (ms): ")
        self.speed_info.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="w")
        self.gravity_box  = Entry(self.frame,textvariable = self.gravity, font=('calibre',20,'normal'), width=8)
        self.gravity_box.grid(row=1, column=1)
        self.speed_box  = Entry(self.frame,textvariable = self.speed, font=('calibre',20,'normal'),  width=8)
        self.speed_box.grid(row=2, column=1)
        self.num_ball_box = Entry(self.frame,textvariable = self.num_balls, font=('calibre',20,'normal'), width=8)
        self.num_ball_box.grid(row=0, column=1)
        self.info =  Label(self.frame, text = "Create balls with random size and\ncolor. Bombs kills balls \nColliding balls\ngain speed")
        self.info.grid(row=12, column=0, columnspan=3, rowspan=5, padx=5, pady=5, sticky="sw")
      
    def start(self, event):
        """ create random balls based on values in entry boxes """
        self.delay = int(self.speed.get())
        self.current_gravity = int(self.gravity.get())
        for i in range(int(self.num_balls.get())):
            rad = r.randint(w // 50, w // 20)
            origo = r.randint(rad+100,w-rad-100), r.randint(rad+100,h-rad-100)
            new_ball = Ball(rad, origo[0], origo[1], colors[r.randint(0,len(colors)-1)], self.delay, self.current_gravity)
            ball_dict[new_ball.ball] = new_ball
            new_ball.move()
        
    def stop(self, event):
        self.canvas.delete("all")

    def update_vars(self, event, delay, current_gravity):
        self.delay = int(self.speed.get())
        self.current_gravity = int(self.gravity.get())
        print(current_gravity)
        for i in ball_dict:
            ball_dict[i].delay = delay
            ball_dict[i].gravity = current_gravity


class Ball():
    """ 
    creates balls with random colors, sie and speed and adds to the app 
    and to a global dict for reference in collission
    """
    def __init__(self, size, xpos, ypos, col, delay, current_gravity):
        self.color = col
        self.size = size
        self.canvas = app.canvas
        if col == "black": # replace black balls with bombs
            self.img = PhotoImage(file = "bomb.png")
            self.ball = self.canvas.create_image(xpos-size, ypos+size, image=self.img, anchor ="nw")
            self.width = self.img.width()
            self.height = self.img.height()
        else:
            self.ball = self.canvas.create_oval(xpos-size,ypos-size,xpos+size, ypos+size, fill= self.color )      
        self.speedx = r.randint(-10,10)
        self.speedy = r.randint(-10,10)
        self.delay = app.delay
        self.gravity = app.current_gravity
        self.collided = False
        
    def __str__(self):
        return str(self.ball)
    
    def move(self):
        app.canvas.move(self.ball, round(self.speedx), round(self.speedy) )
        self.speedy += self.gravity * 0.1
       
        if len(app.canvas.coords(self.ball)) > 0:
            if len(app.canvas.coords(self.ball)) == 2:
                x1, y1 = app.canvas.coords(self.ball)
                x2, y2 = x1 + self.width, y1 + self.height
            else:
                x1, y1, x2, y2 = app.canvas.coords(self.ball)
            if x1 <= 0 or x2 >= w:
                self.speedx *= -1
            if y1 <=0 or y2 >= h: 
                self.speedy = -self.speedy * 0.8
                if y2 >= h: # avoid losing balls due to gravity
                    app.canvas.move(self.ball, 0, - self.gravity) 
            coll = list(app.canvas.find_overlapping(x1, y1, x2, y2)) # get a list of colliding balls
            if self.ball in coll:
                coll.remove(self.ball)            
            for i in coll:
                if self.color == "black" and ball_dict[i].color != "black":
                    app.canvas.delete(i)
                    del ball_dict[i]
                elif ball_dict[i].color ==  "black" and self.color != "black":
                    app.canvas.delete(self.ball)
                else: # change direction (should use a function to calculate new direction)
                    ball_dict[i].speedx *= -1
                    ball_dict[i].speedy *= -1
                    self.speedx *= -1
                    self.speedy *= -1
            if self.ball:
                self.canvas.after(self.delay, self.move)
 

colors = ['blue', 'black', 'green', 'red', 'yellow', 'orange', 'purple', 'lightblue', 'blue', 'pink', 'grey']
ball_dict = {} # link id from creat_oval to Ball

app = App()
app.start("<Button-1>") # start the simulation
app.mainloop()
