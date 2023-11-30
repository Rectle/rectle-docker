from time import sleep

def load(path):
    pass

def func():
    # Load model
    model = load("""{% RECTLE.VAR.MODEL_PATH %}""")
    pass

for i in range(1, 10):
    sleep(4)
    print(f"Generation: {i*1000}/10000" )

score = 10

#% RECTLE.FUNC.SEND_RESULT score %#

print("test")