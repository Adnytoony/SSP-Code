def hms_to_deg(hours, minutes, seconds):
    hms = (hours + minutes/60 + (seconds/3600))*(360/24)
    return hms
    # Converts an angle in (hours, minutes, seconds) to decimal degrees
    # Inputs: hours (int), minutes (int), and seconds (float) of the angle
    # Output: The angle in decimal degrees
print(hms_to_deg(10,20,30))

def dms_to_deg(is_pos, degrees, minutes, seconds):
    dms = degrees + minutes/60 + seconds/3600
    if is_pos == False:
       dms = -dms
    return dms
    # Converts an angle in (hours, minutes, seconds) to decimal degrees
    # Inputs:
    # - is_pos (bool): True if the angle is positive, False if it's negative
    # - degrees (int), minutes (int), and seconds (float) of the angle. Each of these must be positive.
    # Output: The angle in decimal degrees
print(dms_to_deg(False,10,20,30))

def main():
    return ("testing main")
    