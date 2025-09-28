import tkinter as tk
import time
import threading

# ================== Traffic Light Class ==================
class TrafficLight:
    def __init__(self, canvas, x, y, green_time=5, red_time=5):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.green_time = green_time
        self.red_time = red_time
        self.state = "GREEN"
        self.timer = 0

        # Draw traffic light (circle)
        self.light = self.canvas.create_oval(x, y, x+30, y+30, fill="green")

    def update(self):
        self.timer += 1
        if self.state == "GREEN" and self.timer >= self.green_time:
            self.state = "RED"
            self.timer = 0
            self.canvas.itemconfig(self.light, fill="red")
        elif self.state == "RED" and self.timer >= self.red_time:
            self.state = "GREEN"
            self.timer = 0
            self.canvas.itemconfig(self.light, fill="green")


# ================== Car Class ==================
class Car:
    def __init__(self, canvas, x, y, traffic_light):
        self.canvas = canvas
        self.traffic_light = traffic_light
        self.rect = self.canvas.create_rectangle(x, y, x+40, y+20, fill="blue")
        self.speed = 5
        self.wait_time = 0

    def move(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # Check if car is near the traffic light
        if (x2 >= self.traffic_light.x - 40 and 
            x1 <= self.traffic_light.x + 40 and 
            self.traffic_light.state == "RED"):
            # Car waits
            self.wait_time += 1
            return

        # Move car
        self.canvas.move(self.rect, self.speed, 0)

        # Loop car back when it goes off screen
        if x1 > 600:
            self.canvas.move(self.rect, -650, 0)


# ================== Simulation Class ==================
class TrafficSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Simulation - Tkinter")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="lightgrey")
        self.canvas.pack()

        # Road
        self.canvas.create_rectangle(0, 150, 600, 250, fill="black")

        # Traffic light
        self.traffic_light = TrafficLight(self.canvas, 300, 100, green_time=5, red_time=5)

        # Cars
        self.cars = [
            Car(self.canvas, 0, 180, self.traffic_light),
            Car(self.canvas, -150, 180, self.traffic_light),
            Car(self.canvas, -300, 180, self.traffic_light)
        ]

        # Start simulation in thread
        self.running = True
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

        # Button to stop simulation
        self.stop_button = tk.Button(root, text="Stop Simulation", command=self.stop)
        self.stop_button.pack(pady=10)

    def run(self):
        while self.running:
            # Update traffic light
            self.traffic_light.update()

            # Move cars
            for car in self.cars:
                car.move()

            self.root.update_idletasks()
            self.root.update()
            time.sleep(0.5)

    def stop(self):
        self.running = False
        self.root.destroy()


# ================== Run Simulation ==================
if __name__ == "__main__":
    root = tk.Tk()
    sim = TrafficSimulation(root)
    root.mainloop()
