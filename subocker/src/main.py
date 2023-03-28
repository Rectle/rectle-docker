from queue_controller.queue_controller import QueueController
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    queue = QueueController()
    queue.run()

# TODO
# - add log handling
# - safe container turn down
# - discuss of building an virt env in docker container 
# - discuss code preprocess and change chmod of shared files in a volume