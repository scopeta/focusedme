"""The focusedme module implements basic features of a Pomodoro timer
that runs in a terminal and provide a text-based interface.
The timer provides an easy way to break down work into focused sessions,
traditionally 25 minutes in length, separated by short or long breaks.
Each session is known as a pomodoro.
The timer will track the sessions and notify the user of completion,
as well as allow them to control its progress.
"""


import sys
import time
import argparse
from timeit import default_timer
from focusedme.util import in_app_path
from dataclasses import dataclass
from playsound import playsound

import attr


BANNER = r"""
  __                              _ __  __
 / _|                            | |  \/  |
| |_ ___   ___ _   _ ___  ___  __| | \  / | ___
|  _/ _ \ / __| | | / __|/ _ \/ _` | |\/| |/ _ \
| || (_) | (__| |_| \__ \  __/ (_| | |  | |  __/
|_| \___/ \___|\__,_|___/\___|\__,_|_|  |_|\___|""".strip(
    "\r\n"
)
NUM_ROUNDS = 3
LENGHT_ARGS = {"focus_time": 25, "short_break": 5, "long_break": 25}
SECONDS_PER_MIN = 60
RESULTS = r"""
  _   _   _   _     _   _   _   _   _   _   _
 / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \
( Y | o | u | r ) ( r | e | s | u | l | t | s )
 \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/ """.strip(
    "\r\n"
)

GOODBYE = "\n\nThanks for using focusedMe. Goodbye!\n\n"
LENGHT_ARGS = {"focus_time": 25, "short_break": 5, "long_break": 25}
SOUND = True


@attr.s
class View:
    """class responsible for user interaction through terminal."""

    def __format_time(self, remainder):
        """Method that receives timer info and format to present
        in the terminal.
        Receives the a time in seconds and return a user friendly string
        """
        minutes, seconds = divmod(int(remainder), SECONDS_PER_MIN)

        return "{:00}min {:00}s remaining   ".format(minutes, seconds)

    @classmethod
    def ring_bell(cls):
        playsound(in_app_path("Ring01.wav"))

    def show_time(self, remainder, num_round, num_session, type_session):
        """ show timer countdown in terminal. Receives the remainder time
        for the session and print progress for the user"""

        print(
            "Round",
            num_round,
            "/",
            "Session",
            num_session,
            "-",
            type_session.replace("_", " ").upper(),
            ": ",
            self.__format_time(remainder),
            end="",
            flush=True,
        )
        print("\r", end="", flush=True)

    def plot(self, logged_data):
        """ create text from logged data and return it to be plotted to user
        in the terminal """

        print()
        print(RESULTS)
        print()

        for dt in logged_data:
            if "Round" in dt:
                print(dt)
            else:
                print(
                    "".join(map(str, dt)),
                    "-",
                    dt.count("X") * LENGHT_ARGS["focus_time"],
                    "minutes",
                )
                print()

        print("[legend: (X) completed sessions, (O) skipped sessions]")
        print("______________________________________________________\n")

    def run(self, len_args, num_rounds):
        """ method that orchestrates overal execution """

        # initialize with parameters informed through cli arguments
        pomodoro = Pomodoro(len_args, num_rounds)
        rounds = pomodoro.create_rounds()
        log = Log()
        tracker = Tracker(rounds, log)

        while True:
            try:
                tracker.start(self.show_time)
            except KeyboardInterrupt:
                user_cmd = input(
                    "\n\nWhat would you like to do?"
                    "\n\n[S]kip current session, [P]lot summary, "
                    "[ANY] other key to Quit : "
                ).upper()
                if user_cmd == "S":
                    print("\n\nSkipping to next session..\n\n")
                elif user_cmd == "P":
                    log.plot_results(self.plot)
                    print(GOODBYE)
                    sys.exit(0)
                else:
                    print(GOODBYE)
                    sys.exit(0)


@attr.s
class Tracker:
    """ Control timer according to session durations
    and trigger log saving and user interface updates
    """

    rounds = attr.ib()
    log = attr.ib()

    current_round_idx = attr.ib(init=False, default=0)

    def __cur_time(self):
        return int(default_timer())

    def start(self, show_time):
        """method to process the list of rounds.
        It tracks and saves progress while sending visual information
         for the UI function received as a parameter
        """

        # outter loop - runs until end of rounds
        while True:

            # return the valid round, either a new one if completed
            # or the next one available
            self.current_round_idx = self.__get_round()
            # if the current round is already completed, there is
            # no round left and the loop should be broken
            if self.rounds[self.current_round_idx].completed is True:
                break

            # iterate over all session in a round()
            cur_round = self.rounds[self.current_round_idx]
            for i in range(len(cur_round.sessions)):
                cur_session = cur_round.get_current_session()
                # set intermmediary value of "skipped"; once the time is up
                # update session to "done"
                cur_round.update_session("skipped")
                self.log.save_rounds(self.rounds)

                remainder = cur_session.length * SECONDS_PER_MIN

                started_at = self.__cur_time()

                while True:
                    show_time(
                        remainder=remainder,
                        num_round=self.current_round_idx + 1,
                        num_session=cur_round.current_session_idx + 1,
                        type_session=cur_session.session_type,
                    )
                    time.sleep(1)
                    cur = self.__cur_time()
                    remainder = max(remainder - (cur - started_at), 0)
                    started_at = cur
                    if remainder <= 0:
                        break
                cur_round.update_session("done")
                self.log.save_rounds(self.rounds)
                if SOUND:
                    View.ring_bell()

    def __get_round(self):
        """" return the current round
        check if current_round is completed
        otherwise return a new round
        """

        if (self.rounds[self.current_round_idx].completed is True) and (
            self.current_round_idx < len(self.rounds) - 1
        ):
            self.current_round_idx += 1

        return self.current_round_idx


