def key():
    answer_key = ['B','E','B','D','B']
    return answer_key


def map():
    ans_dict = {}
    ans_dict['A'] = 1
    ans_dict['B'] = 2
    ans_dict['C'] = 3
    ans_dict['D'] = 4
    ans_dict['E'] = 5
    return ans_dict

def get_mapped_answers():
    answer_key = key()
    ans_dict = map()
    get_mapped_answers = []
    get_mapped_answers = [ans_dict[ans_key] for ans_key in answer_key]
    return get_mapped_answers
