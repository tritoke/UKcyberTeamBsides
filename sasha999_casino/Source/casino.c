// gcc casino.c -o casino -no-pie

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

enum RouletteColours {
    COLOUR_GREEN = 0,
    COLOUR_RED = 1,
    COLOUR_BLACK = 2,
};

char* colours[] = {
    "0",
    "red",
    "black",
};

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int get_roulette_colour(int num) {
    if (num == 0)
        return COLOUR_GREEN;
    bool even = num % 2 == 0;
    if ((1 <= num && num <= 10) || (19 <= num && num <= 28)) {
        return even ? COLOUR_BLACK : COLOUR_RED;
    }
    return !even ? COLOUR_BLACK : COLOUR_RED;
}

void escape_casino() {
    puts("You successfully escaped the casino!");
    execv("/bin/sh", NULL);
}

int main() {
    setup();
    srand(time(NULL));
    unsigned long money = 10;
    while (money < 0x1337133713371337) {
        printf("Your balance: %lu dubloons\n", money);
        puts("1. Bet on colour");
        puts("2. Bet on number");
        printf("> ");
        int bet_type = -1;
        scanf("%d", &bet_type);
        getchar();
        int choice = -1;
        switch (bet_type) {
            case 1:
                while (1) {
                    char colour[0x10];
                    printf("Pick your colour (red/black): ");
                    fgets(colour, sizeof(colour), stdin);
                    if (colour[0] == 'r' || colour[0] == 'R') {
                        choice = COLOUR_RED;
                        break;
                    } else if (colour[0] == 'b' || colour[0] == 'B') {
                        choice = COLOUR_BLACK;
                        break;
                    }
                }
                break;
            case 2:
                puts("You're bold aren't you!");
                while (!(0 <= choice && choice <= 36)) {
                    printf("Pick your number: ");
                    scanf("%d", &choice);
                    getchar();
                }
                break;
            default:
                continue;
        }
        unsigned long bet = 0;
        while (!(0 < bet && bet <= money)) {
            printf("How much do you want to bet: ");
            scanf("%lu", &bet);
            getchar();
        }
        money -= bet;
        printf("Spinning the roulette wheel...\n");
        int result = rand() % 37;
        if (bet_type == 1) {
            int colour = get_roulette_colour(result);
            printf("The wheel has landed on %s\n", colours[colour]);
            if (choice == colour) {
                printf("You won %lu dubloons!\n", 2*bet);
                money += 2*bet;
            } else {
                puts("You lost :(");
            }
        } else {
            printf("The wheel has landed on %d\n", result);
            if (choice == result) {
                printf("You won %lu dubloons!\n", 36*bet);
                money += 36*bet;
            }
        }
        if (money == 0) {
            puts("You're out of money, shoo!");
            exit(0);
        }
    }
    char escape[100];
    puts("You've been suspected of cheating and the police are on their way!");
    puts("You need to get out of here, and quickly!");
    fgets(escape, 0x100, stdin);
    return 0;
}