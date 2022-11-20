import gym

env = gym.make("LunarLander-v2", render_mode="rgb_array")
env.action_space.seed(42)

observation, info = env.reset(seed=42)

for _ in range(10):
    observation, reward, terminated, truncated, info = env.step(env.action_space.sample())

    if terminated or truncated:
        observation, info = env.reset()
    print(f"{reward}")
env.close()

from time import sleep

for i in range(10):
    print(i + 1)
    sleep(1)