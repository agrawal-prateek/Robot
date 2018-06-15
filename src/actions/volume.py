def increase():
    import alsaaudio
    from os import system
    m = alsaaudio.Mixer('PCM')
    if m.getvolume()[0] < 90:
        m.setvolume(m.getvolume()[0] + 10)
        system("mpg123 /home/pi/Robot/src/audio/okayVolumeIncreased.mp3")
    else:
        system("mpg123 /home/pi/Robot/src/audio/volumeIsAlreadySetToFull.mp3")


def decrease():
    import alsaaudio
    from os import system
    m = alsaaudio.Mixer('PCM')
    if m.getvolume()[0] > 10:
        m.setvolume(m.getvolume()[0] - 10)
        system("mpg123 /home/pi/Robot/src/audio/okayVolumeDecreased.mp3")
    else:
        system("mpg123 /home/pi/Robot/src/audio/volumeIsAlreadySetToMute.mp3")