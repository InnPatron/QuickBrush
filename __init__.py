import bpy

bl_info = {
    "name": "Quick Brush",
    "description": "Set up keybindings for brushes",
    "blender": (3, 4, 0),
    "category": "3D View",
}

paint_brush_slot_count = 10
registered = []
keymap_items = []

def make_paint_brush_op_idname(i):
    return "quick_brush.paint_brush_slot{x}".format(x=i)

def register_paint_brush_slot_ops(n):
    for i in range(0, n):

        def execute(self, context):
            print("Slot op {x} in mode {mode}".format(x=self.slot, mode=bpy.context.mode))
            return {'FINISHED'}

        op_type = type("QuickBrushPaintBrushSlot{x}Op".format(x=i), (bpy.types.Operator, ), {
            "bl_idname": make_paint_brush_op_idname(i),
            "bl_label": "Quick Brush: Paint Brush Slot {x}".format(x=i),
            "slot": i,
            "execute": execute,
        })

        bpy.utils.register_class(op_type)
        registered.append(op_type)

# source: https://blenderartists.org/t/how-to-create-a-shortcut-for-a-custom-script/545177
def register_keymaps(paint_brush_slots):
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Register texture paint bindings
        if "Image Paint" not in kc.keymaps:
            kc.keymaps.new(name="Image Paint", space_type="EMPTY")
        km = kc.keymaps["Image Paint"]
        for i in range(0, paint_brush_slots):
            kmi = km.keymap_items.new(make_paint_brush_op_idname(i), 'NONE', 'PRESS')
            keymap_items.append(kmi)

def unregister_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Unregister texture paint bindings
        km = kc.keymaps["Image Paint"]
        for kmi in km.keymap_items:
            if kmi in keymap_items:
                km.keymap_items.remove(kmi)

def unregister_ops():
    for r in registered:
        bpy.utils.unregister_class(r)

def register():
    register_paint_brush_slot_ops(paint_brush_slot_count)
    # bpy.types.BlendData.quick_brush_data = bpy.props.PointerProperty(type=foo)
    register_keymaps(paint_brush_slot_count)

def unregister():
    unregister_keymaps()
    unregister_ops()

if __name__ == "__main__":
    register()

