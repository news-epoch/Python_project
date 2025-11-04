import datetime
import logging
import traceback

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import easytrader
import time

from orm import trader_info, relation_trader
import tools
from easytrader import refresh_strategies

logger = logging.getLogger('spider')
logger.setLevel(logging.INFO)
# 输出到文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setFormatter(formatter)
# 输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# 添加处理器到日志器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
class autotrade:
    def __init__(self):
        self.application = tools.读取配置文件()
        self.session = tools.创建数据库连接并且返回操作字段(application.get('db').get('url'))
        self.user = easytrader.use(self.application['easytrader']['client']['type'])
        self.user.connect(self.application['easytrader']['client']['path'])  # 替换为你的同花顺路径
        # 无法通过默认方法输入文本，开启type_keys绕过
        user.enable_type_keys_for_editor()
        user.refresh_strategy = refresh_strategies.Toolbar(refresh_btn_index=4)
    def save_trader_to_db(self, security, security_name, trader_code, trader_type, amount, price, trader_time, status):
        session = tools.创建数据库连接并且返回操作字段(application.get('db').get('url'))
        sql = f'INSERT INTO trader_info ("security", "security_name", "trader_code", "trader_type", "amount", "price", "trader_time", "status") VALUES ("{security}", "{security_name}", "{trader_code}", "{trader_type}", "{amount}", "{price}", "{trader_time}", "{status}");'
        session.execute(sql)
        session.commit()

    def 查询当日委托(self)->dict:
        tools.判断验证码控件是否存在()
        tools.同花顺刷新()
        time.sleep(1)
        today_trader_list = self.user.today_entrusts()
        return tools.转换数据格式(today_trader_list)

    def 监控委托(self, trader_code, rate):
        logger.info(f"开始监控挂单，编号：{trader_code}，网格大小为：{rate}元，执行中........")

        current_time = time.strftime("%H:%M:%S", time.localtime())

        if not "09:30:00" <= current_time <= "14:56:00":
            logger.info(f"取消交易，{current_time}不在交易时间区间内")
            return False

        trader = self.查询当日委托().get(trader_code)

        if trader is not None and isinstance(trader, dict):
            date_obj = datetime.datetime.strptime(trader.get('委托日期'), "%Y%m%d")
            for key, value in trader.items():
                logger.info(f"======交易单信息=========")
                logger.info(f"{key}：{value}")
            if trader.get('成交数量') == trader.get('委托数量') or trader.get("备注") == '订单全部成交':
                relation_trader_do_t = self.session.query(relation_trader).filter(relation_trader.monitor_trader_code==trader.get("委托序号"), ).all()
                if len(relation_trader_do_t) == 1:
                    relation_trader_info = relation_trader_do_t[0]
                    self.查询当日委托().get(relation_trader_info.reverse_trader_code)
                logger.info(f"订单已成交，开始执行更新操作")
                self.session.execute(f'UPDATE "main"."trader_info" SET "status" = "{trader.get("备注")}" WHERE "security" = "{trader.get("证券代码")}" AND "trader_code" = "{trader.get("委托序号")}" AND "trader_type" = "{trader_info.get("操作")}";')
                self.session.commit()

                result = None
                if trader.get('操作') == '证券卖出':
                    logger.info(f"监测挂单{trader.get('委托序号')}是属于：{trader.get('操作')}，开始执行买入操作")
                    price = round(trader.get('委托价格') - rate, 3)
                    result = user.buy(trader.get('证券代码'), price=price, amount=trader.get('委托数量'))
                elif trader.get('操作') == '证券买入':
                    logger.info(f"监测挂单{trader.get('委托序号')}是属于：{trader.get('操作')}，开始执行卖出操作")
                    price = round(trader.get('委托价格') + rate, 3)
                    result = user.sell(trader.get('证券代码'), price=price, amount=trader.get('委托数量'))
                if result.get('entrust_no') is not None and isinstance(result.get('entrust_no'), str):
                    tools.判断验证码控件是否存在()
                    self.user.refresh()
                    today_entrusts_map = user.today_entrusts(return_type=1)
                    do_t_trader = today_entrusts_map.get(result.get('entrust_no'))
                    # monitor_trader = trader_info(security=trader.get('证券代码'),security_name=trader.get('证券名称'), trader_code=trader.get('委托序号'), trader_type=trader_info.get('操作'), amount=trader.get('委托数量'), price=trader.get('委托价格'), trader_time=date_obj.strftime("%Y-%m-%d")+" "+trader.get('委托时间'), status=trader.get('备注'))
                    # session.add(monitor_trader)
                    do_t_trader_info = trader_info(security=do_t_trader.get('证券代码'), security_name=do_t_trader.get('证券名称'),
                                     trader_code=do_t_trader.get('委托序号'), trader_type=do_t_trader.get('操作'),
                                     amount=do_t_trader.get('委托数量'), price=do_t_trader.get('委托价格'),
                                     trader_time=date_obj.strftime("%Y-%m-%d") + " " + do_t_trader.get('委托时间'),
                                     status=do_t_trader.get('备注'))

                    session.add(do_t_trader_info)
                    session.commit()




    def 当订单为证券卖出(self, entrust):
        logger.info(f"监测挂单{entrust['委托序号']}是属于：{entrust['操作']}，开始执行买入操作")
        trader_data = self.session.query(trader_info).filter(trader_info.sell_code == str(entrust['委托序号']),trader_info.security == entrust['证券代码']).all()
        price = round(entrust['委托价格'] - 0.01, 3)
        if len(trader_data) == 0:
            # 低于0.01价格买入
            logger.info(f"买入价格为：{price}")
            result = self.user.buy(entrust['证券代码'], price=price, amount=entrust['委托数量'])
            if result.get('entrust_no') is not None and isinstance(result.get('entrust_no'), str):
                # 插入数据
                ti = trader_info(security=entrust['证券代码'],
                                 buy_code=result.get('entrust_no'),
                                 buy_amount=entrust['委托数量'],
                                 buy_price=price,
                                 buy_trader_time=datetime.datetime.now(),
                                 buy_status='订单已报',
                                 sell_code=entrust['委托序号'],
                                 sell_amount=entrust['委托数量'],
                                 sell_price=entrust['委托价格'],
                                 sell_trader_time=entrust['委托时间'],
                                 sell_status=entrust['备注'])
                session.add(ti)
                session.commit()
    def 当订单为证券买入(self, entrust):
        trader_data = self.session.query(trader_info).filter(trader_info.buy_code == str(entrust['委托序号']),trader_info.security == entrust['证券代码']).all()
        price = round(entrust['委托价格'] + 0.01, 3)
        if len(trader_data) == 0:
            result = self.user.sell(entrust['证券代码'], price=price, amount=entrust['委托数量'])
            if result.get('entrust_no') is not None and isinstance(result.get('entrust_no'), str):
                # 插入数据
                ti = trader_info(security=entrust['证券代码'],
                                 sell_code=result.get('entrust_no'),
                                 sell_amount=entrust['委托数量'],
                                 sell_price=price,
                                 sell_trader_time=datetime.datetime.now(),
                                 sell_status='订单已报',
                                 buy_code=entrust['委托序号'],
                                 buy_amount=entrust['委托数量'],
                                 buy_price=entrust['委托价格'],
                                 buy_trader_time=entrust['委托时间'],
                                 buy_status=entrust['备注'])
                session.add(ti)
                session.commit()
