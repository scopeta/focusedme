"""The focusedme module implements basic features of a Pomodoro timer
that runs in a terminal and provide a text-based interface.
The timer provides an easy way to break down work into focused sessions,
traditionally 25 minutes in length, separated by short or long breaks.
Each session is known as a pomodoro.
The timer will track the sessions and notify the user of completion,
as well as allow them to control its progress.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from configparser import ConfigParser
from dataclasses import dataclass, field
from timeit import default_timer
from typing import Callable

import simpleaudio as sa

sys.path.append(".")
sys.path.append("focusedme")
from util import in_app_path  # noqa: E402

BANNER = r"""
  __                              _ __  __
 / _|                            | |  \/  |
| |_ ___   ___ _   _ ___  ___  __| | \  / | ___
|  _/ _ \ / __| | | / __|/ _ \/ _` | |\/| |/ _ \
| || (_) | (__| |_| \__ \  __/ (_| | |  | |  __/
|_| \___/ \___|\__,_|___/\___|\__,_|_|  |_|\___|""".strip(
    "\r\n"
)
SECONDS_PER_MIN = 60
RESULTS = r"""
  _   _   _   _     _   _   _   _   _   _   _
 / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \
( Y | o | u | r ) ( r | e | s | u | l | t | s )
 \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/ """.strip(
    "\r\n"
)

GOODBYE = "\n\nThanks for using focusedMe. Goodbye!\n\n"


@dataclass
class View:
    """class responsible for user interaction through terminal."""

    @classmethod
    def get_color(cls, color: str) -> str:
        """Print fore ground colors in terminal
        use reset value to cancel all colors
        """

        dict_color = {
            "reset": "\033[0m",
            "bold": "\033[01m",
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "orange": "\033[33m",
            "blue": "\033[34m",
            "purple": "\033[35m",
            "cyan": "\033[36m",
            "lightgrey": "\033[37m",
            "darkgrey": "\033[90m",
            "lightred": "\033[91m",
            "lightgreen": "\033[92m",
            "yellow": "\033[93m",
            "lightblue": "\033[94m",
            "pink": "\033[95m",
            "lightcyan": "\033[96m",
        }

        return dict_color[color]

    def __format_time(self, remainder: int) -> str:
        """Method that receives timer info and format to present
        in the terminal.
        Receives the a time in seconds and return a user friendly string
        """
        minutes, seconds = divmod(int(remainder), SECONDS_PER_MIN)

        return "{:00}min {:00}s remaining   ".format(minutes, seconds)

    @classmethod
    def ring_bell(cls, PATH: str) -> None:
        """
        Play a notification sound: use 'afplay' on macOS to avoid simpleaudio issues,
        otherwise use simpleaudio.
        """
        audio_path = in_app_path(PATH)
        try:
            if sys.platform == "darwin":
                subprocess.run(["afplay", audio_path], check=True)
            else:
                wave_obj = sa.WaveObject.from_wave_file(audio_path)
                wave_obj.play()
        except Exception:
            # ignore any playback errors
            pass

    def __get_colore_type(self, stype: str) -> str:
        """return the type string with the chosen color"""
        colored_type = stype
        if stype == "FOCUS TIME":
            colored_type = self.get_color("lightred") + stype + self.get_color("reset")
        elif stype == "SHORT BREAK":
            colored_type = (
                self.get_color("lightgreen") + stype + self.get_color("reset")
            )
        elif stype == "LONG BREAK":
            colored_type = self.get_color("lightblue") + stype + self.get_color("reset")
        return colored_type

    def show_time(
        self, remainder: int, num_round: int, num_session: int, type_session: str
    ) -> None:
        """Show timer countdown in terminal.

        Args:
            remainder: Remaining time in seconds
            num_round: Current round number
            num_session: Current session number
            type_session: Type of session (FOCUS TIME, SHORT BREAK, LONG BREAK)
        """

        colored_type = self.__get_colore_type(
            type_session.replace("_", " ").upper()
        )  # noqa E501

        print(
            "Round",
            num_round,
            "/",
            "Session",
            num_session,
            "-",
            colored_type,
            ": ",
            self.__format_time(remainder),
            end="",
            flush=True,
        )
        print("\r", end="", flush=True)

    def plot(self, logged_data: list[str], time_args: dict[str, int]) -> None:
        """create text from logged data and return it to be plotted to user
        in the terminal"""

        print(self.get_color("green"))
        print(RESULTS)
        print(self.get_color("reset"))

        for dt in logged_data:
            if "Round" in dt:
                print(dt)
            else:
                print(
                    "".join(map(str, dt)),
                    "-",
                    dt.count("X") * time_args["focus_time"],
                    "minutes",
                )
                print()

        print("[legend: (X) completed sessions, (O) skipped sessions]")
        print("______________________________________________________\n")

    def run(self, time_args: dict[str, int], sound_args: dict[str, str]) -> None:
        """method that orchestrates overal execution"""

        # initialize with parameters informed through cli arguments
        pomodoro = Pomodoro(time_args, time_args["num_rounds"])
        rounds = pomodoro.create_rounds()
        log = Log()
        tracker = Tracker(rounds, log)

        while True:
            try:
                tracker.start(self.show_time, sound_args)
            except KeyboardInterrupt:
                user_cmd = input(
                    "\n\nWhat would you like to do?"
                    "\n\n[S]kip current session, [P]lot summary, "
                    "[ANY] other key to Quit : "
                ).upper()
                if user_cmd == "S":
                    print("\n\nSkipping to next session..\n\n")
                elif user_cmd == "P":
                    log.plot_results(self.plot, time_args)
                    print(GOODBYE)
                    sys.exit(0)
                else:
                    print(GOODBYE)
                    sys.exit(0)


@dataclass
class Round:
    """class responsible for creating sessions according to user parameters"""

    len_args: dict[str, int] = field(default_factory=dict)

    # non init attributes
    sessions: list[Session] = field(default_factory=list)
    current_session_idx: int = 0
    completed: bool = False

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

    def __post_init__(self) -> None:
        self.sessions = self.__build_new_round(self.len_args)

    def __build_new_round(self, len_args: dict[str, int]) -> list[Session]:
        """build a list of sessions that will define this round
        acording to len_args
        """
        sessions = []
        for session_type in self.round_template:
            session = Session(session_type, len_args[session_type])
            sessions.append(session)
        return sessions

    # def completed(self)
    def update_session(self, status: str) -> None:
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

    def get_current_session(self) -> "Session":
        """return the instance of the current session."""

        # if the session has already been skipped, go to next session
        if (
            self.sessions[self.current_session_idx].status == "skipped"
            and self.current_session_idx < len(self.sessions) - 1
        ):
            self.current_session_idx += 1

        return self.sessions[self.current_session_idx]


@dataclass
class Session:
    """class responsible for storing session data"""

    session_type: str = ""
    length: int = 0
    status: str = "not started"  # other possible value: skipped, done


@dataclass
class Log:
    """stores progress data for tracked rounds
    and provide text output with summary data
    to be plotted
    """

    tracked_rounds: list[Round] = field(default_factory=list)

    def save_rounds(self, tracked_rounds: list[Round]) -> None:
        """save all tracked rounds"""
        self.tracked_rounds = tracked_rounds

    def plot_results(
        self,
        plot: Callable[[list[str], dict[str, int]], None],
        time_args: dict[str, int],
    ) -> None:
        """return user friendly text with completion information
        about user's focus sessions
        """

        # iterate in tracked_rounds and test for completion
        # format string showing completed and skipped rounds
        # add total focused minutes

        graphic = []
        for i in range(len(self.tracked_rounds)):
            graphic.append("Round #" + str(i + 1) + ": ")
            session_status = "".join(
                "X" if s.status == "done" else "O"
                for s in self.tracked_rounds[i].sessions
                if s.session_type == "focus_time"
            )
            graphic.append(session_status)

        plot(graphic, time_args)


@dataclass
class Config:
    """data class that store the attributes of
    different default values used on the program
    """

    @staticmethod
    def load_init() -> tuple[dict[str, int], dict[str, str]]:
        """return the a object array with the lenght os the default values"""
        file = in_app_path("../config/fm.init")
        config = ConfigParser()
        config.read(file)

        time_args = {}
        sound_args = {}

        for section in list(config["time"]):
            time_args[section] = int(config["time"][section])

        for section in list(config["sound"]):
            sound_args[section] = str(config["sound"][section])

        if sound_args["sound"]:
            bool(sound_args["sound"])

        return time_args, sound_args

    @staticmethod
    def save_init(time_args: dict[str, int], sound_args: dict[str, str]) -> None:
        """save the new values as the default values"""
        file = in_app_path("../config/fm.init")
        config = ConfigParser()
        config.read(file)

        for section in list(config["time"]):
            config.set("time", section, str(time_args[section]))

        for section in list(config["sound"]):
            config.set("sound", section, str(sound_args[section]))

        with open(file, "w") as configfile:
            config.write(configfile)

    @staticmethod
    def show_init(time_args: dict[str, int], sound_args: dict[str, str]) -> None:
        """prints the 'time' values that are saved in the init files."""
        file = in_app_path("../config/fm.init")
        config = ConfigParser()
        config.read(file)

        print("Default Values:")
        print(
            View.get_color("green") + "   Focus Time: " + str(time_args["focus_time"])
        )
        print(
            View.get_color("orange")
            + "   Short Break: "
            + str(time_args["short_break"])
        )
        print(View.get_color("red") + "   Long Break: " + str(time_args["long_break"]))
        print(View.get_color("blue") + "   Rounds: " + str(time_args["num_rounds"]))
        print(View.get_color("purple") + "   Sound: " + str(sound_args["sound"]))
        print(View.get_color("pink") + "   Sound File: " + str(sound_args["path"]))
        print(View.get_color("reset"))


@dataclass
class Pomodoro:
    """class responsible for creating rounds according to user parameters"""

    len_args: dict[str, int] = field(default_factory=dict)
    num_rounds: int = 3

    # non init attributes
    tracker: list = field(default_factory=list)

    def create_rounds(self) -> list[Round]:
        """create and return a list of rounds of size equal to num_rounds and
        configured according to the length attributes.
        """
        rounds = [Round(self.len_args) for _ in range(self.num_rounds)]

        return rounds


@dataclass
class Tracker:
    """Control timer according to session durations
    and trigger log saving and user interface updates
    """

    rounds: list[Round] = field(default_factory=list)
    log: Log = field(default_factory=Log)
    current_round_idx: int = 0

    def __cur_time(self) -> int:
        return int(default_timer())

    def start(
        self,
        show_time: Callable[[int, int, int, str], None],
        sound_args: dict[str, str],
    ) -> None:
        """method to process the list of rounds.
        It tracks and saves progress while sending visual information
         for the UI function received as a parameter
        """

        SOUND = sound_args["sound"]
        PATH = sound_args["path"]

        # outter loop - runs until end of rounds
        while True:

            # return the valid round, either a new one if completed
            # or the next one available
            self.current_round_idx = self.__get_round()
            # if the current round is already completed, there is
            # no round left and the loop should be broken
            if self.rounds[self.current_round_idx].completed:
                break

            # iterate over all session in a round()
            cur_round = self.rounds[self.current_round_idx]
            for _ in range(len(cur_round.sessions)):
                cur_session = cur_round.get_current_session()
                # set intermmediary value of "skipped"; once the time is up
                # update session to "done"
                cur_round.update_session("skipped")
                self.log.save_rounds(self.rounds)

                remainder = cur_session.length * SECONDS_PER_MIN

                started_at = self.__cur_time()

                while True:
                    show_time(
                        remainder,
                        self.current_round_idx + 1,
                        cur_round.current_session_idx + 1,
                        cur_session.session_type,
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
                    View.ring_bell(PATH)

    def __get_round(self) -> int:
        """Return the current round
        check if current_round is completed
        otherwise return a new round
        """
        if (self.rounds[self.current_round_idx].completed) and (
            self.current_round_idx < len(self.rounds) - 1
        ):
            self.current_round_idx += 1

        return self.current_round_idx


def main() -> None:
    """parse cli arguments and start sequence of object calls"""

    print(BANNER, "\n")

    print(
        View.get_color("green")
        + " __ "
        + View.get_color("reset")
        + "A Pomodoro Timer"
        + View.get_color("red")
        + " ___"
        + View.get_color("reset")
        + "\n\n"
    )
    parser = argparse.ArgumentParser(
        description="Welcome to the focusedMe app. Start your Pomodoro timer"
        " and enjoy the focus! (Stop it with Ctrl+c)",
        usage="%(prog)s [-f] [-sb] [-lb] [-r] [-s]",
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
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="save the duration in minutes os the session/break as new default values",
    )

    args = parser.parse_args()
    time_args, sound_args = Config.load_init()
    # dictionary that store Pomodor initialization parameters
    if args.focus_time:
        time_args["focus_time"] = args.focus_time
    if args.short_break:
        time_args["short_break"] = args.short_break
    if args.long_break:
        time_args["long_break"] = args.long_break
    if args.num_rounds:
        time_args["num_rounds"] = args.num_rounds
    if args.save:
        Config.save_init(time_args, sound_args)
        Config.show_init(time_args, sound_args)
    # initialize view
    view = View()
    # start pomodoro
    view.run(time_args, sound_args)


if __name__ == "__main__":
    main()
