# RockPaperScissors

## Inspection
We're given a code with the reducted flag.

Looking a bit at the code, we see that we need to win the computer 5 times in a row.
So, let's check how do we win a game:

```c
bool play () {
  char player_turn[100];
  srand(time(0));
  int r;

  printf("Please make your selection (rock/paper/scissors):\n");
  r = tgetinput(player_turn, 100);
  // Timeout on user input
  if(r == -3)
  {
    printf("Goodbye!\n");
    exit(0);
  }

  int computer_turn = rand() % 3;
  printf("You played: %s\n", player_turn);
  printf("The computer played: %s\n", hands[computer_turn]);

  if (strstr(player_turn, loses[computer_turn])) {
    puts("You win! Play again?");
    return true;
  } else {
    puts("Seems like you didn't win this time. Play again?");
    return false;
  }
}
```

The computer is getting a random result (rock/paper/scissors).
Then, the program checks if the possible losses of the computer's choice are included in in our choice.
Keyword: INCLUDED


So... we can just input a string that every possible loss (rock, paper and scissors) will be included in:

`rockpaperscissors`



## Getting the flag

So all we need to do is win 5 times in a row - no problem!

```python
from pwn import *

WINS_NUM = 5


def main():
    exploit_str = "rockpaperscissors"
    proc = pwnlib.tubes.process.process("game")

    for round_num in range(WINS_NUM):
        print(proc.recv().decode())
        proc.sendline("1")

        print(proc.recv().decode())
        proc.sendline(exploit_str)

    print(proc.recv().decode())


if __name__ == '__main__':
    main()

```
And we get the redacted flag. Let's try this with nc.

```
You win! Play again?
Congrats, here's the flag!
picoCTF{50M3_3X7R3M3_1UCK_58F0F41B}
```