import pygame
import sys
from copy import *
from pygame.locals import *

pygame.init()

# 颜色常量
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (24, 116, 255)
pink = (139, 95, 101)

# 基本距离变量
size = 9  # 9*9标准线
unit = 80  # 正方形单元格边长
console_width = 200  # 右侧控制台宽度
border_width = 50  # 棋盘边缘预留宽度
console_x = [border_width + (size - 1) * unit, border_width + (size - 1) * unit + console_width]  # 计算控制台的有效范围
console_y = [border_width, border_width + (size - 1) * unit]
window_width = border_width * 2 + console_width + (size - 1) * unit  # 计算窗口宽：两个预留宽度+棋盘宽度+面板宽度
window_high = border_width * 2 + (size - 1) * unit  # 计算窗口宽：两个预留宽度+棋盘宽度

# 窗口，字体
screen = pygame.display.set_mode((window_width + 500, window_high))  # 设置窗口的大小，单位为像素
pygame.display.set_caption('不围棋No Go')  # 窗口标题
ziti = pygame.font.Font("素材\simsun.ttc", 20)  # 字体和字号

# 音效文件
sound_black = pygame.mixer.Sound('素材\黑.wav')  # 黑棋声音
sound_white = pygame.mixer.Sound('素材\白.wav')  # 白棋落子声音
sound_win = pygame.mixer.Sound('素材\胜利.mp3')  # 胜利声音
sound_defeat = pygame.mixer.Sound('素材\失败.mp3')  # 失败声音
sound_white_voice = [pygame.mixer.Sound('素材\白子耀眼，若恒星亘古不变.mp3'), pygame.mixer.Sound('素材\黑子深邃，为长夜苍茫莫测.mp3'),
                     pygame.mixer.Sound('素材\方寸棋盘，便是我的天地.mp3'), pygame.mixer.Sound('素材\不得贪胜，不可不胜.mp3'),
                     pygame.mixer.Sound('素材\可以投子认输了.mp3'), pygame.mixer.Sound('素材\没有对胜利的渴求，很快将百无一用.mp3'),
                     pygame.mixer.Sound('素材\棋盘上栖息的，除却输赢，还有阴阳.mp3'), pygame.mixer.Sound('素材\让天下一先.mp3'),
                     pygame.mixer.Sound('素材\若世有神明，亦会胜它半字.mp3'), pygame.mixer.Sound('素材\胜负，半目足以.mp3'),
                     pygame.mixer.Sound('素材\输掉的话，会难过到哭泣吧.mp3'), pygame.mixer.Sound('素材\算得清每颗棋子的价值吗，对你是件困难的事吧.mp3'),
                     pygame.mixer.Sound('素材\纵横十九道内的，是无穷宇宙.mp3')]
sound_white_voice_text = ['白子耀眼，若恒星亘古不变', '黑子深邃，为长夜苍茫莫测', '方寸棋盘，便是我的天地', '不得贪胜，不可不胜', '可以投子认输了', '没有对胜利的渴求，很快将百无一用',
                          '棋盘上栖息的，除却输赢，还有阴阳', '让天下一先', '若世有神明，亦会胜它半字', '胜负，半目足以', '输掉的话，会难过到哭泣吧',
                          '算得清每颗棋子的价值吗，对你是件困难的事吧', '纵横十九道内的，是无穷宇宙']
pygame.mixer.Sound('素材\背景音乐.mp3').play()

# 按钮常量
start_btn_begin_x = 100  # 开始按键起始x值
start_btn_begin_y = 600  # 开始按键起始y值
console_btn_begin_x = console_x[0] + 50  # 控制台按键起始x值
console_btn_begin_y = console_y[0] + 400  # 控制台按键起始y值
btn_high = 50  # 按键高
btn_width = 150  # 按键宽
btn_gap = 20  # 按键间隔
btn_text_x = 35  # 按键文本宽
btn_text_y = 15  # 按键文本高
start_text_x = start_btn_begin_x + btn_text_x  # 按键文本x值
console_text_x = console_btn_begin_x + btn_text_x  # 按键文本x值
man_machine_x = [start_btn_begin_x, start_btn_begin_x + btn_width]  # ”人机模式“按键，x坐标范围
man_machine_y = [start_btn_begin_y, start_btn_begin_y + btn_high]  # y坐标范围
man_man_x = [start_btn_begin_x, start_btn_begin_x + btn_width]  # “人人模式”按键，x坐标范围，不变
man_man_y = [start_btn_begin_y + btn_high + btn_gap, start_btn_begin_y + btn_high + btn_gap + btn_high]  # y坐标范围，加间隔和框高
new_start_x = [console_btn_begin_x, console_btn_begin_x + btn_width]  # “新的一局”按键，x坐标范围
new_start_y = [console_btn_begin_y, console_btn_begin_y + btn_high]  # y坐标范围
exit_game_x = [console_btn_begin_x, console_btn_begin_x + btn_width]  # “退出游戏”按键，x坐标范围，不变
exit_game_y = [console_btn_begin_y + btn_high + btn_gap,
               console_btn_begin_y + btn_high + btn_gap + btn_high]  # y坐标范围，加一遍间隔和框高
