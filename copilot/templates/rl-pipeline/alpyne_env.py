"""
Starter sketch: wrap an AnyLogic model exported from the RL experiment as a Gym env via Alpyne.
This is a skeleton to adapt, not a runnable file.
"""
# from alpyne.client.alpyne_client import AlpyneClient   # see anylogic.help / Alpyne docs
# import gymnasium as gym

# 1. Export the AnyLogic model from the RL experiment.
# 2. Define observation, action, configuration and stop condition in the RL experiment.
#    The RL experiment has no reward field (8.9.10): compute the reward here, from observation fields.
# 3. Launch and control runs from here, exposing reset()/step() like a gym.Env.
