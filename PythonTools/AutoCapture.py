import unreal

'''
__Tool Description__
This tool will automatically snap the current viewport 
to each camera in the level and captures a screenshot
'''

print(""" 
  ___        _        _____             _                  
 / _ \      | |      /  __ \           | |                 
/ /_\ \_   _| |_ ___ | /  \/ __ _ _ __ | |_ _   _ _ __ ___ 
|  _  | | | | __/ _ \| |    / _` | '_ \| __| | | | '__/ _ \ 
| | | | |_| | || (_) | \__/\ (_| | |_) | |_| |_| | | |  __/
\_| |_/\__,_|\__\___/ \____/\__,_| .__/ \__|\__,_|_|  \___|
                                 | |                       
                                 |_|  by ShadyTantawy (Raze)
        """)

# Get all actors in the level
actors = unreal.EditorLevelLibrary.get_all_level_actors()

# Actor type
camera_type = "CineCameraActor"

# Screenshot Resolution
screen_x = 1920
screen_y = 1080

# Screenshot Format (default format: png)
output_format = "png"

i = 0
def run_Capture_Screenshot_Virtual_Cameras(deltatime):
    global i
    for actor in actors[i:]:
        i += 1
        # Actor->name
        actor_name = actor.get_name()
        # Actor->type
        actor_type = str(actor).split("'")[-2]
        
        if actor_type == camera_type:
            unreal.log_warning("Camera Detected --> " + actor_name)
            #print("Camera Detected --> " + actor_name)
            # Get actor rotation
            rotation = actor.get_actor_eyes_view_point()[1]
            # Get actor position
            position = actor.get_actor_location()
            # Snap viewport to camera
            unreal.EditorLevelLibrary.set_level_viewport_camera_info(position, rotation)
            # Take screenshot
            unreal.AutomationLibrary.take_high_res_screenshot(screen_x, screen_y, actor_name + "." + output_format)

            '''
            Stop run_Capture_Screenshot_Virtual_Cameras() 
            to allow unreal to process the current iteration
            [STOP run_Capture_Screenshot_Virtual_Cameras() --> START Unreal]
            '''
            try:
                unreal.unregister_slate_pre_tick_callback(run_Capture_Screenshot_Virtual_Cameras)
            except:
                break

'''
Register run_Capture_Screenshot_Virtual_Cameras() as a callback
to allow it to run later and process the next actor
[STOP Unreal --> START run_Capture_Screenshot_Virtual_Cameras()]
'''
if i != len(actors):
    unreal.register_slate_pre_tick_callback(run_Capture_Screenshot_Virtual_Cameras)
