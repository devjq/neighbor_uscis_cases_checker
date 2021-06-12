from utils import get_status


def case(case_num, n_count=10):
    for i in range(case_num-n_count, case_num+n_count):
        case_num, d, form, status = get_status("MSC"+str(i))
        print(case_num, d, form, status)


if __name__ == "__main__":
    case(1991183376, 20)
