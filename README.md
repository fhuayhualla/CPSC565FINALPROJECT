# Building Traffic Models With Emergent Behavior Using Pygame

## Summary
This simulation models traffic behavior using passive, aggressive, and normal cars, each represented by different colors (green, red, and yellow respectively). It allows users to observe and interact with the dynamics of car behavior under various traffic conditions and driver temperaments in a highway like environment.

## What Is It?
This simulation explores traffic behavior within a highway environment, focusing on different driving styles such as aggressive, passive, and normal (mixed). The model simulates 3, 5, and 7 lane scenarios, aiming to build a dynamic system that mimics real-life traffic. The objective is to gain insights into traffic as an emergent system, where the collective outcomes of individual car behaviors, governed by simple rules, result in complex, realistic traffic patterns. This project tries to understand how traffic congestion potentially emerges from the interactions of different driver personalities and lane configurations.

## How It Works
The simulation uses the Pygame library in Python for building the model. Cars are represented as colored rectangles that move across the screen, simulating a road environment. The quantity of cars that appear in the simulation at any given time depends on their spawning locations and is subject to certain constraints (such as how far each car should be from each other), however world use space is maximized. Each car's behavior is influenced by its speed, the proximity of other cars, and its tendency to change lanes. Aggressive drivers tend to change lanes more frequently and maintain less distance from the car in front of them as well as have a more rapid acceleration characteristic, while passive drivers do the opposite, and normal drivers have a more balanced approached.

## How to Use It
To run the simulation, ensure Python and Pygame are installed, then simply just run the main file. The interface includes buttons such as "Setup" to prepare the initial state, "Go" to start the simulation, and controls for setting preferences like the number of lanes or the distribution of car types or the Schelling effect.

- **Setup Button**: Initializes or resets the simulation environment.
- **Go Button**: Starts or pauses the simulation.
- **Car Preferences**: Allows selection of a preference for more cars of a specific color (driver type).
- **Schelling Button**: Toggles the Schelling mode, which sorts cars based on their speed to simulate sorting in traffic lanes, faster cars go on the left lane (top of the world), slower cars go on the right lane (bottom of the world). 
- **Lane Button**: Adjusts the number of lanes in the simulation. Select from options such as 3, 5, or 7 lanes to see how different lane configurations impact traffic flow and car interactions.

## Things to Notice
Observe how different car behaviors affect traffic flow and lane changes. Notice patterns such as clustering of similar car types when using Schelling and how the model's various features affect overall road speeds.

## Things to Try
- Adjust the number of lanes to see how it influences traffic congestion.
- Change the proportion of aggressive, normal, and passive cars to see how each type affects traffic dynamics.
- Use the Schelling toggle to see how sorting by speed influences traffic flow.

## Extending the Model
Consider adding features such as:
- Other types of road infrastructures (i.e. suburban road).
- Environmental effects like weather conditions that could affect driving behavior.

## Related Models

**Segregation Model (NetLogo)**:

-   **Overview**: Inspired by Thomas Schelling's theories, this model features agents who prefer neighbors of similar characteristics.
-   **Application in Schelling Feature**: The Schelling feature in the simulation adapts by grouping cars in terms of their speed, in this case more aggressive cars staying on the left lane, and more passive cars on the right lane.

## Credits and References
This model was developed using Pygame, a Python library for making multimedia applications. Refer to the Pygame documentation for more details on how to utilize and extend this framework for other simulations.
