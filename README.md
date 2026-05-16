FATEC_projeto_integrador_1ro_sem

# Python Scheduling System for audio-visual sessions

> This program can be run on your command line interface (CMD, Powershell or the CLI used by yout IDE).
---

When run, it asks for the current program operator, stores it, and then shows a menu.

The menu assigns to each number, from 1 to 10, a functionality regarding CRUD functions related to clients and client scheduling.

Those informations are then used to arrange meetings between client and operator, and then it registers the elapsed time of the meeting.
The elapsed time of a meeting is then used for future scheduling.

During execution, the program creates JSON files for storing variables and inputed values.
No SQL databases were used, since the program doesn't require crazy data volumes. This may change in the future.

# 
You can run this code by:
- Double clicking main.py, or
- Openning it directly by your terminal, given you are inside the project's directory.

  For Windows 10 and 11 systems, execute:
    ```
    python .\main.py
    ```
  For linux based systems:
    ```
    python3 main.py
    ```

> This program is still on its development phase. Many existing functionalities may change.
