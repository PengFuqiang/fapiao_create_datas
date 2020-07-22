#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：pfq time:2020/7/1

import global_var
import time
import random
import os
import cv2 as cv
from PIL import Image
from PIL import ImageDraw
from faker import Faker
from numpy import sin, cos, pi

fake = Faker(locale = 'zh_CN')  # 初始化中文简体


def rotate(x, y) :
    """
    点(x,y) 绕(cx,cy)点旋转
    """
    angle = - (rotate_angle * pi / 180)  # 角度转换为弧度计算
    x_new = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
    y_new = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy
    return x_new, y_new


def xy_end(m1, n1, m2, n2, m3, n3, m4, n4) :
    """
    返回旋转之后的坐标值
    """
    m11, n11 = rotate(m1, n1)
    m22, n22 = rotate(m2, n2)
    m33, n33 = rotate(m3, n3)
    m44, n44 = rotate(m4, n4)
    return m11, n11, m22, n22, m33, n33, m44, n44


# 生成日期函数
def print_date() :
    date = fake.date(pattern = '%Y年%m月%d日')
    draw.text((1501, 191), date, fill = (31, 83, 182), font = global_var.ft5)
    # 日期的坐标
    x1, y1 = 1501, 191
    x2, y2 = 1680, 191
    x3, y3 = 1501, 218
    x4, y4 = 1680, 218
    x11, y11, x22, y22, x33, y33, x44, y44 = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(str(x11) + ',' + str(y11) + ',' + str(x22) + ',' + str(y22) + ',' + str(x33) + ',' + str(
            y33) + ',' + str(x44) + ',' + str(y44) + ',' + date + '\n')


