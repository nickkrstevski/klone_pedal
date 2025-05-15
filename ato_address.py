import kipy
import kipy.board_types
import kipy.common_types

kicad = kipy.KiCad()
print(f"Connected to KiCad {kicad.get_version()}")

board = kicad.get_board()
fps = board.get_footprints()
fp0: kipy.board_types.FootprintInstance = fps[0]
print(fp0.texts_and_fields)

