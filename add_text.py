#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：pfq time:2020/7/1

import global_var
import time
import random
import cv2 as cv
from PIL import Image
from PIL import ImageDraw
from faker import Faker
from numpy import sin, cos

fake = Faker(locale = 'zh_CN')  # 初始化中文简体


# from PIL import Image
# from PIL import ImageFilter
# from PIL import ImageEnhance
# from PIL import ImageDraw, ImageFont

class BBox(object):
    def __init__(self, bbox):
        self.left = bbox[0]
        self.top = bbox[1]
        self.right = bbox[2]
        self.bottom = bbox[3]


def rotate(x, y, angle, cx, cy):
    """
    点(x,y) 绕(cx,cy)点旋转
    """
    # angle = angle*pi/180
    x_new = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
    y_new = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy
    return x_new, y_new


# 生成日期函数
def print_date(draw):
    a1 = (2019, 1, 1, 0, 0, 0, 0, 0, 0)  # 设置开始日期时间元组（2019-01-01 00：00：00）
    a2 = (2020, 12, 31, 2, 3, 5, 9, 5, 9)  # 设置截止日期时间元组（2020-12-31 23:59:59）

    start = time.mktime(a1)  # 生成开始时间戳
    end = time.mktime(a2)  # 生成结束时间戳

    t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
    date_tuple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime("%Y年%m月%d日", date_tuple)  # 将时间元组转成格式化字符串（*年*月*日）
    draw.text((1501, 191), date, fill = (31, 83, 182), font = global_var.ft5)


# 生成公司、销售方名字
def createName():
    name = fake.company()  # 生成随机的公司名称
    return name


# 购买方区域文字添加
def purchase(draw):
    name = createName()
    draw.text((436, 253), name, fill = (8, 67, 161), font = global_var.ft6)
    name_length = len(name)
    x_start, y_start = 436, 253
    x_end, y_end = 436 + (name_length * 27), 253 + 30
    x1, y1 = x_start, y_start
    x2, y2 = x_end, y_start
    x3, y3 = x_start, y_end
    x4, y4 = x_end, y_end
    # x11, y11 = rotate(x, y, w, h, angle)

    # 添加纳税人识别号
    id_num = ''.join(str(random.choice(range(10))) for _ in range(15))  # 随机生成15位纳税人识别号
    draw.text((461, 290), id_num, fill = (8, 67, 161), font = global_var.ft7)

    # 添加地址电话
    phone1 = ''.join(str(random.choice(range(10))) for _ in range(3))
    phone2 = ''.join(str(random.choice(range(10))) for _ in range(4))
    phone3 = ''.join(str(random.choice(range(10))) for _ in range(7))
    phone4 = ''.join(str(random.choice(range(10))) for _ in range(8))
    phone_num1 = [phone1, phone2]
    phone_num2 = [phone3, phone4]
    address_phone = fake.address() + ' ' + random.choice(phone_num1) + '-' + random.choice(phone_num2)
    draw.text((433, 338), address_phone, fill = (8, 67, 161), font = global_var.ft8)

    # 添加开户行及账号
    bank1 = ['招商银行', '汉口银行', 'EBA银行']
    bank2 = ['龙阳大道支行', '北京东三环支行', '上海分行', '城北支行']
    # 15或18位账号
    acc = [''.join(str(random.choice(range(10))) for _ in range(15)),
           ''.join(str(random.choice(range(10))) for _ in range(18))]
    bank_account = random.choice(bank1) + random.choice(bank2) + ' ' + random.choice(acc)
    draw.text((436, 380), bank_account, fill = (8, 67, 161), font = global_var.ft6)


