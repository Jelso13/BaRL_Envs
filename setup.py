import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="simpleenvs",
    version="0.3.0",
    author="Joshua Evans",
    author_email="jbe25@bath.ac.uk",
    description="A package providing implementations of sequential decision problems using the SimpleOptions framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ueva/BaRL-Envs",
    packages=setuptools.find_packages(exclude=("test")),
    package_dir={"simpleenvs": "simpleenvs"},
    data_files=[
        (
            "discrete_room_files",
            [
                "simpleenvs/envs/discrete_rooms/data/two_rooms.txt",
                "simpleenvs/envs/discrete_rooms/data/six_rooms.txt",
                "simpleenvs/envs/discrete_rooms/data/nine_rooms.txt",
                "simpleenvs/envs/discrete_rooms/data/xu_four_rooms.txt",
                "simpleenvs/envs/discrete_rooms/data/bridge_room.txt",
                "simpleenvs/envs/discrete_rooms/data/cage_room.txt",
                "simpleenvs/envs/discrete_rooms/data/empty_room.txt",
                "simpleenvs/envs/discrete_rooms/data/small_rooms.txt",
                "simpleenvs/envs/discrete_rooms/data/four_rooms.txt",
                "simpleenvs/envs/discrete_rooms/data/four_rooms_holes.txt",
                "simpleenvs/envs/discrete_rooms/data/maze_rooms.txt",
                "simpleenvs/envs/discrete_rooms/data/spiral_room.txt",
                "simpleenvs/envs/discrete_rooms/data/parr_maze.txt",
                "simpleenvs/envs/discrete_rooms/data/parr_mini_maze.txt",
                "simpleenvs/envs/discrete_rooms/data/ramesh_maze.txt",
            ],
        ),
        (
            "continuous_room_files",
            [
                "simpleenvs/envs/continuous_rooms/data/xu_four_rooms.txt",
                "simpleenvs/envs/continuous_rooms/data/empty_rooms.txt",
            ],
        ),
        (
            "pacman_files",
            ["simpleenvs/envs/grid_pacman/data/four_room.txt"],
        ),
        (
            "taxi_renderer_resources",
            [
                "simpleenvs/renderers/taxi_renderer_resources/taxi_full.png",
                "simpleenvs/renderers/taxi_renderer_resources/taxi_empty.png",
                "simpleenvs/renderers/taxi_renderer_resources/passenger.png",
                "simpleenvs/renderers/taxi_renderer_resources/goal_flag.png",
            ],
        ),
    ],
    install_requires=[
        "simpleoptions",
        "importlib_resources",
        "importlib_metadata",
        "numpy",
        "networkx",
        "pygame",
        "gymnasium",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
)
