import pygame


class Score():
    def __init__(self):
        self.kills = 0
        self.time = 0

    def update_score(self):
        self.kills += 1

    def update_time(self, milliseconds):
        self.time = milliseconds/1000

    # Outputs score to console upon death

    def print_score(self):
        print(f"You destroyed {self.kills} asteroids!")
        print(f"You survived for {self.time} seconds!")