from queue_controller.queue_controller import QueueController
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    queue = QueueController()
    queue.run()