@attr.s
class Pomodoro:
    """main class to store basic pomodoro technique attributes,
    such as length of sessions.
    The user should be able to set the number of rounds and length
    parameter through command line arguments.
    """

    # init attributes
    len_args = attr.ib(factory=dict)
    num_rounds = attr.ib(default=3)

    # non init attributes
    tracker = attr.ib(init=False)

    def create_rounds(self):
        """create and return a list of rounds of size equal to num_rounds and
         configured according to the length attributes.
        """

        rounds = [Round(self.len_args) for i in range(self.num_rounds)]

        return rounds


@attr.s
class Round:
    """class that models a pomodoro round composed by multiple sessions.
    it stores a list of focus sessions and breaks in the sequence they
    should happen.
    Both types of sessions are instances of the Session class.
    """

    len_args = attr.ib()

    sessions = attr.ib(init=False, factory=list)
    current_session_idx = attr.ib(init=False, default=0)
    completed = attr.ib(init=False, default=False)

    round_template = (
        "focus_time",
        "short_break",
        "focus_time",
        "short_break",
        "focus_time",
        "short_break",
        "focus_time",
        "long_break",
    )

    def __attrs_post_init__(self):
        self.sessions = self.__build_new_round(self.len_args)

    def __build_new_round(self, len_args):
        """ build a list of sessions that will define this round
        acording to len_args
        """
        sessions = [
            Session(session_type, len_args[session_type])
            for session_type in self.round_template
        ]
        return sessions

    # def completed(self)
    def update_session(self, status):
        """update session object with status and set
        the current session reference"""

        self.sessions[self.current_session_idx].status = status
        # verify if it is the last session for the round
        # mark Round as completed even if the status is "skipped"
        self.completed = self.current_session_idx == len(self.sessions) - 1

        if (status == "done") and (
            self.current_session_idx < (len(self.sessions) - 1)
        ):  # done and not the last one
            self.current_session_idx += 1

    def get_current_session(self):
        """return the instance of the current session.
        """

        # if the session has already been skipped, go to next session
        if (
            self.sessions[self.current_session_idx].status == "skipped"
            and self.current_session_idx < len(self.sessions) - 1
        ):
            self.current_session_idx += 1

        return self.sessions[self.current_session_idx]


@dataclass
class Session:
    """data class that store the attributes of different types of sessions"""

    session_type: str
    length: int
    status: int = "not started"  # other possible value: skipped, done


@attr.s
class Log:
    """ stores progress data for tracked rounds
    and provide text output with summary data
    to be plotted
    """

    tracked_rounds = attr.ib(factory=list)

    def save_rounds(self, tracked_rounds):
        """ save all tracked rounds
        """
        self.tracked_rounds = tracked_rounds

    def plot_results(self, plot):
        """ return user friendly text with completion information
        about user's focus sessions
        """

        # iterate in tracked_rounds and test for completion
        # format string showing completed and skipped rounds
        # add total focused minutes

        graphic = []
        for i in range(len(self.tracked_rounds)):
            graphic.append("Round #" + str(i + 1) + ": ")
            graphic.append(
                [
                    "X" if s.status == "done" else "O"
                    for s in self.tracked_rounds[i].sessions
                    if s.session_type == "focus_time"
                ]
            )

        plot(graphic)


def main():
    """ parse cli arguments and start sequence of object calls"""

    print(BANNER, "\n")
    print(" __ A Pomodoro Timer ___" + "\n\n")
    parser = argparse.ArgumentParser(
        description="Welcome to the focusedMe app. Start your Pomodoro timer"
        " and enjoy the focus! (Stop it with Ctrl+c)",
        usage="%(prog)s [-f] [-sb] [-lb] [-r]",
    )
    parser.add_argument(
        "-r",
        "--num_rounds",
        type=int,
        metavar="",
        help="number of rounds, default is 3",
    )
    parser.add_argument(
        "-f",
        "--focus_time",
        type=int,
        metavar="",
        help="duration in minutes of the focus session, default is 25 mins",
    )
    parser.add_argument(
        "-sb",
        "--short_break",
        type=int,
        metavar="",
        help="duration in minutes of the short break, default is 5 mins",
    )
    parser.add_argument(
        "-lb",
        "--long_break",
        type=int,
        metavar="",
        help="duration in minutes of the focus session, default is 25 mins",
    )

    args = parser.parse_args()
    # dictionary that store Pomodor initialization parameters
    len_args = LENGHT_ARGS
    num_rounds = NUM_ROUNDS
    if args.focus_time:
        len_args["focus_time"] = args.focus_time
    if args.short_break:
        len_args["short_break"] = args.short_break
    if args.long_break:
        len_args["long_break"] = args.long_break
    if args.num_rounds:
        num_rounds = args.num_rounds

    # initialize view
    view = View()
    # start pomodoro
    view.run(len_args, num_rounds)


if __name__ == "__main__":
    main()
