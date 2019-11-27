# Demonstrates garbage data in Panel that occurs if you use an EnumProperty
# with a dynamic items list. This behavior is documented in the EnumProperty
# documentation.

bl_info = {
    "name" : "Enum Property Test",
    "author" : "Doug Richardson",
    "description" : "",
    "blender" : (2, 81, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
import os

def listdir_fullpath(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory)]

DoNotGarbageCollect=[]

class DougsProps(bpy.types.PropertyGroup):
    my_static_enum: bpy.props.EnumProperty(
        name="Static Enum",
        description="Static Enum description",
        items=(
            ('ENUM_ID_1', 'Enum Name 1', 'Enum Description 1'),
            ('ENUM_ID_2', 'Enum Name 2', 'Enum Description 2'),
            ('ENUM_ID_3', 'Enum Name 3', 'Enum Description 3'),
        ),
        default=None
    )

    def GetDynamicEnumItems(self, context):
        items = []
        for i in range(3):
            identifier = 'à_%d' % i
            name = 'à Enum Name %d' % i
            description = 'à Enum Description %d' % i
            items.append((identifier, name, description))
        # Works fine if you uncomment the next two lines.
        #global DoNotGarbageCollect
        #DoNotGarbageCollect = items
        return itemm

    my_dynamic_enum: bpy.props.EnumProperty(
        name="Dougs Dynamic Enum",
        description="Dynamic Enum description",
        items=GetDynamicEnumItems,
        default=None
    )

class DougPanel(bpy.types.Panel):
    bl_label = "Doug Panel"
    bl_idname = "DR_PT_DougPanel"
    bl_space_type = 'VIEW_3D'    
    bl_context= 'objectmode'
    bl_region_type = 'UI'
    bl_category = 'Doug Panel'

    def draw(self, context):
        P = context.scene.MyProps
        self.layout.prop(P, "my_static_enum")
        self.layout.prop(P, "my_dynamic_enum")


classes = (
    DougsProps,
    DougPanel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.MyProps = bpy.props.PointerProperty(type=DougsProps)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.MyProps

