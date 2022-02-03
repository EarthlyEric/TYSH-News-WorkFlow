import json

input_post_id=6666666666666666

jsonfile = open('./save_post_id.json', 'w')
date=dict(save_post_id=input_post_id)
json.dump(date, jsonfile, indent=4)