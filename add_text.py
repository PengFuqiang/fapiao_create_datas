#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：pfq time:2020/7/1

import time
import random
import os
import cv2 as cv
from PIL import Image
from PIL import ImageDraw
from faker import Faker
from numpy import sin, cos, pi

import global_var
import split_picture

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
    return (str(m11) + ',' + str(n11) + ',' + str(m22) + ',' + str(n22) + ',' + str(m33) + ',' + str(n33) + ',' + str(
        m44) + ',' + str(n44) + ',')

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


# 生成日期函数
def print_date() :
    date = fake.date(pattern = '%Y年%m月%d日')
    draw.text((1501, 191), date, fill = (31, 83, 182), font = global_var.ft5)
    # 日期的坐标
    x1, y1 = 1500, 191
    x2, y2 = 1680, 191
    x3, y3 = 1500, 219
    x4, y4 = 1680, 219
    text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(text + date + '\n')


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
    text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(text + name + '\n')

    # 添加纳税人识别号
    id_num = ''.join(str(random.choice(range(10))) for _ in range(15))  # 随机生成15位纳税人识别号
    draw.text((461, 290), id_num, fill = (8, 67, 161), font = global_var.ft7)
    id_x1, id_y1 = 461, 290
    id_x2, id_y2 = 744, 290
    id_x3, id_y3 = 461, 320
    id_x4, id_y4 = 744, 320
    text = xy_end(id_x1, id_y1, id_x2, id_y2, id_x3, id_y3, id_x4, id_y4)
    with open(filename, 'a+') as f :
        f.write(text + id_num + '\n')
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
    text = xy_end(add_ph_x1, add_ph_y1, add_ph_x2, add_ph_y2, add_ph_x3, add_ph_y3, add_ph_x4, add_ph_y4)
    with open(filename, 'a+') as f :
        f.write(text + address_phone + '\n')

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
    text = xy_end(bank_x1, bank_y1, bank_x2, bank_y2, bank_x3, bank_y3, bank_x4, bank_y4)
    with open(filename, 'a+') as f :
        f.write(text + bank_account + '\n')


# 添加密码区
def password() :
    """
    密码区每行长度都相同为66，高度为33
    """
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
    pwd1_text = xy_end(pwd1_x1, pwd1_y1, pwd1_x2, pwd1_y2, pwd1_x3, pwd1_y3, pwd1_x4, pwd1_y4)
    # 第二行密码的坐标
    pwd2_x1, pwd2_y1 = 1127, 290
    pwd2_x2, pwd2_y2 = 1693, 290
    pwd2_x3, pwd2_y3 = 1127, 321
    pwd2_x4, pwd2_y4 = 1693, 321
    pwd2_text = xy_end(pwd2_x1, pwd2_y1, pwd2_x2, pwd2_y2, pwd2_x3, pwd2_y3, pwd2_x4, pwd2_y4)
    # 第三行密码的坐标
    pwd3_x1, pwd3_y1 = 1127, 323
    pwd3_x2, pwd3_y2 = 1693, 323
    pwd3_x3, pwd3_y3 = 1127, 354
    pwd3_x4, pwd3_y4 = 1693, 354
    pwd3_text = xy_end(pwd3_x1, pwd3_y1, pwd3_x2, pwd3_y2, pwd3_x3, pwd3_y3, pwd3_x4, pwd3_y4)
    # 第四行密码的坐标
    pwd4_x1, pwd4_y1 = 1127, 356
    pwd4_x2, pwd4_y2 = 1693, 356
    pwd4_x3, pwd4_y3 = 1127, 387
    pwd4_x4, pwd4_y4 = 1693, 387
    pwd4_text = xy_end(pwd4_x1, pwd4_y1, pwd4_x2, pwd4_y2, pwd4_x3, pwd4_y3, pwd4_x4, pwd4_y4)
    with open(filename, 'a+') as f :
        f.write(pwd1_text + pwd1 + '\n')
        f.write(pwd2_text + pwd2 + '\n')
        f.write(pwd3_text + pwd3 + '\n')
        f.write(pwd4_text + pwd4 + '\n')


