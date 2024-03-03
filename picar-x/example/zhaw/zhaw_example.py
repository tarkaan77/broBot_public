from robot_hat import TTS


if __name__ == "__main__":
    
    words = ["aaaaaaaaaa","mario kitanovksi, your time will come to an end"]
    tts_robot = TTS()
    
    for i in words:
        print(i)
        tts_robot.say(i)
