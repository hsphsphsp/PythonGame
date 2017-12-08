import cx_Freeze, os

os.environ['TCL_LIBRARY'] = r'C:\Users\User\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\User\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

executables = [cx_Freeze.Executable(script = "quatris.py", base = 'Win32GUI')]

cx_Freeze.setup(
    name="QUATRIS",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["ab_main.wav", 'ct_main.wav', 'f3_main.wav', 'ff_main.wav',
                                            'gta4_soviet.wav', 'h3_neverforget.wav', 'h_onefinaleffort.wav',
                                            'm_sweden.wav', 'p1_stillalive.wav', 'p2_caramiaaddio.wav', 'smb_1-up.wav',
                                            'smb_bump.wav', 'smb_coin.wav', 'smb_gameover.wav', 'smb_mariodie.wav',
                                            'smb_overworld.wav', 'smb_pause.wav', 'tes4o_main.wav',
                                            'tes5s_dragonborn.wav', 'tes5s_farhorizons.wav', 'tetris.wav',
                                            'tloz_intro.wav', 'tw3wh_main.wav', 'freesansbold.ttf']}},
    executables = executables

    )
