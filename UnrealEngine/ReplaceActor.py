import unreal

'''
__Tool Description__
This tool will replace all actors selected from the level
with an asset selected from the content browser
'''

print(""" \n

██████  ███████ ██████  ██       █████   ██████ ███████  █████   ██████ ████████  ██████  ██████  
██   ██ ██      ██   ██ ██      ██   ██ ██      ██      ██   ██ ██         ██    ██    ██ ██   ██ 
██████  █████   ██████  ██      ███████ ██      █████   ███████ ██         ██    ██    ██ ██████  
██   ██ ██      ██      ██      ██   ██ ██      ██      ██   ██ ██         ██    ██    ██ ██   ██ 
██   ██ ███████ ██      ███████ ██   ██  ██████ ███████ ██   ██  ██████    ██     ██████  ██   ██ 
by Shady Tantawy (Raze)
___________________________________
""")

editor_selected_actors          = unreal.EditorLevelLibrary.get_selected_level_actors()
content_browser_selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
if not editor_selected_actors or not content_browser_selected_assets:
    unreal.log_warning("Select actors from the level to be replaced with the asset selected from the content browser!")
else:
    asset_name   = content_browser_selected_assets[0].get_full_name()
    loading_text = "Replacing actors..."
    actors_count = len(editor_selected_actors)

    with unreal.ScopedSlowTask(actors_count, loading_text) as ST:
        ST.make_dialog(True)
        for actor in editor_selected_actors:
            if ST.should_cancel():
                break

            # Get actor rotation
            rotation = actor.get_actor_eyes_view_point()[1]
            # Get actor position
            location = actor.get_actor_location()
            # Get actor name
            actor_name = actor.get_name()
            # Spawn asset at [location, rotation]
            unreal.EditorLevelLibrary.spawn_actor_from_object(content_browser_selected_assets[0], location, rotation)
            # Delete actor
            actor.destroy_actor()

            print("{0} has been replaced by {1}".format(actor_name,asset_name))
            
            # Update bar progress
            ST.enter_progress_frame(1)

