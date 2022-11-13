import gym

with open("src/logs.txt", mode = 'w') as f:

    env = gym.make("LunarLander-v2", render_mode="rgb_array")
    env.action_space.seed(42)

    observation, info = env.reset(seed=42)

    for _ in range(1000):
        observation, reward, terminated, truncated, info = env.step(env.action_space.sample())

        if terminated or truncated:
            observation, info = env.reset()
        f.write(f"{reward}\n")
    env.close()
    f.close()