import ezdxf

def draw_steel_bars_2d(filename, diameter, length, num_bars=1, spacing=0.1, view="side"):
    """
    Create a DWG file with steel bars drawn in 2D.

    Parameters:
        filename (str): Name of the output DWG file.
        diameter (float): Diameter of the steel bars (in meters).
        length (float): Length of the steel bars (in meters).
        num_bars (int): Number of bars to draw.
        spacing (float): Spacing between bars (in meters).
        view (str): View type: "side" for a side view, "section" for a cross-section view.
    """
    # Create a new DXF document
    doc = ezdxf.new()
    msp = doc.modelspace()

    if view == "side":
        # Draw side view: lines representing the bars
        for i in range(num_bars):
            x_offset = i * spacing
            msp.add_line((x_offset, 0), (x_offset, length))
    elif view == "section":
        # Draw cross-section view: circles representing the bars
        for i in range(num_bars):
            x_offset = i * spacing
            msp.add_circle(center=(x_offset, 0), radius=diameter / 2)

    # Save the file
    doc.saveas(filename)
    print(f"Drawing saved as {filename}")

# Example usage
draw_steel_bars_2d(
    filename="steel_bars.dwg",
    diameter=0.02,  # Diameter in meters
    length=2.0,     # Length in meters
    num_bars=5,     # Number of bars
    spacing=0.05,   # Spacing between bars in meters
    view="side"     # Choose "side" or "section"
)