# 添加货物或应税劳务及后面对应的规格价格等内容
def add_goods() :
    """
    货物，型号，单位等每个字符长为26高为29
    其余数字字符宽为13或19
    """
    types = ['g', '/', '*', '+', 'g', 'l', '-', '#', '!', '~', 'h']
    # units = ['升', '次', '支', '件', '袋', '只', '瓶', '盒', '块', '']
    amounts = [random.randint(1, 10), random.randint(1, 100),
               random.randint(1, 1000), random.randint(1, 2000)]
    unit_prices = [round(random.uniform(0, 10), 2), round(random.uniform(0, 100), 2),
                   round(random.uniform(0, 1000), 2)]
    rate = random.choice(range(1, 20))  # 求对应的税率
    total1 = 0  # 各个金额之和
    total2 = 0  # 各个税额之和
    total = 0

    for i in range(4) :
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
        goods_text = xy_end(goods_x1, goods_y1, goods_x2, goods_y2, goods_x3, goods_y3, goods_x4, goods_y4)

        standards_x1, standards_y1 = 596, y
        standards_x2, standards_y2 = 596 + 70, y    # 规格字符宽为70
        standards_x3, standards_y3 = 596, y + 29
        standards_x4, standards_y4 = 596 + 70, y + 29
        standards_text = xy_end(standards_x1, standards_y1, standards_x2, standards_y2, standards_x3, standards_y3,
                                standards_x4, standards_y4)

        units_x1, units_y1 = 804, y
        units_x2, units_y2 = 804 + 26, y
        units_x3, units_y3 = 804, y + 29
        units_x4, units_y4 = 804 + 26, y + 29
        units_text = xy_end(units_x1, units_y1, units_x2, units_y2, units_x3, units_y3, units_x4, units_y4)
        # 最终坐标写入到文件中
        with open(filename, 'a+') as f :
            f.write(goods_text + goods + '\n')
            f.write(standards_text + standards + '\n')
            f.write(units_text + units + '\n')

        amount = random.choice(amounts)  # 取对应的数量
        unit_price = random.choice(unit_prices)  # 取单价
        total_price = amount * unit_price  # 求对应的金额
        tax_amount = rate * total_price * 0.01  # 求对应的税额
        total1 += total_price
        total2 += tax_amount
        draw.text((909, y), str(amount).rjust(8), fill = (8, 67, 161), font = global_var.ft13)  # 添加数量
        # 计算商品数量的坐标
        amount_x1, amount_y1 = 909 + 12 * (8 - len(str(amount))), y
        amount_x2, amount_y2 = 1013, y
        amount_x3, amount_y3 = 909 + 12 * (8 - len(str(amount))), y + 29
        amount_x4, amount_y4 = 1013, y + 29
        amount_text = xy_end(amount_x1, amount_y1, amount_x2, amount_y2, amount_x3, amount_y3, amount_x4, amount_y4)
        # 计算单价的坐标
        draw.text((1069, y), ("%.2f" % unit_price).rjust(8), fill = (8, 67, 161), font = global_var.ft13)  # 添加单价
        unit_price_x1, unit_price_y1 = 1069 + 13 * (8 - len(str(round(unit_price, 2)))), y
        unit_price_x2, unit_price_y2 = 1172, y
        unit_price_x3, unit_price_y3 = 1069 + 13 * (8 - len(str(round(unit_price, 2)))), y + 29
        unit_price_x4, unit_price_y4 = 1172, y + 29
        unit_price_text = xy_end(unit_price_x1, unit_price_y1, unit_price_x2, unit_price_y2, unit_price_x3,
                                 unit_price_y3, unit_price_x4, unit_price_y4)
        # 计算金额的坐标
        draw.text((1267, y), ("%.2f" % total_price).rjust(11), fill = (8, 67, 161), font = global_var.ft13)  # 添加金额
        total_price_x1, total_price_y1 = 1267 + 13 * (8 - len(str(round(total_price, 2)))), y
        total_price_x2, total_price_y2 = 1412, y
        total_price_x3, total_price_y3 = 1267 + 13 * (8 - len(str(round(total_price, 2)))), y + 29
        total_price_x4, total_price_y4 = 1412, y + 29
        total_price_text = xy_end(total_price_x1, total_price_y1, total_price_x2, total_price_y2, total_price_x3,
                                  total_price_y3, total_price_x4, total_price_y4)

        # 计算税率的坐标
        draw.text((1455, y), str(rate) + '%', fill = (8, 67, 161), font = global_var.ft13)  # 添加税率
        rate_x1, rate_y1 = 1455, y
        rate_x2, rate_y2 = 1496, y
        rate_x3, rate_y3 = 1455, y + 29
        rate_x4, rate_y4 = 1496, y + 29
        rate_text = xy_end(rate_x1, rate_y1, rate_x2, rate_y2, rate_x3, rate_y3, rate_x4, rate_y4)
        # 计算税额的坐标
        draw.text((1600, y), ("%.2f" % tax_amount).rjust(10), fill = (8, 67, 161), font = global_var.ft13)  # 添加税额
        tax_x1, tax_y1 = 1600 + 13 * (10 - len(str(round(tax_amount, 2)))), y
        tax_x2, tax_y2 = 1730, y
        tax_x3, tax_y3 = 1600 + 13 * (10 - len(str(round(tax_amount, 2)))), y + 29
        tax_x4, tax_y4 = 1730, y + 29
        tax_text = xy_end(tax_x1, tax_y1, tax_x2, tax_y2, tax_x3, tax_y3, tax_x4, tax_y4)
        with open(filename, 'a+') as f :  # 写入坐标信息
            f.write(amount_text + str(amount) + '\n')
            f.write(unit_price_text + str(unit_price) + '\n')
            f.write(total_price_text + ("%.2f" % total_price) + '\n')
            f.write(rate_text + str(rate) + '%' + '\n')
            f.write(tax_text + ("%.2f" % tax_amount) + '\n')
    # 计算总价
    total = total1 + total2
    big_total = digital_to_chinese(round(total, 2))  # 总金额取两位并转为大写
    # 添加金额前的￥符号
    draw.text((1214, 715), '￥', fill = (8, 67, 161), font = global_var.ft12)
    draw.text((1541, 715), '￥', fill = (8, 67, 161), font = global_var.ft12)
    draw.text((1410, 781), '￥', fill = (8, 67, 161), font = global_var.ft12)

    draw.text((1244, 715), ("%.2f" % total1), fill = (8, 67, 161), font = global_var.ft10)  # 添加金额之和
    draw.text((1571, 715), ("%.2f" % total2), fill = (8, 67, 161), font = global_var.ft10)  # 添加税额之和
    draw.text((1440, 781), ("%.2f" % total), fill = (8, 67, 161), font = global_var.ft10)  # 添加金额税额之和
    draw.text((654, 778), big_total, fill = (8, 67, 161), font = global_var.ft11)  # 添加金额税额之和的中文大写
    # 金额之和坐标
    total1_x1, total1_y1 = 1214, 715
    total1_x2, total1_y2 = 1244 + 19 * len(str("%.2f" % total1)), 715
    total1_x3, total1_y3 = 1214, 745
    total1_x4, total1_y4 = 1244 + 19 * len(str("%.2f" % total1)), 745
    total1_text = xy_end(total1_x1, total1_y1, total1_x2, total1_y2, total1_x3, total1_y3, total1_x4, total1_y4)

    # 税额之和坐标
    total2_x1, total2_y1 = 1541, 715
    total2_x2, total2_y2 = 1571 + 19 * len("%.2f" % total2), 715
    total2_x3, total2_y3 = 1541, 745
    total2_x4, total2_y4 = 1571 + 19 * len("%.2f" % total2), 745
    total2_text = xy_end(total2_x1, total2_y1, total2_x2, total2_y2, total2_x3, total2_y3, total2_x4, total2_y4)

    # 金额+税额之和的坐标
    total_x1, total_y1 = 1410, 781
    total_x2, total_y2 = 1440 + 19 * len("%.2f" % total), 781
    total_x3, total_y3 = 1410, 811
    total_x4, total_y4 = 1440 + 19 * len("%.2f" % total), 811
    total_text = xy_end(total_x1, total_y1, total_x2, total_y2, total_x3, total_y3, total_x4, total_y4)

    # 大写金额税额之和的坐标
    big_x1, big_y1 = 654, 778
    big_x2, big_y2 = 654 + 26 * len(big_total), 778
    big_x3, big_y3 = 654, 803  # 778 + 26
    big_x4, big_y4 = 654 + 26 * len(big_total), 803
    big_text = xy_end(big_x1, big_y1, big_x2, big_y2, big_x3, big_y3, big_x4, big_y4)
    # 写入坐标
    with open(filename, 'a+') as f :
        f.write(total1_text + '￥' + ("%.2f" % total1) + '\n')
        f.write(total2_text + '￥' + ("%.2f" % total2) + '\n')
        f.write(total_text + '￥' + ("%.2f" % total) + '\n')
        f.write(big_text + big_total + '\n')


