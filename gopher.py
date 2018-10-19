def gameDay(hole_lenght, hp, authority, strength):
  # check for dying
  if hole_lenght <= 0 or hp <= 0 or authority <= 0 or strength <= 0:
    return "die"
  return "win"


results = {
    "die": lambda: print("You died!"),
    "win": lambda: print("You win!"),
}

print(results[gameDay])
