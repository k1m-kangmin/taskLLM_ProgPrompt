# envs/tabletop_env.py

import pybullet as p
import pybullet_data
import time
import os

class PickPlaceEnv:
  def __init__(self, record=False):
    self.client = p.connect(p.GUI)
    p.setGravity(0, 0, -9.8)
    assets_path = os.path.join(os.getcwd(), "assets")
    p.setAdditionalSearchPath(assets_path)
    self.record = record
    self.video_log_id = None
    self.objects = {}
    self.held_object = None
    self.positions = {
      "top left corner":     [-0.25, -0.25],
      "top side":            [0.00,  -0.25],
      "top right corner":    [0.25, -0.25],
      "left side":           [-0.25, -0.50],
      "center":              [0.00,  -0.50],
      "right side":          [0.25, -0.50],
      "bottom left corner":  [-0.25, -0.75],
      "bottom side":         [0.00,  -0.75],
      "bottom right corner": [0.25, -0.75]
    }
    self.objects_list = [
      "red block", "green block", "blue block",
      "red bowl", "green bowl", "blue bowl"
    ]

    if self.record:
      os.makedirs("output", exist_ok=True)
      self.video_log_id = p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4, "output/tmp_record.mp4")

    self.load_table()

    def load_table(self):
      assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
      assets_path = os.path.abspath(assets_path)
      p.setAdditionalSearchPath(assets_path)
      
      p.loadURDF("plane.urdf")
      p.loadURDF("table/table.urdf", [0, 0, -0.65], p.getQuaternionFromEuler([0, 0, 0]))



    p.loadURDF("plane.urdf")
    p.loadURDF("table/table.urdf", [0, 0, -0.65], p.getQuaternionFromEuler([0, 0, 0]))


  def reset(self, obj_list):
    self.objects = {}
    base_x = 0.0
    base_y = -0.6
    for i, name in enumerate(obj_list):
      xpos = base_x + (i - len(obj_list) / 2) * 0.1
      ypos = base_y
      obj_id = p.loadURDF("cube_small.urdf", [xpos, ypos, 0.02])
      self.objects[name] = obj_id

  def find_obj(self, name):
    return self.objects[name]

  def pick(self, obj_id):
    self.held_object = obj_id

  def move_held_to(self, x, y):
    if self.held_object is not None:
      pos = [x, y, 0.1]
      p.resetBasePositionAndOrientation(self.held_object, pos, [0, 0, 0, 1])

  def place_at(self, x, y):
    if self.held_object is not None:
      pos = [x, y, 0.02]
      p.resetBasePositionAndOrientation(self.held_object, pos, [0, 0, 0, 1])

  def place_on_target(self, target_id):
    if self.held_object is not None:
      target_pos, _ = p.getBasePositionAndOrientation(target_id)
      new_pos = [target_pos[0], target_pos[1], target_pos[2] + 0.04]
      p.resetBasePositionAndOrientation(self.held_object, new_pos, [0, 0, 0, 1])

  def slide_to(self, obj_id, x, y):
    pos = [x, y, 0.02]
    p.resetBasePositionAndOrientation(obj_id, pos, [0, 0, 0, 1])

  def rotate(self, obj_id, angle_deg):
    quat = p.getQuaternionFromEuler([0, 0, angle_deg * 3.14 / 180])
    pos, _ = p.getBasePositionAndOrientation(obj_id)
    p.resetBasePositionAndOrientation(obj_id, pos, quat)

  def get_obj_pos(self, name):
    obj_id = self.objects[name]
    pos, _ = p.getBasePositionAndOrientation(obj_id)
    return pos[:2]

  def wait(self, seconds):
    for _ in range(int(seconds * 240)):
      p.stepSimulation()
      time.sleep(1 / 240.0)

  def say(self, message):
    print(f"[Robot says]: {message}")

  def pointat(self, obj_name):
    print(f"[Robot points at]: {obj_name}")

  def parse_position(self, text):
    return self.positions[text]

  def parse_obj_name(self, text):
    for obj in self.objects_list:
      if text in obj:
        return obj
    return text

  def get_stack_base_position(self):
    return [0.0, 0.0]

  def release(self):
    self.held_object = None

  def save_video(self, output_path):
    if self.record and self.video_log_id is not None:
      p.stopStateLogging(self.video_log_id)
      os.rename("output/tmp_record.mp4", output_path)

  def goto(self, pos):
    print(f"[Robot arm moves to]: {pos}")