huiqi_x = [console_btn_begin_x, console_btn_begin_x + btn_width]  # “悔棋”按键，x坐标范围，不变
huiqi_y = [console_btn_begin_y + (btn_high + btn_gap) * 2,
           console_btn_begin_y + (btn_high + btn_gap) * 2 + btn_high]  # y坐标范围，再加一遍间隔和框高


# 绘制开始界面
def draw_start():
    screen.blit(pygame.image.load(r"素材\开始界面.jpg"), (0, 0))  # 背景图片填充
    pygame.draw.rect(screen, pink, [man_machine_x[0], man_machine_y[0], btn_width, btn_high])  # 绘制"人机模式”按键框
    screen.blit(ziti.render(f'人机对战', False, black), [start_text_x, start_btn_begin_y + btn_text_y])  # 绘制文本
    pygame.draw.rect(screen, pink, [man_man_x[0], man_man_y[0], btn_width, btn_high])  # 绘制"人人模式”按键框
    screen.blit(ziti.render(f'人人对战', False, black),
                [start_text_x, start_btn_begin_y + btn_high + btn_gap + btn_text_y])  # 绘制文本


# 绘制控制台按钮，不同的模式需要不同的颜色参数
def draw_btn(color):
    pygame.draw.rect(screen, color, [new_start_x[0], new_start_y[0], btn_width, btn_high])  # 绘制按键框
    screen.blit(ziti.render(f'新开一局', False, white), [console_text_x, console_btn_begin_y + btn_text_y])  # 绘制文字
    pygame.draw.rect(screen, color, [exit_game_x[0], exit_game_y[0], btn_width, btn_high])  # 绘制按键框
    screen.blit(ziti.render(f'退出游戏', False, white),
                [console_text_x, console_btn_begin_y + btn_high + btn_gap + btn_text_y])  # 绘制文字
    pygame.draw.rect(screen, color, [huiqi_x[0], huiqi_y[0], btn_width, btn_high])  # 绘制按键框
    screen.blit(ziti.render(f'悔一步棋', False, white),
                [console_text_x, console_btn_begin_y + (btn_high + btn_gap) * 2 + btn_text_y])  # 绘制文字


# 绘制棋盘
def draw_map():
    screen.blit(pygame.image.load(r"素材\棋盘.jpg"), (0, 0))  # 背景图片填充
    for item in range(0, size):  # 绘制行和纵坐标
        pygame.draw.line(screen, black, [border_width, border_width + item * unit],
                         [border_width + (size - 1) * unit, border_width + item * unit], 1)
        screen.blit(ziti.render(f'{item + 1}', True, black), [border_width - 30, border_width + item * unit - 10])
    for item in range(0, size):  # 绘制列和横坐标
        pygame.draw.line(screen, black, [border_width + item * unit, border_width],
                         [border_width + item * unit, border_width + (size - 1) * unit], 1)
        screen.blit(ziti.render(f'{item + 1}', True, black), [border_width + item * unit - 5, border_width - 30])


# 判断开始界面的按钮是否被点击，人机模式返回1，人人模式返回-1
def start_is_click(pos):
    if man_machine_x[0] < pos[0] < man_machine_x[1] and man_machine_y[0] < pos[1] < man_machine_y[1]:
        return 1
    elif man_man_x[0] < pos[0] < man_man_x[1] and man_man_y[0] < pos[1] < man_man_y[1]:
        return -1


