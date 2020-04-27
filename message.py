class Message:
    def __init__(self, init_log = None):
        # 구성: [메세지][횟수]
        self.logs = []
        self.old_logs = []
        if init_log:
            self.add_log(init_log)
    
    def log(self, message, amount=1):
        # 로그가 비어 있으면 그냥 추가
        if not len(self.logs):
            self.logs.append([message,amount])
        # 이 로그가 마지막 로그랑 같으면 그 로그 수를 늘림
        else:
            if self.logs[len(self.logs)-1][0] == message:
                self.logs[len(self.logs)-1][1] += 1
            else:
                self.logs.append([message,amount])
            
    def cout(self):
        if self.logs:
            for log in self.logs:
                if not log[1] == 1:
                    print (F"{log[0]}. x {log[1]}")
                else:
                    print (F"{log[0]}.")
        self.old_logs.extend(self.logs)
        self.logs.clear()
        
if __name__ == '__main__':
    test = Message()
    test.log("This is a test")
    test.log("This is a test")
    test.log("This is a test")
    test.log("Wonder why light is not doing well")
    test.cout()
    test.log("This is a test")
    test.cout()
    print(test.old_logs)
    
    """
    A = [[1,2],[3,4]]
    print (A[0][0])
    """