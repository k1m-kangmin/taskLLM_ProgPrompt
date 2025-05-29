def stack_red_block_on_blue_bowl():
  grab("red block")
  move_to(*get_obj_pos("blue bowl"))
  place_on("blue bowl")
  release()