# 购买方区域文字添加
def purchase() :
    """
    字体宽度为27px，高度为30px
    以此计算字符串范围的四个顶点坐标
    然后调用rotate函数计算旋转之后的顶点坐标
    """
    # 添加公司名称
    name = fake.company()  # 随机生成公司名称
    draw.text((436, 253), name, fill = (8, 67, 161), font = global_var.ft6)
    name_length = len(name)
    x_start, y_start = 436, 253
    x_end, y_end = 436 + (name_length * 26), 253 + 29

    x1, y1 = x_start, y_start
    x2, y2 = x_end, y_start
    x3, y3 = x_start, y_end
    x4, y4 = x_end, y_end
    x11, y11, x22, y22, x33, y33, x44, y44 = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(str(x11) + ',' + str(y11) + ',' + str(x22) + ',' + str(y22) + ',' + str(x33) + ',' + str(
            y33) + ',' + str(x44) + ',' + str(y44) + ',' + name + '\n')

    # 添加纳税人识别号
    id_num = ''.join(str(random.choice(range(10))) for _ in range(15))  # 随机生成15位纳税人识别号
    draw.text((461, 290), id_num, fill = (8, 67, 161), font = global_var.ft7)
    id_x1, id_y1 = 461, 290
    id_x2, id_y2 = 744, 290
    id_x3, id_y3 = 461, 315
    id_x4, id_y4 = 744, 315
    id_x11, id_y11, id_x22, id_y22, id_x33, id_y33, id_x44, id_y44 = \
        xy_end(id_x1, id_y1, id_x2, id_y2, id_x3, id_y3, id_x4, id_y4)
    with open(filename, 'a+') as f :
        f.write(str(id_x11) + ',' + str(id_y11) + ',' + str(id_x22) + ',' + str(id_y22) + ',' + str(id_x33) + ',' + str(
            id_y33) + ',' + str(id_x44) + ',' + str(id_y44) + ',' + id_num + '\n')
    # 添加地址电话
    phone1 = ''.join(str(random.choice(range(10))) for _ in range(3))
    phone2 = ''.join(str(random.choice(range(10))) for _ in range(7))
    address = fake.address()[0 : -7]
    add_len = len(address)
    address_phone = address + ' ' + phone1 + '-' + phone2
    draw.text((433, 338), address_phone, fill = (8, 67, 161), font = global_var.ft8)
    add_ph_x1, add_ph_y1 = 433, 338
    add_ph_x2, add_ph_y2 = 433 + 21 * (add_len + 1) + 12 * 10, 338  # 十个号码加一个空格一个斜杠以及地址长度
    add_ph_x3, add_ph_y3 = 433, 338 + 24
    add_ph_x4, add_ph_y4 = 433 + 21 * (add_len + 1) + 12 * 10, 338 + 24
    add_ph_x11, add_ph_y11, add_ph_x22, add_ph_y22, add_ph_x33, add_ph_y33, add_ph_x44, add_ph_y44 = \
        xy_end(add_ph_x1, add_ph_y1, add_ph_x2, add_ph_y2, add_ph_x3, add_ph_y3, add_ph_x4, add_ph_y4)
    with open(filename, 'a+') as f :
        f.write(str(add_ph_x11) + ',' + str(add_ph_y11) + ',' + str(add_ph_x22) + ',' + str(add_ph_y22) + ',' + str(
            add_ph_x33) + ',' + str(add_ph_y33) + ',' + str(add_ph_x44) + ',' + str(
            add_ph_y44) + ',' + address_phone + '\n')

    # 添加开户行及账号
    bank1 = ['招商银行', '汉口银行', 'EBA银行']
    bank2 = ['龙阳大道支行', '北京东三环支行', '上海分行', '城北支行']
    # 15或18位账号
    acc = [''.join(str(random.choice(range(10))) for _ in range(15)),
           ''.join(str(random.choice(range(10))) for _ in range(18))]
    bank = random.choice(bank1) + random.choice(bank2)
    acc = random.choice(acc)
    bank_len, acc_len = len(bank), len(acc)
    bank_account = bank + ' ' + acc
    draw.text((436, 380), bank_account, fill = (8, 67, 161), font = global_var.ft6)
    bank_x1, bank_y1 = 436, 380
    bank_x2, bank_y2 = 436 + bank_len * 26 + 14 * acc_len, 380
    bank_x3, bank_y3 = 436, 380 + 29
    bank_x4, bank_y4 = 436 + bank_len * 26 + 14 * acc_len, 380 + 29
    bank_x11, bank_y11, bank_x22, bank_y22, bank_x33, bank_y33, bank_x44, bank_y44 = \
        xy_end(bank_x1, bank_y1, bank_x2, bank_y2, bank_x3, bank_y3, bank_x4, bank_y4)
    with open(filename, 'a+') as f :
        f.write(str(bank_x11) + ',' + str(bank_y11) + ',' + str(bank_x22) + ',' + str(bank_y22) + ',' + str(
            bank_x33) + ',' + str(bank_y33) + ',' + str(bank_x44) + ',' + str(bank_y44) + ',' + bank_account + '\n')


