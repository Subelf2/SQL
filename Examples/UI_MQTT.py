import tkinter as tk
import paho.mqtt.client as mqtt

# Window creation
window = tk.Tk()
window.title("Mqtt test")

# frame init
frm = tk.Frame(window, background="light blue", padx=5, pady=5)
frm.pack()

# StringVar to hold the message
message_val = tk.StringVar()

# StringVar to display the latest received message
received_message_val = tk.StringVar()
received_message_val.set("No messages received yet.")

# labels init
msg_lbl = tk.Label(frm, text="Message:", background='light blue', font=("Arial", 24))
msg_lbl.grid(column=1, row=1)

# entry init
msg_entry = tk.Entry(frm, textvariable=message_val, font=("Arial", 24))
msg_entry.grid(column=2, row=1)

# Label to display the latest received message
received_msg_lbl = tk.Label(frm, textvariable=received_message_val, background='light blue', font=("Arial", 18))
received_msg_lbl.grid(column=1, row=3, columnspan=2)

# MQTT functions
def on_connect(client, userdata, flags, rc, props=None):
    print(f"Connected with result code {rc}")
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Message received: {msg.topic} {message}")
    # Update the label with the latest received message
    received_message_val.set(f"Latest message: {message}")

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
mqttc.loop_start()

# Function to send the message
def send_message():
    message = message_val.get()
    if message.strip() == "":
        print("Please enter a message to send.")
    else:
        mqttc.publish("test/topic", message, retain=True)
        print(f"Message sent: {message}")

# button init
send_btn = tk.Button(frm, text="Send Message", command=send_message, font=("Arial", 24))
send_btn.grid(column=1, row=2, columnspan=2)

# Main function, so the UI starts and interacts with the user.
window.mainloop()
