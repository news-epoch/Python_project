
import concurrent.futures
from education_project import education

if __name__ == '__main__':
    education01 = ""

    # 开始登录准备
    while True:
        try:
            education01 = education()
            # education01.getLoginInfo(username="51302919980523555X", password="23555X", zkzh="010818443102")
            education01.getLoginInfo(username="510411199904011426", password="011426", zkzh="010818443102")
            break
        except Exception:
            print("访问失败")
            education01 = ""
            continue

    # 进行多线程登录
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 开启10个线程池
        futures = [executor.submit(education01.login) for _ in range(10)]

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()  # 获取任务的返回值
                if result is not None:
                    if result.__contains__('登录成功'):
                        for f in futures:
                            if f != future and not f.done():
                                f.cancel()
                        break
            except Exception as e:
                print(f"Exception: {e}")

    # # 容量查询
    # print("============================查询开始================================")
    # education01.searchPlace("成都")
    # print("============================查询结束================================")

    while True:
        print("============================报考开始================================")
        text = education01.subjectRegExam(km=["计算机网络原理", "信息资源管理", "管理经济学"], qx="高新区", sz="成都")
        print("============================报考结束================================\n\n")
        if text.__contains__("报考成功"):
            break