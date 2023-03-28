import copy
import random
import numpy as np

from simpleoptions import BaseEnvironment

from simpleenvs.renderers import RoomRenderer

# Import room template files.
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from . import data

with pkg_resources.path(data, "two_rooms.txt") as path:
    default_two_room = path

with pkg_resources.path(data, "six_rooms.txt") as path:
    default_six_room = path

with pkg_resources.path(data, "nine_rooms.txt") as path:
    default_nine_room = path

with pkg_resources.path(data, "xu_four_rooms.txt") as path:
    xu_four_room = path

with pkg_resources.path(data, "bridge_room.txt") as path:
    bridge_room = path

with pkg_resources.path(data, "cage_room.txt") as path:
    cage_room = path

with pkg_resources.path(data, "empty_room.txt") as path:
    empty_room = path

with pkg_resources.path(data, "small_rooms.txt") as path:
    small_rooms = path

with pkg_resources.path(data, "four_rooms.txt") as path:
    four_rooms = path

with pkg_resources.path(data, "four_rooms_holes.txt") as path:
    four_rooms_holes = path

with pkg_resources.path(data, "maze_rooms.txt") as path:
    maze_rooms = path

with pkg_resources.path(data, "spiral_room.txt") as path:
    spiral_rooms = path

with pkg_resources.path(data, "parr_maze.txt") as path:
    parr_maze = path

with pkg_resources.path(data, "parr_mini_maze.txt") as path:
    parr_mini_maze = path

with pkg_resources.path(data, "ramesh_maze.txt") as path:
    ramesh_maze = path

CELL_TYPES_DICT = {".": "floor", "#": "wall", "S": "start", "G": "goal", "A": "agent"}

ACTIONS_DICT = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}


