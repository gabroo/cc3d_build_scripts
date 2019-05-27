from datetime import date


def timestamp_revision_number():
    today = date.today()
    revision_number = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)
    return revision_number


def version_str_to_tuple(version_str):
    """
    parsers version string into tuple (major, minor, build, installer_build)
    :param version_str: {str} version string - format is int.int.int.int
    :return: {tuple} (major, minor, build, windows installer)
    """
    nvc = 4  # number of version components
    # making sure version has entries numbers separated by a comma
    version_str_list = version_str.split('.')
    version_int_list = list(map(lambda x: int(x), version_str_list))

    if len(version_int_list) < nvc:
        print ('Incomplete version information provided. will set missing subversion numbers to 0')
        version_int_list += [0] * (nvc - len(version_int_list))
    elif len(version_int_list) > nvc:
        print ('Too many version components. Will use first {}'.format(nvc))
        version_int_list = version_int_list[:nvc]
    print ('Version is', version_tuple_to_str(version_int_list))

    return tuple(version_int_list)


def version_tuple_to_str(version_component_sequence, number_of_version_components=4):
    """
    Converts version tuple to string
    :param version_component_sequence: {tuple or list of ints}
    :param number_of_version_components: {int} number of version components to be displayed int he version string
    :return: {str}
    """
    return '.'.join(list(map(lambda x: str(x), version_component_sequence[:number_of_version_components])))


def printRuntime(time_interval):
    time_interval = int(time_interval)
    hours = time_interval / (3600 * 1000)
    minutes_interval = time_interval % (3600 * 1000)
    minutes = minutes_interval / (60 * 1000)
    seconds_interval = minutes_interval % (60 * 1000)
    seconds = seconds_interval / (1000)
    miliseconds = seconds_interval % (1000)

    print ("Build RUNTIME ",)
    if hours > 1.0:
        print (hours, " h : ", minutes, " m : ", seconds, " s : ", miliseconds, " ms")
    elif minutes > 1.0:
        print (minutes, " m : ", seconds, " s : ", miliseconds, " ms")
    elif seconds > 1.0:
        print (seconds, " s : ", miliseconds, " ms")
    else:
        print(miliseconds, " ms")
        print ("EQUIVALENT OF      %0.3f seconds" % (time_interval / 1000))


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

# if __name__ == '__main__':
#     print version_str_to_tuple('3.7')
#     print  version_str_to_tuple('3.7.6')
#     print  version_str_to_tuple('3.7.6.1')
#     print  version_str_to_tuple('3.7.6.2.12')
#     print  version_str_to_tuple('3')
#
#     # print version_str_to_tuple('3.a')