# 人机对战游戏逻辑
class Men_Machine_Chess:

    def __init__(self):
        self.chess_position = [[0 for y in range(0, 9)] for x in
                               range(0, 9)]  # 9 * 9的二维列表，用于表示棋盘：0 ~ 无棋子， 1 ~ 黑棋，-1 ~ 白棋
        self.current_record = []  # 列表表达式二维列表记录走棋的路径，用于悔棋和搜索。它的元素是一个元组(棋子类型，chess_position.search_hang，chess_position.search_lie)
        self.chess_status = 0  # 棋子状态，黑棋先走，最开始会赋值为1：0 ~ 未开局和未分出胜负；1 ~ 等待黑棋落子；-1 ~ 等待白棋落子；3 ~ 结束（人类胜）；4 ~ 结束（人类输）
        self.number_white = 0  # 白子个数
        self.number_black = 0  # 黑子个数
        self.visit = [[0 for y in range(0, 9)] for x in range(0, 9)]  # 搜索记录列表，0是没搜索过，1是搜索过

    # 对气进行搜索，由中心向四周深入，如果不是边界，不是异色，是空格气就加一，同色就递归调用
    def search_qi(self, i, j):
        self.visit[i][j] = 1
        search_hang = [1, 0, -1, 0]  # 纵向搜索步伐，行
        search_lie = [0, 1, 0, -1]  # 横向搜索步伐，列
        chess_qi = 0  # 记录气数
        hang = 0
        lie = 0
        for k in range(4):
            hang = i + search_hang[k]
            lie = j + search_lie[k]
            if (hang < 0 or hang > 8) or (lie < 0 or lie > 8): continue
            if self.chess_position[hang][lie] == 0 and self.visit[hang][lie] == 0:
                chess_qi += 1
                self.visit[hang][lie] = 1
            elif self.chess_position[hang][lie] == self.chess_position[i][j] and self.visit[hang][lie] == 0:
                chess_qi += self.search_qi(hang, lie)
        return chess_qi

    # 判断输赢的算法,即对所有有棋子的位置上的棋子的气进行搜索（向四周），如果没有则游戏结束
    def is_win(self):
        is_chess_death = 0  # 0表示未结束,1表示有子死
        chess_live = [[-1 for y in range(0, 9)] for x in range(0, 9)]  # 气的记录列表，-1是指这里没子，正数表示这里的棋子的气的数量
        for i in range(9):
            for j in range(9):
                if self.chess_position[i][j] == 0:
                    chess_live[i][j] = -1
                    continue
                else:
                    self.visit = [[0 for y in range(0, 9)] for x in range(0, 9)]
                    chess_live[i][j] = self.search_qi(i, j)
                    if chess_live[i][j] == 0:
                        is_chess_death = 1
        self.chess_status = 1 if self.number_black > self.number_white else -1
        if self.chess_status == 1:
            self.chess_status = 4 if is_chess_death == 1 else -1
        elif self.chess_status == -1:
            self.chess_status = 3 if is_chess_death == 1 else 1

    # 判断是不是怎么下都是输
    def pre_game_over(self, mp_):  # 提前判断游戏是否结束 返回值  1~等待黑棋落子，-1~等待白棋落子，3~结束，人类胜，4~结束，人类输

        visit = [[1 for i in range(9)] for j in range(9)]
        gas = [[-1 for i in range(9)] for j in range(9)]

        def update_gas_3(mp_):  # 模拟落子后更新气,返回值  1~等待黑棋落子，-1~等待白棋落子，3~结束，人类胜，4~结束，人类输
            x = [1, 0, -1, 0]
            y = [0, 1, 0, -1]

            def dfs(ii, jj):
                visit[ii][jj] = 0
                t = 0  # 记录气数
                for k in range(4):
                    dx = ii + x[k]
                    dy = jj + y[k]
                    if (dx < 0 or dx > 8) or (dy < 0 or dy > 8):  # 越界
                        continue
                    if mp_[dx][dy] == 0 and visit[dx][dy]:
                        t += 1
                        visit[dx][dy] = 0
                    elif mp_[dx][dy] == mp_[ii][jj] and visit[dx][dy]:
                        t += dfs(dx, dy)
                return t

            status_2 = 0  # 0表示未结束
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 0:
                        gas[i][j] = -1
                        continue
                    else:
                        for ii in range(9):
                            for jj in range(9):
                                visit[ii][jj] = 1  # 更新visit
                        gas[i][j] = dfs(i, j)
                        if gas[i][j] == 0:
                            status_2 = 1  # status_2表示是否结束，1表示有子死，0表示无
            num_w = 0
            num_b = 0  # 黑白子数
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 1:
                        num_b += 1
                    elif mp_[i][j] == -1:
                        num_w += 1
            if num_b > num_w:
                status_1 = 1  # status_1表示当前落子方，1为黑子，0为白子
            else:
                status_1 = 0
            if status_1 == 1 and status_2 == 1:
                return 4
            if status_1 == 0 and status_2 == 1:
                return 3
            if status_1 == 1:
                return -1
            if status_1 == 0:
                return 1

        num_w = 0
        num_b = 0  # 黑白子数
        for i in range(9):
            for j in range(9):
                if mp_[i][j] == 1:
                    num_b += 1
                elif mp_[i][j] == -1:
                    num_w += 1
        status_1 = num_b - num_w  # status_1表示当前落子方，1为黑子，0为白子  判断落子方, status_1为1时下一手应该为白，status_1为0时下一手应为黑
        for i in range(9):
            for j in range(9):
                if mp_[i][j] == 0:
                    mp_[i][j] = 1 - 2 * status_1
                    t = update_gas_3(mp_)
                    mp_[i][j] = 0
                    if t == 1 or t == -1:
                        return -t
        return 4 - status_1

    # 电脑选哪个位置落子
    def yixing_GO(self):
        mp_2 = deepcopy(self.chess_position)
        mp_3 = deepcopy(self.chess_position)
        visit = [[1 for i in range(9)] for j in range(9)]
        gas = [[-1 for i in range(9)] for j in range(9)]

        def update_gas_3(mp_):  # 模拟落子后更新气,返回值  1~等待黑棋落子，-1~等待白棋落子，3~结束，人类胜，4~结束，人类输
            x = [1, 0, -1, 0]
            y = [0, 1, 0, -1]

            def dfs(ii, jj):
                visit[ii][jj] = 0
                t = 0  # 记录气数
                for k in range(4):
                    dx = ii + x[k]
                    dy = jj + y[k]
                    if (dx < 0 or dx > 8) or (dy < 0 or dy > 8):  # 越界
                        continue
                    if mp_[dx][dy] == 0 and visit[dx][dy]:
                        t += 1
                        visit[dx][dy] = 0
                    elif mp_[dx][dy] == mp_[ii][jj] and visit[dx][dy]:
                        t += dfs(dx, dy)
                return t

            status_2 = 0  # 0表示未结束
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 0:
                        gas[i][j] = -1
                        continue
                    else:
                        for ii in range(9):
                            for jj in range(9):
                                visit[ii][jj] = 1  # 更新visit
                        gas[i][j] = dfs(i, j)
                        if gas[i][j] == 0:
                            status_2 = 1  # status_2表示是否结束，1表示有子死，0表示无
            num_w = 0
            num_b = 0  # 黑白子数
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 1:
                        num_b += 1
                    elif mp_[i][j] == -1:
                        num_w += 1
            if num_b > num_w:
                status_1 = 1  # status_1表示当前落子方，1为黑子，0为白子
            else:
                status_1 = 0
            if status_1 == 1 and status_2 == 1:
                return 4
            if status_1 == 0 and status_2 == 1:
                return 3
            if status_1 == 1:
                return -1
            if status_1 == 0:
                return 1

        def pre_game_over(mp_):  # 提前判断游戏是否结束 返回值  1~等待黑棋落子，-1~等待白棋落子，3~结束，人类胜，4~结束，人类输
            num_w = 0
            num_b = 0  # 黑白子数
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 1:
                        num_b += 1
                    elif mp_[i][j] == -1:
                        num_w += 1
            status_1 = num_b - num_w  # status_1表示当前落子方，1为黑子，0为白子  判断落子方, status_1为1时下一手应该为白，status_1为0时下一手应为黑
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 0:
                        mp_[i][j] = 1 - 2 * status_1
                        t = update_gas_3(mp_)
                        mp_[i][j] = 0
                        if t == 1 or t == -1:
                            return -t
            return 4 - status_1

        def value_base_mp(mp_):
            p = 0
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 0:
                        mp_[i][j] = 1
                        t = update_gas_3(mp_)
                        if t == 3 or t == 4:
                            p += 1
                        mp_[i][j] = -1
                        t = update_gas_3(mp_)
                        if t == 3 or t == 4:
                            p += 1
                        mp_[i][j] = 0
            return p

        def pg_base_point(mp_, L_p):  # 取某个点的价值
            if mp_[L_p[0]][L_p[1]] != 0:
                return 0
            p = 0
            mp_[L_p[0]][L_p[1]] = -1
            p += value_base_mp(mp_)
            mp_[L_p[0]][L_p[1]] = 0
            return p

        def find_all_point(mp_):  # 获取价值最大点的列表
            L = []
            max_ = -1
            for i in range(9):
                for j in range(9):
                    if mp_[i][j] == 0:
                        mp_[i][j] = -1
                        if update_gas_3(mp_) > 1:
                            mp_[i][j] = 0
                            continue
                        mp_[i][j] = 0
                        L_p = [i, j]
                        t = pg_base_point(mp_, L_p)
                        if t == max_:
                            L = L + [L_p]
                        elif t > max_:
                            L = [L_p]
                            max_ = t
            return L

        def select_point(mp_, L):
            if len(L) == 1:
                return L[0]
            max_ = 0
            t = 0
            Ld = []
            for l in range(len(L)):
                min_ = 20
                for i in range(9):
                    for j in range(9):
                        if mp_[i][j] != 0:
                            if min_ > abs(L[l][0] - i) + abs(L[l][1] - j):
                                min_ = abs(L[l][0] - i) + abs(L[l][1] - j)
                Ld.append(min_)
            for l in range(len(L)):
                if Ld[l] > max_:
                    max_ = Ld[l]
                    t = l
            return L[t]

        l = select_point(mp_3, find_all_point(mp_2))
        return l[0], l[1]

    # 下棋，并判断下棋的正确与否，棋局是否结束（包括人输，人赢），以及切换落子状态
    def move(self, x, y):
        if (self.chess_status != 1 and self.chess_status != -1) or (9 <= x or x < 0 or 9 <= y or y < 0) or (
                self.chess_position[x][y] != 0): return -1  # 不在落子状态（已经结束），落在棋盘外，落在棋子上
        if self.chess_status == 1:  # 棋盘状态更新，根据落子状态更新棋盘，棋子数目
            self.chess_position[x][y] = 1
            self.number_black += 1
        elif self.chess_status == -1:
            self.chess_position[x][y] = -1
            self.number_white += 1
        self.current_record.append((self.chess_position[x][y], x, y))  # 实时记录添加
        self.is_win()  # 赢了不
        if self.chess_status != 3 and self.chess_status != 4: self.chess_status = -1 if self.current_record[-1][
                                                                                            0] == 1 else 1  # 切换状态，黑棋落子完换成白棋，白棋落子完换成黑棋
        return 0

    # 悔棋，游戏结束就不能悔棋了
    def huiqi(self):

        if len(self.current_record) == 0: return  # 棋盘上无子，报错
        last_chess = self.current_record.pop()  # 棋盘上有子，从实时记录中弹出并清除最后一个棋子
        self.chess_position[last_chess[1]][last_chess[2]] = 0  # 历史记录中位置清除，状态保留，即last_chess[0]不变，下次绘制不画该棋子
        if len(self.current_record) != 0: last_chess = self.current_record.pop()  # 棋盘上有子，从实时记录中弹出并清除最后一个棋子
        self.chess_position[last_chess[1]][last_chess[2]] = 0  # 历史记录中位置清除，状态保留，即last_chess[0]不变，下次绘制不画该棋子
        self.chess_status = 1  # 刷新当前棋子状态，如果当前悔的是黑棋，那么状态切换为等待黑棋落子
        self.number_white -= 1  # 棋子数目-1
        self.number_black -= 1


