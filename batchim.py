from yaml_functions import LANG

Batchims = [["이","가"],
            ["을","를"],
            ["은","는"],
            ["으로","로"]]

def 받침(word, *args):
    """
    -: 이/가 1: 을/를 2: 은/는 3: 으로/로
    """
    if LANG == "ko\\":
        if not args: #주격 조사가 기본
            with_Batchim, without_Batchim = Batchims[0]
        elif str(type(args[0])) == "<class 'str'>": # 커스텀 받침 설정, 문자열 둘을 주면
            with_Batchim, without_Batchim = args[0], args[1]
        else:
            with_Batchim, without_Batchim =  Batchims[args[0]]

        criteria = (ord(word[-1]) - 44032) % 28

        if criteria == 0: # 받침 없음
            return word + without_Batchim
        else:
            return word + with_Batchim

    else: return word

if __name__ == "__main__":
    print(받침("사람"))
    print(받침("사람",1))
    print(받침("사람",2))
    print(받침("사람 ","그는 신인가?","그는 누구인가?"))