if __name__ == '__main__':

    # 读取配置文件
    application = tools.读取配置文件()

    # 连接数据库
    session = tools.创建数据库连接并且返回操作字段(application.get('db').get('url'))
    # 查询昨天是否有正t没完的订单
    # logger.info(session.query(trader_info).filter(trader_info.buy_status == '订单全部成交',trader_info.sell_status == '订单全部成交').all())
    #

    # 登录同花顺客户端
    user = easytrader.use(application['easytrader']['client']['type'])
    user.connect(application['easytrader']['client']['path'])  # 替换为你的同花顺路径
    # 无法通过默认方法输入文本，开启type_keys绕过
    logger.info("开启type_keys输入，选择【刷新】按钮")
    user.enable_type_keys_for_editor()
    user.refresh_strategy = refresh_strategies.Toolbar(refresh_btn_index=4)

    # 查询资金状况(可用)
    logger.info("========当前资金状况===========")
    for key, value in dict(user.balance).items():
        logger.info(f"{key}：{value}元")
    logger.info("============================\n")
    # 获取持仓
    positions = user.position
    for position in positions:
        logger.info(f"当前持仓：{position}")

    flag = 0
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(current_time)
        if not "06:30:00" <= current_time <= "14:56:00":
            break

        flag += 1
        if application['easytrader']['trader']['monitor_trader_code'] is None:
            logger.info("暂时没有需要监控的挂单")
            break

        if flag % 100 == 0 and flag != 0:
            logger.info("等待60s，在开始监控挂单")
            time.sleep(60)
        tools.判断验证码控件是否存在()
        user.refresh()
        # user.refresh_strategy.refresh()
        time.sleep(2)
        try:
            today_entrusts = user.today_entrusts(return_type=1)
            tools.判断验证码控件是否存在()
        except Exception as e:
            traceback.print_exc()
            time.sleep(60)
            today_entrusts = user.today_entrusts(return_type=1)
        # 查询当日委托
        logger.info(f"start========================================>")
        # for trader_code,rate in application['easytrader']['trader']['monitor_trader_code'].items():
        #     trader_message = dict(today_entrusts).get(trader_code)
        #     if trader_message is not None and trader_message['备注'] == '订单全部成交':
        #
        for entrust in dict(today_entrusts).values():
            # 判断是否需要监控挂单
            if str(entrust['委托序号']) in application['easytrader']['trader']['monitor_trader_code'].keys():
                logger.info(f"======监测到交易单{entrust['委托序号']}，状态：{entrust['备注']}=========")
                # 判断监控的挂单是否成交，如果没有成交，就跳过。
                if entrust['成交数量'] == entrust['委托数量'] or entrust['备注'] == '订单全部成交':
                    # 获取到监控挂单的浮动系数
                    rate = application['easytrader']['trader']['monitor_trader_code'].get(str(entrust['委托序号']))
                    # 判断监控的挂单属于买入，还是卖出。
                    if entrust['操作'] == '证券卖出':
                        # 监测的挂单属于卖出，那么就执行买入，并且将相关信息录入数据库
                        logger.info(f"监测挂单{entrust['委托序号']}是属于：{entrust['操作']}，开始执行买入操作")
                        data = session.query(trader_info).filter(trader_info.sell_code == str(entrust['委托序号']), trader_info.security == entrust['证券代码']).all()
                        if len(data) == 0:
                            # 低于0.01价格买入
                            price = round(entrust['委托价格'] - rate, 3)
                            # logger.info("买入："+user.buy(entrust['证券代码'], price=price, amount=entrust['委托数量']))
                            logger.info(f"证券代码：{entrust['证券代码']}，委托价格：{price}，委托数量：{entrust['委托数量']}，执行操作：买入")
                            result = user.buy(entrust['证券代码'], price=price, amount=entrust['委托数量'])
                            if result.get('entrust_no') is not None and isinstance(result.get('entrust_no'), str):
                                logger.info(f"证券代码：{entrust['证券代码']}，委托价格：{price}，委托数量：{entrust['委托数量']}，操作：买入成功")
                                # 插入数据
                                ti = trader_info(security=entrust['证券代码'],
                                                 buy_code=result.get('entrust_no'), buy_amount=entrust['委托数量'], buy_price=price,buy_trader_time=datetime.datetime.now(),buy_status='订单已报',
                                                 sell_code=entrust['委托序号'], sell_amount=entrust['委托数量'], sell_price=entrust['委托价格'],sell_trader_time=entrust['委托时间'],sell_status=entrust['备注'])
                                session.add(ti)
                                session.commit()
                                tools.给钉钉推送消息(application['dingding']['url'], '小萝卜活动数据新增', f"证券代码：{entrust['证券代码']}，委托价格：{price}，委托数量：{entrust['委托数量']}，操作：买入成功")
                        elif len(data) == 1:
                            if today_entrusts.get(data.get(0).buy_code)['备注'] == '订单全部成交':
                                print("执行更新操作")
                                pass

                    elif entrust['操作'] == '证券买入':
                        data = session.query(trader_info.sell_code is entrust['委托序号'],trader_info.security is entrust['证券代码']).all()
                        # 高于0.01价格卖出
                        price = round(entrust['委托价格'] + rate, 3)
                        # logger.info(f"挂单卖出：{user.sell(entrust['证券代码'], price=price, amount=entrust['委托数量'])}")
                        result = user.sell(entrust['证券代码'], price=price, amount=entrust['委托数量'])
                        if result.get('entrust_no') is not None and isinstance(result.get('entrust_no'), str):
                            # 插入数据
                            ti = trader_info(security=entrust['证券代码'],
                                             sell_code=result.get('entrust_no'),
                                             sell_amount=entrust['委托数量'],
                                             sell_price=price,
                                             sell_trader_time=datetime.datetime.now(),
                                             sell_status='订单已报',
                                             buy_code=entrust['委托序号'],
                                             buy_amount=entrust['委托数量'],
                                             buy_price=entrust['委托价格'],
                                             buy_trader_time=entrust['委托时间'],
                                             buy_status=entrust['备注'])
                            session.add(ti)
                            session.commit()
                            tools.给钉钉推送消息(application['dingding']['url'], '小萝卜活动数据新增',f"证券代码：{entrust['证券代码']}，委托价格：{price}，委托数量：{entrust['委托数量']}，操作：卖出成功，委托编号为：{result.get('entrust_no')}")
                else:
                    logger.info(f"证券代码：{entrust['证券代码']}\n委托数量：{entrust['委托数量']}\n委托状态：{entrust['备注']}")
                logger.info("===========操作结束========\n")
        logger.info("<========================================END\n")
        time.sleep(2)