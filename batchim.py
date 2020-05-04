from yaml_functions import LANG

def Batchim(word, *args):
    """
    -: 이/가 1: 을/를 2: 은/는 3: 으로/로
    """
    if LANG == "ko\\":
        if not args: #주격 조사가 기본
            with_Batchim, without_Batchim = "이", "가"
        elif args[0] == 1: #목적격 조사, 뒤에 1을 붙이면
            with_Batchim, without_Batchim = "을", "를"
        elif args[0] == 2: #보조사, 뒤에 2을 붙이면
            with_Batchim, without_Batchim = "은", "는"
        elif args[0] == 3: #격조사, 뒤에 3을 붙이면
            with_Batchim, without_Batchim = "으로", "로"
        elif str(type(args[0])) == "<class 'str'>": # 커스텀 받침 설정, 문자열 둘을 주면
            with_Batchim, without_Batchim = args[0], args[1]

        criteria = (ord(word[-1]) - 44032) % 28
        if criteria == 0: #No Batchim!
            return word+without_Batchim
        else:
            return word+with_Batchim
    else: return word

if __name__ == "__main__":
    print(Batchim("사람"))
    print(Batchim("사람",1))
    print(Batchim("사람",2))
    print(Batchim("사람 ","그는 신인가?","그는 누구인가?"))