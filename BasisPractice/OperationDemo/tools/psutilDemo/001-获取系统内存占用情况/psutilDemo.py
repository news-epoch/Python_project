import psutil

if __name__ == '__main__':
    mem = psutil.virtual_memory()
    # 系统总计内存 M
    all_mem = float(mem.total) / 1024 / 1024

    # 系统已经使用内存
    use_mem = float(mem.used) / 1024 / 1024

    # 系统空闲内存
    free_mem = float(mem.free) / 1024 / 1024

    print('系统总计内存:%d.3MB' % all_mem)
    print('系统已经使用内存:%d.3MB' % use_mem)
    print('系统空闲内存:%d.3MB' % free_mem)

    print("=====================")
    print(psutil.net_io_counters(pernic=True))

    # 查看所有进程的内存占用
    ## 查找所有进程
    print(psutil.pids())
    data = list()
    for i in psutil.pids():

        # '{: .2f}'.format(float(p.memory_full_info().uss) / 1024 / 1024 / 1024
        ## 获取进程相关信息
        p = psutil.Process(i)
        p_data = dict()
        if p.name().__contains__("chrome"):
            # print(i)
            p_data = {'name': p.name(), "use_mem": "{:.2f}G".format(float(p.memory_full_info().uss) / 1024 / 1024 / 1024)}
        print(p_data)