# 添加销售方内容
def add_seller() :  # 添加销售方名称
    """
    宽为27高为30
    """
    seller_name = fake.company()
    draw.text((436, 840), seller_name, fill = (8, 67, 161), font = global_var.ft6)
    x1, y1 = 436, 840
    x2, y2 = 436 + 27 * len(seller_name), 840
    x3, y3 = 436, 840 + 30
    x4, y4 = 436 + 27 * len(seller_name), 840 + 30
    text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(text + seller_name + '\n')


def seller_nums() :  # 添加纳税人识别号（销售方）
    """
    宽为20高为30
    """
    id_part = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', chr(random.randint(65, 90))]
    id1 = ''.join(str(random.choice(id_part)) for _ in range(18))
    id2 = ''.join(str(random.choice(id_part)) for _ in range(15))
    seller_num = random.choice([id1, id2])
    draw.text((470, 872), seller_num, fill = (8, 67, 141), font = global_var.ft7)
    x1, y1 = 470, 872
    x2, y2 = 470 + 20 * len(seller_num), 872
    x3, y3 = 470, 902
    x4, y4 = 470 + 20 * len(seller_num), 902
    text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(text + seller_num + '\n')


def add_and_phone() :  # 添加地址、电话（销售方）
    """
    电话宽为14，地址宽为27，高为30
    """
    phone1 = ''.join(str(random.choice(range(10))) for _ in range(3))
    phone2 = ''.join(str(random.choice(range(10))) for _ in range(7))
    address = fake.address()[0 : -7]
    add_len = len(address)
    address_phone = address + ' ' + phone1 + '-' + phone2
    draw.text((420, 915), address_phone, fill = (8, 67, 141), font = global_var.ft6)
    x1, y1 = 420, 915
    x2, y2 = 420 + 27 * (add_len + 1) + 14 * 7, 915
    x3, y3 = 420, 945
    x4, y4 = 420 + 27 * (add_len + 1) + 14 * 7, 945
    text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(text + address_phone + '\n')


