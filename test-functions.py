'''PCO test board'''
# a = 'JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS'

'''Rainbow board with three rows empty'''
# s = "///TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/"

''' Test function for spawning pieces'''
# t, screen = init_screen()
# for x in range(10):
#     b = Board(boardstate=s)
#     print(b.bag.value)
#     print(b.piece.value)
#     b.display_board(t, screen)
#     sleep(1.5)
# screen.mainloop()

'''Test function for kicks [DEPRECATED]'''
# t, screen = init_screen()
# smart_display("T040:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS", t, screen)
# slides = ["T040:9J/",
#           "T35-1:9J/",
#           "T240:9J/",
#           "T140:9J/",
#           rotate_and_update("T040:9J/", "CCW", True),
#           rotate_and_update("T040:9J/", "180", True),
#           rotate_and_update("T040:9J/", "CW", True),
#           "T340:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS",
#           "JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS",
#           #rotate_and_update("T340:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS", "CCW", True),
#           "T040:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS",
#           #rotate_and_update("T040:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS", "CW"),
#           ]
# slideshow(slides, t, screen)
# screen.mainloop()

'''Test functions for various things [DEPRECATED]'''
# dict1 = board_notation_to_dict('JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS')
# print(create_grid(locked_positions=dict1))

# a = boardstate_to_extended_boardstate('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9')
# a = boardstate_to_extended_boardstate('')
# print(a)
# print(extended_boardstate_to_boardstate(a))

# print(access_cell('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9', 2, 1))
# print(change_cell('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9', 1, 5, "S"))

# a = update_boardstate_from_piece_board_notation("S054:JJI4ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS")
# a = update_boardstate('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9', 'I253')
# display_as_text('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9')
# display_as_text('JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS')
# display_as_text(a)

# print(generate_bag("JIZISLZJOTOJZ"))
# a = "I140:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS"
# display_as_text(update_boardstate_from_piece_board_notation(a))
# for x in range(4):
#       a = rotate_piece(a, "CW")
#       b = update_boardstate_from_piece_board_notation(a)
#       display_as_text(b)

# print(generate_bag("JIZISLZJOTOJZ"))

# a = "S345:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS"
# display_as_text(update_boardstate_from_piece_board_notation(a))
# a = rotate_piece(a, "CCW", True)
# b = update_boardstate_from_piece_board_notation(a)
# display_as_text(b)

# a = "S132:JJJ2JJJJJ/JJJJ2JJJJ"
# print(boardstate_to_extended_boardstate(a.split(":")[1]))
# display_as_text(update_boardstate_from_piece_board_notation(a))
# a = rotate_piece(a, "CW", True)
# display_as_text(update_boardstate_from_piece_board_notation(a))
# b = rotate_piece(a, "CW", False, True)
# print(b)
# c = check_kick_tables_repeatedly(b, 1, 2, True)
# print(c)
# print(display_as_text(update_boardstate_from_piece_board_notation(c)))
# print(check_kick_tables("T", 0, 1, 1))
