import bpy

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


# アドオン有効化時コールバック
def register():
    print("レベルエディタが有効化されました。")

# アドオン無効化時コールバック
def unregister():
    print("レベルエディタが無効化されました。")
    
if __name__ == "__main__":
    register()
