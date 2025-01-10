from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from chatbot import get_response, get_response2
import os

# File to store FAQs
FAQ_FILE = "faqs.txt"

# Chatbot Listener
class ChatbotServer(WebSocket):

    def handleMessage(self):
        # Receive a query, process it, and send back the response
        message = self.data
        print(f"Chatbot received query: {message}")

        # Process the query using the chatbot
        response = get_response(message)
        additional_response = get_response2(message)
        
        # Send the chatbot response back to the client
        self.sendMessage(response)
        self.sendMessage(additional_response)
        print(f"Chatbot sent responses: {response}, {additional_response}")

    def handleConnected(self):
        print(f"Chatbot client {self.address} connected")

    def handleClose(self):
        print(f"Chatbot client {self.address} disconnected")



class FAQServer(WebSocket):

    def handleMessage(self):
        
        message = self.data
        print(f"FAQ listener received: {message}")

        try:
            
            with open(FAQ_FILE, "a") as file:
                file.write(message + "\n")
            print(f"FAQ stored: {message}")
            self.sendMessage("FAQ stored successfully.")
        except Exception as e:
            print(f"Error storing FAQ: {e}")
            self.sendMessage("Error storing FAQ.")

    def handleConnected(self):
        print(f"FAQ client {self.address} connected")

    def handleClose(self):
        print(f"FAQ client {self.address} disconnected")


# 
chatbot_port = 3500
faq_port = 3600

chatbot_server = SimpleWebSocketServer('0.0.0.0', 3500, ChatbotServer)
faq_server = SimpleWebSocketServer('0.0.0.0', 3600, FAQServer)

print(f"Starting Chatbot server on port {chatbot_port}")
print(f"Starting FAQ server on port {faq_port}")


from threading import Thread

Thread(target=chatbot_server.serveforever, daemon=True).start()
Thread(target=faq_server.serveforever, daemon=True).start()


while True:
    pass
