# actions.py

env = None  # external injection

def set_env(e):
  """
  Sets the simulation environment.
  Must be called before any action.
  """
  global env
  env = e

def grab(obj_name):
  """
  Grabs the specified object by name.
  """
  obj_id = env.find_obj(obj_name)
  env.pick(obj_id)

def put_first_on_second(obj1, obj2):
  """
  Picks up obj1 and places it on top of obj2.
  """
  grab(obj1)
  move_to(*env.get_obj_pos(obj2))
  place_on(obj2)
  release()

def goto_pos(position_name):
  """
  Moves the arm to a named position.
  """
  pos = env.parse_position(position_name)
  env.goto(pos)

def pick_place(obj_name, target_pos):
  """
  Picks up obj_name and places it at target_pos.
  """
  grab(obj_name)
  move_to(*target_pos)
  place(*target_pos)
  release()

def get_obj_pos(obj_name):
  """
  Returns the position of the object.
  """
  return env.get_obj_pos(obj_name)

def parse_position(text):
  """
  Parses a position name string and returns coordinates.
  """
  return env.parse_position(text)

def parse_obj_name(text):
  """
  Parses a text description and returns a valid object name.
  """
  return env.parse_obj_name(text)

def stack_objects_in_order(obj_list):
  """
  Stacks objects in the given order (bottom to top).
  """
  for i, obj in enumerate(obj_list):
    grab(obj)
    if i == 0:
      move_to(*env.get_stack_base_position())
      place(*env.get_stack_base_position())
    else:
      place_on(obj_list[i-1])
    release()

def say(message):
  """
  Logs or displays a message.
  """
  env.say(message)

def pointat(obj_name):
  """
  Points at the given object.
  """
  env.pointat(obj_name)

def move_to(x, y):
  env.move_held_to(x, y)

def place(x, y):
  env.place_at(x, y)

def place_on(target_name):
  target_id = env.find_obj(target_name)
  env.place_on_target(target_id)

def release():
  env.release()

def wait(seconds):
  env.wait(seconds)