# 界面，声音，按键操作
class Men_Machine_PlayChess(Men_Machine_Chess):

    def __init__(self):
        Men_Machine_Chess.__init__(self)  # 继承
        pygame.init()
        draw_map()  # 绘制棋盘
        self.draw_panel()  # 绘制右侧的控制台

    # 绘制棋子，游戏结束时同时绘制棋谱
    def draw_chess(self):
        index = 1  # 记录走棋路径
        for item in self.current_record:  # 得到棋子坐标
            pygame.draw.circle(screen, black, [border_width + item[1] * unit, border_width + item[2] * unit],
                               int(unit / 2.5)) if item[0] == 1 else pygame.draw.circle(screen, white,
                                                                                        [border_width + item[1] * unit,
                                                                                         border_width + item[2] * unit],
                                                                                        int(unit / 2.5))  # 根据状态判断画哪个颜色
            if self.chess_status == 3 or self.chess_status == 4: screen.blit(ziti.render(f'{index}', False, white),
                                                                             [border_width + item[1] * unit - 5,
                                                                              border_width + item[2] * unit - 10]) if \
            item[0] == 1 else screen.blit(ziti.render(f'{index}', False, black), [border_width + item[1] * unit - 5,
                                                                                  border_width + item[
                                                                                      2] * unit - 10])  # 走棋路径
            index += 1

    # 绘制右侧的状态面板
    def draw_panel(self):
        screen.blit(pygame.image.load(r"素材\人机模式.jpg"), (console_x[0] + 30, 0))  # 背景
        if len(self.current_record) == 0 or self.chess_status == 0:
            screen.blit(ziti.render('开始挑战吧', False, black), [console_x[0] + 50, console_y[0] + 150])  # 根据走棋状态来显示语句
        elif self.chess_status == 1:
            if len(self.current_record) != 0:
                screen.blit(ziti.render(f'{self.current_record[-1][1] + 1, self.current_record[-1][2] + 1}', False, black),
                            [console_x[0] + 50, console_y[0] + 200])
                screen.blit(ziti.render(sound_white_voice_text[(self.number_white - 1) % 12], False, black),
                        [console_x[0] + 50, console_y[0] + 150])  # 语音文本
        elif self.chess_status == 3:
            screen.blit(ziti.render('人类胜！游戏结束！', False, black), [console_x[0] + 50, console_y[0] + 150])
        elif self.chess_status == 4:
            screen.blit(ziti.render('电脑胜！游戏结束！', False, black), [console_x[0] + 50, console_y[0] + 150])
        else:
            screen.blit(ziti.render(' ', False, white), [console_x[0] + 50, console_y[0] + 150])
        draw_btn(black)  # 画按钮

    # 人类落子和音效！
    def play_black_chess(self, pos):
        self.chess_status = self.pre_game_over(self.chess_position)  # 人类落子后游戏有没有结束
        if self.chess_status == 3 or self.chess_status == 4:
            self.draw_panel()
            if self.chess_status == 3:
                sound_win.play()
            elif self.chess_status == 4:
                sound_defeat.play()
            self.draw_chess()
            return
        if self.chess_status == 1: sound_black.play()  # 正确落黑子音效
        temporary_x = round((pos[0] - border_width) / unit)  # 判断当前落子的位置,需要吸附在最近的落棋点，避免难以落子，落子位置-边缘宽度再除以单元格，再四舍五入就是正确坐标
        temporary_y = round((pos[1] - border_width) / unit)
        if self.move(temporary_x, temporary_y) < 0: return -1  # 走棋对不
        pygame.draw.circle(screen, black, [border_width + unit * temporary_x, border_width + unit * temporary_y],
                           int(unit / 2.5))  # 画棋子
        self.draw_panel()  # 更新控制台
        if self.chess_status == 3:
            sound_win.play(), self.draw_chess()  # 有没有赢或者输
        elif self.chess_status == 4:
            sound_defeat.play(), self.draw_chess()

    # 电脑落子
    def play_white_chess(self):
        self.chess_status = self.pre_game_over(self.chess_position)  # 人类落子后游戏有没有结束
        if self.chess_status == 3 or self.chess_status == 4:
            self.draw_panel()
            if self.chess_status == 3:
                sound_win.play()
            elif self.chess_status == 4:
                sound_defeat.play()
            self.draw_chess()
            return

        temporary_x, temporary_y = self.yixing_GO()  # 电脑该下的坐标
        self.move(temporary_x, temporary_y)
        sound_white.play()
        sound_white_voice[(self.number_white - 1) % 12].play()  # 播放语音
        pygame.draw.circle(screen, white, [border_width + unit * temporary_x, border_width + unit * temporary_y],
                           int(unit / 2.5))
        self.draw_panel()

        self.chess_status = self.pre_game_over(self.chess_position)  # 人类落子后游戏有没有结束
        if self.chess_status == 3 or self.chess_status == 4:
            self.draw_panel()
            if self.chess_status == 3:
                sound_win.play()
            elif self.chess_status == 4:
                sound_defeat.play()
            self.draw_chess()
            return

    # 是否点击了按钮，通过键盘范围判断要进行的操作
    def is_click(self, pos):
        if new_start_x[0] < pos[0] < new_start_x[1] and new_start_y[0] < pos[1] < new_start_y[1]:
            enter()  # 是否新的一局
        elif exit_game_x[0] < pos[0] < exit_game_x[1] and exit_game_y[0] < pos[1] < exit_game_y[1]:
            sys.exit()  # 退出系统
        elif self.chess_status != 3 and self.chess_status != 4 and huiqi_x[0] < pos[0] < huiqi_x[1] and huiqi_y[0] < pos[1] < huiqi_y[
            1]:  # 是否悔棋
            if len(self.current_record) == 0:
                return 0
            self.huiqi()
            screen.blit(pygame.image.load(r"素材\棋盘.jpg"), (0, 0))  # 绘制背景图
            draw_map()  # 绘制棋盘
            self.draw_chess()  # 绘制棋子
            self.draw_panel()  # 绘制面板
            return 0
        else:
            return -1  # 没点按钮

    # 开始游戏主循环
    def start(self):
        self.chess_status = 1  # 黑棋先走
        while True:  # 程序主循环
            for event in pygame.event.get():  # 获取事件
                if event.type == QUIT:  # 退出事件
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:  # 鼠标落子或点击按键
                    if self.is_click(event.pos) < 0:  # 非按钮事件，则处理走棋
                        if self.chess_status!=3 and self.chess_status!=4:
                            self.play_black_chess(event.pos)
                elif self.chess_status == -1:
                    self.play_white_chess()
            # 绘制屏幕内容，不断刷新
            pygame.display.update()


