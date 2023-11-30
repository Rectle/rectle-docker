import gym
import sys
import numpy as np
import tensorflow as tf
from keras import models
from PIL import Image

render_env = gym.make("CartPole-v1", render_mode='rgb_array')


def render_episodes(env: gym.Env, model: tf.keras.Model, max_steps: int, episodes: int):
    episodes_images = []
    for e in range(1, episodes + 1):
        state, info = env.reset()
        state = tf.constant(state, dtype=tf.float32)
        screen = env.render()
        images = [Image.fromarray(screen)]
        sum_reward = 0
        for i in range(1, max_steps + 1):
            state = tf.expand_dims(state, 0)
            action_probs, _ = model(state)
            action = np.argmax(np.squeeze(action_probs))

            state, reward, done, truncated, info = env.step(action)
            state = tf.constant(state, dtype=tf.float32)
            print(f"Iteration {i} reward: {reward}")
            
            sum_reward += reward
            # Render screen every 10 steps
            if i % 10 == 0:
                screen = env.render()
                images.append(Image.fromarray(screen))

            if done:
                break
        print(f'Episode {e} : Reward {sum_reward}')
        episodes_images.append(images)
    return episodes_images


model = models.load_model(str(sys.argv[1]) + 'trained_model/')
# Save GIF image
min_episodes_criterion = 100
max_episodes = 2
max_steps_per_episode = 1000
images = render_episodes(render_env, model, max_steps_per_episode, max_episodes)
# loop=0: loop forever, duration=1: play each frame for 1ms
for e in range(0, max_episodes):
    image_file = str(sys.argv[1]) + f'gifs/cartpole-v{e + 1}.gif'
    images[e][0].save(
        image_file, save_all=True, append_images=images[e][1:], loop=0, duration=0.5)