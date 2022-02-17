from Tetris import *
start = time()
t, screen = init_screen()
end = time()
#print(end - start)
# 10.9 second delay

'test function for keybinds'
g = Game(players=1)
g.mainloop()

'test function for 40 row game over check'
# b1 = Board(t, screen, "",
#            "*I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/I9/")
# b1.display_board()
# sleep(0.5)
# while b1.game_over == False:
#     b1.receive_garbage(5, 1)
#     b1.display_board()
#     sleep(0.01)
# b1.display_board()
# sleep(0.5)

'test function for game over check'
# b1 = Board(t, screen)
# while b1.game_over == False:
#     b1.display_board()
#     b1.hard_drop()
# print("game over")

'test function for dt cannon'
b1 = Board(t, screen, "", "*", "dt")
print(b1.bag.value)
'ILTSJZO/JTISLOZ/IOLZSJT'
actions = """CW\nr\nr\nhd\nhd\nhold\nhd\nR\nhd\nR\nhd\nL\nhd\nCW\nL\nhd\nhd\nCW\nR\nhd\nCW\nr\nhd\nCCW\nl\nhd\nR\nl\nhd\nCW\nr\nr\nhd"""
b1.do_actions_from_input(actions)
screen.mainloop()

'test function for t-spin detection'
# names = ["tsd", "tss", "tsm", "stsd", "tst", "fin-tsd", "neo-tsd", "iso-tsd"]
# boards = ['*I1IIIIIIII/3IIIIIII/2IIIIIIII',
#           '*I1IIIIIIII/3IIIIIII/2IIIIIIII', '*1IIIIIIIII', '*2IIIIIIII/2IIIIIIII/1IIIIIIIII//I9', '*1IIIIIIIII/2IIIIIIII/1IIIIIIIII//I9', '*IIIIIIII1I/IIIIIII2I/9I/9I/7III', '*IIIIIII1II/IIIIII2II/8II/9I/7III', '*IIIIIII1II/IIIIIII2I/8II/9I/6IIII']
# actions = ['CW 0.5\nL 0.5\nd 0.5\nCW 0.5\nlock', 'CCW 0.5\nL 0.5\nd 0.5\n180 0.5\nlock', 'd 0.5\nL 0.5\nCW 0.5\nlock', 'd 0.5\nL 0.5\nCW 0.5\nlock', 'd 0.5\nL 0.5\nCW 0.5\nlock', 'd 0.5\n180 0.5\nR 0.5\nCW 0.5\nlock', 'd 0.5\n180 0.5\nR 0.5\nCW 0.5\nlock', 'd 0.5\n180 0.5\nR 0.5\nCCW 0.5\nlock']
# for i in range(len(boards)):
#     b = Board(t, screen, "T0322", boards[i])
#     b.do_actions_from_input(actions[i])
#     print(f"{names[i]}: {b.line_clear_history}")
#     sleep(1)


'''silly test function for random gameplay (game might be ok)'''
# try:
#     directions = ["CW", "CCW", "180"]
#     for _ in range(20):
#         b = Board(t, screen, "", "*")
#         b.display_board()
#         sleep(0.5)
#         for _ in range(20):
#             b.rotate_piece(random.choice(directions))
#             b.display_board()
#             b.change_x(random.randint(-5, 5))
#             b.display_board()
#             a = ""
#             while a is not False:
#                 a = b.move_piece_down()
#                 b.display_board()
#             b.lock_piece()
#             b.display_board()
# except KeyboardInterrupt:
#     print(b.piece_board_notation)


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
#     b.display_board()
#     sleep(1.5)
# screen.mainloop()

'''Working test function for some T, Z, S kicks'''
# t, screen = init_screen()
# tests = ["T140", "Z140", "S150"]
# for test in tests:
#     b = Board(test, "JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS")
#     b.display_board()
#     sleep(0.5)
#     b.rotate_piece("CCW")
#     b.display_board()
#     sleep(0.5)
#     b.rotate_piece("CW")
#     b.display_board()
#     sleep(0.5)

'''Test function for CCW rotation, z piece'''
# p1 = "S0311"
# b1 = "JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS"
# for _ in range(20):
#     pb = construct_piece_board_notation(p1, b1)
#     p1, b1 = rotate_and_update2(pb, "CCW")
#     d = update_boardstate2(b1, Piece(p1))
#     display_as_text(d)
#     print(p1)
#     sleep(1)