def add_bankId() :  # 添加开户行及账号
    """
    银行名称字符宽为27，账号宽为14
    """
    bank1 = ['招商银行', '汉口银行', 'EBA银行']
    bank2 = ['龙阳大道支行', '北京东三环支行', '上海分行', '城北支行']
    bank = random.choice(bank1) + random.choice(bank2)
    bank_len = len(bank)
    # 15或18位账号
    acc = [''.join(str(random.choice(range(10))) for _ in range(15)),
           ''.join(str(random.choice(range(10))) for _ in range(18))]
    account = random.choice(acc)
    acc_len = len(account)
    bank_and_account = bank + ' ' + account
    draw.text((420, 950), bank_and_account, fill = (8, 67, 161), font = global_var.ft6)
    x1, y1 = 420, 950
    x2, y2 = 420 + 27 * (bank_len + 1) + 14 * acc_len, 950
    x3, y3 = 420, 980
    x4, y4 = 420 + 27 * (bank_len + 1) + 14 * acc_len, 980
    text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    with open(filename, 'a+') as f :
        f.write(text + bank_and_account + '\n')


def add_name() :
    # 添加收款人复核人开票人名字
    # 生成随机的三个名字
    name1 = fake.name()
    name2 = fake.name()
    name3 = fake.name()
    draw.text((305, 995), name1, fill = (8, 67, 161), font = global_var.ft6)
    draw.text((722, 995), name2, fill = (8, 67, 161), font = global_var.ft6)
    draw.text((1099, 995), name3, fill = (8, 67, 161), font = global_var.ft6)

    n1_x1, n1_y1 = 305, 995
    n1_x2, n1_y2 = 305 + 27 * len(name1), 995
    n1_x3, n1_y3 = 305, 1025
    n1_x4, n1_y4 = 305 + 27 * len(name1), 1025
    n1_text = xy_end(n1_x1, n1_y1, n1_x2, n1_y2, n1_x3, n1_y3, n1_x4, n1_y4)

    n2_x1, n2_y1 = 722, 995
    n2_x2, n2_y2 = 722 + 27 * len(name2), 995
    n2_x3, n2_y3 = 722, 1025
    n2_x4, n2_y4 = 722 + 27 * len(name2), 1025
    n2_text = xy_end(n2_x1, n2_y1, n2_x2, n2_y2, n2_x3, n2_y3, n2_x4, n2_y4)

    n3_x1, n3_y1 = 1099, 995
    n3_x2, n3_y2 = 1099 + 27 * len(name2), 995
    n3_x3, n3_y3 = 1099, 1025
    n3_x4, n3_y4 = 1099 + 27 * len(name2), 1025
    n3_text = xy_end(n3_x1, n3_y1, n3_x2, n3_y2, n3_x3, n3_y3, n3_x4, n3_y4)
    with open(filename, 'a+') as f :
        f.write(n1_text + name1 + '\n')
        f.write(n2_text + name2 + '\n')
        f.write(n3_text + name3 + '\n')