class DiscreteRoomEnvironment(BaseEnvironment):
    """
    Class representing a discrete "rooms-like" gridworld, as is commonly seen in the HRL literature.
    """

    def __init__(self, room_template_file_path, movement_penalty=-0.001, goal_reward=1.0):
        """
        Initialises a new DiscreteRoomEnvironment object.

        Arguments:
            room_template_file_path {string or Path} -- Path to a gridworld template file.

        Keyword Arguments:
            movement_penalty {float} -- Penalty applied each time step for taking an action. (default: {-1.0})
            goal_reward {float} -- Reward given to the agent upon reaching a goal state. (default: {10.0})
        """
        super().__init__()

        self._initialise_rooms(room_template_file_path)
        self.movement_penalty = movement_penalty
        self.goal_reward = goal_reward
        self.is_reset = False
        self.renderer = None

    def _initialise_rooms(self, room_template_file_path):
        """
        Initialises the envionment according to a given template file.

        Arguments:
            room_template_file_path {string or Path} -- Path to a gridworld template file.
        """

        # Load gridworld template file.
        self.gridworld = np.loadtxt(room_template_file_path, comments="//", dtype=str)

        # Discover start and goal states.
        self.initial_states = []
        self.terminal_states = []
        for y in range(self.gridworld.shape[0]):
            for x in range(self.gridworld.shape[1]):
                if CELL_TYPES_DICT[self.gridworld[y, x]] == "start":
                    self.initial_states.append((y, x))
                elif CELL_TYPES_DICT[self.gridworld[y, x]] == "goal":
                    self.terminal_states.append((y, x))

    def reset(self, state=None):
        """
        Resets the environment, setting the agent's position to a random starting state
        and selecting a random goal state.

        Arguments:
           state {(int, int)} -- The initial state to use. Defaults to None, in which case an state is chosen according to the environment's initial state distribution.

        Returns:
            [(int, int)] -- The agent's initial position.
        """

        if state is None:
            self.position = random.choice(self.initial_states)
        else:
            self.position = copy.deepcopy(state)

        self.current_initial_state = self.position

        self.is_reset = True

        return (self.position[0], self.position[1])

    def step(self, action):
        """
        Executes one time step in the environment in response to an agent's action.

        Arguments:
            action {int} -- The agent's selected action.

        Returns:
            [(int, int), float, bool] -- The environment's next state, the reward earned, and whether the new state is terminal.
        """

        current_state = self.position
        next_state = self.position

        # Computes the agent's next intended position.
        if ACTIONS_DICT[action] == "DOWN":
            next_state = (next_state[0] + 1, next_state[1])
        elif ACTIONS_DICT[action] == "UP":
            next_state = (next_state[0] - 1, next_state[1])
        elif ACTIONS_DICT[action] == "RIGHT":
            next_state = (next_state[0], next_state[1] + 1)
        elif ACTIONS_DICT[action] == "LEFT":
            next_state = (next_state[0], next_state[1] - 1)

        reward = 0
        terminal = False

        # Determines whether the next state is legal and/or terminal.
        if CELL_TYPES_DICT[self.gridworld[next_state[0]][next_state[1]]] == "wall":
            next_state = current_state
        elif self.is_state_terminal(state=(next_state[0], next_state[1])):
            reward += self.goal_reward
            terminal = True

        if terminal:
            self.is_reset = False

        reward += self.movement_penalty

        self.position = next_state

        return next_state, reward, terminal, {}

    def get_action_space(self):
        return list(range(4))

    def get_available_actions(self, state=None):
        """
        Returns the set of available actions for the given state (by default, the current state).

        Keyword Arguments:
            state {(int, int)} -- The state to return available actions for. Defaults to None (uses current state).

        Returns:
            [list(int)] -- The list of actions available in the given state.
        """
        if state is None:
            state = self.position

        if self.is_state_terminal(state):
            return []
        else:
            return self.get_action_space()

    def get_action_mask(self, state=None):
        """
        Returns a boolean mask indicating which actions are available in the given state (by default, the current state).

        A value of True at index i indicates that this action is available.
        A value of False at index i indicates that the corresponding action is not available.

        Keyword Args:
            state {(int, int)} -- The state to return an action mask for. Defaults to None (uses current state).

        Returns:
            [list(bool)] -- A boolean mask indicating action availability in the current state.
        """
        if state is None:
            state = self.position

        if self.is_state_terminal(state):
            return [False for i in range(4)]
        else:
            return [True for i in range(4)]

    def render(self):
        """
        Renders the current environmental state.
        """

        if self.renderer is None:
            self.renderer = RoomRenderer(
                self.gridworld,
                start_state=self.current_initial_state,
                goal_states=self.terminal_states,
            )

        self.renderer.update(
            self.position,
            self.gridworld,
            start_state=self.current_initial_state,
            goal_states=self.terminal_states,
        )

    def close(self):
        """
        Terminates all environment-related processes.
        """
        if self.renderer is not None:
            self.renderer.close()

    def is_state_terminal(self, state=None):
        """
        Returns whether the given state is terminal or not.
        If no state is specified, whether the current state is terminal will be returned.

        Args:
            state (tuple, optional): Whether or not the given state is terminal. Defaults to None (i.e. current state).

        Returns:
            bool: Whether or not the given state is terminal.
        """
        if state is None:
            state = self.position

        # return CELL_TYPES_DICT[self.gridworld[state[0]][state[1]]] == "goal"
        return state in self.terminal_states

    def get_initial_states(self):
        """
        Returns the initial state(s) for this environment.

        Returns:
            List[Tuple[int]]: The initial state(s) in this environment.
        """
        return copy.deepcopy(self.initial_states)

    def get_successors(self, state=None, actions=None):
        """
        Returns a list of states which can be reached by taking an action in the given state.
        If no state is specified, a list of successor states for the current state will be returned.

        Args:
            state (tuple, optional): The state to return successors for. Defaults to None (i.e. current state).
            actions (List[Hashable], optional): The actions to test in the given state when searching for successors. Defaults to None (i.e. tests all available actions).

        Returns:
            list[tuple]: A list of states reachable by taking an action in the given state.
        """
        if state is None:
            state = self.position

        if actions is None:
            actions = self.get_available_actions(state=state)

        successor_states = []
        for action in actions:
            next_state = copy.deepcopy(state)
            if ACTIONS_DICT[action] == "DOWN":
                next_state = (state[0] + 1, state[1])
            elif ACTIONS_DICT[action] == "UP":
                next_state = (state[0] - 1, state[1])
            elif ACTIONS_DICT[action] == "RIGHT":
                next_state = (state[0], state[1] + 1)
            elif ACTIONS_DICT[action] == "LEFT":
                next_state = (state[0], state[1] - 1)

            if CELL_TYPES_DICT[self.gridworld[next_state[0]][next_state[1]]] == "wall":
                next_state = copy.deepcopy(state)

            successor_states.append(next_state)

        return successor_states


