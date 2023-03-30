import bpy

def filter_grease_pencil_brush(self, b):
    return b.use_paint_grease_pencil

def filter_image_texture_brush(self, b):
    return b.use_paint_image

# Needs to be before QuickBrushProperties
class QuickBrushTexturePaintSlot(bpy.types.PropertyGroup):
    brush: bpy.props.PointerProperty(
        type=bpy.types.Brush,
        poll=filter_image_texture_brush,
    )

class QuickBrushGreasePencilSlot(bpy.types.PropertyGroup):
    brush: bpy.props.PointerProperty(
        type=bpy.types.Brush,
        poll=filter_grease_pencil_brush,
    )

class QuickBrushProperties(bpy.types.PropertyGroup):
    copy_to_target: bpy.props.PointerProperty(type=bpy.types.WorkSpace)
    texture_paint_brush_slots: bpy.props.CollectionProperty(type=QuickBrushTexturePaintSlot)
    grease_pencil_brush_slots: bpy.props.CollectionProperty(type=QuickBrushGreasePencilSlot)
