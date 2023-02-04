#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2021/6/22 14:52
# @File     : timeoperator.py
# @Project  : WYTest
# @Desc     : 时间操作
import random
import time
import datetime
import calendar


class TimeOperator:
    @property
    def now(self):
        """
        返回当前时间戳
        :return:
        """
        return time.time()

    @property
    def now1(self):
        """
        以 年-月-日 时:分:秒 格式返回当前时间
        :return:
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @property
    def now2(self):
        """
        以 年-月-日 格式返回当前时间
        :return:
        """
        return time.strftime("%Y-%m-%d", time.localtime())

    @property
    def now3(self):
        """
        以 年月日时分秒 格式返回当前时间
        :return:
        """
        return time.strftime("%Y%m%d%H%M%S", time.localtime())

    @property
    def now4(self):
        """
        13位时间戳
        :return:
        """
        return int(time.time() * 1000)

    def strftime_now(self, strf, d=None):
        """
        以 指定格式 格式返回当前时间
        :return:
        """
        if d:
            return time.strftime(strf, time.localtime(d))
        else:
            return time.strftime(strf, time.localtime())

    @property
    def now_month(self):
        """
        以 年-月 格式返回当前时间
        :return:
        """
        return time.strftime("%Y-%m", time.localtime())

    @property
    def year(self):
        """
        返回当前年
        :return:
        """
        return time.strftime("%Y", time.localtime())

    @property
    def month(self):
        """
        返回当前月
        :return:
        """
        return time.strftime("%m", time.localtime())

    @property
    def day(self):
        """
        返回当前日
        :return:
        """
        return time.strftime("%d", time.localtime())

    def other_month(self, add_num=0):
        """
        当前月份的n个月后的 年-月
        """
        y_m = self.now_month
        y, m = [int(i) for i in y_m.split("-")]
        m += add_num
        if m > 12:
            m -= 12
            y += 1
        return f'{y}-{m:02d}'

    def other_day(self, day):
        """
        以 年-月-日 时:分:秒 格式返回当前时间+偏移时间
        :return:
        """
        return str(datetime.datetime.today() + datetime.timedelta(days=day)).split(".")[0]

    def other_day_num(self, day):
        """
        以时间戳格式返回 当前时间+偏移时间
        @param day:
        @return:
        """
        return int(time.time() * 1000) + 24 * 3600 * day

    def get_age(self, birthday):
        """

        :param birthday: 年-月-日
        :return:
        """
        y, m, d = [int(i) for i in birthday.split('-')]
        birthday = datetime.date(y, m, d)
        today = datetime.date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def get_year_month(self, year=0, month=0):
        now = datetime.datetime.now()
        if year == 0:
            year = now.year
        if month == 0:
            month = now.month
        return year, month

    def get_month_day(self, year=0, month=0):
        """
        获取指定月份第一天和最后一天
        """
        year, month = self.get_year_month(year, month)
        month_first_day, month_last_day = calendar.monthrange(year, month)
        return month_first_day, month_last_day

    def get_random_day(self, year=0, month=0):
        """
        获取指定年月的随机的一天
        """
        year, month = self.get_year_month(year, month)
        month_first_day, month_last_day = self.get_month_day(year, month)
        day = random.randint(month_first_day, month_last_day)
        return f'{year}-{month}-{day:02d}'

    def get_random_time(self):
        """
        获取随机 时:分:秒
        """
        h = random.randint(0, 23)
        m = random.randint(0, 59)
        s = random.randint(0, 59)
        return f'{h:02d}:{m:02d}:{s:02d}'

    def get_other_m_d(self, n=0, t=None):
        """
        获取n个月后的年月日范围
        """
        if t:
            y, m = t.split("-")
        else:
            y, m, _ = self.now2.split("-")
        y = int(y)
        m = int(m) + n
        d1, d2 = self.get_month_day(int(y), m)
        return f'{y:04d}-{m:02d}-{1:02d}', f'{y:04d}-{m:02d}-{d2:02d}'

    def get_localtime(self, time_stamp, time_format='%Y-%m-%d %H:%M:%S'):
        """
        时间戳转化
        @param time_stamp:
        @return:
        """
        if len(str(time_stamp)) == 13:
            time_stamp = time_stamp / 1000
        time_array = time.localtime(time_stamp)
        return time.strftime(time_format, time_array)

    def get_time_stamp(self, time_str, format):
        """
        将指定格式时间转化成时间戳
        @param time_str:
        @param format:
        @return:
        """
        return time.mktime(time.strptime(time_str, format))

    @property
    def get_day_end(self):
        """
        获取今天23:59:59的13位时间戳
        @return:
        """
        t = datetime.datetime(int(self.year), int(self.month), int(self.day), 23, 59, 59)
        t_i = self.get_time_stamp(str(t), "%Y-%m-%d %H:%M:%S")
        return int(t_i * 1000)


timeoperator = TimeOperator()

if __name__ == '__main__':
    # print(timeoperator.other_month())
    # print(timeoperator.other_month(1))
    # print(timeoperator.other_month(2))
    print(timeoperator.get_day_end)
