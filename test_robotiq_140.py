import gymnasium as gym
import mani_skill.envs
import time
import numpy as np

from mani_skill.sensors.camera import (
    Camera,
    CameraConfig,
    parse_camera_configs,
    update_camera_configs_from_dict,
)
env = gym.make("PickCube-v1",
               render_mode = "rgb_array",
               robot_uids = "xarm6_robotiq_140",
               obs_mode = "rgb",
               sensor_configs = dict(width=1280, height=720)

               )
obs, _ = env.reset(seed=0)
env.unwrapped.print_sim_details() # print verbose details about the configuration
done = False
start_time = time.time()
t = 0
camera_image = []
while not done:
    action = np.random.randn(1)
    # print(t)
    t += 1
    if t < 100:
        action = np.array([0,0,0,0,0,0,0.05])
    else:
        action = np.array([0,0,0.1,0,0,0,0.05])
        # import pdb;pdb.set_trace()
    obs, rew, terminated, truncated, info = env.step(action)
    # done = terminated or truncated
    # print("the obs keys are: ", obs['sensor_data']['base_camera']['rgb'].shape)
    camera_image.append(obs['sensor_data']['base_camera']['rgb'][0].detach().cpu().numpy())
    done = False
    
    if t == 200:
        break
    # env.render()
# save the camera image as video    
import cv2

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# Ensure the images are in the correct shape and type for OpenCV (H, W, 3), uint8
# Also, get the correct width and height from the first image
if len(camera_image) > 0:
    first_img = camera_image[0]
    # If the image is not uint8, convert it
    if first_img.dtype != np.uint8:
        first_img = (np.clip(first_img, 0, 1) * 255).astype(np.uint8)
    height, width = first_img.shape[:2]
    out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (width, height))
    for image in camera_image:
        # Convert image to uint8 if necessary
        if image.dtype != np.uint8:
            img_to_write = (np.clip(image, 0, 1) * 255).astype(np.uint8)
        else:
            img_to_write = image
        # If image has an extra batch dimension, squeeze it
        if img_to_write.ndim == 4 and img_to_write.shape[0] == 1:
            img_to_write = img_to_write[0]
        # If image is grayscale, convert to BGR
        if img_to_write.ndim == 2 or (img_to_write.ndim == 3 and img_to_write.shape[2] == 1):
            img_to_write = cv2.cvtColor(img_to_write, cv2.COLOR_GRAY2BGR)
        # If image is RGB, convert to BGR for OpenCV
        if img_to_write.shape[2] == 3:
            img_to_write = cv2.cvtColor(img_to_write, cv2.COLOR_RGB2BGR)
        out.write(img_to_write)
    out.release()
else:
    print("No images to write to gif.")
    
N = info["elapsed_steps"].item()
dt = time.time() - start_time   
FPS = N / (dt)
print(f"Frames Per Second = {N} / {dt} = {FPS}")