# 添加发票代码
def add_fapiao_daima() :
    num_str = ''.join(str(random.choice(range(10))) for _ in range(10))  # 随机生成10位数字发票代码
    draw.text((344, 82), num_str, fill = (72, 75, 68), font = global_var.ft1)  # 添加发票代码
    draw.text((1603, 110), num_str, fill = (31, 83, 182), font = global_var.ft3)  # 添加号码后面的小代码
    # 大的发票代码的坐标
    x1, y1 = 344, 82
    x2, y2 = 624, 82
    x3, y3 = 344, 130
    x4, y4 = 624, 130
    x_text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    # 小的发票代码的坐标
    sx1, sy1 = 1600, 110
    sx2, sy2 = 1735, 110
    sx3, sy3 = 1600, 133
    sx4, sy4 = 1730, 133
    sx_text = xy_end(sx1, sy1, sx2, sy2, sx3, sy3, sx4, sy4)

    with open(filename, 'a+') as f :
        f.write(x_text + num_str + '\n')
        f.write(sx_text + num_str + '\n')


# 添加发票号码
def add_fapiao_hao() :
    no_str = ''.join(str(random.choice(range(10))) for _ in range(8))  # 随机生成8位数字发票号码
    draw.text((1370, 86), no_str, fill = (48, 87, 161), font = global_var.ft2)  # 添加发票号码
    draw.text((1585, 146), no_str, fill = (8, 67, 161), font = global_var.ft4)  # 添加小号码
    # 大的号码坐标
    x1, y1 = 1366, 88
    x2, y2 = 1591, 88
    x3, y3 = 1366, 135
    x4, y4 = 1591, 135
    x_text = xy_end(x1, y1, x2, y2, x3, y3, x4, y4)
    # 小的号码坐标
    sx1, sy1 = 1585, 146
    sx2, sy2 = 1707, 146
    sx3, sy3 = 1585, 174
    sx4, sy4 = 1707, 174
    sx_text = xy_end(sx1, sy1, sx2, sy2, sx3, sy3, sx4, sy4)
    with open(filename, 'a+') as f :
        f.write(x_text + no_str + '\n')
        f.write(sx_text + no_str + '\n')


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
    im.save('test\\pic_origin\\res' + str(index) + '.jpg')  # 保存添加完的图片

    # 图片仿射变换
    img = cv.imread('test\\pic_origin\\res' + str(index) + '.jpg')
    split_picture.split_to_box(img, index)
    rot_mat = cv.getRotationMatrix2D((cx, cy), rotate_angle, 1)
    img_rotated_by_alpha = cv.warpAffine(img, rot_mat, (img.shape[1], img.shape[0]))
    blur_num = int(random.choice(['1', '3', '5', '7']))  # 模糊的程度
    dst_img = cv.GaussianBlur(img_rotated_by_alpha, (blur_num, blur_num), 0)
    # dir_name = 'test\\res\\res' + str(index)
    # os.mkdir(dir_name)

    cv.imwrite('test\\res\\pic' + str(index) + '.jpg', dst_img)  # 保存高斯模糊处理+仿射变换后的图片
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
        filename = 'test\\res\\pic' + str(index) + '.txt'
        main()
