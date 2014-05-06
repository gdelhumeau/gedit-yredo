from gi.repository import GObject, Gedit, Gtk

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_6">
        <separator />
        <menuitem name="EditYRedo" action="EditYRedo"/>
        <separator />
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class YRedoPlugin(GObject.Object, Gedit.WindowActivatable):
  __gtype_name__ = "YRedoPlugin"

  window = GObject.property(type=Gedit.Window)
  
  def __init__(self):
    GObject.Object.__init__(self)

  def do_activate(self):
    self._insert_menu()
    pass

  def do_deactivate(self):
    self._remove_menu()
    self._action_group = None
    pass

  def do_update_state(self):
    pass
    
  def _insert_menu(self):
    # Get the Gtk.UIManager
    manager = self.window.get_ui_manager()
     
    # Create a new action group
    self._action_group = Gtk.ActionGroup("YRedoPluginActions")
    self._action_group.add_actions([("EditYRedo", Gtk.STOCK_REDO, _("Redo"),
                                     "<Control>Y", _("Redo last action"),
                                     self.on_redo_activate)])

    # Insert the action group
    manager.insert_action_group(self._action_group, -1)

    # Merge the UI
    self._ui_id = manager.add_ui_from_string(ui_str)

  def _remove_menu(self):
    # Get the Gtk.UIManager
    manager = self.window.get_ui_manager()

    # Remove the ui
    manager.remove_ui(self._ui_id)

    # Remove the action group
    manager.remove_action_group(self._action_group)

    # Make sure the manager updates
    manager.ensure_update()
    
  # Menu activate handlers
  def on_redo_activate(self, action):
    doc = self.window.get_active_document()
    if not doc:
        return

    doc.redo()
  
