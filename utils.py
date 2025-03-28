import subprocess


def get_connected_device():
    """ Get current connected device(Android / iOS) and its UUID """

    # Check Android
    try:
        adb_output = subprocess.check_output(["adb", "devices"], encoding="utf-8").strip().split("\n")[1:]
        android_devices = [line.split("\t")[0] for line in adb_output if "device" in line]
        if android_devices:
            print(f"Detected Device: {android_devices[0]}")
            return "Android", android_devices[0]
    except Exception as e:
        print(f"Android check Error: {e}")

    # Check iOS
    try:
        ios_output = subprocess.check_output(["idevice_id", "-l"], encoding="utf-8").strip().split("\n")
        if ios_output and ios_output[0]:
            print(f"Detected Device: {ios_output[0]}")
            return "iOS", ios_output[0]
    except Exception as e:
        print(f"iOS check error : {e}")

    return None, None