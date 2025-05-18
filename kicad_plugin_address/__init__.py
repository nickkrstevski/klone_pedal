#!/usr/bin/env python3
'''
This plugin is used to add the atopile_address field values as text on the comments layer.

To use the plugin, add the following code to a file in kicad/9.0/scripting/plugins called "atopile_address.py"

########################################################
plugin_path = r"<PATH_TO_THIS_DIRECTORY>"
import sys
import importlib

if plugin_path not in sys.path:
    sys.path.append(plugin_path)

# if kicad_plugin is already in sys.modules, reload it
for module in sys.modules:
    if "kicad_plugin_address" in module:
        importlib.reload(sys.modules[module])

import kicad_plugin_addressx
########################################################
'''

import pcbnew
import wx
import os
import sys

class AtopileAddressPlugin(pcbnew.ActionPlugin):
    """
    A KiCad plugin that reads the "atopile_address" field from footprints,
    clears all text on the user comments layer, and adds new text based on the field values.
    """
    
    def defaults(self):
        """
        Initialize plugin information
        """
        self.name = "Atopile Address Plugin"
        self.category = "Modify PCB"
        self.description = "Add footprint 'atopile_address' field values as text on the comments layer"
        self.show_toolbar_button = True

        # Icon file (optional)
        icon_path = os.path.join(os.path.dirname(__file__), 'glass_icon.png')
        if os.path.exists(icon_path):
            self.icon_file_name = icon_path
    
    def Run(self):
        """
        Main plugin execution function
        """
        # Get the current board
        board = pcbnew.GetBoard()
        
        # Access the User.Comments layer in KiCad 9
        # The comments layer is typically accessed through pcbnew.Dwgs_User
        comments_layer = pcbnew.Cmts_User
        
        # First, remove all existing text on the comments layer
        self._remove_text_on_comments_layer(board, comments_layer)
        
        # Process all footprints, adding text for those with atopile_address field
        self._add_atopile_address_text(board, comments_layer)
        
        # Refresh the board view
        pcbnew.Refresh()
        
        # Show confirmation dialog
        wx.MessageBox("Atopile addresses have been added to the Comments layer.", 
                     "Atopile Address Plugin", wx.OK | wx.ICON_INFORMATION)
    
    def _remove_text_on_comments_layer(self, board, comments_layer):
        """
        Remove all text from the comments layer
        """
        # Get all board items
        items_to_remove = []
        
        for drawing in board.GetDrawings():
            # Check if the drawing is text and on the comments layer
            if drawing.GetLayer() == comments_layer:
                if type(drawing) == pcbnew.PCB_TEXT or type(drawing) == pcbnew.PCB_TEXTBOX:
                    items_to_remove.append(drawing)
        
        # Remove all identified text items
        for item in items_to_remove:
            board.Remove(item)
    
    def _add_atopile_address_text(self, board, comments_layer):
        """
        Add text for footprints with atopile_address field
        """
        # Process all footprints
        for footprint in board.GetFootprints():
            # Check if the footprint has an atopile_address field
            field_text = self._get_footprint_field(footprint, "atopile_address")
            

            # Get the position of the footprint
            position = footprint.GetPosition()
            
            # Create a new text object
            text = pcbnew.PCB_TEXT(board)
            text.SetText("TEST")
            text.SetText(field_text)
            text.SetLayer(comments_layer)
            text.SetPosition(pcbnew.VECTOR2I(position.x, position.y - 2500000))
            text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
            text.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
            
            # Set text height to 1mm (convert to KiCad internal units)
            # KiCad internal units are nanometers (1mm = 1000000nm)
            text_size = int(1 * 1000000)  # 1mm in internal units
            text.SetTextHeight(text_size)
            text.SetTextWidth(text_size)
            
            # Add the text to the board
            footprint.Add(text)
    
    def _get_footprint_field(self, footprint, field_name):
        """
        Get the value of a specific field from a footprint
        """
        # Try to find the field by name
        field = footprint.GetFieldByName(field_name)
        if field:
            return field.GetText()
        
        return None

# Register the plugin
AtopileAddressPlugin().register()