# 人人部分游戏逻辑，参考人机部分
class Men_Men_Chess:

    def __init__(self):
        self.chess_position = [[0 for y in range(0, 9)] for x in
                               range(0, 9)]  # 9 * 9的二维列表，用于表示棋盘：0 ~ 无棋子， 1 ~ 黑棋，-1 ~ 白棋
        self.current_record = []  # 列表表达式二维列表记录走棋的路径，用于悔棋和搜索。它的元素是一个元组(棋子类型，chess_position.search_hang，chess_position.search_lie)
        self.chess_status = 0  # 棋子状态，黑棋先走，最开始会赋值为1：0 ~ 未开局和未分出胜负；1 ~ 等待黑棋落子；-1 ~ 等待白棋落子；3 ~ 结束（人类胜）；4 ~ 结束（人类输）
        self.number_white = 0  # 白子个数
        self.number_black = 0  # 黑子个数
        self.visit = [[0 for y in range(0, 9)] for x in range(0, 9)]  # 搜索记录列表，0是没搜索过，1是搜索过

    def search_qi(self, i, j):
        search_hang = [1, 0, -1, 0]  # 纵向搜索步伐，行
        search_lie = [0, 1, 0, -1]  # 横向搜索步伐，列
        chess_qi = 0
        self.visit[i][j] = 1
        chess_qi = 0  # 记录气数
        hang = 0
        lie = 0
        for k in range(4):
            hang = i + search_hang[k]
            lie = j + search_lie[k]
            if (hang < 0 or hang > 8) or (lie < 0 or lie > 8): continue
            if self.chess_position[hang][lie] == 0 and self.visit[hang][lie] == 0:
                chess_qi += 1
                self.visit[hang][lie] = 1
            elif self.chess_position[hang][lie] == self.chess_position[i][j] and self.visit[hang][lie] == 0:
                chess_qi += self.search_qi(hang, lie)
        return chess_qi

    def is_win(self):
        is_chess_death = 0
        chess_live = [[-1 for y in range(0, 9)] for x in range(0, 9)]
        for i in range(9):
            for j in range(9):
                if self.chess_position[i][j] == 0:
                    chess_live[i][j] = -1
                    continue
                else:
                    self.visit = [[0 for y in range(0, 9)] for x in range(0, 9)]
                    chess_live[i][j] = self.search_qi(i, j)
                    if chess_live[i][j] == 0: is_chess_death = 1
        if self.chess_status == 1:
            self.chess_status = 4 if is_chess_death == 1 else -1
        elif self.chess_status == -1:
            self.chess_status = 3 if is_chess_death == 1 else 1

    def move(self, x, y):
        if (self.chess_status != 1 and self.chess_status != -1) or (9 <= x or x < 0 or 9 <= y or y < 0) or (
                self.chess_position[x][y] != 0): return -1
        self.chess_position[x][y] = 1 if self.chess_status == 1 else -1
        self.current_record.append((self.chess_position[x][y], x, y))
        self.is_win()
        if self.chess_status != 3 and self.chess_status != 4: self.chess_status = -1 if self.current_record[-1][
                                                                                            0] == 1 else 1
        return 0

    def huiqi(self):
        if len(self.current_record) == 0: return
        last_chess = self.current_record.pop()
        self.chess_position[last_chess[1]][last_chess[2]] = 0
        self.chess_status = 1 if last_chess[0] == 1 else -1


