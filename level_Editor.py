import bpy
import math
import bpy_extras

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Yokoyama Tadanobu",
    "version": (1, 0, 0),
    "blender": (5, 5, 0),
    "location": "3D Viewport > Sidebar > Level Editor",
    "description": "レベルデザイン用のエディタ機能を提供します。",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Object",
}

## XXX_MT_XXX MT = メニュー
## XXX_OT_XXX OT = オプション
## XXX_PT_XXX PT = パネル

# トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #Blenderがクラスを識別するための固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by" + bl_info["author"]

    #サブメニュ０の描画
    def draw(self, context):
        #トップバーの「エディターメニュー」に項目[オペレーター]を追加
        self.layout.operator("wm.url_open_preset" , text = "manual", icon='HELP')
        self.layout.separator()
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text = MYADDON_OT_stretch_vertex.bl_label)
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, text = MYADDON_OT_create_ico_sphere.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, text = MYADDON_OT_export_scene.bl_label)
    
    #既存のメニューにサブメニューを追加
    def submenu(self, context):
        #ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

#オペレーター　頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点を引っ張って伸ばします"
    #Redo,Undo可能オプション
    bl_options = {'REGISTER', 'UNDO'}

    #メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました")
        #オペレーターの命令終了を通知
        return {'FINISHED'}

#オペレーター　ICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.create_ico_sphere"
    bl_label = "ICO球生成"
    bl_description = "ICOを球生成します"
    #Redo,Undo可能オプション
    bl_options = {'REGISTER', 'UNDO'}

    #メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        #オペレーターの命令終了を通知
        return {'FINISHED'}

#オペレーター　シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をexportします"
    #出力するファイルの拡張子
    filename_ext = ".scene"

    #メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        print("シーン情報をExportします")
        self.export()
        self.report({'INFO'}, "シーン情報をExportしました")
        print("シーン情報をexportしました")
        #オペレーターの命令終了を通知
        return {'FINISHED'}
    
    def export(self):
        """ファイルに出力"""
        print("シーン情報出力開始...%r" % self.filepath)

        #ファイルをテキスト形式で書き出し用にオープン
        #スコープを抜けると自動的にクローズされる
        with open(self.filepath, "wt") as file:
            for object in bpy.context.scene.objects:
                #親オブジェクトがあるものはスキップ
                if (object.parent):
                    continue
                #シーン直下のオブジェクトをルートノード(深さ０)とし、再帰関数で捜査
                self.parse_scene_recursive(file, object, 0)

    def parse_scene_recursive(self, file, object, level):
        """シーン解析用再帰関数"""
        #深さ文インデントする
        indent = ''
        for i in range(level):
            indent += "\t"
        #オブジェクト名書き込み
        file.write(indent + object.type + " - " + object.name + "\n")
        trans, rot, scale = object.matrix_local.decompose()
        #回転をQuternionからEulerに変換
        rot = rot.to_euler()
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        file.write(indent + "Trans(%f,%f,%f)\n" % (trans.x, trans.y, trans.z ))
        file.write(indent + "Rotat(%f,%f,%f)\n" % (rot.x, rot.y, rot.z ))
        file.write(indent + "Scale(%f,%f,%f)\n" % (scale.x, scale.y, scale.z ))
        file.write("\n")

        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1);

#オペレーター　カスタムプロパティ['file_name']追加
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.add_filename"
    bl_label = "FileName 追加"
    bl_description = "['file_name']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #['file_name']カスタムプロパティを追加
        context.object["file_name"] = ""

        return {"FINISHED"}

#パネル　ファイル名
class OBJECT_PT_file_name(bpy.types.Panel):
    ###オブジェクトのファイルネームパネル###
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    #サブメニューの描画
    def draw(self, context):
        #パネルに項目を追加
        if ("file_name") in context.object:
            #既にプロパティがあれば、プロパティを表示
            self.layout.prop(context.object, '["file_name"]', text = self.bl_label)
        else:
            #プロパティがなければプロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)



classes = (
    TOPBAR_MT_my_menu,
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    )


# メニュー項目描画
def draw_menu_manual(self, context):
    #self : 呼び出し元のclassインスタンス。C++でいうthisポインタ
    #context : カーソルを合わせた時のポップアップのカスタマイズなどに使用

    #トップバーの「エディターメニュー」に項目を追加
    self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')

# アドオン有効化時コールバック
def register():
    #Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)
    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました。")

# アドオン無効化時コールバック
def unregister():
    #メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    #Blenderクラスからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化されました。")
    

if __name__ == "__main__":
    register()
