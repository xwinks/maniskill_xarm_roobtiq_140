# maniskill_xarm_roobtiq_140
This repo is built for xarm roboti with robotiq-140 gripper load and control for Maniskill environments


To run this repo, you need to install the ManiSkill environment with the xarm_robotiq_140_load_control branch.
```
git clone git@github.com:xwinks/ManiSkill.git
cd ManiSkill
git checkout xarm_robotiq_140_load_control
pip install -e .
```

Here we provide a script to compute the drive for the robotiq-140 gripper. 

```bash
python compute_the_drive_for_robotiq_140.py
```

We also provide a script to test the robotiq-140 gripper in ManiSkill environment with the pick-cube task.

```bash
python test_pick_cube.py --only-count-success --save-video
```