class DiscreteDefaultTwoRooms(DiscreteRoomEnvironment):
    """
    A default two-rooms environment, as is commonly featured in the HRL literature.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(default_two_room, movement_penalty, goal_reward)


class DiscreteDefaultSixRooms(DiscreteRoomEnvironment):
    """
    A default six-rooms environment, as is commonly featured in the HRL literature.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(default_six_room, movement_penalty, goal_reward)


class DiscreteDefaultNineRooms(DiscreteRoomEnvironment):
    """
    A default nine-rooms environment, as is commonly featured in the HRL literature.
    Goal Reward: +1
    Movement Penalty: -0.001
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(default_nine_room, movement_penalty, goal_reward)


class DiscreteXuFourRooms(DiscreteRoomEnvironment):
    """
    The four-room environment used in Xu X., Yang M. & Li G. 2019
    "Constructing Temporally Extended Actions through Incremental
    Community Detection". Contains four offset rooms.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(xu_four_room, movement_penalty, goal_reward)


class BridgeRoom(DiscreteRoomEnvironment):
    """
    A single-room environment feating two routes from the starting state
    to the goal state --- a longer, wider path, and a shorter, thinner path.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(bridge_room, movement_penalty, goal_reward)


class CageRoom(DiscreteRoomEnvironment):
    """
    A single-room environment, with a small "cage" room within the larger room.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(cage_room, movement_penalty, goal_reward)


class EmptyRoom(DiscreteRoomEnvironment):
    """
    A single, empty room environment.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(empty_room, movement_penalty, goal_reward)


class SmallRooms(DiscreteRoomEnvironment):
    """
    A four-room environment comprised of a single large room with
    three smaller rooms above.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(small_rooms, movement_penalty, goal_reward)


class FourRooms(DiscreteRoomEnvironment):
    """
    A default four-rooms environment, as commonly seen in the HRL literature.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(four_rooms, movement_penalty, goal_reward)


class FourRoomsHoles(DiscreteRoomEnvironment):
    """
    A four-room environment, with a number of pillars blocking the way in one of the rooms.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(four_rooms_holes, movement_penalty, goal_reward)


class MazeRooms(DiscreteRoomEnvironment):
    """
    A maze-style environment made up of a number of inter-connected corridors.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(maze_rooms, movement_penalty, goal_reward)


class SpiralRoom(DiscreteRoomEnvironment):
    """
    An environment comprised of a single, spiral-shaped room.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(spiral_rooms, movement_penalty, goal_reward)


class ParrMaze(DiscreteRoomEnvironment):
    """
    The Maze gridworld introduced by Parr and Russell, 1998, to test HAMs.
    Contains ~3600 states.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(parr_maze, movement_penalty, goal_reward)


class ParrMiniMaze(DiscreteRoomEnvironment):
    """
    A smaller section of the Maze gridworld introduced by Parr and Russell, 1998, to test HAMs.
    Contains ~1800 states.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(parr_mini_maze, movement_penalty, goal_reward)


class RameshMaze(DiscreteRoomEnvironment):
    """
    One of the maze gridworlds used by Ramesh et al. 2019 to test Successor Options.
    Goal Reward: +1
    Movement Penalty: -0.01
    """

    def __init__(self, movement_penalty=-0.001, goal_reward=1):
        super().__init__(ramesh_maze, movement_penalty, goal_reward)
