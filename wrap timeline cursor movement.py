import bpy

class MoveTimelineCursor(bpy.types.Operator):
    """Wrap timeline cursor movement"""
    bl_idname = "timeline.move_cursor"
    bl_label = "Move Timeline Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.IntProperty(default=1)

    def execute(self, context):
        scene = context.scene
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        new_frame = scene.frame_current + self.direction

        if new_frame > frame_end:
            new_frame = frame_start
        elif new_frame < frame_start:
            new_frame = frame_end
        
        scene.frame_current = new_frame
        return {'FINISHED'}

# Keymap hinzufügen
addon_keymaps = []

def register():
    bpy.utils.register_class(MoveTimelineCursor)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Screen", space_type='EMPTY')
        kmi = km.keymap_items.new("timeline.move_cursor", 'LEFT_ARROW', 'PRESS', alt=True)
        kmi.properties.direction = -1
        kmi = km.keymap_items.new("timeline.move_cursor", 'RIGHT_ARROW', 'PRESS', alt=True)
        kmi.properties.direction = 1
        addon_keymaps.append(km)

def unregister():
    for km in addon_keymaps:
        bpy.context.window_manager.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(MoveTimelineCursor)

if __name__ == "__main__":
    register()
