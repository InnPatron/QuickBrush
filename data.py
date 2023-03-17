import bpy

def filter_image_texture_brush(self, b):
    return b.use_paint_image

# Needs to be before QuickBrushProperties
class QuickBrushTexturePaintSlot(bpy.types.PropertyGroup):
    brush: bpy.props.PointerProperty(
        type=bpy.types.Brush,
        poll=filter_image_texture_brush,
    )

class QuickBrushProperties(bpy.types.PropertyGroup):
    texture_paint_brush_slots: bpy.props.CollectionProperty(type=QuickBrushTexturePaintSlot)
