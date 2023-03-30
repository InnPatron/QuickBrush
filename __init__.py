bl_info = {
    "name": "Quick Brush",
    "description": "Set up keybindings for brushes",
    "blender": (3, 4, 0),
    "category": "3D View",
}

import bpy
from .settings_ui import *
from .data import *
from .constants import *
from .ops import *
from .grease_pencil_ops import *

registered = []
image_paint_keymap_items = []
grease_pencil_keymap_items = []

def register_slot_ops(n, maker):
    for i in range(0, n):
        op_type = maker(i)
        bpy.utils.register_class(op_type)
        registered.append(op_type)

# source: https://blenderartists.org/t/how-to-create-a-shortcut-for-a-custom-script/545177
def register_keymaps(paint_brush_slots):
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Register texture paint bindings
        register_keymaps_specific(kc, paint_brush_slots, "Image Paint", make_texture_paint_brush_op_idname, image_paint_keymap_items)
        register_keymaps_specific(kc, paint_brush_slots, "Grease Pencil", make_grease_pencil_brush_op_idname, grease_pencil_keymap_items)

def register_keymaps_specific(kc, paint_brush_slots, km_name, maker, cache):
    if km_name not in kc.keymaps:
        kc.keymaps.new(name=km_name, space_type="EMPTY")
    km = kc.keymaps[km_name]
    for i in range(0, paint_brush_slots):
        kmi = km.keymap_items.new(maker(i), 'NONE', 'PRESS')
        cache.append(kmi)

def unregister_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        # Unregister texture paint bindings
        unregister_keymaps_specific(kc.keymaps["Image Paint"], image_paint_keymap_items)
        unregister_keymaps_specific(kc.keymaps["Grease Pencil"], grease_pencil_keymap_items)

def unregister_keymaps_specific(km, source):
    for kmi in km.keymap_items:
        if kmi in source:
            km.keymap_items.remove(kmi)

def unregister_ops():
    bpy.utils.unregister_class(CopyTexturePaintBrushSlotsOp)
    bpy.utils.unregister_class(CopyGreasePencilBrushSlotsOp)
    for r in registered:
        bpy.utils.unregister_class(r)

def register():
    register_slot_ops(SLOT_COUNT, make_texture_brush_op)
    register_slot_ops(SLOT_COUNT, make_grease_pencil_brush_op)
    register_keymaps(SLOT_COUNT)

    bpy.utils.register_class(CopyTexturePaintBrushSlotsOp)
    bpy.utils.register_class(CopyGreasePencilBrushSlotsOp)

    bpy.utils.register_class(QuickBrushTexturePaintSlot)
    bpy.utils.register_class(QuickBrushGreasePencilSlot)

    bpy.utils.register_class(QuickBrushProperties)
    bpy.utils.register_class(QuickBrushPanel)

    # Registered after parent panel
    bpy.utils.register_class(QuickBrushTexturePaintPanel)
    bpy.utils.register_class(QuickBrushGreasePencilPanel)

    bpy.types.WorkSpace.quick_brush_data = bpy.props.PointerProperty(type=QuickBrushProperties)

def unregister():
    unregister_keymaps()
    unregister_ops()

    bpy.utils.unregister_class(QuickBrushPanel)
    bpy.utils.unregister_class(QuickBrushProperties)
    bpy.utils.unregister_class(QuickBrushTexturePaintSlot)
    bpy.utils.unregister_class(QuickBrushTexturePaintPanel)
    del bpy.types.WorkSpace.quick_brush_data

if __name__ == "__main__":
    register()