# 添加密码区
def password() :
    stru = ['+', '-', '*', '/', '<', '>', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # 组成密码的符号和数字
    pwd1 = ''.join(str(random.choice(stru)) for _ in range(27))
    pwd2 = ''.join(str(random.choice(stru)) for _ in range(27))
    pwd3 = ''.join(str(random.choice(stru)) for _ in range(27))
    pwd4 = ''.join(str(random.choice(stru)) for _ in range(27))
    draw.text((1127, 257), pwd1, fill = (8, 67, 161), font = global_var.ft9)
    draw.text((1127, 290), pwd2, fill = (8, 67, 161), font = global_var.ft9)
    draw.text((1127, 323), pwd3, fill = (8, 67, 161), font = global_var.ft9)
    draw.text((1127, 356), pwd4, fill = (8, 67, 161), font = global_var.ft9)
    # 第一行密码的坐标
    pwd1_x1, pwd1_y1 = 1127, 257
    pwd1_x2, pwd1_y2 = 1693, 257
    pwd1_x3, pwd1_y3 = 1127, 288
    pwd1_x4, pwd1_y4 = 1693, 288
    pwd1_x11, pwd1_y11, pwd1_x22, pwd1_y22, pwd1_x33, pwd1_y33, pwd1_x44, pwd1_y44 = \
        xy_end(pwd1_x1, pwd1_y1, pwd1_x2, pwd1_y2, pwd1_x3, pwd1_y3, pwd1_x4, pwd1_y4)
    # 第二行密码的坐标
    pwd2_x1, pwd2_y1 = 1127, 290
    pwd2_x2, pwd2_y2 = 1693, 290
    pwd2_x3, pwd2_y3 = 1127, 321
    pwd2_x4, pwd2_y4 = 1693, 321
    pwd2_x11, pwd2_y11, pwd2_x22, pwd2_y22, pwd2_x33, pwd2_y33, pwd2_x44, pwd2_y44 = \
        xy_end(pwd2_x1, pwd2_y1, pwd2_x2, pwd2_y2, pwd2_x3, pwd2_y3, pwd2_x4, pwd2_y4)
    # 第三行密码的坐标
    pwd3_x1, pwd3_y1 = 1127, 323
    pwd3_x2, pwd3_y2 = 1693, 323
    pwd3_x3, pwd3_y3 = 1127, 354
    pwd3_x4, pwd3_y4 = 1693, 354
    pwd3_x11, pwd3_y11, pwd3_x22, pwd3_y22, pwd3_x33, pwd3_y33, pwd3_x44, pwd3_y44 = \
        xy_end(pwd3_x1, pwd3_y1, pwd3_x2, pwd3_y2, pwd3_x3, pwd3_y3, pwd3_x4, pwd3_y4)
    # 第四行密码的坐标
    pwd4_x1, pwd4_y1 = 1127, 356
    pwd4_x2, pwd4_y2 = 1693, 356
    pwd4_x3, pwd4_y3 = 1127, 387
    pwd4_x4, pwd4_y4 = 1693, 387
    pwd4_x11, pwd4_y11, pwd4_x22, pwd4_y22, pwd4_x33, pwd4_y33, pwd4_x44, pwd4_y44 = \
        xy_end(pwd4_x1, pwd4_y1, pwd4_x2, pwd4_y2, pwd4_x3, pwd4_y3, pwd4_x4, pwd4_y4)
    with open(filename, 'a+') as f :
        f.write(str(pwd1_x11) + ',' + str(pwd1_y11) + ',' + str(pwd1_x22) + ',' + str(pwd1_y22) + ',' + str(
            pwd1_x33) + ',' + str(pwd1_y33) + ',' + str(pwd1_x44) + ',' + str(pwd1_y44) + ',' + pwd1 + '\n')
        f.write(str(pwd2_x11) + ',' + str(pwd2_y11) + ',' + str(pwd2_x22) + ',' + str(pwd2_y22) + ',' + str(
            pwd2_x33) + ',' + str(pwd2_y33) + ',' + str(pwd2_x44) + ',' + str(pwd2_y44) + ',' + pwd2 + '\n')
        f.write(str(pwd3_x11) + ',' + str(pwd3_y11) + ',' + str(pwd3_x22) + ',' + str(pwd3_y22) + ',' + str(
            pwd3_x33) + ',' + str(pwd3_y33) + ',' + str(pwd3_x44) + ',' + str(pwd3_y44) + ',' + pwd3 + '\n')
        f.write(str(pwd4_x11) + ',' + str(pwd4_y11) + ',' + str(pwd4_x22) + ',' + str(pwd4_y22) + ',' + str(
            pwd4_x33) + ',' + str(pwd4_y33) + ',' + str(pwd4_x44) + ',' + str(pwd4_y44) + ',' + pwd4 + '\n')


# 添加货物或应税劳务及后面对应的规格价格等内容
def add_goods() :
    types = ['g', 'ml', '*', ' ', '+', 'kg', 'l', '-', ' ', ' ', ' ']
    # units = ['升', '次', '支', '件', '袋', '只', '瓶', '盒', '块', '']
    amounts = [random.randint(1, 10), random.randint(1, 100),
               random.randint(1, 1000), random.randint(1, 2000)]
    unit_prices = [round(random.uniform(0, 10), 2), round(random.uniform(0, 100), 2),
                   round(random.uniform(0, 1000), 2)]
    rate = random.choice(range(1, 30))  # 求对应的税率
    total1 = 0  # 各个金额之和
    total2 = 0  # 各个税额之和
    total = 0

    for i in range(random.randint(1, 5)) :
        y = 461 + (30 * i)
        goods = fake.sentence()
        standards = fake.word() + random.choice(types)  # 长度为3
        units = random.choice(fake.word())  # 长度为1
        if len(goods) > 14 :
            goods = goods[0 : 14]  # 避免字符串过长
        else :
            goods = goods[0 : -1]  # 去掉最后的标点符号
        goods_len = len(goods)
        draw.text((185, y), goods, fill = (8, 67, 161), font = global_var.ft6)  # 添加货物
        draw.text((596, y), standards, fill = (8, 67, 161), font = global_var.ft6)  # 添加型号规格
        draw.text((804, y), units, fill = (8, 67, 161), font = global_var.ft6)  # 添加单位

        # 获取货物，型号，单位旋转后的坐标
        goods_x1, goods_y1 = 185, y
        goods_x2, goods_y2 = 185 + goods_len * 26, y
        goods_x3, goods_y3 = 185, y + 29
        goods_x4, goods_y4 = 185 + goods_len * 26, y + 29
        goods_x11, goods_y11, goods_x22, goods_y22, goods_x33, goods_y33, goods_x44, goods_y44 = \
            xy_end(goods_x1, goods_y1, goods_x2, goods_y2, goods_x3, goods_y3, goods_x4, goods_y4)

        standards_x1, standards_y1 = 596, y
        standards_x2, standards_y2 = 596 + 26 * 3, y
        standards_x3, standards_y3 = 596, y + 29
        standards_x4, standards_y4 = 596 + 26 * 3, y + 29
        standards_x11, standards_y11, standards_x22, standards_y22, standards_x33, standards_y33, standards_x44, \
        standards_y44 = xy_end(standards_x1, standards_y1, standards_x2, standards_y2, standards_x3, standards_y3,
                               standards_x4, standards_y4)

        units_x1, units_y1 = 804, y
        units_x2, units_y2 = 804 + 26, y
        units_x3, units_y3 = 804, y + 29
        units_x4, units_y4 = 804 + 26, y + 29
        units_x11, units_y11, units_x22, units_y22, units_x33, units_y33, units_x44, units_y44 = \
            xy_end(units_x1, units_y1, units_x2, units_y2, units_x3, units_y3, units_x4, units_y4)
        # 最终坐标写入到文件中
        with open(filename, 'a+') as f :
            f.write(str(goods_x11) + ',' + str(goods_y11) + ',' + str(goods_x22) + ',' + str(goods_y22)
                    + ',' + str(goods_x33) + ',' + str(goods_y33) + ',' + str(goods_x44) + ',' + str(
                goods_y44) + ',' + goods + '\n')
            f.write(str(standards_x11) + ',' + str(standards_y11) + ',' + str(standards_x22) + ',' + str(
                standards_y22) + ',' + str(standards_x33) + ',' + str(standards_y33) + ',' + str(
                standards_x44) + ',' + str(standards_y44) + ',' + standards + '\n')
            f.write(str(units_x11) + ',' + str(units_y11) + ',' + str(units_x22) + ',' + str(units_y22) + ',' + str(
                units_x33) + ',' + str(units_y33) + ',' + str(units_x44) + ',' + str(units_y44) + ',' + units + '\n')

        amount = random.choice(amounts)  # 取对应的数量
        unit_price = random.choice(unit_prices)  # 取单价
        total_price = amount * unit_price  # 求对应的金额
        tax_amount = rate * total_price * 0.01  # 求对应的税额
        total1 += total_price
        total2 += tax_amount
        draw.text((909, y), str(amount).rjust(8), fill = (8, 67, 161), font = global_var.ft13)  # 添加数量
        draw.text((1069, y), ("%.2f" % unit_price).rjust(8), fill = (8, 67, 161),
                  font = global_var.ft13)  # 添加单价
        draw.text((1267, y), ("%.2f" % total_price).rjust(11), fill = (8, 67, 161),
                  font = global_var.ft13)  # 添加金额
        draw.text((1455, y), str(rate) + '%', fill = (8, 67, 161), font = global_var.ft13)  # 添加税率
        draw.text((1600, y), ("%.2f" % tax_amount).rjust(10), fill = (8, 67, 161),
                  font = global_var.ft13)  # 添加税额
    # 计算总价
    total = total1 + total2
    big_total = digital_to_chinese(round(total, 2))  # 总金额取两位并转为大写
    draw.text((1214, 715), '￥', fill = (8, 67, 161), font = global_var.ft12)  # 添加金额之和
    draw.text((1541, 715), '￥', fill = (8, 67, 161), font = global_var.ft12)  # 添加税额之和
    draw.text((1410, 781), '￥', fill = (8, 67, 161), font = global_var.ft12)  # 添加金额税额之和
    draw.text((1244, 715), ("%.2f" % total1), fill = (8, 67, 161), font = global_var.ft10)  # 添加金额之和
    draw.text((1571, 715), ("%.2f" % total2), fill = (8, 67, 161), font = global_var.ft10)  # 添加税额之和
    draw.text((1440, 781), ("%.2f" % total), fill = (8, 67, 161), font = global_var.ft10)  # 添加金额税额之和
    draw.text((654, 778), big_total, fill = (8, 67, 161), font = global_var.ft11)  # 添加金额税额之和的中文大写


# 金额转换为中文大写
def digital_to_chinese(digital) :
    str_digital = str(digital)
    chinese = {'1' : '壹', '2' : '贰', '3' : '叁', '4' : '肆', '5' : '伍', '6' : '陆', '7' : '柒', '8' : '捌', '9' : '玖',
               '0' : '零'}
    chinese2 = ['拾', '佰', '仟', '万', '厘', '分', '角']
    jiao = ''
    bs = str_digital.split('.')
    yuan = bs[0]
    if len(bs) > 1 :
        jiao = bs[1]
    r_yuan = [i for i in reversed(yuan)]
    count = 0
    for i in range(len(yuan)) :
        if i == 0 :
            r_yuan[i] += '圆'
            continue
        r_yuan[i] += chinese2[count]
        count += 1
        if count == 4 :
            count = 0
            chinese2[3] = '亿'

    s_jiao = [i for i in jiao][:2]  # 去掉小于分之后的

    j_count = -1
    for i in range(len(s_jiao)) :
        s_jiao[i] += chinese2[j_count]
        j_count -= 1
    last = [i for i in reversed(r_yuan)] + s_jiao
    last_str = ''.join(last)
    # print(str_digital)
    # print(last_str)
    for i in range(len(last_str)) :
        digital = last_str[i]
        if digital in chinese :
            last_str = last_str.replace(digital, chinese[digital])
    if '零角零分' in last_str :
        last_str.replace('零角零分', '圆整')
    elif '零分' in last_str :
        last_str.replace('零分', '')
    # elif '零角' in last_str and '分' not in last_str :
    #     last_str.replace('零角', '圆整')
    # print(last_str)
    return last_str


# 添加销售方内容
def add_seller() :  # 添加销售方名称
    seller_name = fake.company()
    draw.text((436, 840), seller_name, fill = (8, 67, 161), font = global_var.ft6)


def seller_nums() :  # 添加纳税人识别号（销售方）
    id_part = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', chr(random.randint(65, 90))]
    id1 = ''.join(str(random.choice(id_part)) for _ in range(18))
    id2 = ''.join(str(random.choice(id_part)) for _ in range(15))
    id = [id1, id2]
    draw.text((470, 872), random.choice(id), fill = (8, 67, 141), font = global_var.ft7)


def add_and_phone() :  # 添加地址、电话（销售方）
    add = fake.address()
    phone1 = ''.join(str(random.choice(range(10))) for _ in range(3))
    phone2 = ''.join(str(random.choice(range(10))) for _ in range(4))
    phone3 = ''.join(str(random.choice(range(10))) for _ in range(7))
    phone4 = ''.join(str(random.choice(range(10))) for _ in range(8))
    phone_num1 = [phone1, phone2]
    phone_num2 = [phone3, phone4]
    add_phone = add + ' ' + random.choice(phone_num1) + random.choice(phone_num2)
    draw.text((420, 915), add_phone, fill = (8, 67, 141), font = global_var.ft6)


def add_bankId() :  # 添加开户行及账号
    bank1 = ['招商银行', '汉口银行', 'EBA银行']
    bank2 = ['龙阳大道支行', '北京东三环支行', '上海分行', '城北支行']
    # 15或18位账号
    acc = [''.join(str(random.choice(range(10))) for _ in range(15)),
           ''.join(str(random.choice(range(10))) for _ in range(18))]
    bank_and_account = random.choice(bank1) + random.choice(bank2) + ' ' + random.choice(acc)
    draw.text((420, 950), bank_and_account, fill = (8, 67, 161), font = global_var.ft6)


def add_name() :
    # 添加收款人复核人开票人名字
    # 生成随机的三个名字
    name1 = fake.name()
    name2 = fake.name()
    name3 = fake.name()
    draw.text((305, 995), name1, fill = (8, 67, 161), font = global_var.ft6)
    draw.text((722, 995), name2, fill = (8, 67, 161), font = global_var.ft6)
    draw.text((1099, 995), name3, fill = (8, 67, 161), font = global_var.ft6)


# 添加发票代码
def add_fapiao_daima() :
    num_str = ''.join(str(random.choice(range(10))) for _ in range(10))  # 随机生成10位数字发票代码
    draw.text((344, 82), num_str, fill = (72, 75, 68), font = global_var.ft1)  # 添加发票代码
    draw.text((1603, 110), num_str, fill = (31, 83, 182), font = global_var.ft3)  # 添加号码后面的小代码
    # 大的发票代码的坐标
    x1, y1 = 344, 82
    x2, y2 = 620, 82
    x3, y3 = 344, 130
    x4, y4 = 620, 130
    x11, y11 = rotate(x1, y1)
    x22, y22 = rotate(x2, y2)
    x33, y33 = rotate(x3, y3)
    x44, y44 = rotate(x4, y4)
    # 小的发票代码的坐标
    sx1, sy1 = 1603, 110
    sx2, sy2 = 1730, 110
    sx3, sy3 = 1603, 132
    sx4, sy4 = 1730, 132
    sx11, sy11 = rotate(sx1, sy1)
    sx22, sy22 = rotate(sx2, sy2)
    sx33, sy33 = rotate(sx3, sy3)
    sx44, sy44 = rotate(sx4, sy4)

    with open(filename, 'a+') as f :
        f.write(
            str(x11) + ',' + str(y11) + ',' + str(x22) + ',' + str(y22) + ',' + str(x33) + ',' + str(
                y33) + ',' + str(
                x44) + ',' + str(y44) + ',' + num_str + '\n')
        f.write(str(sx11) + ',' + str(sy11) + ',' + str(sx22) + ',' + str(sy22) + ',' + str(sx33) + ',' + str(
            sy33) + ',' + str(sx44) + ',' + str(sy44) + ',' + num_str + '\n')


# 添加发票号码
def add_fapiao_hao() :
    no_str = ''.join(str(random.choice(range(10))) for _ in range(8))  # 随机生成8位数字发票号码
    draw.text((1370, 86), no_str, fill = (48, 87, 161), font = global_var.ft2)  # 添加发票号码
    draw.text((1585, 146), no_str, fill = (8, 67, 161), font = global_var.ft4)  # 添加小号码
    # 大的号码坐标
    x1, y1 = 1370, 86
    x2, y2 = 1590, 86
    x3, y3 = 1370, 133
    x4, y4 = 1590, 133
    x11, y11 = rotate(x1, y1)
    x22, y22 = rotate(x2, y2)
    x33, y33 = rotate(x3, y3)
    x44, y44 = rotate(x4, y4)
    # 小的号码坐标
    sx1, sy1 = 1585, 146
    sx2, sy2 = 1705, 146
    sx3, sy3 = 1585, 172
    sx4, sy4 = 1705, 172
    sx11, sy11 = rotate(sx1, sy1)
    sx22, sy22 = rotate(sx2, sy2)
    sx33, sy33 = rotate(sx3, sy3)
    sx44, sy44 = rotate(sx4, sy4)
    with open(filename, 'a+') as f :
        f.write(
            str(x11) + ',' + str(y11) + ',' + str(x22) + ',' + str(y22) + ',' + str(x33) + ',' + str(
                y33) + ',' + str(
                x44) + ',' + str(y44) + ',' + no_str + '\n')
        f.write(str(sx11) + ',' + str(sy11) + ',' + str(sx22) + ',' + str(sy22) + ',' + str(sx33) + ',' + str(
            sy33) + ',' + str(sx44) + ',' + str(sy44) + ',' + no_str + '\n')


# 主函数
def main() :
    add_fapiao_daima()  # 添加发票代码
    add_fapiao_hao()  # 添加发票号码
    print_date()  # 生成日期函数
    purchase()  # 购买方区域文字添加
    password()  # 添加密码区
    add_goods()  # 添加货物或应税劳务及后面对应的规格价格等内容
    add_seller()  # 添加销售方内容
    seller_nums()  # 添加纳税人识别号（销售方）
    add_and_phone()  # 添加地址、电话（销售方）
    add_bankId()  # 添加开户行及账号
    add_name()  # 添加收款人复核人开票人名字
    # global_var.im.show()
    im.save('pic_origin\\res' + str(index) + '.jpg')  # 保存添加完的图片

    # 图片仿射变换
    img = cv.imread('pic_origin\\res' + str(index) + '.jpg')
    rot_mat = cv.getRotationMatrix2D((cx, cy), rotate_angle, 1)
    img_rotated_by_alpha = cv.warpAffine(img, rot_mat, (img.shape[1], img.shape[0]))
    blur_num = int(random.choice(['1', '3', '5', '7']))  # 模糊的程度
    dst_1 = cv.GaussianBlur(img_rotated_by_alpha, (blur_num, blur_num), 0)
    dir_name = 'res\\res' + str(index)
    os.mkdir(dir_name)

    cv.imwrite(dir_name + '\\pic.jpg', dst_1)  # 保存高斯模糊处理+仿射变换后的图片
    print(index)


if __name__ == '__main__' :
    for index in range(5) :
        template_num = random.randint(1, 4)
        im = Image.open('pic_template\\template_' + str(template_num) + '.jpg')  # 随机挑选一个模板图
        draw = ImageDraw.Draw(im)
        rotate_angle = random.randint(-7, 7)  # 生成随机的旋转角度（正数为逆时针）
        '''
        模板图片尺寸和处理后的图片尺寸是一致的
        所以中心点是一样的
        '''
        img_tmp = cv.imread('pic_template\\template_' + str(template_num) + '.jpg')
        h, w, c = img_tmp.shape  # 获取图片的高和宽
        cx, cy = w / 2, h / 2  # 得到中心坐标点
        filename = 'res\\write' + str(index) + '.txt'
        main()
