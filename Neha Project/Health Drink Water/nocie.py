# https://blog.finxter.com/how-to-make-a-beep-sound-in-python-linux-macos-win/

# import winsound

# # Set frequency to 2000 Hertz
# frequency = 1500

# # Set duration to 1500 milliseconds (1.5 seconds)
# duration = 1500

# # Make beep sound on Windows
# winsound.Beep(frequency, duration)


# ===================
# https://stackoverflow.com/questions/6537481/python-making-a-beep-noise

# import winsound
# frequency = 2500  # Set Frequency To 2500 Hertz
# duration = 1000  # Set Duration To 1000 ms == 1 second
# winsound.Beep(frequency, duration)

# Python 3.x
import winsound

frequency = 2000
duration = 1000
winsound.Beep(frequency, duration)