# 添加密码区
def password(draw):
    stru = ['+', '-', '*', '/', '<', '>', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # 组成密码的符号和数字
    pwd1 = ''.join(str(random.choice(stru)) for _ in range(27))
    pwd2 = ''.join(str(random.choice(stru)) for _ in range(27))
    pwd3 = ''.join(str(random.choice(stru)) for _ in range(27))
    pwd4 = ''.join(str(random.choice(stru)) for _ in range(27))
    draw.text((1127, 257), pwd1, fill = (8, 67, 161), font = global_var.ft9)
    draw.text((1127, 290), pwd2, fill = (8, 67, 161), font = global_var.ft9)
    draw.text((1127, 323), pwd3, fill = (8, 67, 161), font = global_var.ft9)
    draw.text((1127, 356), pwd4, fill = (8, 67, 161), font = global_var.ft9)


# 添加货物或应税劳务及后面对应的规格价格等内容
def add_goods(draw):
    # goods = ['*住宿服务*住宿费', '*经纪代理服务*代订附加产品', '*物流辅助服务*收派服务费', '住宿费', '*石油制品*车用油', '*中成药*藿香正气软胶囊']
    # types = ['13ml', '30ml', '30ml', '2.5g', '10g', '1g+1g+1g', '6g*12袋 水丸', '20g*1支', '8736', '轻柴油', '0号车用柴油', '']
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

    for i in range(random.randint(1, 5)):
        y = 461 + (30 * i)
        goods = fake.sentence()
        if len(goods) > 14:
            goods = goods[0: 14]
        else:
            goods = goods[0: -1]
        draw.text((185, y), goods, fill = (8, 67, 161), font = global_var.ft6)  # 添加货物
        draw.text((596, y), fake.word() + random.choice(types), fill = (8, 67, 161), font = global_var.ft6)  # 添加型号规格
        draw.text((804, y), random.choice(fake.word()), fill = (8, 67, 161), font = global_var.ft6)  # 添加单位

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
def digital_to_chinese(digital):
    str_digital = str(digital)
    chinese = {'1': '壹', '2': '贰', '3': '叁', '4': '肆', '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖',
               '0': '零'}
    chinese2 = ['拾', '佰', '仟', '万', '厘', '分', '角']
    jiao = ''
    bs = str_digital.split('.')
    yuan = bs[0]
    if len(bs) > 1:
        jiao = bs[1]
    r_yuan = [i for i in reversed(yuan)]
    count = 0
    for i in range(len(yuan)):
        if i == 0:
            r_yuan[i] += '圆'
            continue
        r_yuan[i] += chinese2[count]
        count += 1
        if count == 4:
            count = 0
            chinese2[3] = '亿'

    s_jiao = [i for i in jiao][:2]  # 去掉小于分之后的

    j_count = -1
    for i in range(len(s_jiao)):
        s_jiao[i] += chinese2[j_count]
        j_count -= 1
    last = [i for i in reversed(r_yuan)] + s_jiao
    last_str = ''.join(last)
    # print(str_digital)
    # print(last_str)
    for i in range(len(last_str)):
        digital = last_str[i]
        if digital in chinese:
            last_str = last_str.replace(digital, chinese[digital])
    if '零角零分' in last_str:
        last_str.replace('零角零分', '圆整')
    elif '零分' in last_str:
        last_str.replace('零分', '')
    # elif '零角' in last_str and '分' not in last_str :
    #     last_str.replace('零角', '圆整')
    # print(last_str)
    return last_str


# 添加销售方内容
def add_seller(draw):  # 添加销售方名称
    seller_name = createName()
    draw.text((436, 840), seller_name, fill = (8, 67, 161), font = global_var.ft6)


def seller_nums(draw):  # 添加纳税人识别号（销售方）
    id_part = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', chr(random.randint(65, 90))]
    id1 = ''.join(str(random.choice(id_part)) for _ in range(18))
    id2 = ''.join(str(random.choice(id_part)) for _ in range(15))
    id = [id1, id2]
    draw.text((470, 872), random.choice(id), fill = (8, 67, 141), font = global_var.ft7)


def add_and_phone(draw):  # 添加地址、电话（销售方）
    # add1 = ['北辰区', '嘉定区', '武汉市洪山区', '南京市雨花台区', '哈尔滨市松北区', '郑州经济技术开发区',
    #         '武汉市新洲区', '安徽省合肥市', '上海市长宁区', '天津自贸区', '深圳龙岗区']
    # add2 = ['医药医疗器械工业园', '第九大街99号', '胜辛路500号15幢', '金钟路968号', '空港国际物流园',
    #         '民院路124号', '安德门大街52号', '龙兴路1819号', '坂田街道']
    add = fake.address()
    phone1 = ''.join(str(random.choice(range(10))) for _ in range(3))
    phone2 = ''.join(str(random.choice(range(10))) for _ in range(4))
    phone3 = ''.join(str(random.choice(range(10))) for _ in range(7))
    phone4 = ''.join(str(random.choice(range(10))) for _ in range(8))
    phone_num1 = [phone1, phone2]
    phone_num2 = [phone3, phone4]
    add_phone = add + ' ' + random.choice(phone_num1) + random.choice(phone_num2)
    draw.text((420, 915), add_phone, fill = (8, 67, 141), font = global_var.ft6)


def add_bankId(draw):  # 添加开户行及账号
    bank1 = ['招商银行', '汉口银行', 'EBA银行']
    bank2 = ['龙阳大道支行', '北京东三环支行', '上海分行', '城北支行']
    # 15或18位账号
    acc = [''.join(str(random.choice(range(10))) for _ in range(15)),
           ''.join(str(random.choice(range(10))) for _ in range(18))]
    bank_and_account = random.choice(bank1) + random.choice(bank2) + ' ' + random.choice(acc)
    draw.text((420, 950), bank_and_account, fill = (8, 67, 161), font = global_var.ft6)


def add_name(draw):
    # 添加收款人复核人开票人名字
    # 生成随机的三个名字
    name1 = fake.name()
    name2 = fake.name()
    name3 = fake.name()
    draw.text((305, 995), name1, fill = (8, 67, 161), font = global_var.ft6)
    draw.text((722, 995), name2, fill = (8, 67, 161), font = global_var.ft6)
    draw.text((1099, 995), name3, fill = (8, 67, 161), font = global_var.ft6)


# 主函数
def main():
    for i in range(5):
        template_num = random.randint(1, 4)
        im = Image.open('template_pics\\template_' + str(template_num) + '.jpg')
        draw = ImageDraw.Draw(im)
        angle = random.randint(-10, 10)  # 生成随机的旋转角度
        img_tmp = cv.imread('template_pics\\template_' + str(template_num) + '.jpg')
        h, w, c = img_tmp.shape  # 获取图片的高和宽
        num_str = ''.join(str(random.choice(range(10))) for _ in range(10))  # 随机生成10位数字发票代码
        no_str = ''.join(str(random.choice(range(10))) for _ in range(8))  # 随机生成8位数字发票号码

        draw.text((344, 82), num_str, fill = (72, 75, 68), font = global_var.ft1)  # 添加发票代码
        draw.text((1370, 86), no_str, fill = (48, 87, 161), font = global_var.ft2)  # 添加发票号码
        draw.text((1603, 110), num_str, fill = (31, 83, 182), font = global_var.ft3)  # 添加号码后面的小代码
        draw.text((1585, 146), no_str, fill = (8, 67, 161), font = global_var.ft4)  # 添加小号码
        print_date(draw)  # 生成日期函数
        purchase(draw)  # 购买方区域文字添加
        password(draw)  # 添加密码区
        add_goods(draw)  # 添加货物或应税劳务及后面对应的规格价格等内容
        add_seller(draw)  # 添加销售方内容
        seller_nums(draw)  # 添加纳税人识别号（销售方）
        add_and_phone(draw)  # 添加地址、电话（销售方）
        add_bankId(draw)  # 添加开户行及账号
        add_name(draw)  # 添加收款人复核人开票人名字
        # global_var.im.show()
        im.save('pic_origin\\res' + str(i) + '.jpg')  # 保存添加完的图片

        # 图片仿射变换
        img = cv.imread('pic_origin\\res' + str(i) + '.jpg')
        box = [0, 0, w, h]  # 获取边框坐标
        bbox = BBox(box)
        # center = ((bbox.left + bbox.right) / 2, (bbox.top + bbox.bottom) / 2)
        center = (w / 2, h / 2)
        rot_mat = cv.getRotationMatrix2D(center, angle, 1)
        img_rotated_by_alpha = cv.warpAffine(img, rot_mat, (img.shape[1], img.shape[0]))
        # cv.imwrite('pic_transform\\res' + str(i) + '.jpg', img_rotated_by_alpha)  # 保存仿射变换的图片

        # dst = cv.GaussianBlur(img, (5, 5), 0)  # 高斯模糊
        # cv.imwrite('pic_blur\\res' + str(i) + '.jpg', dst)  # 保存模糊处理后的图片

        # img_1 = cv.imread('pic_transform\\res' + str(i) + '.jpg')
        # dst_1 = cv.GaussianBlur(img_1, (5, 5), 0)
        blur_num = int(random.choice(['1', '3', '5', '7']))
        dst_1 = cv.GaussianBlur(img_rotated_by_alpha, (blur_num, blur_num), 0)
        cv.imwrite('pic_blurplus\\res' + str(i) + '.jpg', dst_1)  # 保存高斯模糊处理+仿射变换后的图片
        print(i)


if __name__ == '__main__':
    main()
