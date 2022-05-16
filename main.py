from multiprocessing import Process
from multiprocessing import Pool, cpu_count
from badminton import Badminton

TIME15TO17 = 6
TIME17TO19 = 8
TIME19TO21 = 10


def rob(booking_time):
    badminton = Badminton(booking_time)
    badminton.booking()


def main():
    print("CPU内核数:{}".format(cpu_count()))
    process_list = []
    time_to_booking = TIME17TO19
    with Pool(6) as p:
    # with Pool(cpu_count()) as p:
        p.map_async(rob, [time_to_booking,
                          time_to_booking + 6,
                          time_to_booking + 12,
                          time_to_booking + 18,
                          time_to_booking + 24,
                          time_to_booking + 30])
        p.close()
        p.join()

    # p1 = Process(target=booking, args=(time_to_booking,))
    # p1.start()
    # p2 = Process(target=booking, args=(time_to_booking + 6,))
    # p2.start()
    # p3 = Process(target=booking, args=(time_to_booking + 12,))
    # p3.start()
    # p4 = Process(target=booking, args=(time_to_booking + 18,))
    # p4.start()
    # p5 = Process(target=booking, args=(time_to_booking + 24,))
    # p5.start()
    # p6 = Process(target=booking, args=(time_to_booking + 30,))
    # p6.start()
    # process_list.append(p1)
    # process_list.append(p2)
    # process_list.append(p3)
    # process_list.append(p4)
    # process_list.append(p5)
    # process_list.append(p6)
    # for p in process_list:
    #     p.join()


if __name__ == "__main__":
    main()
