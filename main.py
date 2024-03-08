from tkinter import Tk, Canvas, ttk, IntVar, Frame
from ttkbootstrap import Style
import numpy as np
import random
import time


class SortingVisualizer:
    def __init__(self, master):
        # control panel
        self.master = master
        self.master.title("Sorting Algorithm Visualizer")
        self.master.resizable(width=0, height=0)

        self.style = Style(theme="darkly")

        self.control_frame = Frame(master)
        self.control_frame.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=5)

        self.array_size_var = IntVar(value=10)
        self.array_size_slider = ttk.Scale(self.control_frame, from_=6, to=500, variable=self.array_size_var,
                                           command=self.on_slider_change)  # Note: Not passing 'value' here

        self.array_size_slider.grid(row=1, column=0, sticky="we", padx=5, pady=5)
        # Initialize the label with the initial value of the slider
        initial_value = self.array_size_var.get()
        self.array_size_label = ttk.Label(self.control_frame, text=f"Elements: {initial_value}")
        self.array_size_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.comparison_count = 0
        self.swap_count = 0

        self.radix_operations = 0

        self.bubble_sort_button = ttk.Button(self.control_frame, text="Bubble Sort", command=self.bubble_sort)
        self.bubble_sort_button.grid(row=0, column=2, padx=5, pady=5)

        self.insertion_sort_button = ttk.Button(self.control_frame, text="Insertion Sort", command=self.insertion_sort)
        self.insertion_sort_button.grid(row=0, column=3, padx=5, pady=5)

        self.selection_sort_button = ttk.Button(self.control_frame, text="Selection Sort", command=self.selection_sort)
        self.selection_sort_button.grid(row=0, column=4, padx=5, pady=5)

        self.merge_sort_button = ttk.Button(self.control_frame, text="Merge Sort", command=self.merge_sort)
        self.merge_sort_button.grid(row=0, column=5, padx=5, pady=5)  # Ensure correct positioning

        self.radix_sort_button = ttk.Button(self.control_frame, text="Radix Sort", command=self.radix_sort)
        self.radix_sort_button.grid(row=0, column=6, padx=5, pady=5)

        self.pancake_sort_button = ttk.Button(self.control_frame, text="Pancake Sort", command=self.pancake_sort)
        self.pancake_sort_button.grid(row=0, column=7, padx=5, pady=5)  # Adjust grid position as needed

        self.merge_label = ttk.Label(self.control_frame, text="Merges: 0")
        self.merge_label.grid(row=1, column=5, padx=4, pady=5)  # Adjust grid positioning as needed

        # Initialize a GUI label for radix sort operations if you haven't already
        self.radix_operations_label = ttk.Label(self.control_frame, text="Radix Ops: 0")
        self.radix_operations_label.grid(row=1, column=6, padx=5, pady=5)  # Adjust position as needed

        self.comparison_label = ttk.Label(self.control_frame, text="Comparisons: 0")
        self.comparison_label.grid(row=1, column=11, padx=5, pady=5)

        self.swap_label = ttk.Label(self.control_frame, text="Swaps: 0")
        self.swap_label.grid(row=0, column=11, padx=5, pady=5)

        # Create the speed control slider
        # Create a label for the speed control slider value
        self.speed_value_label = ttk.Label(self.control_frame, text="Delay: 50 ms")
        self.speed_value_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)



        # Function to update the speed value label
        def update_speed_label(event=None):
            self.speed_value_label.config(text=f"Delay: {int(self.speed_control.get())} ms")

        # Create the speed control slider with the command to update the label
        self.speed_control = ttk.Scale(self.control_frame, from_=1, to=300, orient="horizontal",
                                       command=update_speed_label)
        self.speed_control.grid(row=3, column=0, columnspan=2, sticky="we", padx=5, pady=5)
        self.speed_control.set(50)  # Set default speed
        update_speed_label()  # Initialize label text

        self.canvas = Canvas(master, width=800, height=400, bg="black")
        self.canvas.grid(row=1, column=0, columnspan=6, padx=5, pady=10)

        self.array_size_var.trace("w", self.on_slider_change)

        self.update_array_size_label()


    def update_array_size_label(self, event=None):
         # Get the current value of the slider
         current_value = self.array_size_var.get()
        # Update the label to show the current number of elements
         self.array_size_label.config(text=f"Elements: {current_value}")
        # Call the update function initially to set the label correctly
    def display_bars(self, N, a, highlight=None):
        """
        Display bars on the canvas with optional highlighting.
        :param N: Number of bars.
        :param a: Array of bar heights.
        :param highlight: A list of tuples indicating which bars to highlight and in what color.
        """
        self.canvas.delete("all")
        bar_width = (800 - (N + 1) * 5) / N
        gap = 5

        for i in range(N):
            color = "dodgerblue"
            if highlight and i in [x[0] for x in highlight]:
                color = [x[1] for x in highlight if x[0] == i][0]

            x0 = i * (bar_width + gap) + gap
            y0 = 400 - a[i]
            x1 = x0 + bar_width
            y1 = 400
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def bubble_sort(self):
        self.merge_count = 0
        self.merge_label.config(text="Merges: 0")
        N = self.array_size_var.get()
        a = np.linspace(5, 395, N)
        np.random.shuffle(a)

        self.comparison_count = 0
        self.swap_count = 0

        for i in range(N - 1):
            for j in range(0, N - i - 1):
                self.comparison_count += 1
                self.display_bars(N, a, highlight=[(j, "green"), (j + 1, "green")])
                # Update the comparison label after each comparison
                self.comparison_label.config(text=f"Comparisons: {self.comparison_count}")

                delay = int(self.speed_control.get())
                self.canvas.after(delay)  # Adjusts the visualization speed based on the slider's value

                self.canvas.update_idletasks()
                if a[j] > a[j + 1]:
                    self.swap_count += 1
                    a[j], a[j + 1] = a[j + 1], a[j]
                    self.display_bars(N, a, highlight=[(j, "red"), (j + 1, "red")])
                    # Update the swap label after each swap
                    self.swap_label.config(text=f"Swaps: {self.swap_count}")

                    delay = int(self.speed_control.get())
                    self.canvas.after(delay)  # Adjusts the visualization speed based on the slider's value

                    self.canvas.update_idletasks()

        self.display_bars(N, a)  # Final display to show the sorted array

    def insertion_sort(self):
        self.merge_count = 0
        self.merge_label.config(text="Merges: 0")
        N = self.array_size_var.get()
        a = np.linspace(5, 395, N)
        np.random.shuffle(a)

        self.comparison_count = 0
        self.swap_count = 0

        for i in range(1, N):
            key = a[i]
            j = i - 1

            while j >= 0:
                self.comparison_count += 1
                # Update the comparison count label right after incrementing
                self.comparison_label.config(text=f"Comparisons: {self.comparison_count}")

                if a[j] > key:
                    a[j + 1] = a[j]
                    self.swap_count += 1

                    # Update the swap count label right after incrementing
                    self.swap_label.config(text=f"Swaps: {self.swap_count}")

                    self.display_bars(N, a, highlight=[(j + 1, "red"), (i, "green")])
                    delay = int(self.speed_control.get())
                    self.canvas.after(delay)  # Adjusts the visualization speed based on the slider's value

                    self.canvas.update_idletasks()
                    j = j - 1
                else:
                    # Still update the GUI to highlight where the comparison happens but no swap is needed
                    self.display_bars(N, a, highlight=[(j, "yellow"), (i, "green")])
                    delay = int(self.speed_control.get())
                    self.canvas.after(delay)  # Adjusts the visualization speed based on the slider's value

                    self.canvas.update_idletasks()
                    break  # If no shift is required, exit the while loop

            a[j + 1] = key
            # Display the array with the key in its new position
            self.display_bars(N, a, highlight=[(j + 1, "green")])
            delay = int(self.speed_control.get())
            self.canvas.after(delay)  # Adjusts the visualization speed based on the slider's value

            self.canvas.update_idletasks()

        # Final display to show the sorted array
        self.display_bars(N, a)

    def selection_sort(self):
        self.merge_count = 0
        self.merge_label.config(text="Merges: 0")
        N = self.array_size_var.get()
        a = np.linspace(5, 395, N)
        np.random.shuffle(a)

        self.comparison_count = 0
        self.swap_count = 0

        for i in range(N):
            min_idx = i
            for j in range(i + 1, N):
                self.comparison_count += 1
                # Highlight the current minimum and the element being compared
                self.display_bars(N, a, highlight=[(min_idx, "red"), (j, "green")])
                # Update the comparison count after each comparison
                self.comparison_label.config(text=f"Comparisons: {self.comparison_count}")
                delay = int(self.speed_control.get())
                self.canvas.after(delay)  # Adjusts the visualization speed based on the slider's value

                self.canvas.update_idletasks()

                if a[min_idx] > a[j]:
                    min_idx = j

            # Swapping the found minimum element with the first element if needed
            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]
                self.swap_count += 1
                # Highlight the swap action
                self.display_bars(N, a, highlight=[(i, "green"), (min_idx, "red")])
                # Update the swap count after each swap
                self.swap_label.config(text=f"Swaps: {self.swap_count}")
                delay = int(self.speed_control.get())
                self.canvas.after(delay)  # Adjusts the visualization speed based on the slider's value

                self.canvas.update_idletasks()

        # One final display to show the sorted array without specific highlights
        self.display_bars(N, a)

    def merge_sort(self, a=None, start=0, end=None, level=0):

        if a is None:
            a = np.linspace(5, 395, self.array_size_var.get())
            np.random.shuffle(a)
            self.comparison_count = 0
            self.merge_count = 0  # Using merge_count instead of swap_count for clarity
            end = len(a) - 1

        if start < end:
            mid = (start + end) // 2
            self.merge_sort(a, start, mid, level + 1)
            self.merge_sort(a, mid + 1, end, level + 1)
            self.merge(a, start, mid, end)
            # Example snippet from within your merge_sort method
            #self.merge_label.config(text=f"Merges: {self.merge_count}")

            # Only update the GUI at the top level of recursion
            if level == 0:
                self.display_bars(len(a), a)
                self.comparison_label.config(text=f"Comparisons: {self.comparison_count}")
                self.merge_label.config(text=f"Merges: {self.merge_count}")

    def merge(self, a, start, mid, end):
        left = a[start:mid + 1].copy()
        right = a[mid + 1:end + 1].copy()
        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            self.comparison_count += 1
            # Update the comparison count in real-time
            self.comparison_label.config(text=f"Comparisons: {self.comparison_count}")

            if left[i] < right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            k += 1
            # Optionally, delay for visualization
            self.canvas.after(int(self.speed_control.get()))
            self.display_bars(len(a), a, highlight=[(k - 1, "green")])
            self.canvas.update_idletasks()

        # Handle remaining elements
        while i < len(left) or j < len(right):
            self.merge_count += 1  # Consider completion of this action as part of the merge operation
            if i < len(left):
                a[k] = left[i]
                i += 1
            else:  # Implicitly means j < len(right)
                a[k] = right[j]
                j += 1
            k += 1
            # Optionally, delay for visualization
            self.canvas.after(int(self.speed_control.get()))
            # Update the GUI here as well to reflect the ongoing merge count during the operation
            self.merge_label.config(text=f"Merges: {self.merge_count}")
            self.display_bars(len(a), a)
            self.canvas.update_idletasks()

        # Note: If the merge_count is meant to reflect each merge action's completion,
        # consider incrementing it once per merge call rather than in the loop.

    def counting_sort_for_radix(self, array, exp):
        n = len(array)
        output = [0] * n
        count = [0] * 10

        # Increment radix operations for each digit processing
        for i in range(n):
            index = int(array[i] // exp) % 10
            count[index] += 1
            self.radix_operations += 1
            self.radix_operations_label.config(text=f"Radix Ops: {self.radix_operations}")
            self.canvas.update_idletasks()

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = int(array[i] // exp) % 10
            output[count[index] - 1] = array[i]
            count[index] -= 1
            i -= 1

        for i in range(len(array)):
            array[i] = output[i]
            self.display_bars(n, array, highlight=[(i, "red")])
            delay = int(self.speed_control.get())
            self.canvas.after(delay)
            self.canvas.update_idletasks()

    def radix_sort(self):
        self.comparison_count = 0
        self.swap_count = 0
        self.radix_operations = 0  # Reset the radix operations counter
        self.comparison_label.config(text="Comparisons: 0")
        self.swap_label.config(text="Swaps: 0")
        self.radix_operations_label.config(text="Radix Ops: 0")

        N = self.array_size_var.get()
        a = np.linspace(5, 395, N, dtype=int)
        np.random.shuffle(a)
        self.display_bars(N, a)

        max_num = max(a)
        exp = 1
        while max_num // exp > 0:
            self.counting_sort_for_radix(a, exp)
            exp *= 10
            self.display_bars(N, a)
            self.canvas.update_idletasks()

    def flip(self, arr, k):
        left = 0
        while left < k:
            arr[left], arr[k] = arr[k], arr[left]
            left += 1
            k -= 1
            # Visualization updates for each swap
            self.swap_count += 1
            self.swap_label.config(text=f"Swaps: {self.swap_count}")
            # Highlight the flip operation
            self.display_bars(len(arr), arr, highlight=[(left, "red"), (k, "red")])
            delay = int(self.speed_control.get())
            self.canvas.after(delay)
            self.canvas.update_idletasks()

    def max_index(self, arr, n):
        index = 0
        for i in range(1, n):
            # Highlight the comparison
            self.comparison_count += 1
            self.display_bars(len(arr), arr, highlight=[(index, "green"), (i, "green")])
            delay = int(self.speed_control.get())
            self.canvas.after(delay)
            self.canvas.update_idletasks()

            if arr[i] > arr[index]:
                index = i
        # Ensure the final state is visualized before returning
        self.comparison_label.config(text=f"Comparisons: {self.comparison_count}")
        return index

    def pancake_sort(self):
        self.comparison_count = 0
        self.swap_count = 0
        # Reset counters and labels
        self.comparison_label.config(text="Comparisons: 0")
        self.swap_label.config(text="Swaps: 0")

        N = self.array_size_var.get()
        arr = np.linspace(5, 395, N, dtype=int)
        np.random.shuffle(arr)
        self.display_bars(N, arr)

        n = N
        while n > 1:
            maxdex = self.max_index(arr, n)
            if maxdex != n - 1:
                self.flip(arr, maxdex)
                self.flip(arr, n - 1)
            n -= 1

        # Final display to show the sorted array
        self.display_bars(N, arr)

    def on_slider_change(self, *args):
        # Directly retrieve the current value of the slider from the bound Tkinter variable
        new_value = self.array_size_var.get()

        # Update the label to reflect the current number of elements
        self.array_size_label.config(text=f"Elements: {new_value}")

        # Generate a new array of the specified size and display the bars
        heights = np.linspace(5, 395, new_value)
        np.random.shuffle(heights)
        self.display_bars(new_value, heights)

    # Make sure to adjust the rest of your class definition and methods as needed...
    def on_shuffle_click(self):
        """
        Callback for the shuffle button click.
        """
        N = self.array_size_var.get()
        self.shuffle_bars(N)

    def exit_program(self):
        self.master.quit()


if __name__ == '__main__':
    root = Tk()
    app = SortingVisualizer(root)
    root.mainloop()