class Men_Men_PlayChess(Men_Men_Chess):

    def __init__(self):
        Men_Men_Chess.__init__(self)
        pygame.init()
        draw_map()
        self.draw_panel()

    def draw_chess(self):
        index = 1
        for item in self.current_record:
            pygame.draw.circle(screen, black, [border_width + item[1] * unit, border_width + item[2] * unit],
                               int(unit / 2.5)) if item[0] == 1 else pygame.draw.circle(screen, white,
                                                                                        [border_width + item[1] * unit,
                                                                                         border_width + item[2] * unit],
                                                                                        int(unit / 2.5))  # 根据状态判断画哪个颜色
            if self.chess_status == 3 or self.chess_status == 4: screen.blit(ziti.render(f'{index}', False, white),
                                                                             [border_width + item[1] * unit - 5,
                                                                              border_width + item[2] * unit - 10]) if \
            item[0] == 1 else screen.blit(ziti.render(f'{index}', False, black),
                                          [border_width + item[1] * unit - 5, border_width + item[2] * unit - 10])
            index += 1

    def draw_panel(self):
        screen.blit(pygame.image.load(r"素材\人人模式.jpg"), (console_x[0] + 30, 0))
        if self.chess_status == 0 or self.chess_status == 1:
            screen.blit(ziti.render('黑行..', False, white), [console_x[0] + 50, console_y[0] + 150])
        elif self.chess_status == -1:
            screen.blit(ziti.render('白行..', False, white), [console_x[0] + 50, console_y[0] + 150])
        elif self.chess_status == 3:
            screen.blit(ziti.render('黑胜！游戏结束！', False, white), [console_x[0] + 50, console_y[0] + 150])
        elif self.chess_status == 4:
            screen.blit(ziti.render('白胜！游戏结束！', False, white), [console_x[0] + 50, console_y[0] + 150])
        draw_btn(blue)

    # 不同于人机模式，人人共用同样的下棋函数
    def play_chess(self, pos):
        sound_black.play() if self.chess_status == 1 else sound_white.play()
        temporary_x = round((pos[0] - border_width) / unit)
        temporary_y = round((pos[1] - border_width) / unit)
        if self.move(temporary_x, temporary_y) < 0: return -1
        pygame.draw.circle(screen, black, [border_width + unit * temporary_x, border_width + unit * temporary_y],
                           int(unit / 2.5)) if self.current_record[-1][0] == 1 else pygame.draw.circle(screen, white, [
            border_width + unit * temporary_x, border_width + unit * temporary_y], int(unit / 2.5))
        self.draw_panel()
        if self.chess_status == 3 or self.chess_status == 4: sound_win.play(), self.draw_chess()

    def is_click(self, pos):
        if new_start_x[0] < pos[0] < new_start_x[1] and new_start_y[0] < pos[1] < new_start_y[1]:
            enter()
        elif exit_game_x[0] < pos[0] < exit_game_x[1] and exit_game_y[0] < pos[1] < exit_game_y[1]:
            sys.exit()
        elif huiqi_x[0] < pos[0] < huiqi_x[1] and huiqi_y[0] < pos[1] < huiqi_y[
            1] and self.chess_status != 3 and self.chess_status != 4:
            self.huiqi()
            screen.blit(pygame.image.load(r"素材\棋盘.jpg"), (0, 0))
            draw_map()
            self.draw_chess()
            self.draw_panel()
            return 0
        else:
            return -1

    def start(self):
        self.chess_status = 1  # 黑棋先走
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    if self.is_click(event.pos) < 0:
                        if self.chess_status != 3 and self.chess_status != 4:
                            self.play_chess(event.pos)
            pygame.display.update()


# 游戏主函数
def enter():
    draw_start()  # 绘制开始界面
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:  # 通过鼠标点击判断是否开始游戏
                if start_is_click(event.pos) == 1:
                    play_game = Men_Machine_PlayChess()
                    play_game.start()
                elif start_is_click(event.pos) == -1:
                    play_game = Men_Men_PlayChess()
                    play_game.start()
        pygame.display.update()


if __name__ == '__main__':
    enter()
