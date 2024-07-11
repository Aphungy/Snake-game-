import os

FOOD_DATA_FILE = "food_data.txt"
HIGH_SCORES_FILE = "high_scores.txt"

def save_food_data(food_dict):
    with open(FOOD_DATA_FILE, "w") as file:
        for food_name, food_value in food_dict.items():
            file.write(f"{food_name}:{food_value}\n")

def load_food_data():
    food_dict = {}
    if os.path.exists(FOOD_DATA_FILE):
        with open(FOOD_DATA_FILE, "r") as file:
            for line in file:
                food_name, food_value = line.strip().split(":")
                food_dict[food_name] = int(food_value)
    return food_dict

def load_high_scores():
  high_scores = []
  if os.path.exists(HIGH_SCORES_FILE):
      with open(HIGH_SCORES_FILE, "r") as file:
          for line in file:
              high_scores.append(int(line.strip()))
  else:
      open(HIGH_SCORES_FILE, "w").close() 
  return high_scores

def save_high_scores(high_scores):
  with open(HIGH_SCORES_FILE, "w") as file:
      for score in high_scores:
          file.write(str(score) + "\n")

