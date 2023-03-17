import bpy

bl_info = {
    "name": "Quick Brush",
    "description": "Set up keybindings for brushes",
    "blender": (3, 4, 0),
    "category": "3D View",
}

def make_paint_brush_op_idname(i):
    return "quick_brush.paint_brush_slot{x}".format(x=i)

def paint_brush_slot_factory(n):
    r = []
    for i in range(0, n):
        class QuickBrushPaintBrushSlotOp(object):
            bl_idname = make_paint_brush_op_idname(i)
            bl_label = "Quick Brush Paint Brush Slot #{x}".format(x=i)

        r.append(QuickBrushPaintBrushSlotOp)

    return r

# source: https://blenderartists.org/t/how-to-create-a-shortcut-for-a-custom-script/545177
def register_keymaps(paint_brush_slots):
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Register texture paint bindings
        if "Image Paint" not in kc.keymaps:
            kc.keymaps.new(name="Image Paint", space_type="VIEW_3D")
        km = kc.keymaps["Image Paint"]
        for i in range(0, paint_brush_slots):
            kmi = km.keymap_items.new(make_paint_brush_op_idname(i), '', '')

def unregister_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Unregister texture paint bindings
        km = kc.keymaps["Image Paint"]
        for kmi in km.keymap_items:
            if "quick_brush" in kmi.idname:
                km.keymap_items.remove(kmi)
                break

paint_binding_count = 5

def register():
    # bpy.types.BlendData.quick_brush_data = bpy.props.PointerProperty(type=foo)
    register_keymaps()

def unregister():
    unregister_keymaps()

if __name__ == "__main__":
    register()

