import mido
from time import sleep, time
from bhaptics.haptic_player import HapticPlayer

# List of oct and the actuators (replace with your actual mapping)
note_to_actuator = {
    #0
    "oct1" : {
        24: [1,2,3,7], 26: [1,2,7], 28: [1,2,3,6], 29: [1,2,3,6,7], 31: [1,2,6,7], 33: [1,3,6], 35: [1,3,6,7]
    },
    #2
    "oct2": {
        36: [1,5,2,3,7], 38: [1,5,2,7], 40: [1,5,2,3,6], 41: [1,5,2,3,6,7], 43: [1,5,2,6,7], 45: [1,5,3,6], 47: [1,5,3,6,7]
    },
    #3
    "oct3" : {
        48: [1,5,9,2,3,7], 50: [1,5,9,2,7], 52: [1,5,9,2,3,6], 53: [1,5,9,2,3,6,7], 55: [1,5,9,2,6,7], 57: [1,5,9,3,6], 59: [1,5,9,3,6,7]
    },
    #4
    "oct4" : {
        60: [5,2,3,7], 62: [5,2,7], 64: [5,2,3,6], 65: [5,2,3,6,7], 67: [5,2,6,7], 69: [5,3,6], 71: [5,3,6,7]
    },
    #5
    "oct5" : {
        72: [1,9,2,3,7], 74: [1,9,2,7], 76: [1,9,2,3,6], 77: [1,9,2,3,6,7], 79: [1,9,2,6,7], 81: [1,9,3,6], 83: [1,9,3,6,7]
    },
    #6
    "oct6" : {
        84: [5,9,2,3,7], 86: [5,9,2,7], 88: [5,9,2,3,6], 89: [5,9,2,3,6,7], 91: [5,9,2,6,7], 93: [5,9,3,6], 95: [5,9,3,6,7]
    },
    #7
    "oct7" : {
        96: [9,2,3,7], 98: [9,2,7], 100: [9,2,3,6], 101: [9,2,3,6,7], 103: [9,2,6,7], 105: [9,3,6], 107: [9,3,6,7]
    }
}



# Making a dictionary to track note on times
note_on_times = {}

# Create a HapticPlayer instance
player = HapticPlayer()

# Function to send haptic feedback
#def send_haptic_feedback(note, intensity, duration):
def send_haptic_feedback(note, intensity, duration):
    if any(note in note_to_actuator[f"oct{no_octave}"] for no_octave in range(1,8)):
        no_octave = note // 12 - 1 
        actuators = note_to_actuator[f"oct{no_octave}"][note]
        dot_points = [{"Index": actuator, "Intensity": intensity} for actuator in actuators]
        dot_frame = {
            "Position": "VestBack",
            "DotPoints": dot_points,
           # "DurationMillis": duration
           "DurationMillis": 1000
        }
        player.submit("dotPoint", dot_frame)

# Function to handle incoming MIDI messages
def handle_midi_message(message):
    if message.type == 'note_on':
        note = message.note
        velocity = message.velocity
        print(f"Note On: {note}, Velocity: {velocity}")

        # Convert velocity to intensity (0-100 scale)
        intensity = int((velocity / 127.0) * 100)

        # Store note on time for duration calculation
        note_on_times[note] = time()

        # Send haptic feedback
        send_haptic_feedback(note, intensity, 0)  # Use 0 for duration initially

    elif message.type == 'note_off':
        note = message.note
        if note in note_on_times:
            velocity = message.velocity
            duration = int((time() - note_on_times[note]) * 1000)  # Calculate duration in milliseconds
            del note_on_times[note]  # Remove note from tracking after processing

            # Send haptic feedback with calculated duration
            send_haptic_feedback(note, 0, duration)  # Use 0 for intensity for note off

def main():
    # Use the defined MIDI port name (replace with your actual port name)
    midi_port_name = 'LoopBe Internal MIDI 0'

    # Open the MIDI input port
    with mido.open_input(midi_port_name) as port:
        print(f"Listening on {midi_port_name}...")
        for message in port:
            handle_midi_message(message)

if __name__ == "__main__":
    main()