'''Fixed: Pieces hover over the first column when dropped'''
# b = Board(t, screen, "I001")
# a = True
# b.display_board()
# sleep(1)
# while a is not None:
#     a = b.move_piece_down()
#     b.display_board()
# sleep(2)

# With turtle GUI
# t, screen = init_screen()
# b = Board("S0311", "JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS")
# for _ in range(20):
#     b.display_board()
#     print(b.piece.value)
#     sleep(1)
#     b.rotate_piece("CCW")
#     b.display_board()
#     print(b.piece.value)
#     sleep(1)
#     b.rotate_piece("CCW")

'''Test function that shows bug is fixed (blocks pushing down other blocks)'''
# try:
#     for _ in range(20):
#         b = Board(t, screen)
#         b.display_board()
#         sleep(0.5)
#         for _ in range(20):
#             for _ in range(15):
#                 b.move_piece_down()
#                 b.display_board()
#                 sleep(0.05)
#             b.lock_piece()
#             b.display_board()
# except KeyboardInterrupt:
#     print(construct_piece_board_notation(b.piece.value, b.boardstate))

'''Test function showing impossible left/right movement is caught'''
# Now caught by the move_piece_left/right function
# for _ in range(10):
#     b = Board(t, screen, "I0622")
#     b.move_piece_right()
#     # (the above does not work, it returns None)
#     b.display_board()
#     sleep(1)
#     b.rotate_piece("CCW")
#     b.display_board()
#     sleep(1)

'''Test functions for slideshows'''
# Slideshow is working (although it spawns a random piece)
# slides = ["JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS",
#           "///TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/"]
# slideshow(slides, t, screen)

'''Test function for spawning random pieces'''
# for _ in range(20):
#     b = Board()
#     b.display_board()
#     sleep(0.5)

# Bag generation is working (evidence)
# '''
# ZSLTIOJ/LSITZOJ
# LTIOJ/LSITZOJ/JL
# TIOJ/LSITZOJ/JLO
# IOJ/LSITZOJ/JLOI
# OJ/LSITZOJ/JLOIS
# J/LSITZOJ/JLOISZ
# /LSITZOJ/JLOISZT
# SITZOJ/JLOISZT/Z
# ITZOJ/JLOISZT/ZO
# TZOJ/JLOISZT/ZOI
# ZOJ/JLOISZT/ZOIT
# OJ/JLOISZT/ZOITS
# J/JLOISZT/ZOITSJ
# /JLOISZT/ZOITSJL
# LOISZT/ZOITSJL/Z
# OISZT/ZOITSJL/ZO
# ISZT/ZOITSJL/ZOS
# SZT/ZOITSJL/ZOSJ
# ZT/ZOITSJL/ZOSJL
# T/ZOITSJL/ZOSJLZ
# ZOITSJL/ZOSJLZJ/'''

'''Swooshing movement is fixed'''
# b = Board(t, screen, "S1821")
# for _ in range(10):
#     b.display_board()
#     b.change_x(1)
#     sleep(0.5)

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

''' test function for garbage and actions (deprecated)'''
# dtc = "*OO1LLLIJJJ/OO1SSLIJZZ/J3SSIZZI/J2TTTIOOI/JJ1LTZZOOI/3LZZZSSI/2LL2ZZSS/7Z2"
# g1 = "*g0/g0/g0/g0/g1/g1/g1/g1/g1/OO1LLLIJJJ/OO1SSLIJZZ/J3SSIZZI/J2TTTIOOI/JJ1LTZZOOI/3LZZZSSI/2LL2ZZSS/7Z2"
# b1 = Board(t, screen, "T1022", dtc, "dtc")
# actions = """g1x5 0.5
# g0x4 0.5
# d
# CCW
# CCW
# d
# CCW
# lock
# CW
# L
# d
# CCW
# CCW
# lock
# L
# CW
# d
# lock
# CW
# L
# d
# CW
# lock
# CW
# L
# d
# lock"""

# b1.do_actions_from_input(actions)
# for _ in range(5):
#     with_delay = b1.replay_notation
#     print(with_delay, end="\nending\n")
#     b1 = Board(t, screen, "T1022", dtc, "TITIOJZLSJLOZ")
#     b1.do_actions_from_input(with_delay)
#     sleep(1)
