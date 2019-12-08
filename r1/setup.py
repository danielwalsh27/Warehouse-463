import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["Box.png", "Remove.png", "Warehouse.png", "Arial.ttf"]}},
    executables = executables

    )