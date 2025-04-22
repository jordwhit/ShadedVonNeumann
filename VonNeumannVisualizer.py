import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

def draw_von_neumann(n, center=(0, 0), radius=1, ax=None, depth=0, property_func=None, 
                     parent_color='white', dark_shade='darkgray', light_shade='lightgray', unshaded='white'):
    """
    Recursively draw Von Neumann natural number construction with conditional shading.
    n: natural number to visualize
    center: (x, y) coordinates for the circle's center
    radius: radius of the current circle
    ax: matplotlib axes object
    depth: recursion depth for hierarchy
    property_func: function that takes a number and returns True/False for shading
    parent_color: color of the parent circle
    dark_shade: color for primary shaded circles
    light_shade: color for nested shaded circles
    unshaded: color for unshaded circles
    """
    if ax is None:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

    # Determine shading based on property
    shade = property_func(n) if property_func else False
    if shade:
        # If property is true, use opposite shade of parent
        if parent_color == unshaded:
            facecolor = dark_shade
        elif parent_color == dark_shade:
            facecolor = light_shade
        elif parent_color == light_shade:
            facecolor = dark_shade
    else:
        facecolor = unshaded

    # Draw the current set's circle
    circle = Circle(center, radius, fill=True, facecolor=facecolor, edgecolor='black')
    ax.add_patch(circle)

    if n == 0:
        return  # Empty set, no inner circles

    # Determine inner circle size to maximize space while maintaining buffer
    inner_count = n
    buffer = radius / 12  # Buffer between sibling circles

    if inner_count == 1:
        inner_radius = 0.5 * radius  # Smaller for single inner circle
        inner_distance = 0  # Centered
    elif inner_count == 2:
        inner_radius = (radius - 1.5 * buffer) / 2
        inner_distance = inner_radius + buffer / 2
    else:
        s = np.sin(np.pi / inner_count)
        inner_radius = (radius - buffer) * s / (1 + s)
        inner_radius = max(inner_radius, 0)  # Ensure non-negative
        inner_distance = radius - inner_radius - buffer

    # Position inner circles
    for i in range(n):
        if inner_count == 1:
            inner_center = center
        elif inner_count == 2:
            offset = inner_distance * (-1 if i == 0 else 1)
            inner_center = (center[0] + offset, center[1])
        else:
            angle = 2 * np.pi * i / inner_count
            inner_center = (
                center[0] + inner_distance * np.cos(angle),
                center[1] + inner_distance * np.sin(angle)
            )
        draw_von_neumann(
            i, center=inner_center, radius=inner_radius, ax=ax, depth=depth+1,
            property_func=property_func, parent_color=facecolor,
            dark_shade=dark_shade, light_shade=light_shade, unshaded=unshaded
        )

    if depth == 0:
        ax.set_xlim(center[0] - radius * 1.2, center[0] + radius * 1.2)
        ax.set_ylim(center[1] - radius * 1.2, center[1] + radius * 1.2)
        plt.savefig(f'von_neumann_n{n}.png')
        plt.close()

def visualize_von_neumann(n, property_func=None, dark_shade='darkgray', light_shade='lightgray', unshaded='white'):
    """
    Generate visualization for Von Neumann natural number n with conditional shading.
    n: natural number to visualize
    property_func: function that takes a number and returns True/False for shading
    dark_shade: color for primary shaded circles
    light_shade: color for nested shaded circles
    unshaded: color for unshaded circles
    """
    if property_func is None:
        property_func = lambda x: False  # Default: no shading
    draw_von_neumann(n, property_func=property_func, dark_shade=dark_shade, light_shade=light_shade, unshaded=unshaded)
    print(f"Visualization for {n} saved as von_neumann_n{n}.png")

def custom_property(n):
    """Return True if n has the given property, False otherwise."""
    
    def is_prime(x):
        return x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))
    
    def is_even(x):
        return x % 2 == 0

    return (is_prime(n) or is_even(n)) and n!=0  # Example property: prime or even but not zero

number_to_visualize = 7 # the number that will be visualized
property_func = custom_property # The property we are checking for shading
primary_shade = 'darkblue'  # Primary shade color
secondary_shade = 'lightblue'  # Nested shade color
unshaded = 'white' 
visualize_von_neumann(number_to_visualize, property_func=property_func, dark_shade=primary_shade, light_shade=secondary_shade, unshaded=unshaded)