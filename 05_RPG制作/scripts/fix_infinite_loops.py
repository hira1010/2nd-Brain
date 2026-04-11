import json
import os
import glob

def fix_map_risks(project_path):
    data_path = os.path.join(project_path, "data")
    map_files = glob.glob(os.path.join(data_path, "Map[0-9][0-9][0-9].json"))
    
    fixed_count = 0
    
    for map_file in map_files:
        with open(map_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                continue
                
        modified = False
        if "events" not in data:
            continue
            
        for event in data["events"]:
            if not event: continue
            
            for page in event.get("pages", []):
                # Trigger 3: Autorun, 4: Parallel
                if page.get("trigger") in [3, 4]:
                    cmd_list = page.get("list", [])
                    if not cmd_list: continue
                    
                    has_wait = any(c['code'] in [230, 201, 123, 121, 214] for c in cmd_list)
                    
                    if not has_wait:
                        # Insert Wait 1 frame (Code 230, Parameter [1])
                        # Insert before the last Code 0 command
                        wait_cmd = {"code": 230, "indent": 0, "parameters": [1]}
                        if cmd_list[-1]['code'] == 0:
                            cmd_list.insert(-1, wait_cmd)
                        else:
                            cmd_list.append(wait_cmd)
                        
                        print(f"Fixed loop risk in {os.path.basename(map_file)} Event {event['id']} ({event['name']})")
                        modified = True
                        fixed_count += 1
                        
        if modified:
            with open(map_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
                
    return fixed_count

if __name__ == "__main__":
    path = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\05_RPG制作"
    count = fix_map_risks(path)
    print(f"Total fixes applied: {count}")
