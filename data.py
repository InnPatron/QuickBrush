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
    texture_paint_slot_count: bpy.props.IntProperty(default=10)
    texture_paint_brush_slots: bpy.props.CollectionProperty(type=QuickBrushTexturePaintSlot)

def try_init_collection(c, n):
    size = len(c)
    diff = n - size
    if size <= n:
        for i in range(0, diff):
            b = c.add()
    else:
        for i in range(0, diff):
            c.pop()

class QuickBrushPanel(bpy.types.Panel):
    bl_label = "Quick Brush Workspace Settings"
    bl_idname = "VIEW_3D_PT_QUICK_BRUSH_SETTINGS_LAYOUT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

class QuickBrushTexturePaintPanel(bpy.types.Panel):
    bl_label = "Quick Brush Workspace Settings"
    bl_idname = "VIEW_3D_PT_QUICK_BRUSH_TEXTURE_PAINT_LAYOUT"
    bl_parent_id = "VIEW_3D_PT_QUICK_BRUSH_SETTINGS_LAYOUT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        my_data = context.workspace.quick_brush_data

        try_init_collection(my_data.texture_paint_brush_slots, my_data.texture_paint_slot_count)

        for i in range(0, my_data.texture_paint_slot_count):
            r = layout.row()
            c1 = r.column()
            c2 = r.column()
            c2.alignment="CENTER"
            c2.scale_x = 2
            c1.label(text="Slot {x}".format(x=i+1))
            c2.template_ID(my_data.texture_paint_brush_slots[i], "brush")
